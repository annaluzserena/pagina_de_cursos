# SPEC — RutaLibre

> Versión refinada de la SPEC de clase. La fuente recibida sin editar se conserva en [SPEC-clase-original.md](SPEC-clase-original.md). Esta versión incorpora decisiones de producto y referencias a PRD/TRD.

## 1. Identidad del producto

- **Nombre propio:** RutaLibre.
- **Una línea:** comunidad de estudiantes que descubre, aporta y valida cursos gratuitos y organiza su aprendizaje en roadmaps personales.

## 2. Problema

La oferta de cursos gratuitos está dispersa entre plataformas, universidades, organizaciones y comunidades. La información de requisitos, docentes, edición, evaluaciones y certificados no siempre se presenta de forma uniforme, por lo que comparar opciones exige búsquedas repetidas.

Las listas personales suelen mantenerse en documentos o marcadores sin estados ni una ruta de aprendizaje clara. RutaLibre combina un catálogo comunitario estructurado con roadmaps privados, y agrega validación para reducir la publicación de enlaces inválidos o metadatos incompletos.

La comunidad mejora el catálogo porque cualquier usuario autenticado puede aportar recursos, pero la publicación no es automática: una persona con rol de moderación revisa los aportes y decide si se publican, rechazan o devuelven para corrección.

## 3. Visión

En doce meses, RutaLibre aspira a ser una referencia comunitaria confiable para descubrir cursos gratuitos y convertirlos en itinerarios de aprendizaje organizados, con datos comparables, moderación transparente y progreso personal sencillo.

## 4. Alcance

### Dentro

- Catálogo comunitario público, buscable, filtrable y paginado de cursos validados.
- Registro, inicio de sesión, cierre de sesión y recuperación de contraseña por token temporal de un solo uso.
- Rate limiting obligatorio en login y límites adicionales para registro, recuperación y aportes.
- Aporte autenticado de cursos gratuitos con metadatos requeridos y declaración de si el aportante lo realizó.
- Revisión de aportes por usuarios con rol `moderator`.
- Detalle del curso, inclusión en roadmap personal, eliminación del roadmap y cambio de estado personal.
- Categorías controladas y datos de cursos normalizados.
- Interfaz responsive, mobile-first, accesible y visualmente inspirada en Google Material.
- Persistencia PostgreSQL y ejecución local mediante Docker Compose.

### Fuera (out of scope explícito)

- Venta, pago o promoción de cursos pagos.
- Hospedaje de videos, contenido didáctico o exámenes dentro de RutaLibre; el curso se realiza en la plataforma de origen.
- Emisión o validación automática de certificados.
- Integración OAuth/SSO con proveedores externos.
- Aplicación móvil nativa, notificaciones push y modo offline.
- Mensajería, comentarios, foros, seguidores y chat.
- Recomendaciones con IA, ranking social o gamificación.
- Roadmaps colaborativos o públicos en el MVP.
- Automatización de la validación mediante scraping; el moderador revisa manualmente URL y metadatos.
- Recuperación de cuentas mediante SMS o soporte humano automatizado.

## 5. Reglas de producto clave

| # | Regla | Origen |
|---|---|---|
| BR-001 | Un curso aportado no aparece en el catálogo público hasta ser validado por moderación. | SPEC de clase + decisión para resolver quién valida |
| BR-002 | Quien aporta un curso declara si lo realizó. | SPEC de clase |
| BR-003 | Solo usuarios autenticados pueden aportar cursos o gestionar su roadmap. | Decisión propia |
| BR-004 | Cada usuario solo puede consultar y modificar su propio roadmap. | Decisión propia; autorización server-side |
| BR-005 | El catálogo incluye solo cursos gratuitos con URL activa y metadatos obligatorios completos. | SPEC de clase + decisión propia |
| BR-006 | No se permite más de un curso con la misma URL canónica; el backend valida duplicados. | Decisión propia |
| BR-007 | Un curso validado puede ser agregado al roadmap por cualquier usuario autenticado; agregarlo no cambia el catálogo global. | Interpretación de “incluirlo en su catálogo/roadmap” |

El detalle completo de reglas está en [PRD.md](PRD.md), §7.

## 6. Stack registrado

Las versiones exactas instaladas todavía no se registraron porque la Instancia A no debe incluir código ni entornos de ejecución. Las versiones objetivo son las de la SPEC de clase y deberán verificarse al comenzar la Instancia B.

| Capa | Tecnología | Versión objetivo / estado |
|---|---|---|
| Frontend | React + Vite + pnpm | React 19 estable; Vite y pnpm estables compatibles; exactas pendientes de instalación |
| Backend | FastAPI + uv | FastAPI estable indicada por la SPEC (referencia 0.158.2 al 21/10/2026); verificar disponibilidad real al instalar |
| Base de datos | PostgreSQL | 18.6, fijado por la consigna |
| Infra (dev) | Docker + Docker Compose | versiones estables compatibles; registrar `docker --version` y `docker compose version` |

No se declara que estas versiones estén instaladas ni verificadas.

## 7. Restricciones técnicas heredadas de la SPEC de clase

