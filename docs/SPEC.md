# SPEC — Especificación general del sistema

- Estado: borrador inicial
- Versión: 0.1
- Producto: Plataforma de Cursos Gratuitos
- Audiencia: equipo de desarrollo, docente, QA y responsables del producto

## 1. Propósito

Definir el problema, los límites, los actores, las reglas de negocio, los requisitos funcionales y no funcionales y los criterios globales de aceptación de una aplicación web para descubrir cursos gratuitos y recorrer itinerarios de aprendizaje.

## 2. Problema y oportunidad

Una persona que desea aprender una habilidad suele encontrar cursos dispersos y carece de una forma sencilla de ordenarlos en una secuencia coherente. La plataforma busca centralizar la exploración de cursos y ofrecer roadmaps curados, inscripción y seguimiento básico del progreso.

## 3. Objetivos

1. Permitir explorar un catálogo de cursos gratuitos.
2. Proporcionar registro, autenticación y recuperación segura de cuenta.
3. Permitir a administradores mantener cursos, categorías y roadmaps.
4. Permitir a estudiantes guardar cursos, inscribirse, registrar su progreso y publicar roadmaps propios.
5. Presentar roadmaps ordenados por etapas y dependencias.
6. Proteger las operaciones mediante autenticación, autorización, validación y limitación de solicitudes.
7. Facilitar ejecución reproducible local con Docker Compose.

## 4. No objetivos del MVP

- Alojar o reproducir videos de cursos.
- Crear un LMS completo con evaluaciones, certificados o mensajería.
- Cobrar pagos o gestionar suscripciones.
- Garantizar la disponibilidad o calidad de cursos externos.
- Integrar proveedores OAuth/social login.
- Implementar recomendaciones basadas en IA.
- Crear una aplicación móvil nativa.
- Administrar contenidos de terceros sin respetar sus términos y licencias.

## 5. Glosario

- **Curso:** recurso formativo que describe una oportunidad de aprendizaje gratuita, con título, descripción, URL externa opcional, dificultad, duración estimada y categoría.
- **Roadmap:** itinerario de aprendizaje compuesto por etapas y cursos ordenados.
- **Etapa:** agrupación lógica dentro de un roadmap.
- **Inscripción:** relación entre un usuario y un curso que indica su estado de aprendizaje.
- **Progreso:** estado registrado por el estudiante para una inscripción.
- **CRUD:** crear, consultar, actualizar y eliminar (o archivar) un recurso.
- **Rate limit:** política que limita solicitudes por sujeto, ruta y ventana temporal.
- **Token de recuperación:** secreto temporal de un solo uso para autorizar el cambio de contraseña.
- **RBAC:** control de acceso basado en roles.

## 6. Actores y permisos

### 6.1 Visitante
Puede consultar los cursos y roadmaps publicados, buscar, filtrar, ver detalles, registrarse e iniciar el proceso de recuperación de contraseña. No puede modificar contenido ni consultar información privada de estudiantes.

### 6.2 Estudiante autenticado
Puede realizar las acciones de visitante, administrar los datos de perfil permitidos, inscribirse en cursos, modificar su progreso y consultar sus inscripciones. Solo puede acceder a sus propios datos privados. También puede crear y publicar roadmaps propios.

### 6.3 Administrador
Puede crear, editar, publicar, archivar y administrar cursos, categorías y roadmaps. Las acciones administrativas deben verificarse en el backend. La administración de usuarios, si se incluye, debe tener permisos explícitos y quedar auditada.

### 6.4 Principio de mínimo privilegio
El rol predeterminado al registrarse es `student`. Ningún endpoint debe aceptar el rol enviado por el cliente como fuente de autoridad. La asignación de `admin` se realiza mediante un proceso administrativo controlado.

## 7. Alcance funcional

### 7.1 Catálogo
- Listar cursos publicados.
- Buscar por texto.
- Filtrar por categoría, dificultad y etiquetas cuando estén disponibles.
- Ordenar por criterios documentados.
- Paginar resultados.
- Ver detalle del curso.
- Mostrar estados vacíos, carga y error.

