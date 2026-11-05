# Démo __BRAND__

Démo visuelle de l'outil proposé à __BRAND__ (données fictives, aucune base de données). Développée par HeraHub.

## Lancer
```
pip install -r requirements.txt
python manage.py runserver
```
Ouvrir http://127.0.0.1:8000 → écran de connexion (n'importe quel profil, aucun mot de passe vérifié).

Polices (Google Fonts), icônes (Lucide) et graphiques (Chart.js) viennent d'un CDN : connexion internet requise.

## Écrans
<!-- tableau Module | URL, rempli à la fin -->

## Structure
- `core/data/<module>.py` : données fictives, une fonction par jeu de données. En production, ces fonctions deviennent des requêtes ORM (mêmes noms, mêmes retours).
- `core/views/<module>.py` : vues fines (données → template).
- `core/templates/<module>/` : écrans. `core/templates/core/` : coquille, connexion, accueil.
- `core/static/css/tokens.css` : identité du client (couleurs, polices, rayons). `app.css` / `app.js` : composants communs.
- `DESIGN_GUIDE.md` : règles et composants pour ajouter un écran.

## Outils
- `tools/smoke.py` : parcourt toutes les pages (1440 et 390 px) : erreurs JS, débordements, modales, liens morts.
- `tools/shot.py` : capture d'écran d'une page (Playwright).
