def test_categories_are_compact_and_unpaginated(client, auth_headers):
    response = client.get("/v1/categories", headers=auth_headers)
    payload = response.json()
    assert response.status_code == 200
    assert payload["total_categories"] == 3
    kitchen = next(item for item in payload["results"] if item["category_id"] == "kitchen-dining")
    assert kitchen["product_count"] == 5
    assert kitchen["in_stock_count"] == 4


def test_category_filters_and_limit(client, auth_headers):
    response = client.get(
        "/v1/categories/kitchen-dining/products",
        params={"max_price": 100, "max_shipping_days": 2, "limit": 10},
        headers=auth_headers,
    )
    assert response.status_code == 200
    assert all(item["price"] <= 100 for item in response.json()["results"])
    assert all(item["shipping_days"] <= 2 for item in response.json()["results"])
    assert len(response.json()["results"]) <= 10


def test_search_structured_constraints(client, auth_headers):
    response = client.get(
        "/v1/search/products",
        params={
            "query": "practical kitchen",
            "recipient": "her",
            "occasion": "housewarming",
            "max_price": 50,
        },
        headers=auth_headers,
    )
    assert response.status_code == 200
    assert response.json()["results"][0]["product_id"] == "KD-004"


def test_detail_reports_recommendation_eligibility(client, auth_headers):
    response = client.get("/v1/products/KD-007", headers=auth_headers)
    assert response.status_code == 200
    assert response.json()["product"]["stock_status"] == "out_of_stock"
    assert response.json()["recommendation_eligibility"]["can_recommend_as_available"] is False


def test_unknown_resources_and_empty_search(client, auth_headers):
    category = client.get("/v1/categories/not-real/products", headers=auth_headers)
    product = client.get("/v1/products/not-real", headers=auth_headers)
    empty = client.get(
        "/v1/search/products",
        params={"query": "spaceship telescope"},
        headers=auth_headers,
    )
    assert category.status_code == 404
    assert category.json()["error"]["code"] == "CATEGORY_NOT_FOUND"
    assert product.status_code == 404
    assert product.json()["error"]["code"] == "PRODUCT_NOT_FOUND"
    assert empty.status_code == 200
    assert empty.json()["results"] == []


def test_invalid_range_and_parameter_use_structured_errors(client, auth_headers):
    invalid_range = client.get(
        "/v1/search/products",
        params={"query": "gift", "min_price": 100, "max_price": 50},
        headers=auth_headers,
    )
    invalid_limit = client.get(
        "/v1/search/products",
        params={"query": "gift", "limit": 11},
        headers=auth_headers,
    )
    assert invalid_range.status_code == 422
    assert invalid_range.json()["error"]["code"] == "INVALID_PRICE_RANGE"
    assert invalid_limit.status_code == 422
    assert invalid_limit.json()["error"]["code"] == "INVALID_ARGUMENT"
