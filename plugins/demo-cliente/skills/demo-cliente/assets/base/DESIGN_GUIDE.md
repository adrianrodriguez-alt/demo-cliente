# __BRAND__ · guía para construir una pantalla de la demo

> Documento escrito por el lead antes de lanzar los módulos. Cada agente de módulo lo lee entero antes de tocar nada.

## Contexto del cliente
<!-- 3-5 líneas: qué hace el cliente, quién usará la herramienta, qué problema principal resuelve la demo. -->

**Idioma de la interfaz:** __UI_LANGUAGE__. Todo el texto visible va en este idioma (código y nombres de variables en inglés o en el idioma de la demo, como ya esté en el módulo).

**Vocabulario del oficio** (úsalo tal cual en etiquetas, datos y botones):
<!-- lista de 10-20 términos sacados del CDC y las transcripciones, con su sentido en una línea si no es obvio -->

**Personas** (están en `core.data.common.USERS`; úsalas como responsables, autores, asignados):
<!-- nombre · rol · qué hace en la herramienta -->

## Reglas innegociables
1. **Páginas despejadas.** Un solo `<h1>` por página dentro de `.page-head`, **sin subtítulo**, sin párrafo de explicación, sin «eyebrow». Si hace falta explicar algo → tooltip `data-tip="…"` (normalmente en un `.tip-icon` con el icono `info`).
2. **Botones simples**: etiqueta corta con verbo de acción («Nouveau devis», «Envoyer», «Valider»). Sin flechas «→» en las etiquetas, sin emojis.
3. **CRUD en modales**, nunca en página aparte: listado + crear / editar / eliminar en modales que **funcionan de verdad** (la fila aparece, cambia o desaparece). Ver § CRUD más abajo. Cabecera de modal = **un solo título corto** + botón cerrar. Detalle de un elemento = cajón lateral (`<dialog class="drawer">`) o modal.
4. **Casi todo es clicable**: cada botón hace algo (abre modal/cajón, filtra, cambia de pestaña, toast de confirmación). Ningún `href="#"` sin `data-toast`/`data-open`. `tools/smoke.py` lo comprueba.
5. **Identidad**: un solo botón de color de marca (`.btn-primary`) por zona de pantalla; el color de marca no pasa del ~5 % de la superficie; no inventes colores: usa las variables de `core/static/css/tokens.css` (`--brand-*`, `--ink-*`, `--success`…). Cifras con `.num`.
6. **Nada de tarjetas por defecto**: elige la disposición que sirve al contenido (tabla, kanban, lista, calendario, pantalla táctil, línea de tiempo, plano…). La pregunta es «¿cómo trabaja esta persona hoy, en papel o en Excel?» y se diseña a partir de eso.
7. **Datos verosímiles**: nombres de clientes/proveedores creíbles para el país y sector, importes con sentido, fechas cercanas a «hoy» (__TODAY__), referencias con el formato real del cliente si aparece en los documentos. Nunca «Client A», «Lorem ipsum», «Test».
8. **Textos cortos**, en minúscula de frase, sin relleno ni frases de marketing dentro de la herramienta.
<!-- Reglas de la carta gráfica del cliente (si existe), copiadas aquí tal cual: -->

## Archivos: quién toca qué
- **Solo posees**: `core/views/<modulo>.py`, `core/data/<modulo>.py`, `core/templates/<modulo>/*.html` y, si hace falta, `core/static/css/<modulo>.css` / `core/static/js/<modulo>.js`.
- **No modifiques nunca**: `__SLUG__/urls.py`, `core/context_processors.py`, `core/static/css/tokens.css`, `core/static/css/app.css`, `core/static/js/app.js`, `core/templates/core/*`, `core/templates/partials/*`, ni los archivos de otro módulo. Si falta un componente, créalo en el CSS de tu módulo con clases prefijadas (ej. `.prod-…`).
- Las funciones de vista ya existen (stubs) con su nombre definitivo: reemplaza el cuerpo, conserva el nombre.
- Datos compartidos: `core.data.common` (BRAND, USERS, helpers `eur`, `keur`, `initials`, y lo que el lead añada).
- **Camino a producción**: las vistas solo llaman a funciones de `core/data/<modulo>.py` que devuelven dicts/listas. Mañana esas funciones harán consultas ORM con el mismo nombre y la misma forma de retorno, y vistas y plantillas no cambian. Así que nada de lógica de datos en las plantillas ni en JS.

