from decimal import Decimal

import pytest

from app.catalog.repository import InvalidPriceRangeError


def test_housewarming_kitchen_under_fifty(repository):
    result = repository.search(
        "practical kitchen",
        recipient="her",
        occasion="housewarming",
        max_price=Decimal("50"),
        in_stock_only=True,
    )
    assert result.results[0].product_id == "KD-004"
    assert all(item.price <= 50 for item in result.results)


def test_two_day_filter_is_hard(repository):
    result = repository.search("coffee", max_shipping_days=2)
    assert result.results
    assert all(item.shipping_days <= 2 for item in result.results)


def test_chef_knife_under_one_hundred_has_no_exact_match(repository):
    result = repository.search("chef knife", max_price=Decimal("100"))
    assert all(item.product_id != "KD-001" for item in result.results)
    assert all(item.name != "Chef's Knife 20cm" for item in result.results)


def test_default_stock_filter_and_explicit_out_of_stock_search(repository):
    default = repository.search("cold brew carafe")
    assert default.results == []
    explicit = repository.search("cold brew carafe", in_stock_only=False)
    assert explicit.results[0].product_id == "KD-007"


def test_empty_budget_and_zero_score_return_no_results(repository):
    assert repository.search("premium", max_price=Decimal("5")).results == []
    assert repository.search("spaceship telescope").results == []


def test_search_collapses_duplicate_names(repository):
    result = repository.search("herb garden")
    assert [item.name for item in result.results].count("Herb Garden Kit") == 1


def test_category_browse_keeps_source_rows_and_paginates(repository):
    page = repository.browse("kitchen-dining", limit=2)
    assert page.returned_count == 2
    assert page.next_offset == 2
    assert all(item.category_id == "kitchen-dining" for item in page.results)


def test_anyone_is_compatible_with_specific_recipient(repository):
    result = repository.search("coffee", recipient="her")
    assert result.results[0].recipient == "anyone"


def test_invalid_price_range(repository):
    with pytest.raises(InvalidPriceRangeError):
        repository.search("gift", min_price=Decimal("100"), max_price=Decimal("50"))
