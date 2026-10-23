# Checklist de autorrevisión — Instancia A

Marcar cada punto antes de enviar el correo. Un ítem incumplido puede generar observación docente.

## Repositorio y gate

- [ x ] Repositorio GitHub con nombre descriptivo y acceso para el docente.
- [ x ] Primer commit preserva la SPEC oficial sin editar; historia posterior muestra refinamiento.
- [ x ] No hay código fuente de aplicación, lockfiles, `node_modules`, `.venv` ni artefactos de build antes de aprobación.
- [ x ] Existe `.gitignore` preparado para React/Vite/pnpm, Python/uv y Docker.
- [ x ] El repo contiene README y siete documentos dentro de `docs/` con los nombres de la consigna.
- [ x ] La historia no está compuesta únicamente por commits directos a `main`; el flujo de ramas está documentado.
- [ x ] Todos los commits siguen Conventional Commits.

## Documentación

- [ x ] SPEC refinada se entiende sin haber asistido a clase y registra decisiones/vacíos.
- [ x ] PRD contiene objetivos, al menos dos personas, seis historias, criterios verificables, RF/RNF, reglas, out of scope y preguntas abiertas.
- [ x ] TRD registra stack, versiones a verificar, al menos tres decisiones con alternativas y justificación, arquitectura, carpetas, Docker, convenciones y riesgos.
- [ x ] UX-UI contiene tokens concretos, estados de componentes, mobile-first sin media queries base, menú sándwich y accesibilidad.
- [ x ] APPFlow contiene sitemap, rutas, fichas de pantalla y al menos tres flujos completos.
- [ x ] BackendSchema contiene ER diagram, entidades, estados, endpoints, auth y paginación de todos los listados.
- [ x ] Implementation Plan define P0, módulos/dependencias, tareas con DoD, orden de ejecución, testing y riesgos.
- [ x ] README usa estructura y propósito de la plantilla; enlaces internos funcionan.
- [ x ] Los diagramas Mermaid renderizan en GitHub.

## Coherencia cruzada

- [ x ] Todas las funciones de SPEC tienen requisitos/historias en PRD.
- [ x ] Las reglas de producto tienen modelo/API correspondiente.
- [ x ] Cada ruta de APPFlow tiene los endpoints necesarios en BackendSchema.
- [ x ] Cada historia P0 tiene al menos una tarea y un criterio de aceptación.
- [ x ] Validación de cursos, roles y estados es consistente en todos los documentos.
- [ x ] Login, recuperación y rate limit están definidos en PRD, TRD, APPFlow, BackendSchema y Plan.
- [ x ] Todos los listados, incluidas moderación y Mis aportes, tienen paginación.
- [ x ] Mobile-first, mejora progresiva, menú sándwich y Screaming Architecture aparecen con cumplimiento verificable.

## Entrega por correo

- [ x ] Completar `docs/EMAIL_ALUMNO.md` con URL real, nombre, legajo, flujo Git y SHA real.
- [ x ] Abrir repositorio en ventana incógnita para comprobar acceso y legibilidad.
- [ x ] Enviar correo a la dirección docente indicada en la consigna, no a un destinatario inventado.
- [ x ] Enviar enlace al repo; no adjuntar ZIP/PDF como sustituto del repositorio.
