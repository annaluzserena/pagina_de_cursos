import { defineConfig, loadEnv } from 'vite'
import react from '@vitejs/plugin-react'

// https://vite.dev/config/
export default defineConfig(({ mode }) => {
  const env = loadEnv(mode, process.cwd(), '')
  // Destino del backend; configurable para Docker Compose (p. ej. http://backend:8000).
  const apiTarget = env.VITE_API_PROXY_TARGET || 'http://localhost:8000'

  return {
    plugins: [react()],
    server: {
      port: 5173,
      host: true,
      // El navegador llama a /api/* en el mismo origen; Vite lo reenvía al backend.
      // Evita CORS y facilita cookies de sesión (TRD §4).
      proxy: {
        '/api': { target: apiTarget, changeOrigin: true },
      },
    },
  }
})
