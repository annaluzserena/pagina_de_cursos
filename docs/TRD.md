# TRD — Technical Requirements Document

- Versión: 0.1
- Estado: propuesta técnica inicial
- Referencia funcional: `SPEC.md`, `PRD.md`

## 1. Stack

### Frontend
- React 19.
- Vite.
- TypeScript.
- pnpm.
- React Router para navegación.
- TanStack Query (o alternativa equivalente) para estado remoto y caché.
- React Hook Form y Zod para formularios y validación de experiencia.
- Vitest y React Testing Library para pruebas.
- CSS Modules o CSS organizado por capas; evitar estilos globales que sobrescriban accidentalmente componentes.

### Backend
- Python con versión fijada y soportada.
- FastAPI.
- uv para gestión del entorno y dependencias.
- Pydantic v2 para esquemas.
- SQLAlchemy 2.x para ORM.
- Alembic para migraciones.
- PostgreSQL.
- pytest y HTTPX para pruebas.
- Biblioteca mantenida para hashing de contraseñas, preferentemente Argon2id.
- Cliente de correo abstraído detrás de un servicio.

### Infraestructura
- Dockerfiles separados para frontend y backend.
- Docker Compose, con PostgreSQL incluido, para portabilidad.
- PostgreSQL en servicio propio para desarrollo local.
- Volumen persistente de base de datos.
- Health checks y dependencias de arranque.
- No exponer PostgreSQL públicamente en producción.

## 2. Arquitectura lógica

Arquitectura cliente-servidor con API REST:

1. El navegador ejecuta la SPA de React.
2. El frontend llama a la API FastAPI mediante HTTPS en producción.
3. FastAPI valida datos, sesión, permisos y límites de solicitud.
4. La capa de servicio aplica reglas de negocio.
5. SQLAlchemy persiste datos en PostgreSQL.
6. Un servicio de correo envía enlaces de recuperación.
7. Los logs y eventos de auditoría excluyen secretos.

La UI no es autoridad de seguridad. Toda autorización se vuelve a comprobar en cada operación del backend.

## 3. Organización propuesta del repositorio

```text
pagina_de_cursos/
├── frontend/
│   ├── src/
│   │   ├── app/
│   │   ├── components/
│   │   ├── features/
│   │   │   ├── auth/
│   │   │   ├── courses/
│   │   │   ├── roadmaps/
│   │   │   ├── enrollments/
│   │   │   └── admin/
│   │   ├── lib/
│   │   ├── routes/
│   │   ├── styles/
│   │   └── test/
│   ├── public/
│   ├── package.json
│   └── vite.config.ts
├── backend/
│   ├── app/
│   │   ├── api/
│   │   │   ├── deps.py
│   │   │   └── v1/
│   │   ├── core/
│   │   ├── db/
│   │   ├── models/
│   │   ├── schemas/
│   │   ├── repositories/
│   │   ├── services/
│   │   ├── security/
│   │   └── main.py
│   ├── migrations/
│   ├── tests/
│   └── pyproject.toml
├── docs/
├── compose.yaml
├── .env.example
├── .gitignore
└── README.md
```

## 4. Responsabilidades por capa

- **API/router:** HTTP, parámetros, códigos de estado y dependencias de autenticación.
- **Schema:** validación y serialización de entrada/salida; nunca exponer modelos ORM completos por defecto.
- **Service:** reglas de negocio y coordinación transaccional.
- **Repository:** consultas y persistencia cuando la complejidad lo justifique.
- **Model:** entidades ORM, relaciones e invariantes persistentes.
- **Security:** hash de contraseñas, emisión/validación de sesión, permisos, tokens y rate limit.
- **Core/config:** configuración tipada, logging y manejo común de errores.

No es necesario crear abstracciones innecesarias para cada función pequeña. La separación debe ayudar a probar y mantener el sistema, no añadir capas vacías.

## 5. Convenciones API

