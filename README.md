# demo-cliente · skill de Claude Code

Prepara la **demo inicial de un cliente nuevo** a partir de su cahier des charges (CDC) y su auditoría:

1. Recoge los documentos del cliente (MCP de Koralya + carpetas locales).
2. Traduce al español los documentos clave (`documentos/traducciones_es/`).
3. Escribe un resumen del proyecto y propone un mapa de pantallas. Se para aquí y espera tu confirmación.
4. Construye un back-office **Django + JS** con la marca del cliente, en su idioma, con CRUD en modales. Lo verifica con capturas.

## Instalación (plugin de Claude Code)

Dentro de Claude Code:
```
/plugin marketplace add adrianrodriguez-alt/demo-cliente
/plugin install demo-cliente@koralya
```
O desde la terminal:
```
claude plugin marketplace add adrianrodriguez-alt/demo-cliente
claude plugin install demo-cliente@koralya
```
Después abre una conversación **nueva**. La skill se activa sola cuando pides una demo, o se llama con `/demo-cliente:demo-cliente`.

**Actualizar:** `/plugin marketplace update koralya` (o activa la actualización automática en `/plugin` → Marketplaces).

## Requisitos
- **Conector MCP de Koralya** activo en Claude (para leer el CDC y los documentos del cliente).
- Python 3.11+ con `pip install "Django>=5,<6" playwright`.
- Google Chrome instalado (las herramientas de captura lo usan) o `python -m playwright install chromium`.

## Uso
Abre Claude Code en una carpeta vacía y pídelo con tus palabras, sin nombrar la skill:

```
Vamos a hacer la demo de <cliente>. Busca en Koralya el CDC y todo lo que haya del cliente,
léetelo, tradúceme lo importante, hazme un resumen y empezamos con el proyecto Django.
```
También puedes llamarla directamente con `/demo-cliente <cliente>`.

Te preguntará el idioma de la app (francés por defecto) y el alcance. Si el cliente no tiene carta gráfica, te preguntará también de dónde sacar los colores: su web, colores descritos con palabras o que decida ella.

## Qué hay dentro
| Ruta | Qué es |
|---|---|
| `.claude-plugin/` | Manifiesto del plugin y del marketplace `koralya`. |
| `skills/demo-cliente/SKILL.md` | El proceso completo (lo lee Claude). |
| `skills/demo-cliente/references/` | Guías por fase: recopilación, traducciones, identidad visual, plan, construcción y revisión. |
| `skills/demo-cliente/scripts/scaffold.py` | Crea el proyecto Django a partir de un `plan.json` (rutas, navegación y pantallas vacías). |
| `skills/demo-cliente/scripts/tokens.py` | Genera la paleta (`tokens.css`) a partir del color del cliente. |
| `skills/demo-cliente/scripts/cahier_to_md.py` | Convierte el CDC del MCP (HTML) a Markdown. |
| `skills/demo-cliente/assets/base/` | Base Django común: componentes, JS de interacciones (modales, CRUD, kanban…), login, herramientas `smoke.py` y `shot.py`. |

La carpeta de cada cliente (documentos, traducciones, demo) se crea fuera de este repo, en el directorio donde abras Claude Code.
