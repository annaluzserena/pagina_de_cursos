# PRD — Product Requirements Document

- Versión: 0.1
- Estado: borrador para validación
- Referencia: `SPEC.md`

## 1. Visión del producto

Ayudar a personas autodidactas a descubrir cursos gratuitos y avanzar mediante itinerarios de aprendizaje claros, ordenados y medibles.

## 2. Usuarios objetivo

### Estudiante autodidacta
Busca aprender una habilidad, no quiere pagar por los cursos y necesita una secuencia sugerida. Valora la búsqueda, los filtros, la claridad de requisitos previos y el seguimiento del avance.

### Administrador de contenido
Necesita publicar y mantener cursos y roadmaps de manera consistente, con validaciones que eviten enlaces rotos, duplicados y orden incorrecto.

## 3. Propuesta de valor

- Catálogo organizado de recursos gratuitos.
- Roadmaps que convierten una lista de recursos en un recorrido progresivo.
- Seguimiento sencillo del aprendizaje.
- Experiencia rápida, clara y sin ruido visual.
- Cuenta segura con recuperación y controles antiabuso.

## 4. Métricas de éxito iniciales

Son objetivos de producto para evaluar, no garantías de rendimiento:

- 100 % de endpoints protegidos con pruebas de autorización.
- 100 % de flujos críticos de autenticación cubiertos por pruebas de integración.
- Un usuario nuevo puede registrarse e inscribirse en un curso sin asistencia.
- Un administrador puede crear y publicar un curso mediante el flujo documentado.
- No existen defectos bloqueantes conocidos en los flujos principales.
- La navegación con teclado permite completar login, búsqueda e inscripción.
- Los errores de validación se muestran junto al campo pertinente y con mensaje comprensible.

## 5. Priorización

- **P0:** imprescindible para que el MVP sea seguro y funcional.
- **P1:** importante para una experiencia completa, implementable tras P0.
- **P2:** mejora futura.

## 6. Funcionalidades

### F-01 — Catálogo público (P0)
El visitante puede consultar cursos publicados en una lista paginada.

Criterios:
- La respuesta contiene datos mínimos para representar cada curso.
- No se exponen cursos en borrador ni archivados.
- La paginación tiene límites máximos del lado del servidor.
- Si no hay resultados, se muestra un estado vacío con opción de limpiar filtros.

### F-02 — Búsqueda y filtros (P0)
El visitante puede buscar por título y descripción y filtrar por categoría y dificultad.

Criterios:
- Los filtros se pueden combinar.
- Los parámetros inválidos se rechazan o normalizan de forma documentada.
- El orden predeterminado es estable.
- El backend usa consultas parametrizadas y no concatena SQL de usuario.

### F-03 — Registro (P0)
El visitante crea una cuenta.

Campos mínimos: nombre visible, email, contraseña y confirmación de contraseña en frontend. La confirmación no necesita almacenarse.

Criterios:
- El email se normaliza y tiene restricción única.
- La contraseña se valida en backend según una política explícita.
- La respuesta no devuelve hash ni secretos.
- El rol inicial es `student`.
- Se limita el abuso por IP y por identificador.

### F-04 — Login y logout (P0)
El usuario inicia y termina una sesión.

Criterios:
- Mensaje genérico para credenciales inválidas.
- El endpoint tiene rate limit igual a 5 intentos.
- El frontend puede consultar la sesión actual.
- Logout invalida la sesión del servidor o revoca el mecanismo elegido.
- Las cookies tienen atributos de seguridad configurados.

### F-05 — Recuperación de contraseña (P0)
El usuario solicita un enlace de recuperación y establece una contraseña nueva.

Criterios:
- La respuesta inicial es genérica tanto para emails registrados como no registrados.
- El token se genera criptográficamente, expira y se usa una sola vez.
- Se almacena el hash del token, no el token en texto plano.
- El cambio de contraseña invalida el token.
- Se revocan sesiones existentes según la política de seguridad.
- Se aplican límites a solicitudes y validaciones del token.
- No se registran tokens ni URLs completas de recuperación en logs.

### F-06 — CRUD de cursos (P0)
Un administrador crea, consulta, actualiza y archiva cursos.

Campos sugeridos: título, slug, descripción corta, descripción completa, URL externa opcional, categoría, dificultad, duración estimada, estado de publicación y fechas.

Criterios:
- Validación del slug y unicidad.
- URL con esquema permitido, preferentemente HTTPS.
- La API rechaza acciones de usuarios no administradores con 403.
- El archivado conserva integridad referencial.
- Las operaciones de escritura tienen pruebas.

### F-07 — Categorías (P0)
El administrador mantiene categorías utilizadas en el catálogo.

Criterios:
- Nombre y slug únicos.
- No se elimina una categoría en uso sin una política explícita.
- Los cursos no publicados no se vuelven visibles por un cambio de categoría.

### F-08 — Roadmaps (P0)
El administrador crea un itinerario con etapas ordenadas y cursos asociados. El estudiante también puede crear y publicar itinerarios personalizados.

