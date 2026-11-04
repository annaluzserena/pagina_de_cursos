# RutaLibre — Backend

FastAPI + SQLAlchemy 2 + Alembic + PostgreSQL. Organizado por dominio (`auth`, `categories`, `courses`, `moderation`, `roadmaps`) con capas router → service → repository → model.

## Puesta en marcha

```bash
cp .env.example .env            # ajustar DATABASE_URL y SECRET_KEY
cd backend
uv sync
uv run alembic upgrade head     # crea el esquema
uv run python -m app.seed --demo   # categorías + moderador + 50 cursos demo (idempotente)
uv run uvicorn app.main:app --reload --port 8000
```

Docs interactivas: http://localhost:8000/docs · Salud: `GET /health`

Usuarios de prueba (solo local): moderadora `moderadora@rutalibre.local` / `Moderadora-Local-123`.

## Docker
```bash
docker compose up
```

## Endpoints (`/api/v1`)

| Área | Endpoints |
|---|---|
| Auth | `POST /auth/register`, `/auth/login`, `/auth/logout`, `GET /auth/me`, `POST /auth/password/forgot`, `/auth/password/reset` |
| Catálogo | `GET /courses` (`q`, `category_id`, `topic`, `offers_certificate`), `GET /courses/{id}`, `GET /categories` |
| Aportes | `POST /contributions`, `GET /me/contributions` |
| Moderación | `GET /moderation/contributions`, `GET /moderation/contributions/{id}`, `POST /moderation/contributions/{id}/decision` |
| Roadmap | `GET/POST /me/roadmap`, `PATCH/DELETE /me/roadmap/{item_id}` |

Listados: `{items, total, limit, offset}`, `limit` 1–100 (def. 20), `offset` ≥ 0. Errores: `{error:{code,message,details,request_id}}`.