## Plantilla de página
```django
{% extends "core/base.html" %}
{% load static %}
{% block title %}Prospects{% endblock %}
{% block extra_head %}<link rel="stylesheet" href="{% static 'css/commercial.css' %}">{% endblock %}
{% block content %}
<div class="page-head">
  <h1>Prospects</h1>
  <div class="actions">
    <button class="btn btn-outline" type="button" data-toast="Export lancé"><i data-lucide="download"></i>Exporter</button>
    <button class="btn btn-primary" type="button" data-open="m-new"><i data-lucide="plus"></i>Nouveau prospect</button>
  </div>
</div>
…
{% endblock %}
{% block modals %} <dialog …> {% endblock %}
{% block scripts %} <script>…</script> {% endblock %}
```
Pantalla completa sin barra lateral (ej. pantalla de taller, quiosco, móvil de campo): `{% extends "core/base_bare.html" %}` (fondo oscuro).
Gráficos: en `extra_head` añade `<script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.1/dist/chart.umd.min.js" defer></script>` y, en `DOMContentLoaded`, `ui.chart("#id", config)`; tienes `ui.colors` (brand, brandSoft, dark, gray, grid, success, danger, info, muted) y `ui.gridScales()`. Datos Python → JS: `{{ data|json_script:"id" }}`.
Iconos: Lucide, `<i data-lucide="nombre"></i>` (se convierte en `<svg class="icon">`). Si inyectas HTML dinámico, llama después a `ui.icons()`.

## Componentes disponibles (`app.css`; página modelo: `core/templates/core/dashboard.html`)
- Maquetación: `.page-head` (+ `.actions`), `.grid .grid-2/3/4`, `.span-2`, `.stack`, `.row`, `.row-between`, `.toolbar` (+ `.spacer`), `.mt-8/16/24`.
- Tarjetas: `.card`, `.card-pad`, `.card-head` (h2 + `.card-link`), `.card-body`; KPI `.kpi` (`.kpi-top`, `.kpi-icon[.neutral]`, `.kpi-value` + `<small>` unidad, `.kpi-label`).
- Botones: `.btn` + `.btn-primary | .btn-dark | .btn-outline | .btn-tonal | .btn-ghost | .btn-danger`, tamaños `.btn-sm | .btn-lg`; `.icon-btn[.sm|.bordered]`; `.fab`.
- Badges: `.badge` + `.orange|.success|.warning|.danger|.info|.dark` (`.orange` = color de marca; `.plain` = sin punto); `.count-pill[.light]`.
- Avatares: `.avatar[.sm|.lg|.gray|.dark|.soft]`, `.avatars`, `.logo-tile` (iniciales de empresa).
- Navegación local: `.tabs` + `.tab[.is-active]`; `.segmented`; `.chip[.is-active]`.
- Formularios: `.field > label + .input|.select|.textarea`, `.input-icon` (icono + input), `.input-sm`, `.search-input`, `.form-grid` (+ `.full`), `.check`, `.switch`, `.dropzone`.
- Tablas: `.table-wrap > table.table`; `.cell-main` (b + small); `td.num`; `td.wrap` (por defecto el texto no salta de línea); `tr.is-clickable`; `.actions-cell`.
- Listas: `.list > .list-item` (`.grow`, b, small). Alertas: `.alert.orange|success|danger|info`. Estado vacío: `.empty` + `.halo`.
- Progreso: `.progress[.ok|.warn|.danger|.dark] > i[style=width:x%]`, `.progress-inline`.
- Kanban: `<div class="kanban" data-kanban data-toast-prefix="Commande déplacée vers">` > `.kcol` > `.kcol-head` (`.dot`, `h3`, `.count-pill.light.kcol-count`) + `.kcards` > `.kcard` (b + `.meta`). Arrastrar y soltar incluido, evento `kanban:moved`.
- Línea de tiempo: `.timeline > .tl-item[.done|.current]` (b + small).
- Menú «…»: `<div class="menu"><button class="icon-btn sm" data-menu><i data-lucide="ellipsis"></i></button><div class="menu-pop"> <button data-toast="…"><i data-lucide="pencil"></i>Modifier</button> … <hr> <button class="danger" …>Supprimer</button></div></div>` (`.menu-pop.up` / `.left` para la posición).
- Tooltips: `data-tip="texto"` (+ `data-tip-pos="bottom|left|right"`). No sobre `<input>`/`<img>`: envuélvelos en un `<span>`.

