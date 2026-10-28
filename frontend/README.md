# RutaLibre — Frontend (T3)

```bash
cd frontend
pnpm install
pnpm dev        # http://localhost:5173
```

El proxy de Vite reenvía `/api/*` a `http://localhost:8000` (backend T2).
Para otro destino: `VITE_API_PROXY_TARGET` (ver `.env.example`).

Pantalla: Catálogo (`GET /api/v1/courses`) con estados loading / error / vacío y paginación.
