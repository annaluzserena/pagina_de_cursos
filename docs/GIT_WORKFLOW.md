# Flujo de Git — RutaLibre

## Estrategia elegida: GitHub Flow simplificado

- `main`: documentación revisada y, después de la aprobación, versión integrada del MVP.
- Una rama por documento o lote coherente: `docs/spec-refinement`, `docs/prd`, `docs/trd`, `docs/ux-ui`, `docs/appflow`, `docs/backend-schema`, `docs/implementation-plan`; durante desarrollo `feat/M1-auth`, `feat/M2-catalog`, etc.; correcciones `fix/<tema>`.
- Todo cambio se integra mediante Pull Request, revisión del diff y merge a `main`. No hacer todo el trabajo directo sobre `main`.
- Un PR debe explicar propósito, archivos afectados, verificación realizada y referencias a requisito/ticket. Para cambios de documentación, comprobar enlaces relativos y renderizado Markdown/Mermaid.
- Una rama se elimina después del merge. Para correcciones observadas por el docente, crear rama de corrección, registrar SHA y responder en el mismo hilo de correo.

## Conventional Commits

Formato: `tipo(alcance opcional): descripción imperativa y específica`.

Tipos esperados: `docs`, `feat`, `fix`, `refactor`, `test`, `build`, `ci`, `chore`, `perf`, `revert`.

Ejemplos:

- `docs: add product rules and resolve spec gaps`
- `docs(ux-ui): define responsive tokens and component states`
- `docs(api): map roadmap endpoints to user stories`
- `feat(auth): add password reset flow`
- `fix(roadmap): enforce ownership on item updates`
- `test(courses): cover published catalog pagination`

Evitar mensajes como `wip`, `cambios`, `update`, `final` o `arreglos` sin contexto. Un commit debe representar una unidad lógica y no mezclar funcionalidades no relacionadas.

## Historia observable de Instancia A

1. Primer commit: `SPEC.md` oficial de clase sin editar, según la consigna. En la versión final de archivos se conserva como `docs/SPEC-clase-original.md`; al crear el repositorio, debe committearse primero con el nombre/ruta exactos que indique el docente y después renombrarse/copiarse como archivo histórico si corresponde.
2. Refinamiento: `docs: refine product spec and document decisions`.
3. Resto de documentos en ramas separadas o lotes coherentes con PRs mergeados.
4. No agregar código fuente, lockfiles ni artefactos de ejecución antes de APROBADO + T1.

## Política de revisión

- Verificar que el PRD cubra el alcance de SPEC.
- Verificar que cada pantalla tenga endpoints en BackendSchema.
- Verificar que cada historia P0 tenga tarea en Implementation Plan.
- Ejecutar checklist de entrega y comprobar que el repo sea entendible sin contexto oral.