Criterios:
- Cada etapa tiene título, descripción opcional y posición.
- Cada curso asociado tiene posición explícita.
- La API devuelve etapas y cursos en orden.
- Un roadmap no publicado no se muestra públicamente.
- El administrador puede previsualizarlo antes de publicar.

### F-09 — Inscripciones (P0)
Un estudiante se inscribe en un curso publicado.

Criterios:
- El usuario se obtiene de la sesión autenticada.
- La combinación usuario/curso es única.
- Un visitante recibe 401.
- Un curso archivado no admite nuevas inscripciones.
- La operación es idempotente o responde con conflicto controlado ante duplicados.

### F-10 — Progreso (P0)
El estudiante registra el estado de un curso.

Estados: `not_started`, `in_progress`, `completed`.

Criterios:
- Solo el propietario puede actualizar la inscripción.
- Se conserva `created_at` y se actualiza `updated_at`.
- La interfaz representa el estado con texto y no solo color.
- La API valida la transición y los valores permitidos.

### F-11 — Perfil de usuario (P1)
El estudiante consulta y actualiza los datos de perfil permitidos.

Criterios:
- No puede cambiar su rol.
- No puede leer ni modificar el perfil privado de otra persona.
- La contraseña se cambia por un flujo separado.

### F-12 — Panel administrativo (P1)
Área privada para gestionar cursos, categorías y roadmaps.

Criterios:
- La navegación administrativa se oculta para roles no autorizados por UX, pero la API verifica siempre los permisos.
- Se muestran errores accionables y confirmación antes de archivar.
- Formularios conservan los datos ante errores recuperables.

### F-13 — Auditoría mínima (P1)
Registrar acciones sensibles como cambios de rol, publicación y archivado de contenido, sin almacenar secretos.

## 7. Historias de usuario

- **HU-01:** Como visitante, quiero explorar cursos para encontrar recursos relevantes.
- **HU-02:** Como visitante, quiero filtrar por categoría y dificultad para reducir resultados.
- **HU-03:** Como visitante, quiero registrarme para guardar mi progreso.
- **HU-04:** Como usuario, quiero iniciar y cerrar sesión de forma segura.
- **HU-05:** Como usuario, quiero recuperar mi contraseña si la olvido.
- **HU-06:** Como administrador, quiero crear y editar cursos para mantener el catálogo actualizado.
- **HU-07:** Como administrador, quiero archivar cursos obsoletos sin romper referencias.
- **HU-08:** Como administrador/estudiante, quiero organizar cursos en etapas para construir un roadmap.
- **HU-09:** Como estudiante, quiero inscribirme en un curso para registrar mi aprendizaje.
- **HU-10:** Como estudiante, quiero marcar un curso en progreso o completado para conocer mi avance.
- **HU-11:** Como estudiante, quiero consultar mis inscripciones para retomar el aprendizaje.
- **HU-12:** Como administrador, quiero publicar un roadmap para hacerlo visible.
- **HU-13:** Como usuario, quiero recibir mensajes claros cuando un formulario falle.
- **HU-14:** Como usuario, quiero que la plataforma funcione en móvil y con teclado.

## 8. MVP y fuera de alcance

### Incluido en MVP
Catálogo, búsqueda básica, registro, login/logout, recuperación, rate limit, CRUD administrativo de cursos/categorías/roadmaps, inscripciones, progreso, Docker Compose, migraciones y pruebas de seguridad esenciales.

### Fuera del MVP
OAuth, gamificación, comentarios, certificados, pagos, notificaciones push, analítica avanzada, editor visual de dependencias y recomendaciones personalizadas.

## 9. Flujos de aceptación de alto nivel

### Registro
1. El visitante abre registro.
2. Completa campos válidos.
3. El backend valida, normaliza email y aplica rate limit.
4. La cuenta se crea con rol predeterminado.
5. Se muestra confirmación sin exponer datos sensibles.

### Recuperación
1. El usuario solicita recuperación.
2. Se muestra una respuesta genérica.
3. Si la cuenta existe, se envía un enlace temporal.
4. El usuario establece una nueva contraseña.
5. El token se invalida y se revocan sesiones según política.
6. El usuario puede iniciar sesión con la nueva contraseña.

### Publicación de curso
1. Administrador autenticado abre el panel.
2. Crea o edita un curso.
3. El backend valida los datos y permisos.
4. El administrador guarda como borrador o publica.
5. El catálogo solo muestra el curso cuando está publicado.

## 10. Definición de terminado (DoD)

Una historia está terminada cuando:
- cumple sus criterios de aceptación;
- incluye validación del backend y mensajes de interfaz;
- incluye pruebas unitarias o de integración apropiadas;
- verifica autenticación, autorización y abuso si corresponde;
- está documentada cuando cambia un contrato;
- pasa lint, typecheck y pruebas automatizadas;
- no expone secretos ni datos privados en logs;
- se revisa accesibilidad básica y responsive;
- se integra mediante revisión de código.
