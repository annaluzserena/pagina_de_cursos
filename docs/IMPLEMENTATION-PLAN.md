# Plan de implementación

- Versión: 0.1
- Referencias: todos los documentos de producto y diseño

## 1. Estrategia

Implementar en incrementos verticales: cada fase debe dejar una parte funcional y comprobable del producto. Priorizar contratos, seguridad y modelo de datos antes de ampliar la interfaz. No desarrollar todo el frontend separado del backend durante demasiado tiempo.

## 2. Fase 0 — Validación y decisiones

Tareas:
- Revisar alcance del MVP con docente/equipo.
- Confirmar verificación de email, estrategia de sesión y proveedor de correo.
- Definir política de recuperación, rate limit y retención.
- Resolver si roadmap/progreso es global o específico del itinerario.
- Confirmar reglas de publicación y archivado.
- Acordar convenciones de ramas, commits y revisión.

Entregables:
- Documentos aprobados.
- Lista de decisiones pendientes resueltas o registradas como ADR.
- Criterios de aceptación confirmados.

Criterio de salida: no hay decisiones de seguridad críticas sin responsable o fecha.

## 3. Fase 1 — Repositorio e infraestructura local

Tareas:
- Crear estructura de frontend y backend.
- Inicializar React 19 + Vite + TypeScript con pnpm.
- Inicializar FastAPI y proyecto Python gestionado por uv.
- Crear `compose.yaml`, Dockerfiles y `.env.example`.
- Levantar PostgreSQL con volumen y health check.
- Agregar lint, format y typecheck.
- Crear endpoints de health/readiness.
- Documentar comandos de desarrollo.

Pruebas:
- Stack inicia desde entorno limpio.
- Frontend puede alcanzar la API.
- API puede conectarse a PostgreSQL.
- Secretos no están en Git ni en imágenes.

Entregables: entorno de desarrollo reproducible y pipeline básico.

## 4. Fase 2 — Persistencia y migraciones

Tareas:
- Configurar SQLAlchemy.
- Crear modelos iniciales y migración Alembic.
- Agregar restricciones e índices.
- Configurar sesiones de base de datos y transacciones.
- Definir datos semilla solo para desarrollo.
- Probar migración desde cero.

Pruebas:
- Restricciones de unicidad.
- Relaciones y borrados/archivado.
- Migración hacia delante.
- Transacciones ante errores.

Entregables: esquema versionado y repositorio de persistencia probado.

## 5. Fase 3 — Autenticación y seguridad base

Tareas:
- Registro y normalización de email.
- Hash de contraseñas.
- Login/logout y consulta de sesión.
- Autorización por roles.
- Protección CSRF si se usan cookies para mutaciones.
- Recuperación de contraseña.
- Abstracción de proveedor de correo.
- Rate limit para rutas sensibles.
- Respuestas de error uniformes.
- Logs sin secretos.

Pruebas:
- Registro válido y duplicado.
- Credenciales incorrectas.
- Sesión expirada/revocada.
- Token de recuperación inválido, vencido y reutilizado.
- No enumeración en recuperación.
- Rate limit y HTTP 429.
- Usuario no admin bloqueado en endpoints administrativos.
- Acceso a recursos de otro usuario denegado.

Entregables: sistema de identidad seguro y documentado.

## 6. Fase 4 — Catálogo y CRUD de cursos/categorías

Tareas:
- Endpoints públicos de listado/detalle.
- Búsqueda, filtros y paginación.
- CRUD administrativo.
- Validación de URL, slug y estado.
- Archivado y políticas de referencias.
- Componentes frontend de listado, filtros y detalle.
- Formularios administrativos.

Pruebas:
- Solo se muestran publicados.
- Paginación y filtros combinados.
- No admin no puede modificar.
- Slug duplicado.
- URL inválida.
- Archivado con inscripciones/referencias.

Entregables: catálogo utilizable y administración básica.

## 7. Fase 5 — Roadmaps

Tareas:
- Modelo de etapas y asociaciones.
- Endpoints de lectura y administración.
- Creación/edición transaccional.
- Ordenamiento de etapas y cursos.
- Publicación/archivado.
- Vista pública y vista administrativa.

Pruebas:
- Orden estable.
- Restricciones de posiciones.
- Fallo de operación no deja roadmap parcialmente guardado.
- Roadmap borrador no visible públicamente.
- Curso archivado tratado según política acordada.

