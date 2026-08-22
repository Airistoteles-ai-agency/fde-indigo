import json

EXPECTED_OPERATIONS = {
    "get_categories",
    "get_products_by_category",
    "search_products",
    "get_product_details",
}


def operations(schema):
    return {
        operation["operationId"]: operation
        for path in schema["paths"].values()
        for operation in path.values()
        if isinstance(operation, dict) and "operationId" in operation
    }


def test_schema_has_exact_tools_security_and_https_server(client):
    schema = client.get("/openapi.json").json()
    found = operations(schema)
    assert set(found) == EXPECTED_OPERATIONS
    assert schema["servers"][0]["url"] == "https://catalog.example.test"
    security = schema["components"]["securitySchemes"]["CatalogApiKey"]
    assert security == {
        "type": "apiKey",
        "description": "Secret server-to-server key configured in Indigo. Never place it in a URL.",
        "in": "header",
        "name": "X-API-Key",
    }
    assert all(operation["security"] == [{"CatalogApiKey": []}] for operation in found.values())
    assert "/healthz" not in schema["paths"]
    assert "/readyz" not in schema["paths"]


def test_tool_descriptions_bounds_errors_and_no_secret(client):
    schema = client.get("/openapi.json").json()
    found = operations(schema)
    assert all("Use" in operation["description"] for operation in found.values())
    assert all("Do not" in operation["description"] for operation in found.values())
    search = found["search_products"]
    parameters = {parameter["name"]: parameter for parameter in search["parameters"]}
    assert parameters["query"]["schema"]["minLength"] == 1
    assert parameters["query"]["schema"]["maxLength"] == 200
    assert parameters["limit"]["schema"]["maximum"] == 10
    assert "422" in search["responses"]
    encoded = json.dumps(schema)
    assert "test-key-that-is-not-a-production-secret" not in encoded
