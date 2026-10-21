# Plataforma de Cursos Gratuitos

## 1. Descripción

Aplicación web para descubrir cursos gratuitos, crear una cuenta, organizar un plan de aprendizaje mediante roadmaps y registrar el progreso. El proyecto se desarrolla con React 19, Vite, TypeScript, pnpm, FastAPI, Python, uv, PostgreSQL y Docker Compose.

## 2. Documentación

- [SPEC.md](SPEC.md): especificación general del sistema.
- [PRD.md](PRD.md): requisitos de producto, historias de usuario y MVP.
- [TRD.md](TRD.md): arquitectura y decisiones técnicas.
- [UX-UI.md](UX-UI.md): experiencia de usuario y sistema visual.
- [APPFLOW.md](APPFLOW.md): mapa de navegación y flujos.
- [BACKEND-SCHEMA.md](BACKEND-SCHEMA.md): modelo de datos y contrato conceptual del backend.
- [IMPLEMENTATION-PLAN.md](IMPLEMENTATION-PLAN.md): fases, tareas, pruebas y entregables.

## 3. Estado

Esta documentación define una propuesta inicial. Las decisiones marcadas como pendientes deben resolverse antes de implementar la funcionalidad correspondiente. Los límites de rate limit, retención de datos, proveedores de correo y política de sesiones deben configurarse por entorno y validarse con pruebas.

## 4. Requisitos previos

- Docker Engine y Docker Compose v2.
- Git.
- Node.js en una versión LTS compatible con Vite y pnpm, si se desea ejecutar el frontend fuera de Docker.
- Python compatible con la versión elegida por el proyecto y uv, si se desea ejecutar el backend fuera de Docker.

## 5. Puesta en marcha futura

Cuando se implemente el proyecto, el flujo esperado será:

1. Clonar el repositorio.
2. Copiar `.env.example` a `.env` y configurar los secretos locales.
3. Ejecutar `docker compose up --build`.
4. Aplicar las migraciones de Alembic mediante el comando documentado por el backend.
5. Abrir la URL local del frontend.
6. Consultar `/docs` en el backend para explorar la API en desarrollo.

No deben incorporarse secretos reales al repositorio. El comando definitivo de migración, los puertos y los nombres de servicios deberán coincidir con `TRD.md` y el archivo Compose implementado.

## 6. Convenciones

- Los documentos de producto describen qué debe hacer el sistema; los documentos técnicos describen cómo se implementará.
- Los cambios que alteren requisitos, seguridad o contratos deben reflejarse en los documentos pertinentes.
- Toda funcionalidad se considera terminada cuando cumple sus criterios de aceptación, tiene pruebas apropiadas y no introduce regresiones conocidas.
