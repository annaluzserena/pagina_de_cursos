# PRD — Product Requirements Document — RutaLibre

> **Qué es:** define el qué y el porqué del producto, los usuarios, las funcionalidades y los límites. No prescribe la organización del código. **Definition of done:** una persona puede implementar cada historia sin decisiones de producto implícitas; las historias tienen criterios verificables y el fuera de alcance está explícito.

## 1. Resumen ejecutivo

RutaLibre es una webapp comunitaria para descubrir cursos gratuitos estructurados, aportar cursos y, tras una validación manual, incorporarlos al catálogo comunitario. Las personas registradas crean un roadmap privado para planificar su aprendizaje y marcar el avance de cada curso. El MVP prioriza catálogo, autenticación segura, aportes moderados y roadmap personal.

## 2. Objetivos y métricas de éxito

| Objetivo | Señal de éxito en MVP |
|---|---|
| Descubrir cursos sin crear cuenta | Visitante puede buscar, filtrar, abrir detalles y paginar catálogo sin autenticarse. |
| Mejorar la calidad del catálogo | Ningún curso `pending_review` o `rejected` aparece en catálogo público. |
| Facilitar aportes completos | Backend valida todos los campos obligatorios y muestra errores asociados a los campos. |
| Permitir planificar el aprendizaje | Usuario puede agregar un curso válido, verlo en su roadmap, cambiar estado y quitarlo. |
| Proteger las cuentas | Login tiene rate limit server-side; contraseñas se almacenan con hash adaptativo; recuperación usa token temporal de un solo uso. |
| Mantener comportamiento consistente | Todas las colecciones están paginadas, ordenadas de forma estable y limitadas por máximo de página. |

Metas cuantitativas iniciales para una prueba manual: 100% de endpoints de listado con paginación; 100% de pruebas de aceptación P0 ejecutadas manualmente antes de la entrega; cero credenciales en texto plano; cero acceso cruzado a roadmaps entre usuarios. No son métricas de producción ni se afirma que ya estén verificadas.

## 3. Personas

### Persona 1 — Martina, estudiante autodidacta

- **Contexto:** estudia y trabaja; encuentra cursos gratuitos en múltiples plataformas.
- **Motivaciones:** comparar opciones, guardar cursos relevantes y organizar el orden de aprendizaje.
- **Frustraciones hoy:** enlaces dispersos, datos incompletos y listas personales sin estados.
- **Historias tipo:** “Quiero encontrar cursos de Python sin abrir diez sitios”; “quiero guardar los que haré después”; “quiero ver qué tengo en curso”.

### Persona 2 — Diego, colaborador de la comunidad

- **Contexto:** realizó cursos gratuitos y quiere compartir recursos útiles.
- **Motivaciones:** aportar un curso una sola vez y que otros puedan descubrirlo con información consistente.
- **Frustraciones hoy:** formularios que no explican qué falta y catálogos con enlaces vencidos.
- **Historias tipo:** “Quiero proponer un curso con los datos completos”; “quiero saber si mi aporte está pendiente o fue rechazado”.

### Persona 3 — Sofía, moderadora

- **Contexto:** persona autorizada para revisar calidad de aportes.
- **Motivaciones:** publicar cursos reales, gratuitos, completos y no duplicados.
- **Frustraciones hoy:** tener que buscar manualmente datos repartidos o no conocer qué se modificó.
- **Historias tipo:** “Quiero revisar los aportes pendientes”; “quiero aprobar o rechazar con un motivo claro”.

## 4. User stories

