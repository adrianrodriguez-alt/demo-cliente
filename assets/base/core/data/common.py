"""Données fictives partagées par tous les écrans de la démo.

Règle : des données VRAISEMBLABLES tirées de l'audit (vrais prénoms de l'équipe,
vrai vocabulaire métier, références et montants crédibles), jamais « Client A », « Lorem ».
Chaque module met ses propres données dans core/data/<module>.py.
"""

BRAND = {
    "name": "__BRAND__",
    "claim": "",            # phrase courte de l'écran de connexion, tirée de la promesse du CDC
    "baseline": "",         # activité du client en quelques mots (pied de l'écran de connexion)
    "email_domain": "__DOMAIN__",
}

# Une entrée par personne interviewée / utilisatrice de l'outil (la première = profil par défaut).
USERS = {
    "direction": {"key": "direction", "name": "Direction", "initials": "DI", "role": "Direction"},
}


def eur(n):
    """10200 -> « 10 200 € » (espace fine insécable, format français)."""
    return f"{n:,}".replace(",", "\u202f") + "\u00a0€"


def keur(n):
    return f"{round(n / 1000)}\u00a0k€"


def initials(name):
    words = [w for w in name.replace("-", " ").split() if w[:1].isupper()] or name.split()
    first = words[0]
    return (first[0] + (words[1][0] if len(words) > 1 else first[1:2])).upper()
