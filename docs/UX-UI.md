# UX-UI — Experiencia de usuario e interfaz

- Versión: 0.1
- Referencias: `PRD.md`, `APPFLOW.md`

## 1. Objetivo de diseño

Construir una interfaz clara, confiable, ligera y predecible, inspirada en la simplicidad visual de Google Search: espacio en blanco, jerarquía tipográfica evidente, controles reconocibles y pocas distracciones. La referencia es conceptual; no se deben copiar marca, logotipo ni elementos propietarios.

## 2. Principios

1. **Claridad antes que decoración:** el contenido y la acción principal deben ser evidentes.
2. **Consistencia:** un mismo patrón visual debe significar lo mismo en toda la aplicación.
3. **Feedback inmediato:** toda acción informa carga, éxito o error.
4. **Accesibilidad:** navegación por teclado, foco visible, contraste adecuado y etiquetas semánticas.
5. **Diseño responsive:** los flujos esenciales deben funcionar en móvil y escritorio.
6. **Seguridad comprensible:** explicar errores sin filtrar información sensible.
7. **Reversibilidad:** confirmar acciones destructivas y preferir archivar a borrar.
8. **Rendimiento percibido:** skeletons o indicadores discretos para cargas reales; evitar animaciones innecesarias.

## 3. Dirección visual

- Fondo general claro, blanco o gris muy tenue.
- Superficies de tarjetas blancas con borde sutil.
- Texto principal gris oscuro de alto contraste.
- Color primario azul para enlaces y acciones principales.
- Colores semánticos para éxito, advertencia y error, siempre acompañados por texto o icono.
- Bordes redondeados moderados y sombras muy suaves.
- Tipografía sans-serif del sistema o una fuente web con fallback.
- Iconografía consistente; no usar iconos sin etiqueta cuando la acción no sea evidente.
- Evitar gradientes fuertes, fondos oscuros dominantes y exceso de tarjetas.

## 4. Tokens iniciales

Valores de referencia, sujetos a prueba de contraste:

- `--color-bg: #FFFFFF`
- `--color-surface: #FFFFFF`
- `--color-surface-muted: #F8F9FA`
- `--color-text: #202124`
- `--color-text-muted: #5F6368`
- `--color-primary: #1A73E8`
- `--color-border: #DADCE0`
- `--color-success: #188038`
- `--color-warning: #B06000`
- `--color-danger: #D93025`
- Espaciado basado en escala de 4 u 8 px.
- Contenedor principal con ancho máximo aproximado de 1120 px.
- Ancho de lectura de texto largo aproximado de 65–75 caracteres por línea.
- Foco visible de al menos 2 px, con separación suficiente del componente.

Los colores y tamaños finales deben comprobarse con herramientas de contraste. No depender únicamente del color para comunicar estado.

## 5. Estructura general

### Header público
- Marca textual de la plataforma.
- Enlaces: Cursos, Roadmaps.
- Acción principal: Iniciar sesión o avatar/menú de cuenta.
- Registro como acción secundaria visible para visitantes.
- En móvil, navegación compacta accesible por teclado.

### Footer
- Enlaces a información del proyecto, contacto o ayuda si existen.
- Política de privacidad y términos solo cuando estén redactados y aprobados.
- No inventar páginas legales inexistentes.

### Contenido
- Contenedor centrado.
- Títulos con jerarquía semántica.
- Breadcrumbs en páginas profundas si ayudan a orientarse.
- Una acción primaria por sección cuando sea posible.

## 6. Pantallas

### Inicio (`/`)
- Mensaje principal: aprender gratis, a tu ritmo.
- Campo de búsqueda prominente.
- Accesos a cursos y roadmaps.
- Cursos destacados solo si hay contenido editorial disponible.
- CTA para explorar el catálogo.
- No exigir login para explorar.

### Catálogo (`/courses`)
- Título y cantidad de resultados.
- Búsqueda.
- Filtros por categoría y dificultad.
- Ordenamiento.
- Lista o grilla responsive de tarjetas.
- Paginación.
- Estado vacío con opción para limpiar filtros.
- Estado de error con botón de reintento.

### Detalle de curso (`/courses/:slug`)
- Título, descripción, dificultad, duración y categoría.
- Botón para abrir el recurso externo cuando exista.
- Botón de inscripción para usuario autenticado.
- Para visitantes, CTA para iniciar sesión/registrarse conservando el destino.
- Estado de progreso visible para el estudiante.
- Atribución y licencia del recurso externo si corresponde.

### Roadmaps (`/roadmaps`)
- Lista de itinerarios publicados.
- Objetivo, nivel, etapas y cantidad de cursos cuando estén disponibles.
- Filtros solo si el catálogo justifica su uso.
- Creación de roadmap si es un estudiante autenticado.

### Detalle de roadmap (`/roadmaps/:slug`)
- Objetivo y descripción.
- Etapas numeradas.
- Cursos en orden.
- Indicadores de completado para estudiantes autenticados.
- Explicación de prerequisitos cuando estén definidos.
- No usar únicamente conectores visuales para indicar orden; incluir texto/semántica.

### Registro (`/register`)
- Nombre, email, contraseña y confirmación.
- Mostrar requisitos de contraseña antes del envío.
- Errores junto al campo y resumen accesible si hay varios.
- Mensaje genérico ante conflictos que puedan facilitar enumeración, según política.

