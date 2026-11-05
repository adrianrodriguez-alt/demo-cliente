from core.data.common import BRAND, USERS
from core.ui_text import texts

# Navigation du back-office (le lead la remplit avec les modules validés).
# Entrée simple : {"label", "icon" (Lucide), "url" (nom de route)}.
# Entrée à enfants : {"label", "icon", "children": [{"label", "url", "icon", "count"?}]} → panneau au survol.
# Séparateur : {"section": "Titre"}.
NAV = [
    {"label": "Accueil", "icon": "house", "url": "dashboard"},
]


def shell(request):
    current = request.resolver_match.url_name if request.resolver_match else ""
    nav = []
    for item in NAV:
        entry = dict(item)
        children = entry.get("children")
        if children:
            entry["active"] = any(c["url"] == current for c in children)
            entry["url"] = children[0]["url"]
        else:
            entry["active"] = entry.get("url") == current
        nav.append(entry)
    default = next(iter(USERS))
    user_key = request.session.get("user", default) if hasattr(request, "session") else default
    return {
        "nav": nav,
        "current_url": current,
        "me": USERS.get(user_key, USERS[default]),
        "all_users": USERS.values(),
        "brand": BRAND,
        "t": texts(),
    }
