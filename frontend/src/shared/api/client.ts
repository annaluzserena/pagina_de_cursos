/** Envelope de error uniforme del backend (TRD TD-004). */
export interface ApiErrorBody {
  error: {
    code: string
    message: string
    details: Record<string, string>
    request_id: string
  }
}

export class ApiError extends Error {
  status: number
  code: string

  constructor(status: number, code: string, message: string) {
    super(message)
    this.name = 'ApiError'
    this.status = status
    this.code = code
  }
}

const API_BASE = '/api/v1'

export async function apiGet<T>(path: string, signal?: AbortSignal): Promise<T> {
  let response: Response
  try {
    response = await fetch(`${API_BASE}${path}`, {
      headers: { Accept: 'application/json' },
      credentials: 'same-origin',
      signal,
    })
  } catch (err) {
    if (err instanceof DOMException && err.name === 'AbortError') throw err
    throw new ApiError(0, 'network_error', 'No se pudo conectar con el servidor.')
  }

  if (!response.ok) {
    let code = 'http_error'
    let message = `Error ${response.status}`
    try {
      const body = (await response.json()) as ApiErrorBody
      code = body.error.code
      message = body.error.message
    } catch {
      /* respuesta sin JSON: se conserva el mensaje genérico */
    }
    throw new ApiError(response.status, code, message)
  }

  return (await response.json()) as T
}
