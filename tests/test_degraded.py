from pathlib import Path

import pytest
from fastapi.testclient import TestClient

from app.main import create_app
from app.settings import Settings


def test_degraded_process_is_live_not_ready(tmp_path: Path):
    settings = Settings(
        api_key="test-key",
        catalog_csv_path=tmp_path / "missing.csv",
        public_base_url="https://catalog.example.test",
        app_env="test",
    )
    client = TestClient(create_app(settings))
    health = client.get("/healthz")
    readiness = client.get("/readyz")
    catalog = client.get("/v1/categories", headers={"X-API-Key": "test-key"})
    assert health.status_code == 200
    assert health.json()["catalog_status"] == "degraded"
    assert readiness.status_code == 503
    assert catalog.status_code == 503
    assert catalog.json()["error"]["code"] == "CATALOG_UNAVAILABLE"


def test_missing_api_key_configuration_fails(monkeypatch):
    monkeypatch.delenv("CATALOG_API_KEY", raising=False)
    with pytest.raises(RuntimeError, match="CATALOG_API_KEY"):
        Settings.from_env()
