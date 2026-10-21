# Backend Schema — Modelo de datos y API

- Versión: 0.1
- Referencias: `SPEC.md`, `TRD.md`

## 1. Convenciones

- PostgreSQL.
- Claves primarias UUID recomendadas para evitar exponer secuencias previsibles; también se aceptan IDs enteros si el equipo documenta la decisión.
- Timestamps `TIMESTAMPTZ` en UTC.
- `created_at` y `updated_at` en entidades mutables.
- Índices y restricciones definidos en migraciones Alembic.
- Nombres SQL en `snake_case`.
- Campos sensibles omitidos de respuestas públicas.

## 2. Entidades

### 2.1 users

| Campo | Tipo conceptual | Reglas |
|---|---|---|
| id | UUID | PK |
| display_name | VARCHAR(80) | NOT NULL |
| email | CITEXT o VARCHAR normalizado | NOT NULL, UNIQUE |
| password_hash | TEXT | NOT NULL |
| role | ENUM/VARCHAR | `student` o `admin`; default `student` |
| is_active | BOOLEAN | NOT NULL, default true |
| created_at | TIMESTAMPTZ | NOT NULL |
| updated_at | TIMESTAMPTZ | NOT NULL |

No devolver `password_hash`. La normalización y unicidad del email deben ser consistentes. Si no se usa `CITEXT`, guardar una representación normalizada y crear restricción única apropiada.

### 2.2 password_reset_tokens

| Campo | Tipo conceptual | Reglas |
|---|---|---|
| id | UUID | PK |
| user_id | UUID | FK users, ON DELETE CASCADE |
| token_hash | TEXT | NOT NULL, UNIQUE |
| expires_at | TIMESTAMPTZ | NOT NULL |
| used_at | TIMESTAMPTZ | nullable |
| created_at | TIMESTAMPTZ | NOT NULL |

Índice por `user_id` y `expires_at`. El token original no se persiste. Las filas vencidas pueden purgarse mediante tarea controlada.

### 2.3 categories

| Campo | Tipo conceptual | Reglas |
|---|---|---|
| id | UUID | PK |
| name | VARCHAR(80) | NOT NULL |
| slug | VARCHAR(100) | NOT NULL, UNIQUE |
| description | TEXT | nullable |
| created_at | TIMESTAMPTZ | NOT NULL |
| updated_at | TIMESTAMPTZ | NOT NULL |

### 2.4 courses

| Campo | Tipo conceptual | Reglas |
|---|---|---|
| id | UUID | PK |
| category_id | UUID | FK categories, nullable según política |
| title | VARCHAR(180) | NOT NULL |
| slug | VARCHAR(200) | NOT NULL, UNIQUE |
| summary | VARCHAR(300) | NOT NULL |
| description | TEXT | NOT NULL |
| external_url | TEXT | nullable |
| difficulty | VARCHAR/ENUM | beginner/intermediate/advanced/all_levels |
| estimated_minutes | INTEGER | CHECK > 0 o NULL |
| status | VARCHAR/ENUM | draft/published/archived |
| created_by | UUID | FK users |
| created_at | TIMESTAMPTZ | NOT NULL |
| updated_at | TIMESTAMPTZ | NOT NULL |
| published_at | TIMESTAMPTZ | nullable |

La URL debe validarse en el backend. Si se aceptan solo cursos gratuitos, el contenido editorial debe confirmar que el recurso cumple esa condición; la plataforma no puede inferir automáticamente que todos los enlaces son gratuitos.

### 2.5 roadmaps

| Campo | Tipo conceptual | Reglas |
|---|---|---|
| id | UUID | PK |
| title | VARCHAR(180) | NOT NULL |
| slug | VARCHAR(200) | NOT NULL, UNIQUE |
| summary | VARCHAR(300) | NOT NULL |
| description | TEXT | NOT NULL |
| difficulty | VARCHAR/ENUM | nivel definido |
| status | VARCHAR/ENUM | draft/published/archived |
| created_by | UUID | FK users |
| created_at | TIMESTAMPTZ | NOT NULL |
| updated_at | TIMESTAMPTZ | NOT NULL |
| published_at | TIMESTAMPTZ | nullable |

