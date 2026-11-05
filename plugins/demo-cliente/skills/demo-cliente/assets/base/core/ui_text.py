"""Textes de l'interface commune (coquille, connexion), dans la langue de la démo.

Les écrans métier sont écrits directement dans la langue de la démo ; seuls les
textes du socle passent par ce dictionnaire (variable `t` dans les templates).
"""
from django.conf import settings

TEXT = {
    "fr": {
        "search": "Rechercher", "search_placeholder": "Aller à une page, un client, un dossier…", "escape": "Échap",
        "notifications": "Notifications", "mark_read": "Tout marquer lu", "menu": "Menu", "close": "Fermer",
        "view_as": "Voir la démo en tant que", "logout": "Se déconnecter",
        "login": "Connexion", "email": "Adresse e-mail", "password": "Mot de passe", "forgot": "Oublié ?",
        "reset_sent": "Lien de réinitialisation envoyé", "show_password": "Afficher le mot de passe",
        "profile": "Profil", "profile_tip": "Démo : chaque profil ouvre l'outil avec son point de vue.",
        "stay": "Rester connecté", "sign_in": "Se connecter", "hello": "Bonjour",
        "wip": "Écran en préparation", "moved_to": "Déplacé vers", "cancel": "Annuler",
        "confirm_delete": "Supprimer cet élément ?", "delete": "Supprimer", "deleted": "Élément supprimé",
        "saved": "Modifications enregistrées", "done": "C'est fait", "confirm": "Confirmation",
        "built_by": "Développé par HeraHub",
    },
    "es": {
        "search": "Buscar", "search_placeholder": "Ir a una página, un cliente, un expediente…", "escape": "Esc",
        "notifications": "Notificaciones", "mark_read": "Marcar todo como leído", "menu": "Menú", "close": "Cerrar",
        "view_as": "Ver la demo como", "logout": "Cerrar sesión",
        "login": "Iniciar sesión", "email": "Correo electrónico", "password": "Contraseña", "forgot": "¿La has olvidado?",
        "reset_sent": "Enlace de recuperación enviado", "show_password": "Mostrar la contraseña",
        "profile": "Perfil", "profile_tip": "Demo: cada perfil abre la herramienta con su punto de vista.",
        "stay": "Mantener la sesión", "sign_in": "Entrar", "hello": "Hola",
        "wip": "Pantalla en preparación", "moved_to": "Movido a", "cancel": "Cancelar",
        "confirm_delete": "¿Eliminar este elemento?", "delete": "Eliminar", "deleted": "Elemento eliminado",
        "saved": "Cambios guardados", "done": "Hecho", "confirm": "Confirmación",
        "built_by": "Desarrollado por HeraHub",
    },
    "en": {
        "search": "Search", "search_placeholder": "Go to a page, a client, a file…", "escape": "Esc",
        "notifications": "Notifications", "mark_read": "Mark all as read", "menu": "Menu", "close": "Close",
        "view_as": "View the demo as", "logout": "Sign out",
        "login": "Sign in", "email": "Email address", "password": "Password", "forgot": "Forgot?",
        "reset_sent": "Reset link sent", "show_password": "Show password",
        "profile": "Profile", "profile_tip": "Demo: each profile opens the tool from its own point of view.",
        "stay": "Keep me signed in", "sign_in": "Sign in", "hello": "Hello",
        "wip": "Screen in progress", "moved_to": "Moved to", "cancel": "Cancel",
        "confirm_delete": "Delete this item?", "delete": "Delete", "deleted": "Item deleted",
        "saved": "Changes saved", "done": "Done", "confirm": "Confirm",
        "built_by": "Built by HeraHub",
    },
}


def texts():
    return TEXT.get(settings.LANGUAGE_CODE.split("-")[0], TEXT["fr"])
