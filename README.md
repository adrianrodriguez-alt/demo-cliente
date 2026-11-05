# demo-cliente · skill de Claude Code

Prepara la **demo inicial de un cliente nuevo** a partir de su cahier des charges (CDC) y su auditoría:

1. Recoge los documentos del cliente (MCP de Koralya + carpetas locales).
2. Traduce al español los documentos clave (`documentos/traducciones_es/`).
3. Escribe un resumen del proyecto y propone un mapa de pantallas. Se para aquí y espera tu confirmación.
4. Construye un back-office **Django + JS** con la marca del cliente, en su idioma, con CRUD en modales. Lo verifica con capturas.

## Instalación

Clona el repo dentro de tus skills de usuario de Claude Code:

```powershell
git clone https://github.com/adrianrodriguez-alt/demo-cliente.git "$env:USERPROFILE\.claude\skills\demo-cliente"
```
(macOS/Linux: `~/.claude/skills/demo-cliente`). Abre una conversación **nueva** de Claude Code. Si escribes `/`, debería aparecer `demo-cliente`.

Para actualizar: `git -C "$env:USERPROFILE\.claude\skills\demo-cliente" pull`.

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
| `SKILL.md` | El proceso completo (lo lee Claude). |
| `references/` | Guías por fase: recopilación, traducciones, identidad visual, plan, construcción y revisión. |
| `scripts/scaffold.py` | Crea el proyecto Django a partir de un `plan.json` (rutas, navegación y pantallas vacías). |
| `scripts/tokens.py` | Genera la paleta (`tokens.css`) a partir del color del cliente. |
| `scripts/cahier_to_md.py` | Convierte el CDC del MCP (HTML) a Markdown. |
| `assets/base/` | Base Django común: componentes, JS de interacciones (modales, CRUD, kanban…), login, herramientas `smoke.py` y `shot.py`. |

La carpeta de cada cliente (documentos, traducciones, demo) se crea fuera de este repo, en el directorio donde abras Claude Code.