### 2.6 roadmap_stages

| Campo | Tipo conceptual | Reglas |
|---|---|---|
| id | UUID | PK |
| roadmap_id | UUID | FK roadmaps, ON DELETE CASCADE |
| title | VARCHAR(180) | NOT NULL |
| description | TEXT | nullable |
| position | INTEGER | NOT NULL, CHECK >= 0 |
| created_at | TIMESTAMPTZ | NOT NULL |
| updated_at | TIMESTAMPTZ | NOT NULL |

Restricción única propuesta: `(roadmap_id, position)`.

### 2.7 roadmap_stage_courses

| Campo | Tipo conceptual | Reglas |
|---|---|---|
| stage_id | UUID | FK roadmap_stages, ON DELETE CASCADE |
| course_id | UUID | FK courses |
| position | INTEGER | NOT NULL, CHECK >= 0 |
| is_required | BOOLEAN | NOT NULL, default true |
| created_at | TIMESTAMPTZ | NOT NULL |

PK compuesta `(stage_id, course_id)` y restricción única `(stage_id, position)`. Si se requiere que un curso no aparezca más de una vez en todo un roadmap, esa regla necesita validación adicional o un modelo distinto.

### 2.8 enrollments

| Campo | Tipo conceptual | Reglas |
|---|---|---|
| id | UUID | PK |
| user_id | UUID | FK users, ON DELETE CASCADE |
| course_id | UUID | FK courses |
| status | VARCHAR/ENUM | not_started/in_progress/completed |
| enrolled_at | TIMESTAMPTZ | NOT NULL |
| started_at | TIMESTAMPTZ | nullable |
| completed_at | TIMESTAMPTZ | nullable |
| created_at | TIMESTAMPTZ | NOT NULL |
| updated_at | TIMESTAMPTZ | NOT NULL |

Restricción única `(user_id, course_id)`. Validar coherencia temporal al cambiar estado. El estado `completed` puede establecer `completed_at`; al volver a `in_progress`, la política debe definir si se limpia.

### 2.9 audit_events (P1)

| Campo | Tipo conceptual | Reglas |
|---|---|---|
| id | UUID | PK |
| actor_user_id | UUID | FK users, nullable para eventos de sistema |
| action | VARCHAR(100) | NOT NULL |
| entity_type | VARCHAR(100) | NOT NULL |
| entity_id | UUID | nullable |
| metadata | JSONB | solo metadatos no sensibles |
| created_at | TIMESTAMPTZ | NOT NULL |

No registrar contraseñas, tokens, cookies ni cuerpos completos de solicitudes. Restringir lectura de auditoría.

## 3. Relaciones

- Un usuario crea muchos cursos.
- Una categoría agrupa muchos cursos.
- Un usuario crea muchos roadmaps.
- Un roadmap contiene muchas etapas.
- Una etapa contiene muchos cursos mediante `roadmap_stage_courses`.
- Un usuario tiene muchas inscripciones.
- Un curso tiene muchas inscripciones.
- Un usuario puede tener muchos tokens de recuperación a lo largo del tiempo.

## 4. Diagrama ER textual

```text
users 1 --- N courses          (created_by)
categories 1 --- N courses
users 1 --- N roadmaps         (created_by)
roadmaps 1 --- N roadmap_stages
roadmap_stages 1 --- N roadmap_stage_courses
courses 1 --- N roadmap_stage_courses
users 1 --- N enrollments
courses 1 --- N enrollments
users 1 --- N password_reset_tokens
users 1 --- N audit_events
```

## 5. Índices sugeridos

