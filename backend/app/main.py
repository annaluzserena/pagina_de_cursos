import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.auth.router import router as auth_router
from app.categories.router import router as categories_router
from app.core import ratelimit
from app.core.config import get_settings
from app.core.db import get_session_factory
from app.core.errors import register_error_handlers
from app.core.middleware import register_middleware
from app.courses.router import router as courses_router
from app.moderation.router import router as moderation_router
from app.roadmaps.router import router as roadmaps_router

logging.basicConfig(level=logging.INFO)


@asynccontextmanager
async def lifespan(_: FastAPI):
    get_settings().validate_for_runtime()
    try:  # limpieza de intentos viejos (retención corta); no debe impedir arrancar
        with get_session_factory()() as db:
            ratelimit.purge_old(db)
            db.commit()
    except Exception:
        logging.getLogger("rutalibre").warning("No se pudo purgar login_attempts al iniciar.")
    yield


app = FastAPI(title="RutaLibre API", version="0.2.0", lifespan=lifespan)

register_middleware(app)
app.add_middleware(
    CORSMiddleware,
    allow_origins=get_settings().cors_origins_list,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PATCH", "DELETE"],
    allow_headers=["Content-Type"],
)
register_error_handlers(app)


@app.get("/health", tags=["health"])
def health() -> dict[str, str]:
    return {"status": "ok"}


PREFIX = "/api/v1"
for r in (auth_router, categories_router, courses_router, moderation_router, roadmaps_router):
    app.include_router(r, prefix=PREFIX)
