import type { Course } from './types'

function Tag({ label, value }: { label: string; value: boolean }) {
  // El estado se comunica con texto, no solo con color (UX-UI §1.4).
  return (
    <li className={`tag ${value ? 'tag--yes' : 'tag--no'}`}>
      {label}: {value ? 'Sí' : 'No'}
    </li>
  )
}

export default function CourseCard({ course }: { course: Course }) {
  return (
    <article className="card">
      <h3 className="card__title">{course.title}</h3>
      <p className="card__meta">
        {course.topic} · {course.version} · {course.edition_year}
      </p>
      <p className="card__meta">Docentes: {course.instructors}</p>
      <ul className="tags" aria-label="Características del curso">
        <Tag label="Cuestionarios" value={course.has_quizzes} />
        <Tag label="Examen" value={course.requires_exam} />
        <Tag label="Certificado" value={course.offers_certificate} />
        <Tag
          label={
            course.endorsing_organization
              ? `Aval (${course.endorsing_organization})`
              : 'Aval'
          }
          value={course.is_endorsed}
        />
      </ul>
      <a
        className="btn btn--secondary"
        href={course.source_url}
        target="_blank"
        rel="noopener noreferrer"
      >
        Ir al curso{course.provider ? ` en ${course.provider}` : ''}
        <span className="visually-hidden"> (sitio externo, se abre en una pestaña nueva)</span>
        <span aria-hidden="true"> ↗</span>
      </a>
    </article>
  )
}