| # | Restricción | Cómo se cumplirá |
|---|---|---|
| 1 | Mobile-first con mejora progresiva; base sin media queries y `@media (min-width: ...)` solo para mejorar pantallas grandes. | CSS base usable desde 320 px; media queries únicamente para sumar columnas, espacio y navegación ampliada. No usar reglas desktop para reparar la base. |
| 2 | Paginación de todas las consultas de listado y sus tablas. | Todo endpoint de colección usa paginación `limit/offset` con `total`, límites máximos y orden estable. Tablas de moderación también paginan. |
| 3 | Menú sándwich en mobile. | Navegación compacta con botón accesible, nombre accesible, `aria-expanded` y cierre tras navegar; en viewport amplio se transforma en navegación visible. |
| 4 | Screaming Architecture. | Backend organizado por dominios (`auth`, `courses`, `roadmaps`, `moderation`, `categories`), separando API, servicios y persistencia dentro de cada módulo. |
| 5 | Inspiración Google/Material clara. | Tokens concretos de color, tipografía, espaciado, elevación, radio y estados en [UX-UI.md](UX-UI.md). |

## 8. Vacíos de la SPEC de clase y decisiones tomadas

| # | Vacío detectado | Opciones consideradas | Decisión | Dónde se desarrolla |
|---|---|---|---|---|
| 1 | ¿Quién valida los cursos? | Publicación automática; validación docente; moderación comunitaria con rol. | Moderador autenticado; el aporte queda `pending_review`. No hay auto-publicación. | PRD §7; BackendSchema §2–3 |
| 2 | ¿Qué roles existen? | Solo usuario; usuario/moderador; administrador completo. | `user` y `moderator`; el primer moderador se provisiona manualmente en entorno controlado. No existe panel de administración general en MVP. | PRD §9; TRD §2 |
| 3 | ¿Qué significa “incluir en mi catálogo”? | Copiar curso; marcar favorito; incorporarlo a un roadmap. | Crear una entrada personal en `roadmap_items`; un curso puede estar en un roadmap por usuario una sola vez. | PRD US-006; BackendSchema §1 |
| 4 | ¿Qué búsqueda existe? | Texto; filtros; ambos. | Búsqueda por título, tema, docente y plataforma, más filtro por categoría, tema y certificados; todas las listas paginadas. | PRD RF-004; APPFlow §3 |
| 5 | ¿Qué datos son obligatorios? | Solo campos enumerados; campos opcionales adicionales. | URL, categoría, tema, título, versión, año, docentes/disertantes y declaración de toma son obligatorios; cuestionarios, examen, certificado y aval son booleanos obligatorios con valores sí/no. | PRD §5 y §7 |
| 6 | ¿Cómo se trata un curso duplicado? | Permitir; advertir; rechazar. | Rechazar URL canónica duplicada, sin revelar datos privados del aportante. | PRD BR-004; BackendSchema §4 |
| 7 | ¿El roadmap tiene estados? | Solo lista; estado de avance. | Cada elemento permite `planned`, `in_progress`, `completed`; el estado inicial es `planned`. | PRD US-006; BackendSchema §1 |
| 8 | ¿Cómo funciona recuperación de contraseña? | Token firmado; token aleatorio persistido; proveedor externo. | Token aleatorio de un solo uso, guardado como hash, expiración de 30 minutos y respuesta genérica ante email existente/inexistente. Envío por email; desarrollo usa SMTP configurable o salida de email de prueba. | TRD TD-001; BackendSchema §3 |
| 9 | ¿Cómo se implementa rate limit? | Solo frontend; memoria local; almacenamiento compartido. | Backend con límite por IP y por identificador normalizado; Redis queda fuera del MVP y se documenta la limitación de memoria por proceso. Para una sola instancia de desarrollo se usa almacenamiento persistente en PostgreSQL o librería compatible con backend compartido. | TRD TD-002 |
| 10 | ¿Qué significa “URL activa”? | Validación sintáctica; comprobación manual; crawler. | Validación sintáctica en backend y revisión manual del moderador. No se garantiza automáticamente que el proveedor esté disponible en todo momento. | PRD BR-005; TRD TD-005 |
| 11 | ¿Qué campos admite “lo avala una organización”? | Booleano solamente; nombre de entidad. | Booleano requerido `is_endorsed`; `endorsing_organization` es opcional y se exige cuando el valor es sí. | BackendSchema §1 |
| 12 | ¿Se necesita verificar el email? | Obligatorio; opcional; no verificar. | No se exige verificación de email para el MVP, para reducir dependencias; recuperación sí requiere email funcional. La decisión puede revisarse si el docente lo exige. | PRD §10; TRD TD-001 |

## 9. Historia de la SPEC (autoregistro de cambios)

| Fecha | Cambio | Por qué |
|---|---|---|
| 20/10/2026 | SPEC preliminar discutida en aula. | Registro histórico provisto en los materiales. |
| 21/10/2026 | SPEC oficial recibida. | Fuente inicial sin editar, preservada en `SPEC-clase-original.md`. |
| 22/10/2026 | Refinamiento de alcance, roles, validación, roadmap, seguridad y datos. | Resolver vacíos y asegurar coherencia entre los siete documentos. |
