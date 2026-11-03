"""Envelope de errores uniforme (TRD TD-004 / BackendSchema §3)."""
import logging
import uuid

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException

logger = logging.getLogger("rutalibre")


class AppError(Exception):
    def __init__(
        self,
        status_code: int,
        code: str,
        message: str,
        details: dict[str, str] | None = None,
        headers: dict[str, str] | None = None,
    ) -> None:
        super().__init__(message)
        self.status_code = status_code
        self.code = code
        self.message = message
        self.details = details or {}
        self.headers = headers or {}


def unauthorized(message: str = "Necesitás iniciar sesión.") -> AppError:
    return AppError(401, "unauthorized", message)


def forbidden(message: str = "No tenés permiso para realizar esta acción.") -> AppError:
    return AppError(403, "forbidden", message)


def not_found(message: str = "Recurso no encontrado.") -> AppError:
    return AppError(404, "not_found", message)


def conflict(code: str, message: str) -> AppError:
    return AppError(409, code, message)


def validation_error(details: dict[str, str], message: str = "Datos inválidos.") -> AppError:
    return AppError(422, "validation_error", message, details)


def rate_limited(retry_after: int) -> AppError:
    return AppError(
        429,
        "rate_limited",
        f"Demasiados intentos. Probá de nuevo en {retry_after} segundos.",
        headers={"Retry-After": str(retry_after)},
    )


def envelope(request: Request | None, code: str, message: str, details: dict | None = None) -> dict:
    request_id = getattr(getattr(request, "state", None), "request_id", None) or str(uuid.uuid4())
    return {"error": {"code": code, "message": message, "details": details or {}, "request_id": request_id}}


def register_error_handlers(app: FastAPI) -> None:
    @app.exception_handler(AppError)
    async def app_error_handler(request: Request, exc: AppError):
        return JSONResponse(
            status_code=exc.status_code,
            content=envelope(request, exc.code, exc.message, exc.details),
            headers=exc.headers,
        )

    @app.exception_handler(RequestValidationError)
    async def validation_handler(request: Request, exc: RequestValidationError):
        details: dict[str, str] = {}
        for err in exc.errors():
            loc = ".".join(str(p) for p in err["loc"] if p not in ("body", "query", "path"))
            msg = str(err["msg"]).removeprefix("Value error, ")
            details[loc or "_"] = msg  # nunca se devuelve el valor recibido (puede ser una contraseña)
        return JSONResponse(
            status_code=422,
            content=envelope(request, "validation_error", "Datos inválidos.", details),
        )

    @app.exception_handler(StarletteHTTPException)
    async def http_handler(request: Request, exc: StarletteHTTPException):
        code = {404: "not_found", 405: "method_not_allowed"}.get(exc.status_code, "http_error")
        message = "Recurso no encontrado." if exc.status_code == 404 else str(exc.detail)
        return JSONResponse(
            status_code=exc.status_code,
            content=envelope(request, code, message),
            headers=getattr(exc, "headers", None),
        )

    @app.exception_handler(Exception)
    async def unhandled_handler(request: Request, exc: Exception):
        # Sin stack trace en la respuesta (TRD TD-004); el detalle queda en logs del servidor.
        logger.exception("Error no controlado")
        return JSONResponse(
            status_code=500,
            content=envelope(request, "internal_error", "Error interno del servidor."),
        )
