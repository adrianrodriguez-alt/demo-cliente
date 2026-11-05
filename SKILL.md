---
name: demo-cliente
description: Prepara la demo inicial de un cliente nuevo de Koralya/HeraHub a partir de su cahier des charges (CDC) y su auditoría. Recoge los documentos (MCP Koralya y carpetas locales), los traduce al español para el equipo, resume el proyecto y construye un back-office Django + JS limpio, con la marca del cliente y listo para evolucionar a producción, sin aspecto de «hecho por IA». Úsala siempre que alguien quiera empezar la demo, maqueta o prototipo de un cliente, «montar el proyecto Django» de un cliente nuevo, convertir un CDC o una auditoría en pantallas, o diga cosas como «vamos a hacer la demo de Wutao», «léete el CDC de X y empezamos», «prepárame las maquetas para el cliente», aunque no diga la palabra «demo».
---

# Demo de cliente a partir del CDC

Koralya (marca de cara al cliente: **HeraHub**) desarrolla aplicaciones Django a medida. Antes de cada proyecto se hace una demo en 3-4 horas a partir de los documentos que deja el mediador (CDC, auditoría, transcripciones, carta gráfica). Esta skill convierte ese trabajo en un proceso repetible que produce:

1. `documentos/traducciones_es/`: los documentos clave traducidos al español para que el equipo los lea tranquilamente.
2. Un **resumen en español** del proyecto y de lo que hay que leer.
3. `<slug>_demo/`: un proyecto Django monolítico con todas las pantallas de la demo, en el idioma del cliente, con su marca, verificado con capturas.

La referencia de calidad es nuestra mejor demo hasta ahora (una pyme industrial): páginas despejadas, vocabulario real del oficio, cada pantalla con la forma que pide su tarea (kanban, pantalla táctil de taller, tablas…), todo clicable y cero errores. Lo que la hace buena no es el CSS sino la disciplina: **primero una base común y una guía de diseño escrita para ESTE cliente; después los módulos en paralelo; al final una verificación con capturas.** Respeta ese orden.

La comunicación con el usuario es siempre en **español**, aunque la app vaya en francés.

## Fase 0 · Arranque y preguntas

1. `who_am_i()` del MCP Koralya (si las herramientas `mcp__claude_ai_Koralya__*` están diferidas, cárgalas con ToolSearch en una sola llamada). Así sabes quién eres y a qué clientes tienes acceso.
2. Identifica al cliente. Si el usuario no lo ha nombrado, o el nombre es ambiguo, usa `list_clients(query)` y pregúntale. Anota `trabajadores_asignados`: es el equipo del proyecto y sale en el resumen.
3. Haz las preguntas iniciales en **una sola** llamada a AskUserQuestion (no preguntes lo que ya se sabe por la conversación):
   - **Idioma de la app**: Francés (recomendado, la mayoría de clientes) / Español / Inglés.
   - **Alcance de la demo**: Back-office completo con todos los procesos del CDC (recomendado) / Solo los 2-3 módulos prioritarios / Una pantalla o un flujo concreto.
   - Pregunta también si existe la **web del cliente** solo si ya sabes que no hay carta gráfica. Si no lo sabes aún, déjalo para la fase 2.
4. Carpeta de trabajo: `<directorio actual>/<cliente>/` con `documentos/` y `<slug>_demo/` dentro. Si el directorio actual ya es la carpeta del cliente (contiene sus documentos), trabaja ahí mismo. No crees nada dentro de otra demo existente.

## Fase 1 · Recoger los documentos

Lee [references/recopilacion.md](references/recopilacion.md) y síguelo. En resumen:
- `get_cahier(cliente)` es la fuente principal y, si está validado, la que manda. Suele ser enorme, así que se guarda en disco y se convierte con `scripts/cahier_to_md.py`.
- `list_documents`/`search_documents` + `read_document` para el resto: auditoría, recomendaciones, transcripciones, carta gráfica, Excels de procesos actuales, etc.
- Busca también en local (la carpeta del cliente, descargas que el usuario indique). Los `.zip` del MCP no se pueden descargar: si hay uno con la auditoría, pide al usuario que lo descomprima en `documentos/`.
- Todo acaba en `documentos/` con su nombre original y el CDC en Markdown.

