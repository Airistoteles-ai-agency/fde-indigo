def test_missing_key_is_401(client):
    response = client.get("/v1/categories")
    assert response.status_code == 401
    assert response.json()["error"]["code"] == "AUTHENTICATION_REQUIRED"


def test_invalid_key_is_403(client):
    response = client.get("/v1/categories", headers={"X-API-Key": "incorrect"})
    assert response.status_code == 403
    assert response.json()["error"]["code"] == "INVALID_API_KEY"


def test_valid_key_succeeds(client, auth_headers):
    response = client.get("/v1/categories", headers=auth_headers)
    assert response.status_code == 200
