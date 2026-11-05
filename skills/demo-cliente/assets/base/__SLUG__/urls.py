from django.urls import path
from django.views.generic import RedirectView

from core.views import auth, dashboard

# Une ligne par écran. Les modules ajoutent leurs vues ici (le lead s'en charge
# avant de lancer les modules, pour qu'aucun module n'ait à toucher ce fichier).
urlpatterns = [
    path("", RedirectView.as_view(pattern_name="login", permanent=False)),
    path("connexion/", auth.login, name="login"),
    path("deconnexion/", auth.logout, name="logout"),

    path("accueil/", dashboard.home, name="dashboard"),
]
