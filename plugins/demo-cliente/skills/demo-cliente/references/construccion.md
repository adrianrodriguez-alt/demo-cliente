# Construcción: base, módulos y revisión

## Base (lead)
Al terminar esta fase, un desconocido que abra el proyecto tiene que poder construir una pantalla nueva solo con `DESIGN_GUIDE.md` y `dashboard.html` como ejemplo.

1. **Scaffold**
   ```
   python <skill>/scripts/scaffold.py --plan <cliente>/plan.json --dest <cliente>
   ```
   Si tienes que regenerar con `--force`, para antes el servidor, porque en Windows bloquea la carpeta.
2. **Marca**: `partials/mark.html` (símbolo SVG currentColor), `static/img/favicon.svg`, logo en `static/img/` si lo hay. En `login.html` adapta `.login-motif` (gran versión del símbolo con trazo animado, como el tejado de nuestra demo de referencia) y rellena `BRAND.claim` (frase corta y concreta sacada de la promesa del CDC, ej. «Du devis à la facture, au même endroit.») y `BRAND.baseline` (actividad en pocas palabras).
3. **Personas**: `USERS` en `core/data/common.py` = las personas reales entrevistadas o que usarán la herramienta, con su rol real (la primera es la dirección o quien patrocina el proyecto). Son los perfiles del login y los responsables en los datos.
4. **Datos compartidos** en `common.py`: clientes, proveedores, productos/referencias del oficio, que usan varios módulos. Inventados pero verosímiles: nombres de empresas creíbles del país y del sector, ciudades reales de su zona, referencias con el formato del cliente. Así un mismo cliente aparece con el mismo nombre en Commercial, Production y Factures, y eso hace que la demo parezca un sistema y no un conjunto de maquetas.
5. **Dashboard** (`core/views/dashboard.py` + `core/templates/core/dashboard.html`): «Bonjour <nombre>», 4 KPI del oficio con tooltip que explica el cálculo, un gráfico, 2-3 listas «à traiter aujourd'hui». Usa datos de `common.py` coherentes con lo que mostrarán los módulos. Es la página modelo: hazla impecable.
6. **Notificaciones** (`partials/notifications.html`): 3-4 notificaciones concretas que enlacen a pantallas de módulos.
7. **`DESIGN_GUIDE.md`**: rellena contexto, vocabulario (10-20 términos), personas y reglas de la carta gráfica. Elimina los comentarios `<!-- -->` ya resueltos.
8. **Servidor y comprobación**:
   ```
   python manage.py runserver 127.0.0.1:8765      # en segundo plano, con autoreload
   export MSYS_NO_PATHCONV=1 DEMO_BASE=http://127.0.0.1:8765
   python tools/smoke.py && python tools/shot.py /accueil/ <scratchpad>/home.png --full
   ```
   Mira la captura del login y del dashboard antes de lanzar los módulos. Los errores de la base se multiplican por cada módulo.

Si es un solo módulo o una sola pantalla, puedes construirlo tú directamente tras la base, sin subagentes.

## Brief de módulo (un subagente por módulo, todos en el mismo mensaje)
```
Construyes el módulo «<Label>» de la demo <Cliente> (proyecto Django en <ruta proyecto>).

1. Lee entero <ruta proyecto>/DESIGN_GUIDE.md y mira core/templates/core/dashboard.html,
   core/static/css/app.css (componentes) y core/data/common.py (datos compartidos).
2. Contexto de tu módulo (del CDC, traducido por el lead):
   <copia aquí la sección del CDC de este módulo: lo que se ha entendido, los desarrollos
    previstos, «Pour qui», tareas con su carga, citas útiles de las transcripciones>
3. Pantallas que construyes (las vistas stub ya existen en core/views/<key>.py con estos nombres):
   - <screen key> · <url> · forma: <kanban / tabla + cajón / pantalla taller…> · perfil: <persona>
     · acción principal: <…> · debe mostrar: <2-4 cosas concretas del CDC>
   …
4. Solo posees: core/views/<key>.py, core/data/<key>.py, core/templates/<key>/,
   core/static/css/<key>.css, core/static/js/<key>.js. No toques nada más; si algo común
   falla, dilo en tu respuesta en vez de arreglarlo.
5. Datos en core/data/<key>.py: funciones que devuelven listas/dicts (mañana serán
   consultas ORM con el mismo nombre). Reutiliza los clientes/productos de common.py.
   Toda entidad que el usuario gestione lleva CRUD completo en modales (listado + crear /
   editar / eliminar que modifican la lista de verdad): sigue DESIGN_GUIDE.md § CRUD y el
   modelo core/templates/core/ejemplo_crud.html.
6. Verifica: servidor en http://127.0.0.1:<port>. python manage.py check;
   python tools/smoke.py --only /<prefijo url>/ (0 KO); capturas con tools/shot.py
   de cada pantalla (a 1440 --full y a 390) y de cada modal; míralas y corrige.
7. Responde en 10 líneas: pantallas hechas, qué hace cada botón principal,
   problemas comunes detectados (si los hay), resultado del smoke.
```
Si el módulo es grande (más de 4 pantallas complejas), pártelo en dos subagentes con archivos de plantilla separados. `core/views/<key>.py` y `core/data/<key>.py` los escribe entonces uno solo, el primero.

## Revisión (lead, tras los módulos)
Ejecuta `python tools/smoke.py --shots <scratchpad>/shots` y mira **todas** las capturas. Pasa esta lista pantalla a pantalla:

**Texto**
- [ ] Un solo `<h1>`, sin subtítulo ni párrafo explicativo. Explicaciones en tooltip.
- [ ] Todo en el idioma de la app, sin restos de otro idioma ni «Lorem», «Test», «Client A».
- [ ] Vocabulario del oficio del cliente y personas reales del audit.
- [ ] Botones con verbo corto, sin flechas ni emojis.

**Diseño**
- [ ] Un solo `.btn-primary` por zona; el color de marca, discreto.
- [ ] La forma sigue al trabajo (no todo son tarjetas): al menos 3 formas distintas en toda la demo.
- [ ] Nada de colores inventados: todo sale de los tokens. Busca hex sueltos en los CSS de módulo con `grep -n "#[0-9a-fA-F]\{3,6\}" core/static/css/<m>.css`; los de `tokens.css` sí se permiten.
- [ ] Cifras alineadas (`.num`, `td.num`), importes con el formato del país.
- [ ] A 390 px se lee, no hay desbordamiento y la navegación se abre.

**Interacción**
- [ ] Cada botón hace algo: modal, cajón, toast, filtro o pestaña. El smoke detecta enlaces muertos y modales que no abren.
- [ ] Cada entidad gestionable tiene su CRUD completo en modales según el patrón de `DESIGN_GUIDE.md` § CRUD: crear añade la fila, editar abre la modal rellenada y actualiza la fila, eliminar pide confirmación y la quita. Pruébalo con un clic real en al menos una pantalla por módulo (`shot.py --click`).
- [ ] Detalle en cajón lateral; títulos de modal cortos.
- [ ] Coherencia entre módulos: el pedido «5758» de Dupont Industrie es el mismo en Production, Ventes y Expéditions.

**Código**
- [ ] Vistas finas; datos en `core/data/<m>.py`; nada de datos escritos a mano en las plantillas más allá de textos.
- [ ] `python manage.py check` limpio y smoke con 0 problemas.

Los fallos de un módulo se los devuelves al mismo subagente (SendMessage) o los corriges tú si son pequeños.
