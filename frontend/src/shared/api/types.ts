/** Forma estándar de las listas paginadas (BackendSchema §3). */
export interface Page<T> {
  items: T[]
  total: number
  limit: number
  offset: number
}
