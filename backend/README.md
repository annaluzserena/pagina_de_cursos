# RutaLibre — Backend (T2)

```bash
cd backend
cp .env.example .env
uv sync
uv run uvicorn app.main:app --reload --port 8000
```

- `curl http://localhost:8000/health` → `{"status":"ok"}`
- `curl http://localhost:8000/api/v1/courses` → `{items,total,limit,offset}` (datos hardcodeados, solo `published`)
- Docs OpenAPI: http://localhost:8000/docs