## Fase 2 · Traducciones (en segundo plano) y lectura

1. **Lanza las traducciones ya**, en paralelo y en segundo plano, según [references/traducciones.md](references/traducciones.md): un subagente por documento (CDC, recomendaciones, carta gráfica, cada transcripción…). No bloquean nada: tú sigues leyendo y construyendo mientras traducen.
2. **Léelo todo tú.** El CDC entero; las recomendaciones; las transcripciones al menos en diagonal, buscando vocabulario, nombres, cifras y quejas concretas. Sin esta lectura la demo sale genérica: el vocabulario real y los detalles de las transcripciones son lo que hace que el cliente se reconozca.
3. **Identidad visual**: sigue [references/identidad-visual.md](references/identidad-visual.md). Si hay carta gráfica, se aplica tal cual. Si no la hay, pregunta al usuario con las tres opciones (web del cliente / colores dichos con palabras / que lo decida la skill) y tradúcelo a `identity` del plan.

## Fase 3 · Resumen y plan (punto de control con el usuario)

Escribe `documentos/RESUMEN_ES.md` y muéstralo en el chat, con el formato de [references/plan-demo.md](references/plan-demo.md):
- El cliente en 5 líneas, el equipo, los problemas principales con cifras y lo que se le ha prometido.
- **Qué debe leer el usuario** (los 3-5 documentos imprescindibles, con su ruta y el motivo).
- El **mapa de pantallas** propuesto: módulos en el orden de prioridad del CDC, pantallas con la forma que tendrá cada una y por qué, y el perfil que la usa.
- La identidad visual elegida.

Pide confirmación del mapa de pantallas antes de construir: es la única decisión cara de cambiar después. Si el usuario dijo que no hacía falta confirmar, sigue.

## Fase 4 · Base (la haces tú, el lead)

Sigue [references/construccion.md](references/construccion.md) § Base:
1. Escribe `plan.json` y ejecuta `python scripts/scaffold.py --plan plan.json --dest <carpeta cliente>`. Esto genera el proyecto, `tokens.css`, las rutas, la navegación y los stubs de cada pantalla.
2. Personaliza lo común: logo y símbolo (`partials/mark.html`, favicon), `core/data/common.py` (BRAND, USERS con las personas reales del audit, datos compartidos), notificaciones, motivo de la pantalla de login y **dashboard** como página modelo.
3. Rellena `DESIGN_GUIDE.md` (contexto, vocabulario, personas, reglas de la carta gráfica). Es lo único que leerán los agentes de módulo, así que tiene que bastarles.
4. Arranca el servidor en segundo plano (`python manage.py runserver 127.0.0.1:8765`) y comprueba la base con `tools/smoke.py` y capturas antes de seguir.

## Fase 5 · Módulos en paralelo

Lanza un subagente por módulo, **todos en el mismo mensaje**, con el brief de [references/construccion.md](references/construccion.md) § Brief de módulo. Cada uno posee solo sus archivos (`core/views/<m>.py`, `core/data/<m>.py`, `core/templates/<m>/`, `css/<m>.css`, `js/<m>.js`). Por eso pueden trabajar a la vez sin pisarse.

## Fase 6 · Verificación y revisión

1. `python tools/smoke.py --shots <scratchpad>/shots` → 0 problemas a 1440 y 390 px.
2. Mira **todas** las capturas tú mismo y pasa la lista anti-slop de [references/construccion.md](references/construccion.md) § Revisión. Corrige o devuelve al subagente lo que falle.
3. Comprueba que las traducciones han terminado y que están en `documentos/traducciones_es/`.
4. Completa la tabla de pantallas del `README.md` del proyecto.

## Fase 7 · Entrega

Mensaje final en español, breve:
- Cómo arrancar la demo (comando y URL) y por qué pantalla empezar a enseñarla.
- Lista de pantallas por módulo (una línea cada una).
- Rutas de las traducciones y del resumen.
- Decisiones que tomaste sin preguntar (colores, pantallas descartadas, supuestos sobre datos) y puntos del CDC «à confirmer» que la demo da por resueltos.
- Resultado real del smoke test (no digas «todo bien» sin haberlo ejecutado).
