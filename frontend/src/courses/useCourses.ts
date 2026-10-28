import { useCallback, useEffect, useState } from 'react'
import type { Page } from '../shared/api/types'
import { fetchCourses } from './api'
import type { Course } from './types'

export type CoursesState =
  | { status: 'loading' }
  | { status: 'error'; message: string }
  | { status: 'success'; data: Page<Course> }

type Settled =
  | { key: string; ok: true; data: Page<Course> }
  | { key: string; ok: false; message: string }

export function useCourses(limit: number, offset: number) {
  const [attempt, setAttempt] = useState(0)
  const [settled, setSettled] = useState<Settled | null>(null)
  const key = `${limit}:${offset}:${attempt}`

  useEffect(() => {
    const controller = new AbortController()

    fetchCourses(limit, offset, controller.signal)
      .then((data) => setSettled({ key, ok: true, data }))
      .catch((err: unknown) => {
        if (err instanceof DOMException && err.name === 'AbortError') return
        const message = err instanceof Error ? err.message : 'Ocurrió un error inesperado.'
        setSettled({ key, ok: false, message })
      })

    return () => controller.abort()
  }, [limit, offset, key])

  // "loading" se deriva: no hay resultado para la consulta actual todavía.
  let state: CoursesState = { status: 'loading' }
  if (settled && settled.key === key) {
    state = settled.ok
      ? { status: 'success', data: settled.data }
      : { status: 'error', message: settled.message }
  }

  const retry = useCallback(() => setAttempt((n) => n + 1), [])
  return { state, retry }
}