- Prefijo: `/api/v1`.
- JSON como formato de intercambio.
- Fechas ISO 8601 con zona horaria.
- Paginación con `limit` y `offset` para el MVP; validar límites y documentar estabilidad. Puede evolucionar a cursor.
- Nombres de recursos en plural.
- Códigos HTTP semánticos.
- OpenAPI generado por FastAPI.
- Errores consistentes, sin trazas internas en producción.

### Códigos frecuentes
- `200 OK`: lectura o actualización con respuesta.
- `201 Created`: creación.
- `204 No Content`: operación exitosa sin cuerpo.
- `400 Bad Request`: solicitud mal formada o regla de entrada no representable mejor con otro código.
- `401 Unauthorized`: falta autenticación válida.
- `403 Forbidden`: autenticado, sin permiso.
- `404 Not Found`: recurso inexistente o deliberadamente oculto por política de privacidad.
- `409 Conflict`: conflicto de unicidad o estado.
- `422 Unprocessable Entity`: validación de esquema o dominio, según contrato.
- `429 Too Many Requests`: límite excedido.
- `500 Internal Server Error`: error inesperado, con identificador de correlación.

## 6. Contrato de error sugerido

```json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Revisá los campos indicados.",
    "details": [
      {
        "field": "title",
        "code": "required",
        "message": "El título es obligatorio."
      }
    ],
    "request_id": "identificador-opaco"
  }
}
```

No devolver detalles de stack trace, consultas SQL, rutas internas ni secretos.

## 7. Autenticación y sesiones

### Estrategia propuesta
Para una SPA y API desplegadas bajo el mismo sitio, preferir cookie de sesión `HttpOnly`, `Secure` en producción, `SameSite=Lax` o una política ajustada al flujo y `Path` mínimo. Elegir entre sesión opaca almacenada en servidor o mecanismo firmado revocable; documentar expiración, renovación y revocación.

Si se usa cookie para autenticar solicitudes mutables, analizar y aplicar protección CSRF (token anti-CSRF y/o estrategia de origen según arquitectura). CORS no reemplaza CSRF.

No guardar tokens de sesión de larga duración en `localStorage` si puede evitarse. Si el despliegue exige bearer tokens, definir expiración breve, renovación, revocación y almacenamiento con un análisis de amenazas explícito.

### Contraseñas
- Hash con Argon2id y parámetros actualizados.
- No cifrar reversiblemente ni almacenar contraseñas en texto plano.
- Limitar intentos y evitar mensajes que faciliten enumeración.
- No registrar credenciales.
- No enviar contraseñas por email.

### Recuperación
- Generar secreto aleatorio con fuente criptográfica.
- Enviar por canal confiable.
- Guardar solo hash del token.
- Aplicar caducidad configurable y uso único.
- Invalidar tokens previos cuando se solicite uno nuevo, si la política lo determina.
- Construir enlaces con un origen frontend permitido por configuración; no confiar en el header `Host` sin validación.
- Respuesta genérica para prevenir enumeración de cuentas.

## 8. Rate limiting

Aplicar límites al menos en:
- `POST /auth/register`
- `POST /auth/login`
- `POST /auth/password/forgot`
- `POST /auth/password/reset`
- verificación de email, si existe
- endpoints de escritura y búsquedas costosas cuando proceda.

Política:
- Combinar límite por IP y por identificador normalizado para login/recuperación, cuidando no permitir que terceros bloqueen permanentemente una cuenta.
- Responder 429 y `Retry-After` cuando se pueda estimar la espera.
- No usar solo memoria local si hay múltiples réplicas: preferir un backend compartido como Redis si el despliegue lo requiere. Para un MVP de una sola instancia, documentar las limitaciones del almacenamiento local y no presentarlo como protección distribuida.
- Confiar en IP reenviada solo desde proxies conocidos y configurados.
- Registrar métricas agregadas, no contraseñas ni tokens.
- Los límites definitivos se configurarán mediante variables de entorno y pruebas; no deben considerarse valores universales.

## 9. Seguridad adicional

