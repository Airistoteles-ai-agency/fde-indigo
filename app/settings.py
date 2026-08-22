from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path
from urllib.parse import urlparse


@dataclass(frozen=True, slots=True)
class Settings:
    api_key: str
    catalog_csv_path: Path = Path("data/gift-shop-catalog.csv")
    public_base_url: str = "http://localhost:8000"
    app_env: str = "development"

    def __post_init__(self) -> None:
        if not self.api_key.strip():
            raise RuntimeError("CATALOG_API_KEY must be configured and non-empty.")
        parsed = urlparse(self.public_base_url)
        if parsed.scheme not in {"http", "https"} or not parsed.netloc:
            raise RuntimeError("PUBLIC_BASE_URL must be an absolute HTTP(S) URL.")

    @classmethod
    def from_env(cls) -> Settings:
        api_key = os.getenv("CATALOG_API_KEY", "")
        if not api_key.strip():
            raise RuntimeError("CATALOG_API_KEY must be configured and non-empty.")
        return cls(
            api_key=api_key,
            catalog_csv_path=Path(
                os.getenv("CATALOG_CSV_PATH", "data/gift-shop-catalog.csv")
            ),
            public_base_url=os.getenv("PUBLIC_BASE_URL", "http://localhost:8000"),
            app_env=os.getenv("APP_ENV", "development"),
        )
