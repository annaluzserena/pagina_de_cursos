# UX-UI — Guía visual de estilos — RutaLibre

## 1. Principios

1. **Claridad antes que decoración:** el contenido del curso, sus condiciones y su estado deben leerse rápidamente.
2. **Inspiración Google/Material:** superficie clara, azul primario, tipografía sans-serif, espacios generosos, radios redondeados y elevación sutil.
3. **Mobile-first y mejora progresiva:** el diseño base funciona sin media queries; `@media (min-width: ...)` solo agrega mejoras en pantallas mayores.
4. **Estados explícitos:** carga, error, vacío, éxito, deshabilitado, pendiente y rechazo siempre tienen representación textual además del color.
5. **Accesibilidad por defecto:** teclado, foco visible, etiquetas persistentes, contraste suficiente y objetivos táctiles cómodos.

## 2. Design tokens

### 2.1 Paleta de colores

| Token | Valor | Uso |
|---|---|---|
| `--color-primary` | `#1A73E8` | Acción principal, enlaces y foco destacado. |
| `--color-primary-hover` | `#1558B0` | Hover/pressed de acción primaria. |
| `--color-primary-container` | `#D3E3FD` | Selección y fondo suave de elementos primarios. |
| `--color-text` | `#202124` | Texto principal. |
| `--color-text-muted` | `#5F6368` | Ayuda, metadatos y texto secundario. |
| `--color-background` | `#FFFFFF` | Fondo principal. |
| `--color-surface` | `#FFFFFF` | Cards y formularios. |
| `--color-surface-subtle` | `#F8F9FA` | Secciones secundarias y fondo de página suave. |
| `--color-border` | `#DADCE0` | Bordes, separadores e inputs. |
| `--color-success` | `#137333` | Confirmaciones y estado completado; siempre acompañado por texto/icono. |
| `--color-warning` | `#B06000` | Pendiente de revisión o advertencia. |
| `--color-danger` | `#B3261E` | Errores y acciones destructivas. |
| `--color-info` | `#1967D2` | Información no crítica. |

Los colores se deben revisar con herramienta de contraste antes de implementar; el texto normal debe cumplir WCAG AA (4.5:1) y el texto grande/controles al menos 3:1. No comunicar estado únicamente con color.

### 2.2 Tipografía

- **Familia:** `Roboto, Arial, sans-serif` (fallback local; no bloquear renderizado si la fuente remota falla).
- **Base:** 16 px, line-height 1.5.
- **Escala:** `12 px` metadatos compactos; `14 px` texto auxiliar; `16 px` cuerpo; `20 px` título de card; `24 px` título de página; `32 px` encabezado destacado.
- **Peso:** 400 cuerpo, 500 etiquetas y botones, 600 encabezados. Evitar párrafos largos en peso 300.
- No usar texto en mayúsculas como único medio para distinguir estados.

### 2.3 Espaciado, radios, sombras, z-index

| Token | Valor | Uso |
|---|---|---|
| `--space-1` | `4px` | Separación mínima. |
| `--space-2` | `8px` | Elementos relacionados. |
| `--space-3` | `12px` | Interior de controles compactos. |
| `--space-4` | `16px` | Espaciado base entre bloques. |
| `--space-6` | `24px` | Separación entre secciones. |
| `--space-8` | `32px` | Secciones amplias. |
| `--space-12` | `48px` | Separación principal en desktop. |
| `--radius-sm` | `8px` | Inputs y chips. |
| `--radius-md` | `12px` | Cards y modales. |
| `--radius-pill` | `999px` | Chips y botones tipo píldora cuando aplique. |
| `--shadow-card` | `0 1px 2px rgba(60,64,67,.15), 0 1px 3px 1px rgba(60,64,67,.08)` | Elevación baja. |
| `--shadow-dialog` | `0 8px 24px rgba(32,33,36,.20)` | Diálogo/modal. |
| `--z-header` | `10` | Header sticky opcional. |
| `--z-menu` | `20` | Menú móvil desplegado. |
| `--z-toast` | `40` | Notificaciones. |
| `--z-dialog` | `50` | Modal y backdrop. |

### 2.4 Bloque de variables listo para copiar