## CRUD (listado + modales) — modelo: `core/templates/core/ejemplo_crud.html`
Toda entidad que el usuario gestione (clientes, pedidos, artículos, contactos…) se presenta así, sin JS propio:
- **Listado**: `<table id="t-x">`, cada fila `<tr data-row data-status="…">`, cada valor visible `data-field="nombre"` (+ `data-value="raw"` si lo mostrado difiere del valor del formulario, ej. un badge «Livrée» con valor `livree`). Contador opcional: `<span data-count-of="#t-x">`.
- **Crear**: botón `data-open="m-x"` → modal vacía en modo creación. Al guardar, la fila se añade arriba, resaltada, a partir de `<template data-row-template>` (dentro de la tabla, con la misma estructura de fila y los `data-field` vacíos).
- **Editar**: botón `data-edit="m-x"` dentro de la fila (normalmente en el menú «…») → misma modal en modo edición con los campos `name="…"` rellenados desde los `data-field` de la fila. Al guardar, la fila se actualiza.
- **Títulos según modo**: `<h2><span data-if="create">Nouveau client</span><span data-if="edit">Modifier le client</span></h2>`.
- **Formulario**: `<form data-demo data-crud="#t-x" data-toast="Client créé" data-toast-edit="Client modifié">`. Los `name` de los campos = los `data-field` de la fila.
- **Eliminar**: `<button data-delete data-confirm="Supprimer Dupont Industrie ?" data-toast="Client supprimé">` dentro de la fila → modal de confirmación común (ya está en la base) → la fila desaparece con animación. `data-confirm` sin `data-delete` = confirmar cualquier acción irreversible (solo toast).
- **Badges que cambian con el valor**: `data-classes='{"ouverte": "badge info", "livree": "badge success"}'` en el elemento `data-field`.
- **Filtros tras editar**: si el campo de estado se llama `status`, actualiza también `data-status` de la fila y los filtros siguen funcionando.
- Eventos para lógica extra: `crud:created`, `crud:updated`, `crud:deleted` (en `document`, con `detail.row`).

## Comportamientos JS incluidos (`app.js`, objeto global `ui`)
- `data-open="idDialog"` abre modal/cajón; `data-close` cierra; clic en el fondo cierra. `data-fill="clave"` en un elemento de la modal recibe `data-clave` del disparador (ej. botón `data-open="d-client" data-name="Dupont Industrie"` → `<h2 data-fill="name">`).
- Modal: `<dialog class="modal [wide|xl]" id="…"><form data-demo data-toast="Prospect créé"> <div class="modal-head"><h2>Nouveau prospect</h2><button class="icon-btn" type="button" data-close aria-label="Fermer"><i data-lucide="x"></i></button></div> <div class="modal-body">…</div> <div class="modal-foot"><button class="btn btn-ghost" type="button" data-close>Annuler</button><button class="btn btn-primary" type="submit">Créer</button></div></form></dialog>`. El submit cierra + toast; el evento `demo:submitted` permite añadir visualmente una fila.
- Cajón: `<dialog class="drawer" id="…">` misma estructura.
- `data-toast="Mensaje"` en cualquier botón → toast (`data-toast-type="warn"` para la variante de marca); `data-close-after` cierra también la modal. JS: `ui.toast(msg)`.
- Pestañas: contenedor `data-tabs`, botones `.tab[data-tab=x]`, paneles `[data-panel=x]` (los demás `hidden`).
- Filtros: contenedor `data-filter-target="#idLista"` con botones `[data-filter="valor|all"]` (chips/segmented/tabs); los elementos filtrados llevan `data-status="valor"`.
- Búsqueda: `<input data-search="#idLista">` filtra las `tbody tr` y los `[data-searchable]`.

## Verificar tu trabajo (obligatorio)
El servidor ya está en marcha en `http://127.0.0.1:__PORT__` (recarga automática). En Git Bash, desde la raíz del proyecto:
```
export MSYS_NO_PATHCONV=1 DEMO_BASE=http://127.0.0.1:__PORT__
python manage.py check
python tools/smoke.py --only /<tu-modulo>/
python tools/shot.py /<tu-modulo>/<pantalla>/ <scratchpad>/x.png --full
python tools/shot.py /<tu-modulo>/<pantalla>/ <scratchpad>/m.png --click "[data-open=m-new]"
```
No puede quedar ningún `KO` ni ningún `ERR:`. Mira las capturas (herramienta Read sobre el PNG) y corrige hasta que todo esté limpio, alineado, sin texto de más, a 1440 px de ancho y legible a 390 px.
