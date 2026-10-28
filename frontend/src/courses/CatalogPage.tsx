import { useState } from 'react'
import Pagination from '../shared/ui/Pagination'
import CourseCard from './CourseCard'
import { useCourses } from './useCourses'

const PAGE_SIZE = 20

export default function CatalogPage() {
  const [offset, setOffset] = useState(0)
  const { state, retry } = useCourses(PAGE_SIZE, offset)

  return (
    <section aria-labelledby="catalog-title">
      <h1 id="catalog-title" className="page-title">
        Catálogo comunitario
      </h1>

      {state.status === 'loading' && (
        <div role="status" aria-live="polite">
          <p className="muted">Cargando cursos…</p>
          <div className="grid" aria-hidden="true">
            {[0, 1, 2].map((i) => (
              <div key={i} className="card skeleton" />
            ))}
          </div>
        </div>
      )}

      {state.status === 'error' && (
        <div className="notice notice--error" role="alert">
          <p>
            <strong>No pudimos cargar los cursos.</strong> {state.message}
          </p>
          <button type="button" className="btn btn--primary" onClick={retry}>
            Reintentar
          </button>
        </div>
      )}

      {state.status === 'success' && state.data.items.length === 0 && (
        <div className="notice" role="status">
          <p>
            <strong>Todavía no hay cursos publicados.</strong>
          </p>
          <p className="muted">Cuando la comunidad aporte cursos y se aprueben, aparecerán acá.</p>
        </div>
      )}

      {state.status === 'success' && state.data.items.length > 0 && (
        <>
          <p className="muted" aria-live="polite">
            {state.data.total} {state.data.total === 1 ? 'curso' : 'cursos'}
          </p>
          <div className="grid">
            {state.data.items.map((course) => (
              <CourseCard key={course.id} course={course} />
            ))}
          </div>
          <Pagination
            total={state.data.total}
            limit={state.data.limit}
            offset={state.data.offset}
            onChange={setOffset}
          />
        </>
      )}
    </section>
  )
}
