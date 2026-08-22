from __future__ import annotations

from pathlib import Path

import pytest

from app.catalog.loader import CatalogLoadError, load_catalog
from app.catalog.models import StockStatus


def test_valid_catalog_maps_real_fields(products):
    assert len(products) == 8
    moka = next(product for product in products if product.product_id == "KD-004")
    assert moka.category_id == "kitchen-dining"
    assert moka.currency == "EUR"
    assert moka.occasions == ("housewarming", "birthday")
    assert moka.shipping_days == 2
    assert moka.gift_wrap_available is True


def test_optional_values_and_zero_day_shipping(products):
    gift_card = next(product for product in products if product.product_id == "EX-001")
    assert gift_card.rating is None
    assert gift_card.reviews_count is None
    assert gift_card.occasions == ()
    assert gift_card.color is None
    assert gift_card.shipping_days == 0


def test_zero_stock_is_out_of_stock(products):
    candle = next(product for product in products if product.product_id == "HL-004")
    assert candle.stock_status is StockStatus.OUT_OF_STOCK


@pytest.mark.parametrize(
    ("mutator", "expected"),
    [
        (lambda text: text.replace("KD-002,Paring", "KD-001,Paring"), "duplicate product_id"),
        (lambda text: text.replace("149,16", "not-a-price,16"), "price_eur must be numeric"),
        (lambda text: text.replace("46,9", "46,-1"), "stock must be non-negative"),
    ],
)
def test_invalid_required_values_fail_entire_catalog(tmp_path: Path, mutator, expected):
    source = Path(__file__).parent / "fixtures" / "catalog_valid.csv"
    target = tmp_path / "invalid.csv"
    target.write_text(mutator(source.read_text(encoding="utf-8")), encoding="utf-8")
    with pytest.raises(CatalogLoadError, match=expected):
        load_catalog(target)


def test_missing_file_and_empty_catalog_fail(tmp_path: Path):
    with pytest.raises(CatalogLoadError, match="unavailable"):
        load_catalog(tmp_path / "missing.csv")

    empty = tmp_path / "empty.csv"
    empty.write_text(
        (Path(__file__).parent / "fixtures" / "catalog_valid.csv")
        .read_text(encoding="utf-8")
        .splitlines()[0]
        + "\n",
        encoding="utf-8",
    )
    with pytest.raises(CatalogLoadError, match="at least one"):
        load_catalog(empty)
