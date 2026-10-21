# APPFLOW — Mapa de navegación y flujos

- Versión: 0.1
- Referencias: `PRD.md`, `UX-UI.md`, `TRD.md`

## 1. Mapa de rutas

```text
/
├── /courses
│   └── /courses/:slug
├── /roadmaps
│   └── /roadmaps/:slug
|   └── /roadmaps/new
|   └── /roadmaps/:slug/edit
├── /login
├── /register
├── /forgot-password
├── /reset-password?token=...
├── /my-learning                 [estudiante]
├── /profile                     [usuario autenticado]
└── /admin                       [administrador]
    ├── /admin/courses
    │   ├── /admin/courses/new
    │   └── /admin/courses/:id/edit
    ├── /admin/categories
    ├── /admin/roadmaps
    │   ├── /admin/roadmaps/new
    │   └── /admin/roadmaps/:id/edit
    └── /admin/users             [opcional; solo si se aprueba]
```

## 2. Matriz de acceso

| Ruta | Visitante | Estudiante | Administrador |
|---|---:|---:|---:|
| Inicio | Sí | Sí | Sí |
| Catálogo y detalle público | Sí | Sí | Sí |
| Roadmaps publicados | Sí | Sí | Sí |
| Login/registro | Sí | Redirigir o informar sesión activa | Redirigir o informar sesión activa |
| Recuperación | Sí | Sí | Sí |
| Mi aprendizaje | No | Sí | Sí, solo su propia área si aplica |
| Perfil propio | No | Sí | Sí |
| Panel admin | No | No | Sí |

La matriz de frontend mejora la navegación, pero el backend aplica los permisos en cada endpoint.

## 3. Flujo de visitante

1. Abre `/`.
2. Puede ir a `/courses` o `/roadmaps`.
3. Busca y filtra recursos.
4. Abre un detalle.
5. Si intenta inscribirse, se le solicita iniciar sesión o registrarse.
6. Después de autenticarse, vuelve al destino solo si la ruta de retorno es interna y está permitida.

## 4. Flujo de registro

```text
Inicio / Catálogo
    -> Registro
    -> Validación de campos
    -> POST /api/v1/auth/register
        -> 201: mostrar confirmación
        -> 409: conflicto controlado
        -> 422: errores de campos
        -> 429: informar espera
        -> 5xx: error recuperable
    -> Login o sesión iniciada según política
```

El frontend no debe decidir si un email ya existe mediante llamadas de consulta previas. La unicidad se garantiza en la base de datos.

## 5. Flujo de login

```text
Login
  -> Enviar credenciales
  -> POST /api/v1/auth/login
      -> éxito: guardar estado de sesión no sensible y navegar
      -> 401: mensaje genérico
      -> 429: informar espera
      -> error de red: permitir reintentar
```

Al cargar la aplicación, consultar `GET /api/v1/auth/me` para reconstruir el estado de sesión cuando se use cookie. No tratar el estado React como autoridad de autorización.

## 6. Flujo de logout

1. El usuario selecciona “Cerrar sesión”.
2. El frontend envía `POST /api/v1/auth/logout`.
3. El backend invalida la sesión y limpia la cookie si corresponde.
4. El frontend limpia el estado de usuario y cachés privadas.
5. Navega a inicio o login.

Si falla la red, informar el resultado de forma segura y evitar mantener datos privados visibles indefinidamente.

## 7. Recuperación de contraseña

```text
Login -> ¿Olvidaste tu contraseña?
    -> /forgot-password
    -> POST /api/v1/auth/password/forgot
    -> Mostrar mensaje genérico
    -> Usuario abre enlace de email
    -> /reset-password?token=...
    -> POST /api/v1/auth/password/reset
        -> éxito: token invalidado, mostrar confirmación
        -> token inválido/vencido: ofrecer solicitar otro
        -> 429: informar espera
    -> Login
```

El token debe excluirse de logs, herramientas de analítica y reportes de errores. La aplicación debe evitar cargar recursos de terceros en la página de reset que puedan recibir la URL con token mediante cabeceras referer; configurar política `Referrer-Policy` adecuada.

## 8. Flujo de catálogo

1. Abrir `/courses`.
2. Obtener cursos publicados con parámetros de búsqueda y paginación.
3. Mostrar skeleton durante carga.
4. Mostrar resultados, vacío o error.
5. Al cambiar filtros, actualizar la consulta y volver a la primera página.
6. Abrir `/courses/:slug`.

Los parámetros de URL pueden representar búsqueda, filtros y página para permitir compartir enlaces.

## 9. Flujo de inscripción

1. Usuario abre detalle de curso.
2. Si no está autenticado, se solicita login.
3. Si está autenticado, enviar `POST /api/v1/enrollments`.
4. El backend deriva el usuario desde la sesión y verifica que el curso esté publicado.
5. Si ya existe inscripción, responder según contrato idempotente o con `409`.
6. Actualizar caché de catálogo/detalle y mostrar confirmación.
7. El curso aparece en `/my-learning`.

## 10. Flujo de progreso

1. Estudiante abre “Mi aprendizaje”.
2. Selecciona un curso.
3. Cambia el estado de progreso.
4. Envía `PATCH /api/v1/enrollments/{id}` o endpoint equivalente.
5. Backend verifica propiedad y transición válida.
6. UI actualiza el estado solo al confirmar éxito; ante error, revierte o vuelve a consultar.

## 11. Flujo administrativo

### Crear curso
`/admin/courses` -> “Nuevo curso” -> formulario -> validar -> `POST /api/v1/admin/courses` -> confirmar -> volver a lista.

### Editar curso
Lista -> editar -> cargar detalle -> guardar cambios -> `PATCH` o `PUT` -> confirmar cambios.

### Archivar curso
Lista/detalle -> archivar -> diálogo de confirmación -> endpoint de archivado -> actualizar lista. Si hay referencias, conservar integridad.

### Crear roadmap
Lista -> nuevo -> datos generales -> añadir etapas -> ordenar cursos -> previsualizar -> guardar borrador -> publicar. La persistencia de etapas y asociaciones debe realizarse de forma transaccional.

## 12. Guardas y rutas de retorno

- Las rutas privadas comprueban el estado de sesión antes de mostrar contenido privado.
- La ruta administrativa exige rol admin en frontend y backend.
- No aceptar URLs externas arbitrarias como `returnTo`; permitir solo rutas internas conocidas.
- En carga inicial, mostrar estado de comprobación de sesión para evitar parpadeos entre pantallas.
- Un 401 en endpoint protegido puede disparar limpieza de sesión y redirección; evitar bucles de redirección.
- Un 403 no debe tratarse automáticamente como logout: puede ser un usuario autenticado sin permiso.

## 13. Navegación accesible

- Header con enlaces semánticos.
- Enlaces para navegación y botones para acciones.
- Breadcrumbs en administración profunda.
- Foco inicial apropiado tras navegación modal o error.
- Al guardar, anunciar el resultado sin mover el foco de forma inesperada.