### 7.2 Cuenta y autenticación
- Registrar cuenta con nombre visible, email y contraseña.
- Normalizar email para evitar duplicados por diferencias de mayúsculas/minúsculas.
- Iniciar sesión y cerrar sesión.
- Consultar la sesión actual.
- Solicitar recuperación de contraseña.
- Validar token de recuperación y establecer nueva contraseña.
- Aplicar rate limiting a registro, login, recuperación y endpoints sensibles.
- Evitar revelar si un email existe en las respuestas de recuperación.
- No almacenar contraseñas ni tokens de recuperación en texto plano.

### 7.3 Cursos
- Crear, consultar, actualizar y archivar cursos.
- Validar campos y URL.
- Impedir que visitantes o estudiantes modifiquen el catálogo.
- No borrar físicamente cursos referenciados por inscripciones o roadmaps sin una política explícita.

### 7.4 Categorías
- Administrar categorías.
- Evitar nombres duplicados después de normalización.
- No permitir eliminar categorías que estén en uso sin reasignación o archivado.

### 7.5 Roadmaps
- Crear, editar, publicar y archivar itinerarios.
- Definir etapas ordenadas.
- Asociar cursos a etapas con una posición explícita.
- Evitar duplicados accidentales de un mismo curso en una etapa, salvo que una decisión futura lo permita.
- Mostrar progreso del estudiante cuando corresponda.

### 7.6 Inscripciones y progreso
- Inscribirse en un curso publicado.
- Impedir inscripciones duplicadas activas para el mismo usuario y curso.
- Cambiar el estado de progreso entre `not_started`, `in_progress` y `completed`.
- Permitir consultar las inscripciones propias.
- El backend debe derivar el usuario desde la sesión autenticada, nunca confiar en un `user_id` arbitrario enviado por el cliente.

## 8. Requisitos funcionales

- **RF-001:** El sistema debe permitir registrar una cuenta con email único y contraseña que cumpla la política configurada.
- **RF-002:** El sistema debe permitir iniciar sesión con credenciales válidas.
- **RF-003:** El sistema debe rechazar credenciales incorrectas sin indicar cuál campo fue el causante.
- **RF-004:** El sistema debe permitir cerrar la sesión actual e invalidar la credencial de sesión.
- **RF-005:** El sistema debe exponer una operación para conocer el usuario autenticado actual.
- **RF-006:** El sistema debe permitir solicitar recuperación de contraseña con respuesta genérica.
- **RF-007:** El sistema debe emitir un token de recuperación aleatorio, temporal y de un solo uso, almacenando solo su hash.
- **RF-008:** El sistema debe invalidar el token de recuperación después de usarlo y revocar las sesiones existentes según la política definida.
- **RF-009:** El sistema debe aplicar rate limiting por IP y, cuando sea apropiado, por cuenta o identificador normalizado.
- **RF-010:** El sistema debe listar cursos publicados con paginación.
- **RF-011:** El sistema debe permitir buscar y filtrar cursos.
- **RF-012:** El sistema debe mostrar detalles de un curso.
- **RF-013:** El administrador debe poder crear cursos.
- **RF-014:** El administrador debe poder actualizar cursos.
- **RF-015:** El administrador debe poder archivar cursos.
- **RF-016:** El administrador debe poder gestionar categorías.
- **RF-017:** El administrador debe poder crear y mantener roadmaps.
- **RF-018:** El roadmap debe mantener el orden explícito de etapas y cursos.
- **RF-019:** El estudiante debe poder inscribirse en un curso publicado.
- **RF-020:** El estudiante debe poder consultar sus inscripciones.
- **RF-021:** El estudiante debe poder actualizar su estado de progreso.
- **RF-022:** El sistema debe impedir el acceso a recursos privados de otros usuarios.
- **RF-023:** La API debe validar entradas y devolver errores consistentes.
- **RF-024:** La aplicación debe presentar estados de carga, vacío, éxito y error.
- **RF-025:** El sistema debe registrar eventos de seguridad relevantes sin guardar contraseñas, tokens ni datos secretos.
- **RF-026:** El estudiante debe poder crear y publicar sus propios roadmaps.

