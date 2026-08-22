from __future__ import annotations

from decimal import Decimal
from typing import Annotated

from fastapi import APIRouter, Depends, Path, Query, Request

from app.api.dependencies import require_api_key
from app.api.errors import APIError
from app.catalog.models import (
    CategoryCollection,
    ErrorResponse,
    ProductCollection,
    ProductDetailResponse,
    RecommendationEligibility,
)
from app.catalog.repository import (
    CatalogRepository,
    CatalogUnavailableError,
    CategoryNotFoundError,
    InvalidPriceRangeError,
    ProductNotFoundError,
)

router = APIRouter(
    prefix="/v1",
    tags=["Catalog"],
    dependencies=[Depends(require_api_key)],
)

ERROR_RESPONSES = {
    401: {"model": ErrorResponse, "description": "Missing API key."},
    403: {"model": ErrorResponse, "description": "Invalid API key."},
    404: {"model": ErrorResponse, "description": "Unknown category or product."},
    422: {"model": ErrorResponse, "description": "Invalid argument."},
    503: {"model": ErrorResponse, "description": "Catalog unavailable."},
}


def repository(request: Request) -> CatalogRepository:
    return request.app.state.repository


def execute(call):
    try:
        return call()
    except CatalogUnavailableError as exc:
        raise APIError(
            503,
            "CATALOG_UNAVAILABLE",
            "The product catalog is temporarily unavailable.",
            "Stop product recommendations and retry later.",
        ) from exc
    except CategoryNotFoundError as exc:
        raise APIError(
            404,
            "CATEGORY_NOT_FOUND",
            f"Category {exc.args[0]!r} does not exist.",
            "Call get_categories and retry with a returned category_id.",
        ) from exc
    except ProductNotFoundError as exc:
        raise APIError(
            404,
            "PRODUCT_NOT_FOUND",
            f"Product {exc.args[0]!r} does not exist.",
            "Use search_products to find the current product_id.",
        ) from exc
    except InvalidPriceRangeError as exc:
        raise APIError(
            422,
            "INVALID_PRICE_RANGE",
            "min_price must be less than or equal to max_price.",
            "Retry with a lower min_price or a higher max_price.",
        ) from exc


@router.get(
    "/categories",
    operation_id="get_categories",
    summary="List the available gift categories",
    description=(
        "Use when the user asks what types of gifts can be browsed or has not selected "
        "a category. Do not call automatically when a valid category or contextual "
        "product request is already known. Returns every compact category summary."
    ),
    response_model=CategoryCollection,
    responses=ERROR_RESPONSES,
)
def get_categories(request: Request) -> CategoryCollection:
    results = execute(lambda: repository(request).categories())
    return CategoryCollection(results=results, total_categories=len(results))


@router.get(
    "/categories/{category_id}/products",
    operation_id="get_products_by_category",
    summary="Browse products in one known category",
    description=(
        "Use when a category_id returned by get_categories is known and the user wants "
        "to browse it with hard price, stock, or delivery constraints. Do not use for "
        "cross-category natural-language discovery or fetch details for every result."
    ),
    response_model=ProductCollection,
    responses=ERROR_RESPONSES,
)
def get_products_by_category(
    request: Request,
    category_id: Annotated[str, Path(description="Exact category_id from get_categories.")],
    min_price: Annotated[
        Decimal | None, Query(ge=0, description="Optional minimum price in EUR.")
    ] = None,
    max_price: Annotated[
        Decimal | None, Query(ge=0, description="Hard maximum price in EUR.")
    ] = None,
    max_shipping_days: Annotated[
        int | None,
        Query(ge=0, le=7, description="Hard maximum catalog shipping estimate in days."),
    ] = None,
    in_stock_only: Annotated[
        bool, Query(description="Exclude zero-stock products when true.")
    ] = True,
    limit: Annotated[int, Query(ge=1, le=10, description="Page size, maximum 10.")] = 5,
    offset: Annotated[int, Query(ge=0, description="Zero-based result offset.")] = 0,
) -> ProductCollection:
    return execute(
        lambda: repository(request).browse(
            category_id,
            min_price=min_price,
            max_price=max_price,
            max_shipping_days=max_shipping_days,
            in_stock_only=in_stock_only,
            limit=limit,
            offset=offset,
        )
    )


@router.get(
    "/search/products",
    operation_id="search_products",
    summary="Search products across the catalog",
    description=(
        "Use for natural-language or cross-category discovery involving interests, "
        "recipient, occasion, intended use, budget, or delivery constraints. Send concise "
        "catalog concepts rather than the whole conversation. Use this with "
        "in_stock_only=false to resolve an exact product name before requesting detail. "
        "Do not use when only the category list or a known product_id is needed."
    ),
    response_model=ProductCollection,
    responses=ERROR_RESPONSES,
)
def search_products(
    request: Request,
    query: Annotated[
        str,
        Query(
            min_length=1,
            max_length=200,
            description="Concise product need, interest, occasion, use, or exact name.",
            examples=["practical kitchen gift"],
        ),
    ],
    category_id: Annotated[
        str | None, Query(description="Optional exact ID from get_categories.")
    ] = None,
    recipient: Annotated[
        str | None, Query(min_length=1, max_length=40, description="Recipient such as her or him.")
    ] = None,
    occasion: Annotated[
        str | None, Query(min_length=1, max_length=40, description="Occasion such as housewarming.")
    ] = None,
    min_price: Annotated[Decimal | None, Query(ge=0, description="Minimum EUR price.")] = None,
    max_price: Annotated[
        Decimal | None, Query(ge=0, description="Hard maximum EUR price.")
    ] = None,
    max_shipping_days: Annotated[
        int | None, Query(ge=0, le=7, description="Hard maximum shipping estimate.")
    ] = None,
    in_stock_only: Annotated[
        bool, Query(description="Exclude zero-stock products when true.")
    ] = True,
    limit: Annotated[int, Query(ge=1, le=10, description="Page size, maximum 10.")] = 5,
    offset: Annotated[int, Query(ge=0, description="Zero-based result offset.")] = 0,
) -> ProductCollection:
    return execute(
        lambda: repository(request).search(
            query,
            category_id=category_id,
            recipient=recipient,
            occasion=occasion,
            min_price=min_price,
            max_price=max_price,
            max_shipping_days=max_shipping_days,
            in_stock_only=in_stock_only,
            limit=limit,
            offset=offset,
        )
    )


@router.get(
    "/products/{product_id}",
    operation_id="get_product_details",
    summary="Get full facts for one known product ID",
    description=(
        "Use only when product_id is already known from a collection operation and full "
        "facts must be verified. For a product name, call search_products first. Do not "
        "use this operation for discovery or catalog enumeration."
    ),
    response_model=ProductDetailResponse,
    responses=ERROR_RESPONSES,
)
def get_product_details(
    request: Request,
    product_id: Annotated[str, Path(min_length=1, description="Exact source product_id.")],
) -> ProductDetailResponse:
    product = execute(lambda: repository(request).detail(product_id))
    available = product.stock_quantity > 0
    return ProductDetailResponse(
        product=product,
        recommendation_eligibility=RecommendationEligibility(
            can_recommend_as_available=available,
            reason=("Product is in stock." if available else "Product is out of stock."),
        ),
    )
