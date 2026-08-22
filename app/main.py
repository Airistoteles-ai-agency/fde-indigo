from __future__ import annotations

import logging
import time

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError

from app.api.errors import APIError, api_error_handler, validation_error_handler
from app.api.routes import router
from app.catalog.loader import CatalogLoadError, load_catalog
from app.catalog.models import HealthResponse, ReadinessResponse
from app.catalog.repository import CatalogRepository
from app.settings import Settings

logger = logging.getLogger("catalog.requests")


def create_app(
    settings: Settings | None = None,
    repository: CatalogRepository | None = None,
) -> FastAPI:
    settings = settings or Settings.from_env()
    if repository is None:
        try:
            repository = CatalogRepository(load_catalog(settings.catalog_csv_path))
        except CatalogLoadError as exc:
            logger.error("Catalog started in degraded mode: %s", exc)
            repository = CatalogRepository.degraded(str(exc))

    application = FastAPI(
        title="Gift Shop Catalog API",
        version="1.0.0",
        description=(
            "Deterministic, authenticated catalog tools for the Indigo Product Discovery "
            "Agent. Product facts come only from the configured CSV."
        ),
        servers=[{"url": settings.public_base_url.rstrip("/"), "description": settings.app_env}],
    )
    application.state.settings = settings
    application.state.repository = repository
    application.add_exception_handler(APIError, api_error_handler)
    application.add_exception_handler(RequestValidationError, validation_error_handler)

    @application.middleware("http")
    async def request_metrics(request: Request, call_next):
        started = time.perf_counter()
        response = await call_next(request)
        elapsed_ms = (time.perf_counter() - started) * 1000
        logger.info(
            "request_complete method=%s path=%s status=%s duration_ms=%.2f",
            request.method,
            request.url.path,
            response.status_code,
            elapsed_ms,
        )
        return response

    @application.get("/healthz", include_in_schema=False, response_model=HealthResponse)
    def health() -> HealthResponse:
        return HealthResponse(
            catalog_status="ready" if repository.is_ready else "degraded"
        )

    @application.get(
        "/readyz",
        include_in_schema=False,
        response_model=ReadinessResponse,
        responses={503: {"model": ReadinessResponse}},
    )
    def ready():
        if repository.is_ready:
            return ReadinessResponse(status="ready", catalog_status="ready")
        from fastapi.responses import JSONResponse

        return JSONResponse(
            status_code=503,
            content=ReadinessResponse(
                status="degraded",
                catalog_status="degraded",
                detail=repository.unavailable_reason,
            ).model_dump(),
        )

    application.include_router(router)
    return application
