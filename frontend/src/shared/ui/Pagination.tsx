interface Props {
  total: number
  limit: number
  offset: number
  onChange: (offset: number) => void
}

export default function Pagination({ total, limit, offset, onChange }: Props) {
  if (total === 0) return null
  const from = offset + 1
  const to = Math.min(offset + limit, total)
  const hasPrev = offset > 0
  const hasNext = offset + limit < total
  const page = Math.floor(offset / limit) + 1
  const pages = Math.ceil(total / limit)

  return (
    <nav className="pagination" aria-label="Paginación de resultados">
      <p className="pagination__range">
        {from}–{to} de {total}
      </p>
      <div className="pagination__controls">
        <button
          type="button"
          className="btn btn--secondary"
          disabled={!hasPrev}
          onClick={() => onChange(Math.max(0, offset - limit))}
        >
          Anterior
        </button>
        <span className="pagination__page" aria-current="page">
          Página {page} de {pages}
        </span>
        <button
          type="button"
          className="btn btn--secondary"
          disabled={!hasNext}
          onClick={() => onChange(offset + limit)}
        >
          Siguiente
        </button>
      </div>
    </nav>
  )
}
