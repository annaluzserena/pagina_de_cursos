# RutaLibre — Backend (T2)

```bash
cd backend
uv sync
uv run uvicorn app.main:app --reload --reload-exclude '.venv' --port 8000
```

- `curl http://localhost:8000/health` → `{"status":"ok"}`
- `curl http://localhost:8000/api/v1/courses` → `{items,total,limit,offset}` (datos hardcodeados, solo `published`)
- Docs OpenAPI: http://localhost:8000/docs
