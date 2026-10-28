import { apiGet } from '../shared/api/client'
import type { Page } from '../shared/api/types'
import type { Course } from './types'

export function fetchCourses(
  limit: number,
  offset: number,
  signal?: AbortSignal,
): Promise<Page<Course>> {
  return apiGet<Page<Course>>(`/courses?limit=${limit}&offset=${offset}`, signal)
}
