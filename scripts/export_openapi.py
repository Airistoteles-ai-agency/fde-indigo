# ruff: noqa: E402 -- direct script execution must add the repository root first.

from __future__ import annotations

import json
import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from app.catalog.repository import CatalogRepository
from app.main import create_app
from app.settings import Settings


def main() -> None:
    settings = Settings(
        api_key=os.getenv("CATALOG_API_KEY", "schema-export-placeholder-not-a-secret"),
        catalog_csv_path=Path(os.getenv("CATALOG_CSV_PATH", "data/gift-shop-catalog.csv")),
        public_base_url=os.getenv("PUBLIC_BASE_URL", "https://catalog-api.example.com"),
        app_env=os.getenv("APP_ENV", "schema-export"),
    )
    app = create_app(settings, CatalogRepository.degraded("Schema export does not load data."))
    output = ROOT / "openapi.json"
    output.write_text(
        json.dumps(app.openapi(), indent=2, sort_keys=True, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    print(f"Exported {output}")


if __name__ == "__main__":
    main()