- `users(email)` único.
- `courses(slug)` único.
- `courses(status, published_at)`.
- `courses(category_id, status)`.
- `courses(difficulty, status)`.
- `roadmaps(slug)` único.
- `roadmaps(status, published_at)`.
- `roadmap_stages(roadmap_id, position)` único.
- `roadmap_stage_courses(stage_id, position)` único.
- `enrollments(user_id, course_id)` único.
- `enrollments(user_id, status)`.
- `password_reset_tokens(token_hash)` único y `expires_at`.
- Índices GIN/full-text solo cuando la búsqueda real los justifique.

## 6. Contratos de API propuestos

Prefijo `/api/v1`.

### Autenticación
- `POST /auth/register`
- `POST /auth/login`
- `POST /auth/logout`
- `GET /auth/me`
- `POST /auth/password/forgot`
- `POST /auth/password/reset`
- `POST /auth/email/verify` (si se habilita)
- `POST /auth/email/resend-verification` (si se habilita)

### Catálogo
- `GET /courses`
- `GET /courses/{slug}`
- `GET /categories`
- `GET /roadmaps`
- `GET /roadmaps/{slug}`

### Aprendizaje
- `GET /me/enrollments`
- `POST /enrollments`
- `PATCH /enrollments/{enrollment_id}`
- `POST /roadmap/new`
- `PATCH /roadmap/{slug}/edit`

### Perfil
- `GET /me`
- `PATCH /me`

### Administración
- `POST /admin/courses`
- `PATCH /admin/courses/{course_id}`
- `POST /admin/courses/{course_id}/archive`
- `POST /admin/categories`
- `PATCH /admin/categories/{category_id}`
- `POST /admin/roadmaps`
- `PATCH /admin/roadmaps/{roadmap_id}`
- `POST /admin/roadmaps/{roadmap_id}/publish`
- `POST /admin/roadmaps/{roadmap_id}/archive`

Se recomienda usar endpoints explícitos de publicación/archivado si permiten validar transiciones. Para CRUD genérico se puede utilizar `DELETE` solo cuando el borrado físico sea realmente válido y esté documentado.

## 7. Esquemas conceptuales

### CoursePublic
- `id`
- `title`
- `slug`
- `summary`
- `description`
- `external_url`
- `difficulty`
- `estimated_minutes`
- `category`
- `published_at`

No incluye `created_by` interno ni información de auditoría salvo necesidad explícita.

### CourseCreate
- `title`
- `slug` opcional si se genera en servidor
- `summary`
- `description`
- `external_url`
- `difficulty`
- `estimated_minutes`
- `category_id`
- `status` limitado a valores permitidos por el rol y flujo administrativo

### UserPublic
- `id`
- `display_name`
- `email` solo en contexto propio/admin autorizado
- `role` solo si el cliente necesita conocerlo y el acceso está autorizado
- `created_at`

Nunca incluye `password_hash`, tokens, cookies ni secretos.

### EnrollmentPublic
- `id`
- `course`
- `status`
- `enrolled_at`
- `started_at`
- `completed_at`
- `updated_at`

No aceptar `user_id` en el payload de creación para determinar el dueño. El dueño se deriva de la sesión.

## 8. Transacciones e integridad

- Crear roadmap, etapas y asociaciones en una transacción.
- La restricción única de inscripción es la protección final ante solicitudes concurrentes.
- Capturar conflictos de unicidad y traducirlos a errores API estables.
- Al archivar un curso, definir qué ocurre con las inscripciones y roadmaps: recomendación inicial, conservar referencias históricas y bloquear nuevas inscripciones.
- Las migraciones deben probarse desde una base vacía y desde la versión previa.
- Definir política de backup y restauración antes de producción.

## 9. Privacidad y retención

- Definir cuánto tiempo se conservan tokens vencidos y eventos de auditoría.
- El borrado de cuenta debe resolver relaciones y obligaciones de retención.
- No almacenar más información personal que la necesaria.
- Restringir consultas de datos privados por dueño y rol.