### Login (`/login`)
- Email y contraseña.
- Mostrar/ocultar contraseña con control accesible.
- Enlace a recuperación.
- Mensaje genérico para credenciales inválidas.
- Si el usuario llega desde una ruta protegida, conservar una ruta de retorno validada localmente.

### Solicitud de recuperación (`/forgot-password`)
- Campo email.
- Mensaje posterior genérico, independientemente de si existe cuenta.
- Evitar confirmar la existencia del email.

### Restablecer contraseña (`/reset-password`)
- Nueva contraseña y confirmación.
- Token recibido en URL; no exponerlo en logs ni analítica.
- Mensaje claro para token vencido o inválido y opción para solicitar otro.
- Tras completar, informar éxito y dirigir a login.

### Mi aprendizaje (`/my-learning`)
- Cursos inscritos.
- Estado de progreso.
- Acceso rápido para continuar.
- Estado vacío que invite a explorar cursos.

### Perfil (`/profile`)
- Datos editables permitidos.
- Cambio de contraseña separado.
- Acción de cerrar sesión.
- Información sobre la cuenta sin exponer datos innecesarios.

### Administración (`/admin`)
- Navegación para cursos, categorías y roadmaps.
- Listas con búsqueda, paginación y estado.
- Formularios con validación y guardado explícito.
- Confirmación para archivar.
- No mostrar información privada innecesaria de estudiantes.

## 7. Componentes reutilizables

- `AppHeader` con menú hamburguesa, `AppFooter`, `PageContainer`.
- `Button` con variantes primary, secondary, text y danger.
- `TextField`, `PasswordField`, `SelectField`, `TextareaField`.
- `FormField` con label, hint y error.
- `CourseCard`, `RoadmapCard`, `StageList`.
- `StatusBadge` con texto accesible.
- `Pagination`, `SearchInput`, `FilterPanel`.
- `LoadingSkeleton`, `EmptyState`, `ErrorState`.
- `ConfirmDialog`.
- `Toast` para notificaciones no críticas.
- `ProtectedRoute` y `AdminRoute` como ayuda de navegación, nunca como sustituto de autorización de backend.

## 8. Estados de interfaz

Toda vista que depende de API debe contemplar:
- **Inicial/cargando:** indicador o skeleton sin saltos bruscos.
- **Éxito con datos:** contenido y acciones.
- **Éxito vacío:** explicación y siguiente acción.
- **Error recuperable:** mensaje simple y reintento.
- **Error de validación:** mensaje próximo al campo.
- **No autenticado:** solicitar sesión conservando destino cuando sea seguro.
- **Sin permiso:** informar falta de autorización sin revelar recursos privados.
- **Rate limit:** explicar que debe esperar antes de volver a intentar.
- **Offline o timeout:** indicar que no se pudo completar y evitar afirmar que la acción se guardó.

## 9. Formularios

- Cada campo tiene etiqueta visible.
- No usar placeholder como única etiqueta.
- Validación en blur y submit sin bloquear innecesariamente la escritura.
- Mensajes en lenguaje claro, sin códigos internos.
- En errores, conservar los campos no sensibles.
- No conservar ni volver a mostrar contraseñas tras fallar un envío.
- Deshabilitar el botón durante envío para reducir dobles clics, pero validar duplicados también en backend.
- Asociar errores con `aria-describedby` y anunciar cambios relevantes.
- Confirmar el resultado de operaciones exitosas.

## 10. Accesibilidad

Objetivo: WCAG 2.2 AA para flujos principales.

- Contraste de texto normal al menos 4.5:1 y texto grande al menos 3:1.
- Foco visible y orden de tabulación lógico.
- Semántica HTML adecuada y encabezados jerárquicos.
- Labels accesibles para controles.
- Diálogos con foco gestionado, Escape y retorno de foco.
- No comunicar estado solo con color.
- Objetivos táctiles cómodos.
- Respetar `prefers-reduced-motion`.
- Probar zoom y reflow en anchos pequeños.
- Pruebas manuales con teclado y lector de pantalla en flujos críticos.

## 11. Responsive

- Móvil: una columna, filtros plegables, botones de ancho apropiado y header compacto.
- Tablet: una o dos columnas según el contenido.
- Escritorio: catálogo en grilla o lista; filtros laterales solo si aportan valor.
- Evitar anchos fijos que causen scroll horizontal.
- Formularios centrados con ancho legible.
- Las tablas administrativas deben tener alternativa usable en pantallas pequeñas.

## 12. Microcopy

Preferir frases concretas:
- “No encontramos cursos con esos filtros.”
- “No se pudo completar la operación. Intentá nuevamente.”
- “Si existe una cuenta con ese email, recibirás instrucciones para continuar.”
- “Tu sesión venció. Iniciá sesión nuevamente.”

Evitar culpar al usuario, exponer errores técnicos o confirmar información de cuentas durante recuperación.

## 13. UX de seguridad

- El rate limit se comunica sin mostrar el umbral exacto si facilitaría abuso.
- No renderizar HTML arbitrario proveniente de descripciones de cursos.
- Los enlaces externos se identifican como tales.
- Los cambios administrativos destructivos requieren confirmación.
- El frontend no almacena secretos sensibles ni asume que un botón oculto protege un endpoint.
