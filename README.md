# RutaLibre — Roadmap de Cursos

> WebApp comunitaria para descubrir y aportar cursos gratuitos validados y organizar roadmaps personales de aprendizaje.
>
> **Estado:** Instancia A — documentación pendiente de aprobación docente. No contiene código fuente de la aplicación.

**Stack previsto:** React 19 + Vite + pnpm · FastAPI + uv · PostgreSQL 18.6 · Docker + Docker Compose.

## Cómo levantarlo

### Backend (T2)

```bash
cd backend
cp .env.example .env
uv sync
uv run uvicorn app.main:app --reload --port 8000
```

- `curl http://localhost:8000/health` → `{"status":"ok"}`
- `curl http://localhost:8000/api/v1/courses` → `{items,total,limit,offset}` (datos hardcodeados, solo `published`)
- Docs OpenAPI: http://localhost:8000/docs

## Qué hace

Las personas pueden explorar un catálogo público y paginado de cursos gratuitos aportados por la comunidad. Los aportes quedan en revisión y solo se publican tras una validación de moderación. Las personas registradas pueden aportar cursos, declarar si los realizaron y sumar cursos validados a su roadmap privado, donde organizan su aprendizaje.

## Documentación

| Documento | Pregunta que responde | Enlace |
|---|---|---|
| SPEC | ¿Qué se pidió construir y cómo se resolvieron los vacíos? | [docs/SPEC.md](docs/SPEC.md) |
| PRD | ¿Para quién es, qué hace y qué queda fuera? | [docs/PRD.md](docs/PRD.md) |
| TRD | ¿Cómo se construirá técnicamente y por qué? | [docs/TRD.md](docs/TRD.md) |
| UX-UI | ¿Cómo se ve y se comporta la interfaz? | [docs/UX-UI.md](docs/UX-UI.md) |
| APPFlow | ¿Qué pantallas existen y cómo se navegan? | [docs/APPFlow.md](docs/APPFlow.md) |
| BackendSchema | ¿Qué datos persiste y qué API expone? | [docs/BackendSchema.md](docs/BackendSchema.md) |
| Implementation Plan | ¿En qué orden se implementa y cuándo está hecho? | [docs/IMPLEMENTATION_PLAN.md](docs/IMPLEMENTATION_PLAN.md) |
| SPEC original de clase | Registro fuente sin editar | [docs/SPEC-clase-original.md](docs/SPEC-clase-original.md) |
| Checklist de entrega | Autorrevisión previa al correo | [docs/CHECKLIST_ENTREGA.md](docs/CHECKLIST_ENTREGA.md) |
| Flujo Git | Ramas, merge y commits | [docs/GIT_WORKFLOW.md](docs/GIT_WORKFLOW.md) |
| Plantilla de correo | Texto a completar al entregar | [docs/EMAIL_ALUMNO.md](docs/EMAIL_ALUMNO.md) |

## Cómo leer la documentación

Leer primero la SPEC refinada; después PRD y TRD; luego UX-UI, APPFlow y BackendSchema; finalmente el plan. Las decisiones de producto deben ser coherentes con historias y reglas; cada pantalla que lee o modifica datos debe corresponder a un endpoint; y cada historia P0 debe tener tareas en el plan.

## Estado por instancia

| Instancia | Contenido | Estado |
|---|---|---|
| A — Documentación | 7 documentos, README, `.gitignore`, checklist y flujo Git | En preparación; aprobación pendiente |
| B — MVP | Ejecutar tareas P0 solo después del correo APROBADO y recepción del T1 | Bloqueada por aprobación |
| Clase 27/10 | Testing unitario/integración, Docker multi-stage y gestión del cambio | Posterior |

## Instrucciones de desarrollo

No ejecutar ni crear código fuente, lockfiles, entornos virtuales ni directorios de dependencias durante la Instancia A. Después de la aprobación, las instrucciones reproducibles de ejecución local se incorporarán aquí con comandos exactos, URLs y datos seed verificados. Hasta entonces, no se afirma que la aplicación pueda levantarse.

## Versionado

Flujo elegido: GitHub Flow simplificado. `main` contiene documentación revisada; cada documento o módulo se trabaja en una rama `docs/<tema>` o `feat/<modulo>`, se integra mediante Pull Request y se elimina la rama después del merge. Commits bajo Conventional Commits. Ver [docs/GIT_WORKFLOW.md](docs/GIT_WORKFLOW.md).

## Referencias

- [GitHub — Writing on GitHub](https://docs.github.com/en/get-started/writing-on-github)
- [GitHub — Diagramas Mermaid](https://docs.github.com/en/get-started/writing-on-github/working-with-advanced-formatting/creating-diagrams)
- [Material Design 3](https://m3.material.io/)