| ID | Prioridad | Historia | Criterios de aceptación |
|---|---|---|---|
| US-001 | P0 | Como visitante, quiero explorar el catálogo para descubrir cursos sin registrarme. | - [ ] `GET /api/v1/courses` devuelve solo cursos publicados/validados.<br>- [ ] La respuesta contiene `items`, `total`, `limit`, `offset`.<br>- [ ] El listado tiene orden estable y no devuelve más que `limit`.<br>- [ ] Catálogo vacío muestra estado vacío y CTA para aportar/iniciar sesión. |
| US-002 | P0 | Como visitante, quiero abrir el detalle de un curso para evaluar si me sirve. | - [ ] El detalle muestra título, tema, categoría, versión, año, docentes, enlace externo y datos de cuestionario/examen/certificado/aval.<br>- [ ] Un curso no validado no es accesible por API pública.<br>- [ ] El enlace externo se abre de forma segura y se identifica como externo. |
| US-003 | P0 | Como usuario, quiero registrarme e iniciar sesión para gestionar mis cursos. | - [ ] Registro valida email y política de contraseña y evita emails duplicados.<br>- [ ] Login correcto crea sesión segura.<br>- [ ] Login incorrecto devuelve mensaje genérico y aplica rate limit.<br>- [ ] Logout invalida la sesión. |
| US-004 | P0 | Como usuario, quiero recuperar mi contraseña para recuperar el acceso a mi cuenta. | - [ ] Solicitud responde con mensaje genérico independientemente de si el email existe.<br>- [ ] Token aleatorio expira a los 30 minutos y solo puede usarse una vez.<br>- [ ] Al restablecer, se invalida el token y las sesiones existentes se invalidan o se exige volver a iniciar sesión. |
| US-005 | P0 | Como usuario autenticado, quiero aportar un curso gratuito para compartirlo con la comunidad. | - [ ] Formulario solicita URL, categoría, tema, título, versión, año, docentes, declaración de toma y cuatro respuestas sí/no.<br>- [ ] Backend valida URL, año, categoría y campos obligatorios.<br>- [ ] Curso nuevo queda `pending_review` y no aparece en catálogo público.<br>- [ ] URL duplicada no se acepta y se explica el problema sin filtrar datos privados. |
| US-006 | P0 | Como usuario autenticado, quiero agregar un curso validado a mi roadmap para organizar mi aprendizaje. | - [ ] Solo cursos validados se pueden agregar.<br>- [ ] El curso aparece en el roadmap privado con estado inicial `planned`.<br>- [ ] No se duplica el mismo curso en el roadmap del mismo usuario.<br>- [ ] Otro usuario no puede leer ni modificar el roadmap ajeno. |
| US-007 | P0 | Como usuario, quiero cambiar el estado o quitar un curso de mi roadmap para mantenerlo actualizado. | - [ ] Estados admitidos: `planned`, `in_progress`, `completed`.<br>- [ ] Se puede cambiar el estado y quitar el elemento propio.<br>- [ ] Una modificación ajena devuelve 404 o 403 sin revelar información sensible. |
| US-008 | P1 | Como usuario, quiero buscar y filtrar cursos para encontrar opciones relevantes. | - [ ] Búsqueda de texto en título, tema, docente o proveedor.<br>- [ ] Filtros por categoría, tema y presencia de certificado.<br>- [ ] Filtros y búsqueda conservan paginación y se pueden limpiar. |
| US-009 | P0 | Como moderadora, quiero revisar aportes pendientes para decidir qué se publica. | - [ ] Solo rol `moderator` accede a la cola.<br>- [ ] La cola es paginada y muestra metadatos y URL.<br>- [ ] Aprobar cambia estado a `published`; rechazar requiere motivo y cambia a `rejected`.<br>- [ ] Se registra quién revisó y cuándo. |
| US-010 | P1 | Como usuario, quiero consultar el estado de mis aportes para saber si debo actuar. | - [ ] El usuario ve únicamente sus aportes y sus estados.<br>- [ ] Rechazos muestran el motivo de moderación.<br>- [ ] El listado está paginado. |
| US-011 | P0 | Como usuario, quiero consultar categorías para clasificar correctamente un curso. | - [ ] El formulario consume la lista del backend.<br>- [ ] Solo categorías activas son válidas al crear aportes.<br>- [ ] El endpoint de categorías está paginado si se modela como listado ampliable. |

## 5. Requisitos funcionales

| ID | Requisito | Historia relacionada |
|---|---|---|
| RF-001 | Registrar cuenta con email único y contraseña validada. | US-003 |
| RF-002 | Autenticar y cerrar sesión de forma segura. | US-003 |
| RF-003 | Solicitar y completar recuperación de contraseña por token temporal. | US-004 |
| RF-004 | Aplicar rate limiting al login en backend, con respuesta HTTP 429 y `Retry-After` cuando corresponda. | US-003 |
| RF-005 | Listar cursos publicados con paginación y filtros. | US-001, US-008 |
| RF-006 | Consultar detalle público solo de cursos publicados. | US-002 |
| RF-007 | Crear aportes completos en estado pendiente. | US-005 |
| RF-008 | Revisar y aprobar/rechazar aportes con auditoría. | US-009 |
| RF-009 | Consultar los propios aportes y su estado. | US-010 |
| RF-010 | Agregar/quitar curso al roadmap propio y actualizar estado. | US-006, US-007 |
| RF-011 | Aplicar autorización por rol y propiedad en cada operación protegida. | US-003, US-006, US-009 |
| RF-012 | Exponer categorías activas para formularios. | US-011 |

## 6. Requisitos no funcionales