- Validación estricta del lado servidor.
- Consultas parametrizadas/ORM.
- Protección contra asignación masiva: no aceptar `role`, `is_admin` u otros campos privilegiados en esquemas de usuario comunes.
- Verificar propiedad del recurso en operaciones de inscripción y progreso.
- Política de CORS limitada a orígenes explícitos.
- HTTPS en producción.
- Cabeceras de seguridad apropiadas en el punto de entrada.
- Dependencias actualizadas y análisis de vulnerabilidades.
- Límites de tamaño de cuerpo y timeout.
- Protección contra enumeración de usuarios.
- Política de logs y retención.
- Backups y prueba de restauración.
- Secretos fuera de imágenes y repositorio.

## 10. Base de datos y transacciones

- PostgreSQL como fuente de verdad.
- Restricciones `NOT NULL`, `UNIQUE`, `CHECK` y claves foráneas para invariantes.
- Fechas con zona horaria (`TIMESTAMPTZ`).
- Índices sobre columnas de búsqueda, claves foráneas y estados consultados frecuentemente.
- Migraciones versionadas con Alembic.
- No ejecutar migraciones automáticamente en cada réplica de producción sin coordinación.
- Usar transacciones para cambios relacionados, por ejemplo crear roadmap, etapas y asociaciones.

## 11. Configuración y entorno

Variables ilustrativas; los nombres finales deben mantenerse consistentes con el código:

```env
APP_ENV=development
API_PREFIX=/api/v1
DATABASE_URL=postgresql+psycopg://app:change-me@db:5432/courses
FRONTEND_ORIGIN=http://localhost:5173
SESSION_SECRET=replace-with-random-secret
SESSION_TTL_MINUTES=60
PASSWORD_RESET_TTL_MINUTES=30
RATE_LIMIT_STORAGE_URL=
MAIL_FROM=
MAIL_PROVIDER_API_KEY=
```

`.env.example` contiene solo valores ficticios. `SESSION_SECRET` debe generarse de forma segura en cada entorno. No usar credenciales por defecto en despliegues públicos.

## 12. Docker Compose

Servicios esperados:
- `frontend`: servidor de desarrollo en local o servidor de archivos estáticos en imagen de producción.
- `api`: FastAPI.
- `db`: PostgreSQL con volumen persistente y health check.
- Opcional `redis`: almacenamiento compartido para rate limit/sesiones si la arquitectura elegida lo necesita.

Usar usuarios no privilegiados en imágenes, imágenes base fijadas, `.dockerignore`, health checks y redes internas. No incluir `.env` ni credenciales en la imagen. La configuración de desarrollo no debe confundirse con la de producción.

## 13. Observabilidad

- Logs estructurados.
- Nivel de log configurable.
- Request ID/correlation ID.
- Métricas de errores, latencia, 401/403/429 y fallos de correo.
- No loguear tokens de recuperación, cookies, contraseñas ni cuerpos sensibles.
- Endpoint de salud separado de readiness cuando sea necesario.
- Mensajes de error públicos genéricos y detalle interno solo en logs protegidos.

## 14. Pruebas

### Backend
- Unitarias de servicios y validaciones.
- Integración con PostgreSQL de prueba.
- API tests para códigos HTTP y contrato.
- Permisos por rol y propiedad.
- Recuperación, expiración y uso único.
- Rate limit y respuestas 429.
- Migraciones desde base vacía.
- Casos de carrera para inscripción duplicada.

### Frontend
- Componentes y formularios.
- Validación de estados de carga/error/vacío.
- Rutas protegidas y navegación.
- Accesibilidad básica.
- Flujos integrados con API simulada o entorno de prueba.

### End-to-end
Registro/login, catálogo, inscripción, progreso, recuperación y CRUD administrativo.

## 15. Decisiones técnicas pendientes

- Cookie de sesión opaca frente a sesión firmada.
- Redis para rate limit desde el MVP o solo al escalar.
- Proveedor de correo.
- Estrategia de despliegue y proxy TLS.
- Búsqueda PostgreSQL simple frente a búsqueda full-text.
- Política de borrado de cuenta y retención de auditoría.