```css
:root {
  --color-primary: #1A73E8;
  --color-primary-hover: #1558B0;
  --color-primary-container: #D3E3FD;
  --color-text: #202124;
  --color-text-muted: #5F6368;
  --color-background: #FFFFFF;
  --color-surface: #FFFFFF;
  --color-surface-subtle: #F8F9FA;
  --color-border: #DADCE0;
  --color-success: #137333;
  --color-warning: #B06000;
  --color-danger: #B3261E;
  --color-info: #1967D2;
  --font-family: Roboto, Arial, sans-serif;
  --space-1: 4px;
  --space-2: 8px;
  --space-3: 12px;
  --space-4: 16px;
  --space-6: 24px;
  --space-8: 32px;
  --space-12: 48px;
  --radius-sm: 8px;
  --radius-md: 12px;
  --radius-pill: 999px;
  --shadow-card: 0 1px 2px rgba(60,64,67,.15), 0 1px 3px 1px rgba(60,64,67,.08);
  --shadow-dialog: 0 8px 24px rgba(32,33,36,.20);
  --z-header: 10;
  --z-menu: 20;
  --z-toast: 40;
  --z-dialog: 50;
}
```

## 3. Estrategia mobile-first con mejora progresiva

- Base sin media queries, usable desde 320 px: una columna, controles a ancho disponible, botones con área táctil mínima de 44 × 44 px, formularios apilados y navegación compacta.
- No escribir CSS base que dependa de un breakpoint para corregir overflow o legibilidad.
- `@media (min-width: 600px)`: agregar separación horizontal, formularios en dos columnas cuando tenga sentido y catálogo de dos columnas.
- `@media (min-width: 900px)`: tres columnas de cursos cuando el ancho real lo permita, contenedor centrado hasta 1200 px y navegación expandida.
- `@media (min-width: 1200px)`: ampliar márgenes y separar filtros del contenido si hay espacio.
- No usar `@media (max-width: ...)` como mecanismo principal de adaptación. Respetar `prefers-reduced-motion` como mejora de accesibilidad.
- Catálogo y tablas mantienen controles de paginación en todos los tamaños; en mobile, tablas administrativas pueden convertirse en filas-card manteniendo todos los datos y acciones.

## 4. Componentes (anatomía + estados)

### 4.1 Botón (primario / secundario / peligro)

- Anatomía: área interactiva, etiqueta verbal, icono opcional a la izquierda y estado de carga opcional.
- Primario: fondo azul, texto blanco; una acción primaria por bloque cuando sea posible.
- Secundario: fondo blanco, borde gris y texto oscuro.
- Peligro: rojo para eliminación o rechazo irreversible; requiere confirmación si la acción no es fácilmente reversible.
- Estados: default, hover, focus-visible, active, disabled y loading. En loading conservar ancho y etiqueta accesible (“Guardando…”).
- No usar `<a>` estilizado como botón para acciones; enlaces navegan, botones ejecutan acciones.

### 4.2 Campo de formulario (input / select)

- Label persistente arriba del control; placeholder es ejemplo, nunca reemplaza el label.
- Ayuda y error conectados mediante `aria-describedby`; error textual y foco en primer campo inválido al enviar.
- Estados: default, focus, invalid, disabled, read-only.
- Email: `type=email`, autocomplete adecuado; contraseña: `autocomplete=current-password` o `new-password` según flujo.
- Preguntas “¿tiene cuestionarios?”, “¿requiere examen?”, “¿entrega certificado?” y “¿lo avala una organización?” deben ser radios Sí/No, no checkboxes ambiguos.

### 4.3 Card de curso

- Contenido: título, categoría, tema, año/versión, docente, etiquetas de cuestionario/examen/certificado/aval, y acción según contexto.
- El CTA “Ver curso” abre detalle; “Agregar al roadmap” solo se muestra como acción disponible a usuario autenticado y el backend vuelve a validar permiso.
- Estado del curso se muestra como texto: “Publicado”, “Pendiente de revisión” o “Rechazado” solo en espacios privados/moderación; el catálogo público nunca presenta cursos no publicados.
- Card completa enlazable solo si no contiene botones anidados; evitar áreas clicables anidadas.

### 4.4 Lista/tabla paginada

- Cabecera muestra total de resultados y rango visible, por ejemplo “21–40 de 63”.
- Controles anterior/siguiente, página actual y selector de tamaño si el tiempo lo permite. Tamaño predeterminado 20; opciones 10/20/50, máximo 100 en API.
- Conserva filtros al cambiar de página; al cambiar filtros vuelve a offset 0.
- Estado de carga con skeleton; estado vacío con explicación y acción; error con “Reintentar”.
- En mobile, filas de moderación pueden presentarse como cards apiladas; todas las colecciones siguen paginadas.