| ID | Requisito | Notas / verificación |
|---|---|---|
| RNF-001 | Todos los listados deben estar paginados. | API y UI; `limit` predeterminado 20, máximo 100, `offset` no negativo, total incluido. |
| RNF-002 | Mobile-first con mejora progresiva. | Estilos base sin media queries; solo `min-width` para mejorar. |
| RNF-003 | Menú sándwich en mobile. | Teclado, foco visible y `aria-expanded`. |
| RNF-004 | Contraseñas nunca se almacenan en claro. | Hash Argon2id recomendado; bcrypt mínimo requerido por SPEC. Ver TRD. |
| RNF-005 | Secretos fuera del repositorio. | Variables de entorno y `.env.example` sin valores secretos. |
| RNF-006 | Autorización en backend. | No confiar en ocultar botones o IDs enviados por frontend. |
| RNF-007 | API consistente. | Prefijo `/api/v1`, validación de entrada, errores JSON uniformes. |
| RNF-008 | Responsive desde 320 px y usable con teclado. | Ver UX-UI §6. |
| RNF-009 | Tiempos razonables para MVP local. | Con 1.000 cursos seed, objetivo de respuesta p95 menor a 500 ms en consultas simples en entorno local de referencia; medir, no asumir. |
| RNF-010 | Despliegue reproducible en máquina limpia. | Después de aprobación: `docker compose up --build` levanta servicios y migraciones/seed documentados. |
| RNF-011 | Listados con orden determinista. | Orden por campo explícito y `id` como desempate. |
| RNF-012 | No filtrar existencia de cuentas. | Respuesta genérica en recuperación y errores de autenticación. |

## 7. Reglas de negocio

| ID | Regla | Fuente |
|---|---|---|
| BR-001 | Solo cursos validados/publicados aparecen en el catálogo público. | SPEC clase |
| BR-002 | El aportante declara si realizó el curso. | SPEC clase |
| BR-003 | Solo usuarios autenticados pueden aportar y gestionar roadmaps. | Decisión propia |
| BR-004 | La URL canónica de un curso es única; no se admiten duplicados. | Decisión propia |
| BR-005 | Los campos enumerados en SPEC son obligatorios; las cuatro preguntas se responden sí/no explícitamente. | SPEC + interpretación explícita |
| BR-006 | Si `is_endorsed=true`, `endorsing_organization` debe contener el nombre de la organización; si es false, puede ser nulo. | Decisión propia |
| BR-007 | Un aporte comienza en `pending_review`; el moderador puede aprobar o rechazar con motivo. | Decisión propia para resolver validación |
| BR-008 | Un curso puede aparecer una sola vez en el roadmap de cada usuario. | Decisión propia |
| BR-009 | Cada elemento del roadmap pertenece a un usuario y a un curso; el estado es `planned`, `in_progress` o `completed`. | Decisión propia |
| BR-010 | Moderación y autorización se verifican en backend, nunca solo en la interfaz. | Seguridad |
| BR-011 | Un token de recuperación expira, es de un solo uso y se guarda en forma de hash. | Seguridad |
| BR-012 | Los años de edición se validan contra un rango razonable: 1900 hasta el año actual + 1. | Decisión propia |

## 8. Fuera de alcance (out of scope)

- Pagos, suscripciones, cursos pagos o comisiones.
- Hospedaje o reproducción de contenido de terceros.
- Emisión de certificados, validación automática de certificados o scraping de proveedores.
- OAuth, SSO, MFA, SMS y aplicaciones nativas.
- Roadmaps compartidos/públicos, comentarios, mensajes y redes sociales.
- Recomendaciones basadas en IA, gamificación y analítica avanzada.
- Panel administrativo general; el rol moderador cubre únicamente la cola de aportes.
- Producción de alta disponibilidad, escalado horizontal y despliegue cloud como requisito de MVP.
- Tests unitarios obligatorios, Docker multi-stage, optimización avanzada de imágenes y healthchecks avanzados: quedan para la clase del 27/10, aunque el plan deja puntos de extensión.

## 9. Supuestos y decisiones sobre la SPEC de clase

La validación se realiza con rol `moderator`; el catálogo es público pero los aportes y roadmaps requieren cuenta. “Incluir en el catálogo personal” se implementa como relación de roadmap, no como copia del curso. El roadmap es privado. Los metadatos obligatorios y la estrategia de recuperación se detallan en [SPEC.md §8](SPEC.md) y [BackendSchema.md](BackendSchema.md). Las decisiones técnicas, incluidas sesiones, rate limiting y almacenamiento de tokens, están en [TRD.md](TRD.md).

## 10. Preguntas abiertas

| Pregunta | Impacto | Estado |
|---|---|---|
| ¿El docente exige verificación de email antes de permitir aportes? | Medio; afecta email y flujo de registro. | Decisión provisional: no requerida en MVP; confirmar con docente. |
| ¿La moderación debe estar disponible para una cuenta docente precreada o asignarse desde consola? | Medio; afecta provisión del rol. | Decidido: provisión manual por seed/configuración en entorno controlado; no endpoint público para elevar roles. |
| ¿Se exige proveedor SMTP real para demo? | Medio; afecta recuperación E2E. | Decidido: SMTP configurable; localmente se admite servidor de email de prueba, documentando cómo inspeccionar el mensaje. |

---

**Trazabilidad:** SPEC §4–8; TRD §2–6; UX-UI §3–6; APPFlow §1–5; BackendSchema §1–4; IMPLEMENTATION_PLAN módulos M0–M5.