Entregables: itinerarios publicados y editables.

## 8. Fase 6 — Inscripciones y progreso

Tareas:
- Crear y listar inscripciones propias.
- Actualizar estado.
- Integrar acciones desde curso y roadmap.
- Crear “Mi aprendizaje”.
- Refrescar estado remoto tras mutaciones.

Pruebas:
- Requiere sesión.
- No permite duplicados.
- No permite cambiar progreso ajeno.
- No permite inscribirse en curso no publicado.
- Estados y timestamps coherentes.
- Pruebas de concurrencia para inscripción.

Entregables: ciclo de aprendizaje funcional.

## 9. Fase 7 — UX, accesibilidad y robustez

Tareas:
- Completar estados de carga, vacío, error y rate limit.
- Revisar responsive.
- Navegación por teclado.
- Contraste y etiquetas.
- Manejo global de errores.
- Revisar expiración de sesión.
- Añadir límites de tamaño, timeouts y cabeceras.
- Revisar enlaces externos y contenido no confiable.

Pruebas:
- Teclado en flujos críticos.
- Viewports móvil/tablet/escritorio.
- Formularios con errores.
- Recuperación ante timeout y pérdida de conexión.
- Verificación manual de accesibilidad.

Entregables: UX consistente y accesible.

## 10. Fase 8 — Integración, documentación y entrega

Tareas:
- Ejecutar suites completas.
- Añadir pruebas end-to-end de flujos principales.
- Revisar OpenAPI.
- Verificar instalación limpia.
- Documentar backups y restauración si el despliegue lo requiere.
- Revisar dependencias y secretos.
- Preparar demo con datos ficticios.
- Registrar limitaciones conocidas.

Criterio de salida:
- La instalación funciona siguiendo README.
- Migraciones aplican sin intervención no documentada.
- Tests críticos pasan.
- Los endpoints sensibles tienen pruebas de autorización y rate limit.
- No hay secretos versionados.
- Se conocen y documentan limitaciones restantes.

## 11. Matriz de trazabilidad

| Requisito | Fase principal | Pruebas clave |
|---|---|---|
| Registro/login/logout | 3 | auth integration |
| Recuperación | 3 | token expiry/use once/no enumeration |
| Rate limit | 3 | 429 and bypass/config tests |
| Catálogo y búsqueda | 4 | filtros, paginación, publicación |
| CRUD cursos/categorías | 4 | permisos, validación, archivado |
| Roadmaps | 5 | orden, transacciones, publicación |
| Inscripciones | 6 | unicidad y propiedad |
| Progreso | 6 | transición y autorización |
| UX accesible | 7 | teclado, contraste, responsive |
| Reproducibilidad | 1 y 8 | instalación limpia y Compose |

## 12. Gestión de riesgos

- **Recuperación de contraseña insegura:** revisar token de un solo uso, hash, caducidad y no enumeración.
- **Rate limit ineficaz con varias réplicas:** usar almacenamiento compartido y configurar proxy confiable.
- **Escalada de privilegios:** permitir campos de rol solo en flujos administrativos controlados.
- **IDOR/BOLA en inscripciones:** filtrar por usuario autenticado y probar acceso cruzado.
- **Migraciones inconsistentes:** probar desde base vacía y versión anterior.
- **Scope creep:** diferir funciones P1/P2 que no sean necesarias para el MVP.
- **Mala experiencia en errores:** definir estados y microcopy antes de cerrar los formularios.
- **Dependencia de recursos externos:** indicar claramente que la disponibilidad del curso externo no está garantizada.

## 13. Estrategia de ramas y revisión

Propuesta sencilla para trabajo académico:
- `main`: versión estable.
- ramas cortas por funcionalidad o issue.
- pull request con resumen, pruebas y capturas cuando corresponda.
- revisión por otra persona del equipo.
- no mezclar refactors grandes con cambios funcionales.
- commits descriptivos y pequeños.

## 14. Definition of Ready

Una tarea está lista cuando tiene:
- objetivo claro;
- criterios de aceptación;
- dependencias identificadas;
- contrato de API o UI definido si aplica;
- riesgos de seguridad identificados;
- forma de probar el resultado.

## 15. Definition of Done

Una tarea está terminada cuando cumple la DoD de `PRD.md`, pasa las pruebas pertinentes, está integrada y documentada, y no rompe los flujos ya entregados.
