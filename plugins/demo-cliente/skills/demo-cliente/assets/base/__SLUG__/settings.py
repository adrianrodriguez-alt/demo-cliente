"""Démo __BRAND__ : données fictives en mémoire (core/data), aucune base métier.

Passage en production : ajouter django.contrib.auth/admin, une base de données,
des modèles par module, et remplacer les fonctions de core/data par des requêtes ORM
(mêmes noms, mêmes structures renvoyées) : les vues et les templates ne changent pas.
"""
import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.environ.get("DJANGO_SECRET_KEY", "demo-__SLUG__-not-for-production")
DEBUG = os.environ.get("DJANGO_DEBUG", "1") == "1"
ALLOWED_HOSTS = os.environ.get("DJANGO_ALLOWED_HOSTS", "*").split(",")

INSTALLED_APPS = [
    "django.contrib.staticfiles",
    "core",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
]

SESSION_ENGINE = "django.contrib.sessions.backends.signed_cookies"

ROOT_URLCONF = "__SLUG__.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "core.context_processors.shell",
            ],
        },
    },
]

WSGI_APPLICATION = "__SLUG__.wsgi.application"

DATABASES = {}

LANGUAGE_CODE = "__LANG_CODE__"
TIME_ZONE = "__TIME_ZONE__"
USE_I18N = True
USE_TZ = True

STATIC_URL = "static/"
STATIC_ROOT = BASE_DIR / "staticfiles"
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