### 4.5 Menú sándwich

- Botón con etiqueta accesible “Abrir menú de navegación”, icono de tres líneas y `aria-expanded`.
- Al abrir, muestra enlaces principales: Catálogo, Aportar curso (si autenticado), Mi roadmap (si autenticado), Mis aportes y Cuenta/Salir.
- Cierra al seleccionar ruta, al presionar Escape y al hacer click fuera cuando la implementación lo soporte sin perjudicar accesibilidad.
- En pantalla amplia, los enlaces se presentan en header sin ocultar navegación esencial.

### 4.6 Modal

- Reservado para confirmaciones o tareas breves, no para formularios largos.
- Título claro, descripción, acción principal y secundaria; foco atrapado mientras está abierto y devuelto al disparador al cerrar.
- Escape cierra salvo operación irreversible en progreso; backdrop no debe ser el único método de cierre.

### 4.7 Toast (notificación)

- Confirmación breve después de una acción, por ejemplo “Curso agregado al roadmap”.
- No usar toast como único lugar para errores de validación de formularios.
- Mensajes con `role=status` o `aria-live=polite`; errores críticos pueden usar `role=alert`.
- No desaparecer demasiado rápido; permitir lectura suficiente y no cubrir controles importantes.

### 4.8 Skeleton y Empty state

- Skeleton reproduce la forma aproximada del contenido, sin parpadeo; se anuncia estado de carga cuando sea necesario.
- Catálogo vacío: “Todavía no hay cursos publicados” y CTA para iniciar sesión/aportar si corresponde.
- Roadmap vacío: “Tu roadmap está vacío” con enlace a catálogo.
- Mis aportes vacío: explicar que los aportes aparecerán al enviar el primer curso.
- Error de red: mantener filtros cuando sea posible, mostrar reintento y no borrar contenido previo útil.

## 5. Layout y navegación

- Header con marca RutaLibre, entrada Catálogo y menú responsive. Usuario autenticado ve acceso a Roadmap, Aportar y Mis aportes; moderador ve además Moderación.
- Contenido con ancho fluido y padding base de 16 px; ancho máximo 1200 px en pantallas amplias.
- Catálogo: encabezado y búsqueda arriba, filtros plegables en mobile, resultados paginados.
- Detalle de curso: información en bloques, metadatos legibles y CTA externo; agregar al roadmap claramente separado del enlace del proveedor.
- Formularios: una columna en mobile; secciones “Datos del curso”, “Características” y “Tu experiencia”; botones al final y errores cerca del campo.
- Roadmap: lista de cursos con estado editable, acción quitar y enlace al detalle. No mostrar información de otros usuarios.
- Moderación: cola paginada, detalle completo y acciones aprobar/rechazar con motivo. Confirmar la decisión antes de ejecutarla.

## 6. Accesibilidad mínima (no negociable)

- Semántica HTML correcta; un `h1` principal por página y jerarquía de encabezados lógica.
- Todo operable por teclado; orden de tabulación natural, foco visible y sin trampas salvo modal con manejo correcto de foco.
- Contraste WCAG AA, etiquetas explícitas y mensajes de error comprensibles.
- Controles táctiles de al menos 44 × 44 px cuando sea viable.
- Iconos decorativos ocultos a lectores de pantalla; iconos de acción con nombre accesible.
- No depender solo de color; estados siempre incluyen texto o icono con etiqueta.
- Respetar zoom del navegador; no bloquear ampliación.
- Formularios con `autocomplete`, `required` y tipo de input apropiado; la validación backend es la autoridad final.
- Enlaces externos indican que se sale de RutaLibre; usar `rel="noopener noreferrer"` cuando se abre nueva pestaña.
- Animaciones reducidas cuando `prefers-reduced-motion: reduce` está activo.

## 7. Iconografía y assets

- Usar Material Symbols o iconos SVG consistentes, de un solo estilo y con etiquetas accesibles cuando transmitan significado.
- Evitar emojis como iconografía de navegación o estados críticos.
- No depender de fotos de curso para entender el contenido; no se requieren imágenes en el MVP.
- Cualquier imagen futura debe tener texto alternativo apropiado; assets decorativos usan alt vacío.
- Fuentes y assets deben tener licencia compatible y quedar documentados.

---

**Referencia visual:** [Material Design 3](https://m3.material.io/), [Material Symbols](https://fonts.google.com/icons), [WCAG 2.2](https://www.w3.org/TR/WCAG22/).
