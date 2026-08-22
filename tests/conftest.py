from __future__ import annotations

from pathlib import Path

import pytest
from fastapi.testclient import TestClient

from app.catalog.loader import load_catalog
from app.catalog.repository import CatalogRepository
from app.main import create_app
from app.settings import Settings

FIXTURE = Path(__file__).parent / "fixtures" / "catalog_valid.csv"
TEST_KEY = "test-key-that-is-not-a-production-secret"


@pytest.fixture
def products():
    return load_catalog(FIXTURE)


@pytest.fixture
def repository(products):
    return CatalogRepository(products)


@pytest.fixture
def settings():
    return Settings(
        api_key=TEST_KEY,
        catalog_csv_path=FIXTURE,
        public_base_url="https://catalog.example.test",
        app_env="test",
    )


@pytest.fixture
def client(settings, repository):
    return TestClient(create_app(settings, repository))


@pytest.fixture
def auth_headers():
    return {"X-API-Key": TEST_KEY}
