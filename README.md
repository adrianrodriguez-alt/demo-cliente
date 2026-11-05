# Koralya · plugins de Claude Code

Marketplace interno del equipo de Koralya / HeraHub: skills y plugins de Claude Code que usamos en el día a día.

| Plugin | Qué hace |
|---|---|
| [`demo-cliente`](plugins/demo-cliente/) | Prepara la demo inicial de un cliente a partir de su CDC: recoge y traduce los documentos, resume el proyecto y construye un back-office Django + JS con la marca del cliente. |

## Instalar
Dentro de Claude Code:
```
/plugin marketplace add adrianrodriguez-alt/koralya-plugins
/plugin install demo-cliente@koralya
```
Abre una conversación nueva y ya está disponible. Para ver todos los plugins del marketplace, escribe `/plugin`.

**Actualizar:** `/plugin marketplace update koralya`, o activa la actualización automática en `/plugin` → Marketplaces.

## Añadir tu plugin
1. Haz un fork de este repo, o crea una rama si eres colaborador.
2. Copia la carpeta [`plantilla/`](plantilla/) a `plugins/<nombre-de-tu-plugin>/` y edita:
   - `.claude-plugin/plugin.json`: `name` (el nombre de la carpeta), `description`, `version`, `author`.
   - `skills/<nombre-de-tu-skill>/SKILL.md`: la skill. Puedes poner varias skills en el mismo plugin.
3. Añade tu plugin a la lista `plugins` de [`.claude-plugin/marketplace.json`](.claude-plugin/marketplace.json):
   ```json
   { "name": "nombre-de-tu-plugin", "source": "./plugins/nombre-de-tu-plugin", "description": "…" }
   ```
4. Compruébalo: `claude plugin validate .` (debe decir *Validation passed*).
5. Abre un **pull request**. Adrián lo revisa y lo aprueba: nada entra en `main` sin revisión.

Para publicar cambios en un plugin existente, sube su `version` en `plugin.json`. Si no la subes, los que ya lo tienen instalado no reciben la actualización.

**Nunca subas** contraseñas, tokens ni documentos de clientes (audits, transcripciones, CDC). Este repo es público.
