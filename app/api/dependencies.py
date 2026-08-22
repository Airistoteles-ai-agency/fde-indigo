from __future__ import annotations

import secrets
from typing import Annotated

from fastapi import Request, Security
from fastapi.security import APIKeyHeader

from app.api.errors import APIError

api_key_header = APIKeyHeader(
    name="X-API-Key",
    scheme_name="CatalogApiKey",
    description="Secret server-to-server key configured in Indigo. Never place it in a URL.",
    auto_error=False,
)


def require_api_key(
    request: Request,
    provided_key: Annotated[str | None, Security(api_key_header)],
) -> None:
    if provided_key is None:
        raise APIError(
            401,
            "AUTHENTICATION_REQUIRED",
            "X-API-Key is required.",
            "Configure the Catalog Tool Collection header with an Indigo secret.",
        )
    configured_key = request.app.state.settings.api_key
    if not secrets.compare_digest(provided_key, configured_key):
        raise APIError(
            403,
            "INVALID_API_KEY",
            "The supplied API key is invalid.",
            "Verify the secret configuration; do not retry the same value.",
        )
