# Recopilación de documentos

Objetivo: tener en `<cliente>/documentos/` todo lo que describe al cliente, con el CDC en Markdown legible. No hace falta pedir permiso para buscar: búscalo todo y luego informa de lo que encontraste.

## Estructura de destino
```
<cliente>/
├── documentos/
│   ├── cahier_des_charges.md        ← CDC del MCP convertido (versión vigente)
│   ├── <archivos tal cual>          ← auditoría, recomendaciones, transcripciones, Excels…
│   ├── Charte graphique/            ← si existe
│   ├── traducciones_es/             ← fase 2
│   └── RESUMEN_ES.md                ← fase 3
└── <slug>_demo/                     ← fase 4
```
Si el usuario ya tiene una carpeta `documentos/` (u otra con los archivos del cliente), úsala y no dupliques.

## 1. CDC (fuente principal)
```
get_cahier(cliente)
```
- La respuesta incluye `status` (draft / pending_client / pending_csm / validated), la versión y `contenido` (normalmente HTML con entidades).
- Casi siempre supera el límite de salida y el harness la guarda en un `.txt` (JSON). **No intentes leerla con Read**: conviértela directamente:
  ```
  python <skill>/scripts/cahier_to_md.py "<ruta del .txt guardado>" "<cliente>/documentos/cahier_des_charges.md"
  ```
  Si la respuesta vino entera en el chat, guarda el JSON en un archivo y conviértelo igual.
- Si hay un CDC en local (dentro de un zip de auditoría, por ejemplo) y otro en el MCP, **manda el del MCP si está `validated`**: es la versión que el cliente ha corregido. Menciona las diferencias relevantes en el resumen.
- Si el estado no es `validated`, dilo en el resumen: la demo se basa en un borrador.

## 2. Resto de documentos del MCP
```
list_documents(cliente)                 # raíz: carpetas + archivos
list_documents(cliente, folder_id=N)    # dentro de una carpeta
search_documents(cliente, "audit")      # busca por nombre/ruta en todo el árbol
read_document(cliente, doc_id, max_chars=60000)   # texto de PDF/Word/Excel/texto
```
- Recorre el árbol entero (las carpetas suelen ser pocas). Búsquedas útiles: `audit`, `rapport`, `recommandation`, `cahier`, `charte`, `graphique`, `transcription`, `synthèse`, `devis`, `process`.
- Qué leer y guardar como `.md`/`.txt` en `documentos/` (nombre original + extensión de texto):
  - Auditoría, recomendaciones, síntesis, transcripciones de entrevistas.
  - Excels/PDF que describen **cómo trabajan hoy** (seguimientos, tablas de pedidos, workflows). Son oro para los datos ficticios y para elegir la forma de cada pantalla.
  - Guías de uso de herramientas actuales (para saber qué se sustituye y qué no).
- No hace falta guardar facturas, extractos contables ni documentos administrativos sin relación con el alcance. Menciónalos si existen.
- Imágenes (capturas de WhatsApp, fotos de pizarras, logos): `read_document` no extrae texto. Anótalas en el resumen. Si una parece el logo o una captura de su herramienta actual, pide al usuario que la descargue si la necesitas.
- **Los `.zip` no se pueden descargar por el MCP** (`get_document` no da URL). Si hay un zip con la auditoría completa (típico: «Rapport d'audit complet.zip»), pide al usuario que lo descargue y descomprima en `documentos/`. Mientras tanto, avanza con el CDC.

## 3. Contexto operativo (opcional, rápido)
- `get_client_context(cliente, include=["roadmap","meetings"])`: si ya hay roadmap o reuniones, pueden aclarar prioridades.
- `get_recent_meetings` / `get_meeting_transcript` si el CDC menciona una reunión de arranque con decisiones.
No te detengas aquí si no aporta.

## 4. Búsqueda local
Busca en el directorio de trabajo y en la carpeta que indique el usuario: `charte*`, `*graphique*`, `*audit*`, `*cahier*`, `*.zip`, logos (`*logo*`, `*.svg`). Si hay un zip local, descomprímelo en `documentos/` (en una carpeta nueva, sin ejecutar nada de dentro).

## 5. Qué contar al usuario al terminar esta fase
Una lista corta: qué encontraste, de dónde viene y qué falta (por ejemplo: «no hay carta gráfica» o «el audit completo está en un zip que hay que descargar»).
