from __future__ import annotations

from collections import defaultdict
from decimal import Decimal

from app.catalog.loader import normalize_text
from app.catalog.models import (
    CategorySummary,
    Product,
    ProductCollection,
    ProductSummary,
    StockStatus,
)
from app.catalog.search import score_product


class CatalogUnavailableError(RuntimeError):
    pass


class CategoryNotFoundError(LookupError):
    pass


class ProductNotFoundError(LookupError):
    pass


class InvalidPriceRangeError(ValueError):
    pass


class CatalogRepository:
    def __init__(
        self,
        products: tuple[Product, ...] = (),
        *,
        unavailable_reason: str | None = None,
    ) -> None:
        self._products = products
        self._by_id = {product.product_id: product for product in products}
        self._unavailable_reason = unavailable_reason

    @classmethod
    def degraded(cls, reason: str) -> CatalogRepository:
        return cls(unavailable_reason=reason)

    @property
    def is_ready(self) -> bool:
        return self._unavailable_reason is None

    @property
    def unavailable_reason(self) -> str | None:
        return self._unavailable_reason

    def _ensure_ready(self) -> None:
        if not self.is_ready:
            raise CatalogUnavailableError(self._unavailable_reason or "Catalog is unavailable.")

    def categories(self) -> list[CategorySummary]:
        self._ensure_ready()
        grouped: dict[str, list[Product]] = defaultdict(list)
        for product in self._products:
            grouped[product.category_id].append(product)

        result: list[CategorySummary] = []
        for category_id, products in grouped.items():
            available = [
                product for product in products if product.stock_status is StockStatus.IN_STOCK
            ]
            prices = [product.price for product in available]
            result.append(
                CategorySummary(
                    category_id=category_id,
                    name=products[0].category_name,
                    product_count=len(products),
                    in_stock_count=len(available),
                    min_price=min(prices) if prices else None,
                    max_price=max(prices) if prices else None,
                )
            )
        return sorted(result, key=lambda category: category.name)

    def detail(self, product_id: str) -> Product:
        self._ensure_ready()
        try:
            return self._by_id[product_id]
        except KeyError as exc:
            raise ProductNotFoundError(product_id) from exc

    def browse(
        self,
        category_id: str,
        *,
        min_price: Decimal | None = None,
        max_price: Decimal | None = None,
        max_shipping_days: int | None = None,
        in_stock_only: bool = True,
        limit: int = 5,
        offset: int = 0,
    ) -> ProductCollection:
        self._ensure_ready()
        category_ids = {product.category_id for product in self._products}
        if category_id not in category_ids:
            raise CategoryNotFoundError(category_id)
        self._validate_prices(min_price, max_price)
        products = self._filter(
            self._products,
            category_id=category_id,
            min_price=min_price,
            max_price=max_price,
            max_shipping_days=max_shipping_days,
            in_stock_only=in_stock_only,
        )
        products.sort(key=lambda product: (product.price, product.product_id))
        return self._page(
            products,
            limit,
            offset,
            {
                "category_id": category_id,
                "min_price": min_price,
                "max_price": max_price,
                "max_shipping_days": max_shipping_days,
                "in_stock_only": in_stock_only,
            },
        )

    def search(
        self,
        query: str,
        *,
        category_id: str | None = None,
        recipient: str | None = None,
        occasion: str | None = None,
        min_price: Decimal | None = None,
        max_price: Decimal | None = None,
        max_shipping_days: int | None = None,
        in_stock_only: bool = True,
        limit: int = 5,
        offset: int = 0,
    ) -> ProductCollection:
        self._ensure_ready()
        self._validate_prices(min_price, max_price)
        if category_id is not None and category_id not in {
            product.category_id for product in self._products
        }:
            raise CategoryNotFoundError(category_id)

        products = self._filter(
            self._products,
            category_id=category_id,
            recipient=recipient,
            occasion=occasion,
            min_price=min_price,
            max_price=max_price,
            max_shipping_days=max_shipping_days,
            in_stock_only=in_stock_only,
        )
        scored = []
        for product in products:
            score = score_product(product, query)
            if score > 0:
                scored.append((score, product))
        scored.sort(
            key=lambda item: (
                -item[0],
                -(item[1].rating if item[1].rating is not None else -1),
                -(item[1].reviews_count if item[1].reviews_count is not None else -1),
                item[1].price,
                item[1].product_id,
            )
        )
        unique: list[Product] = []
        names: set[str] = set()
        for _, product in scored:
            name = normalize_text(product.name)
            if name not in names:
                names.add(name)
                unique.append(product)

        return self._page(
            unique,
            limit,
            offset,
            {
                "query": query,
                "category_id": category_id,
                "recipient": recipient,
                "occasion": occasion,
                "min_price": min_price,
                "max_price": max_price,
                "max_shipping_days": max_shipping_days,
                "in_stock_only": in_stock_only,
            },
        )

    @staticmethod
    def _validate_prices(min_price: Decimal | None, max_price: Decimal | None) -> None:
        if min_price is not None and max_price is not None and min_price > max_price:
            raise InvalidPriceRangeError

    @staticmethod
    def _filter(
        products: tuple[Product, ...],
        *,
        category_id: str | None = None,
        recipient: str | None = None,
        occasion: str | None = None,
        min_price: Decimal | None = None,
        max_price: Decimal | None = None,
        max_shipping_days: int | None = None,
        in_stock_only: bool = True,
    ) -> list[Product]:
        requested_recipient = normalize_text(recipient) if recipient else None
        requested_occasion = normalize_text(occasion) if occasion else None
        return [
            product
            for product in products
            if (category_id is None or product.category_id == category_id)
            and (min_price is None or product.price >= min_price)
            and (max_price is None or product.price <= max_price)
            and (
                not in_stock_only or product.stock_status is StockStatus.IN_STOCK
            )
            and (
                max_shipping_days is None or product.shipping_days <= max_shipping_days
            )
            and (
                requested_recipient is None
                or product.recipient in {requested_recipient, "anyone"}
            )
            and (
                requested_occasion is None or requested_occasion in product.occasions
            )
        ]

    @staticmethod
    def _page(
        products: list[Product],
        limit: int,
        offset: int,
        filters: dict[str, object],
    ) -> ProductCollection:
        page = products[offset : offset + limit]
        next_offset = offset + len(page) if offset + len(page) < len(products) else None
        clean_filters = {
            key: float(value) if isinstance(value, Decimal) else value
            for key, value in filters.items()
            if value is not None
        }
        return ProductCollection(
            results=[ProductSummary.from_product(product) for product in page],
            total_matches=len(products),
            returned_count=len(page),
            offset=offset,
            next_offset=next_offset,
            filters_applied=clean_filters,
        )