## 9. Requisitos no funcionales

- **RNF-001 Seguridad:** toda operación protegida debe verificar autenticación y autorización en el backend.
- **RNF-002 Contraseñas:** almacenar únicamente hashes robustos con algoritmo apropiado para contraseñas, preferentemente Argon2id mediante una biblioteca mantenida.
- **RNF-003 Transporte:** producción debe utilizar HTTPS.
- **RNF-004 Secretos:** secretos y claves deben inyectarse por entorno o gestor de secretos; no versionarse.
- **RNF-005 Validación:** validar en frontend por experiencia y en backend por seguridad e integridad.
- **RNF-006 Accesibilidad:** apuntar a WCAG 2.2 AA para flujos principales.
- **RNF-007 Responsive:** soportar anchos móviles, tablet y escritorio.
- **RNF-008 Mantenibilidad:** separar rutas, servicios, esquemas, persistencia y configuración.
- **RNF-009 Pruebas:** cubrir lógica crítica, permisos, autenticación, recuperación y CRUD.
- **RNF-010 Observabilidad:** logs estructurados, health checks y errores con identificador de correlación cuando sea posible.
- **RNF-011 Integridad:** las restricciones importantes deben imponerse también en PostgreSQL.
- **RNF-012 Rendimiento:** definir y medir objetivos con datos representativos; como objetivo inicial de desarrollo, las consultas normales del catálogo deberían responder en menos de 500 ms en el entorno de referencia, excluyendo red externa.
- **RNF-013 Compatibilidad:** probar navegadores modernos basados en Chromium, Firefox y Safari.
- **RNF-014 Privacidad:** recopilar solo datos necesarios y permitir una política documentada de baja y eliminación.
- **RNF-015 Reproducibilidad:** un desarrollador debe poder iniciar el stack local con instrucciones versionadas.

## 10. Reglas de negocio

- **RN-001:** todos los usuarios nuevos reciben el rol `student`.
- **RN-002:** solo los cursos publicados aparecen en el catálogo público.
- **RN-003:** un curso puede estar asociado a una categoría o a varias; decisión propuesta para el MVP: una categoría principal y etiquetas opcionales.
- **RN-004:** un roadmap público solo puede incluir cursos visibles según la política de publicación.
- **RN-005:** las etapas y cursos de un roadmap tienen posiciones explícitas y estables.
- **RN-006:** una inscripción se identifica por usuario y curso; la base de datos impide duplicados.
- **RN-007:** solo el dueño de una inscripción puede cambiar su progreso.
- **RN-008:** las operaciones administrativas deben verificar rol en el servidor.
- **RN-009:** los cursos se archivan en lugar de eliminarse físicamente cuando tienen referencias.
- **RN-010:** los tokens de recuperación son de un solo uso y caducan.
- **RN-011:** las respuestas de recuperación no deben confirmar la existencia de una cuenta.
- **RN-012:** al superar un rate limit = 5, la API devuelve HTTP 429 y, cuando corresponda, `Retry-After`.
- **RN-013:** las fechas se almacenan en UTC y se serializan en ISO 8601 con zona horaria.
- **RN-014:** los errores no revelan trazas, secretos ni detalles internos en producción.

## 11. Criterios globales de aceptación

- Un visitante puede explorar cursos publicados sin iniciar sesión.
- Un usuario puede registrarse, iniciar y cerrar sesión.
- La recuperación funciona con token temporal y de un solo uso.
- Los límites de solicitudes bloquean intentos excesivos sin depender solo del frontend.
- Un estudiante no puede ejecutar operaciones administrativas ni leer datos privados de terceros.
- Un administrador puede mantener cursos, categorías y roadmaps.
- Un estudiante puede inscribirse y actualizar su progreso.
- La interfaz informa correctamente carga, éxito, vacío y error.
- Las pruebas automatizadas cubren los flujos críticos.
- La aplicación puede ejecutarse de forma reproducible en el entorno documentado.
