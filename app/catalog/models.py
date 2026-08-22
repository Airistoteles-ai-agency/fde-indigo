from __future__ import annotations

from decimal import Decimal
from enum import StrEnum
from typing import Any, Literal

from pydantic import BaseModel, ConfigDict, Field, field_serializer


class StockStatus(StrEnum):
    IN_STOCK = "in_stock"
    OUT_OF_STOCK = "out_of_stock"


class Product(BaseModel):
    model_config = ConfigDict(frozen=True)

    product_id: str
    name: str
    category_id: str
    category_name: str
    subcategory: str
    brand: str
    price: Decimal = Field(ge=0)
    currency: Literal["EUR"] = "EUR"
    stock_quantity: int = Field(ge=0)
    stock_status: StockStatus
    rating: float | None = Field(default=None, ge=0, le=5)
    reviews_count: int | None = Field(default=None, ge=0)
    recipient: str
    occasions: tuple[str, ...] = ()
    tags: tuple[str, ...] = ()
    color: str | None = None
    material: str | None = None
    gift_wrap_available: bool
    shipping_days: int = Field(ge=0, le=7)
    description: str

    @field_serializer("price", when_used="json")
    def serialize_price(self, value: Decimal) -> float:
        return float(value)


class ProductSummary(BaseModel):
    product_id: str
    name: str
    category_id: str
    category_name: str
    subcategory: str
    price: Decimal
    currency: Literal["EUR"] = "EUR"
    stock_status: StockStatus
    shipping_days: int
    recipient: str
    occasions: tuple[str, ...]
    rating: float | None
    description: str

    @field_serializer("price", when_used="json")
    def serialize_price(self, value: Decimal) -> float:
        return float(value)

    @classmethod
    def from_product(cls, product: Product) -> ProductSummary:
        return cls(**product.model_dump(include=set(cls.model_fields)))


class RecommendationEligibility(BaseModel):
    can_recommend_as_available: bool
    reason: str


class ProductDetailResponse(BaseModel):
    product: Product
    recommendation_eligibility: RecommendationEligibility


class ProductCollection(BaseModel):
    results: list[ProductSummary]
    total_matches: int
    returned_count: int
    offset: int
    next_offset: int | None
    filters_applied: dict[str, Any]


class CategorySummary(BaseModel):
    category_id: str
    name: str
    product_count: int
    in_stock_count: int
    min_price: Decimal | None
    max_price: Decimal | None
    currency: Literal["EUR"] = "EUR"

    @field_serializer("min_price", "max_price", when_used="json")
    def serialize_price(self, value: Decimal | None) -> float | None:
        return float(value) if value is not None else None


class CategoryCollection(BaseModel):
    results: list[CategorySummary]
    total_categories: int


class ErrorBody(BaseModel):
    code: str
    message: str
    recovery_hint: str


class ErrorResponse(BaseModel):
    error: ErrorBody


class HealthResponse(BaseModel):
    status: Literal["alive"] = "alive"
    catalog_status: Literal["ready", "degraded"]


class ReadinessResponse(BaseModel):
    status: Literal["ready", "degraded"]
    catalog_status: Literal["ready", "degraded"]
    detail: str | None = None
