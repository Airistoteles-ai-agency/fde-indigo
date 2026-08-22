from __future__ import annotations

import csv
import re
import unicodedata
from decimal import Decimal, InvalidOperation
from pathlib import Path

from pydantic import ValidationError

from app.catalog.models import Product, StockStatus

REQUIRED_HEADERS = {
    "product_id",
    "name",
    "category",
    "subcategory",
    "brand",
    "price_eur",
    "stock",
    "rating",
    "reviews_count",
    "recipient",
    "occasion",
    "tags",
    "color",
    "material",
    "gift_wrap",
    "shipping_days",
    "description",
}

CATEGORY_NAMES = {
    "home & living": "Home & Living",
    "books & stationery": "Books & Stationery",
    "kitchen & dining": "Kitchen & Dining",
    "tech & gadgets": "Tech & Gadgets",
    "beauty & wellness": "Beauty & Wellness",
    "experiences": "Experiences",
    "games & puzzles": "Games & Puzzles",
    "jewellery": "Jewellery",
    "kids": "Kids",
    "outdoor & travel": "Outdoor & Travel",
    "pets": "Pets",
}


class CatalogLoadError(RuntimeError):
    """The source cannot produce a trustworthy catalog."""


def normalize_text(value: str) -> str:
    value = unicodedata.normalize("NFKD", value)
    value = "".join(character for character in value if not unicodedata.combining(character))
    return " ".join(value.casefold().strip().split())


def normalize_category(raw: str) -> tuple[str, str]:
    key = normalize_text(raw)
    key = re.sub(r"\s+and\s+", " & ", key)
    key = re.sub(r"\s*&\s*", " & ", key)
    display = CATEGORY_NAMES.get(key)
    if display is None:
        raise CatalogLoadError(f"Unsupported category value: {raw!r}.")
    category_id = re.sub(r"[^a-z0-9]+", "-", key).strip("-")
    return category_id, display


def _required(row: dict[str, str], field: str, row_number: int) -> str:
    value = (row.get(field) or "").strip()
    if not value:
        raise CatalogLoadError(f"Row {row_number}: {field} is required.")
    return value


def _optional(row: dict[str, str], field: str) -> str | None:
    value = (row.get(field) or "").strip()
    return value or None


def _list(row: dict[str, str], field: str) -> tuple[str, ...]:
    value = (row.get(field) or "").strip()
    if not value:
        return ()
    return tuple(item.strip().casefold() for item in value.split("|") if item.strip())


def _decimal(value: str, field: str, row_number: int) -> Decimal:
    try:
        parsed = Decimal(value)
    except InvalidOperation as exc:
        raise CatalogLoadError(f"Row {row_number}: {field} must be numeric.") from exc
    if parsed < 0:
        raise CatalogLoadError(f"Row {row_number}: {field} must be non-negative.")
    return parsed


def _integer(value: str, field: str, row_number: int) -> int:
    try:
        parsed = int(value)
    except ValueError as exc:
        raise CatalogLoadError(f"Row {row_number}: {field} must be an integer.") from exc
    if parsed < 0:
        raise CatalogLoadError(f"Row {row_number}: {field} must be non-negative.")
    return parsed


def _optional_float(value: str | None, field: str, row_number: int) -> float | None:
    if value is None:
        return None
    try:
        return float(value)
    except ValueError as exc:
        raise CatalogLoadError(f"Row {row_number}: {field} must be numeric or blank.") from exc


def _optional_integer(value: str | None, field: str, row_number: int) -> int | None:
    if value is None:
        return None
    return _integer(value, field, row_number)


def _gift_wrap(value: str, row_number: int) -> bool:
    normalized = normalize_text(value)
    if normalized == "yes":
        return True
    if normalized == "no":
        return False
    raise CatalogLoadError(f"Row {row_number}: gift_wrap must be yes or no.")


def load_catalog(path: Path) -> tuple[Product, ...]:
    try:
        source = path.open("r", encoding="utf-8", newline="")
    except OSError as exc:
        raise CatalogLoadError(f"Catalog file is unavailable: {path}.") from exc

    with source:
        reader = csv.DictReader(source)
        headers = set(reader.fieldnames or ())
        missing = sorted(REQUIRED_HEADERS - headers)
        if missing:
            raise CatalogLoadError(f"Catalog is missing required headers: {', '.join(missing)}.")

        products: list[Product] = []
        ids: set[str] = set()
        for row_number, row in enumerate(reader, start=2):
            product_id = _required(row, "product_id", row_number)
            if product_id in ids:
                raise CatalogLoadError(f"Row {row_number}: duplicate product_id {product_id!r}.")
            ids.add(product_id)
            category_id, category_name = normalize_category(
                _required(row, "category", row_number)
            )
            stock = _integer(_required(row, "stock", row_number), "stock", row_number)
            try:
                product = Product(
                    product_id=product_id,
                    name=_required(row, "name", row_number),
                    category_id=category_id,
                    category_name=category_name,
                    subcategory=_required(row, "subcategory", row_number),
                    brand=_required(row, "brand", row_number),
                    price=_decimal(
                        _required(row, "price_eur", row_number), "price_eur", row_number
                    ),
                    stock_quantity=stock,
                    stock_status=(
                        StockStatus.IN_STOCK if stock > 0 else StockStatus.OUT_OF_STOCK
                    ),
                    rating=_optional_float(_optional(row, "rating"), "rating", row_number),
                    reviews_count=_optional_integer(
                        _optional(row, "reviews_count"), "reviews_count", row_number
                    ),
                    recipient=_required(row, "recipient", row_number).casefold(),
                    occasions=_list(row, "occasion"),
                    tags=_list(row, "tags"),
                    color=_optional(row, "color"),
                    material=_optional(row, "material"),
                    gift_wrap_available=_gift_wrap(
                        _required(row, "gift_wrap", row_number), row_number
                    ),
                    shipping_days=_integer(
                        _required(row, "shipping_days", row_number),
                        "shipping_days",
                        row_number,
                    ),
                    description=_required(row, "description", row_number),
                )
            except ValidationError as exc:
                raise CatalogLoadError(f"Row {row_number}: {exc.errors()[0]['msg']}.") from exc
            products.append(product)

    if not products:
        raise CatalogLoadError("Catalog must contain at least one product.")
    return tuple(products)
