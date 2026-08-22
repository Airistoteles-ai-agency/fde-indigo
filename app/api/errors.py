from __future__ import annotations

from typing import Any

from fastapi import Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse


class APIError(RuntimeError):
    def __init__(
        self,
        status_code: int,
        code: str,
        message: str,
        recovery_hint: str,
    ) -> None:
        super().__init__(message)
        self.status_code = status_code
        self.code = code
        self.message = message
        self.recovery_hint = recovery_hint

    def payload(self) -> dict[str, dict[str, str]]:
        return {
            "error": {
                "code": self.code,
                "message": self.message,
                "recovery_hint": self.recovery_hint,
            }
        }


async def api_error_handler(_: Request, exc: APIError) -> JSONResponse:
    return JSONResponse(status_code=exc.status_code, content=exc.payload())


async def validation_error_handler(_: Request, exc: RequestValidationError) -> JSONResponse:
    error: dict[str, Any] = exc.errors()[0]
    location = ".".join(str(part) for part in error.get("loc", ()) if part != "query")
    message = error.get("msg", "Request validation failed.")
    return JSONResponse(
        status_code=422,
        content={
            "error": {
                "code": "INVALID_ARGUMENT",
                "message": f"{location}: {message}" if location else message,
                "recovery_hint": "Correct the documented parameter and retry once.",
            }
        },
    )
