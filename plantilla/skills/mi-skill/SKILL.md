---
name: mi-skill
description: Qué hace la skill y CUÁNDO debe usarla Claude. Sé concreto e incluye frases que diría alguien del equipo («prepárame el informe de horas de X», «revisa el ticket HH-…»). Claude decide si la usa leyendo solo esta descripción.
---

# Mi skill

Instrucciones para Claude, en imperativo y explicando el porqué de cada paso.

## Pasos
1. …
2. …

Si la skill trae scripts o plantillas, guárdalos junto a este archivo (`scripts/`, `references/`, `assets/`) y llámalos con su ruta completa: `python "${CLAUDE_SKILL_DIR}/scripts/mi_script.py"`.
