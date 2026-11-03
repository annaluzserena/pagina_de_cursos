"""Request ID y defensa CSRF por verificación de Origin (BackendSchema §3.1)."""
import uuid

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from app.core.config import get_settings
from app.core.errors import envelope

UNSAFE = {"POST", "PUT", "PATCH", "DELETE"}


def register_middleware(app: FastAPI) -> None:
    @app.middleware("http")
    async def request_context(request: Request, call_next):
        request.state.request_id = str(uuid.uuid4())

        if request.method in UNSAFE:
            origin = request.headers.get("origin")
            if origin and origin not in get_settings().cors_origins_list:
                same_host = origin.split("://", 1)[-1] == request.headers.get("host")
                if not same_host:
                    return JSONResponse(
                        status_code=403,
                        content=envelope(request, "forbidden_origin", "Origen no permitido."),
                    )

        response = await call_next(request)
        response.headers["X-Request-ID"] = request.state.request_id
        response.headers.setdefault("X-Content-Type-Options", "nosniff")
        return response
