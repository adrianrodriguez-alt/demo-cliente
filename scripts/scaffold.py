"""Crée le projet Django de démo à partir de assets/base et d'un plan d'écrans.

python scaffold.py --plan plan.json --dest <dossier parent>

plan.json :
{
  "slug": "acme",                       # paquet Python + nom du dossier (<slug>_demo)
  "brand": "Acme",                      # nom affiché
  "domain": "acme.fr",                  # domaine des e-mails de démo
  "lang": "fr",                         # fr | es | en  (langue de l'interface)
  "time_zone": "Europe/Paris",
  "port": 8765,                         # port du serveur de démo (DESIGN_GUIDE, tools)
  "identity": {"brand": "#F07D00", "ink": "#1E1D1D", "accent": null,
               "font_title": "Poppins", "font_body": "Montserrat",
               "shape": "pill", "sidebar": "dark"},
  "modules": [
    {"key": "commercial", "label": "Commercial", "icon": "briefcase",
     "section": null,                   # optionnel : titre de séparateur dans la navigation avant ce module
     "screens": [
       {"key": "pipeline", "label": "Pipeline", "url": "commercial/pipeline/", "icon": "kanban"},
       {"key": "prospects", "label": "Prospects", "url": "commercial/prospects/", "icon": "contact"}
     ]}
  ]
}
Pour chaque écran : route nommée "<module>_<screen>", vue stub core/views/<module>.py:<screen>,
dossier core/templates/<module>/, fichier core/data/<module>.py, entrée de navigation.
"""
import argparse
from datetime import date
import json
import keyword
import re
import shutil
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
BASE = HERE.parent / "assets" / "base"
LANG_CODES = {"fr": "fr-fr", "es": "es-es", "en": "en-gb"}
TEXT_EXT = {".py", ".html", ".css", ".js", ".md", ".txt", ".svg"}


def ident(s):
    s = re.sub(r"[^0-9a-zA-Z_]", "_", s).strip("_").lower()
    if not s or s[0].isdigit() or keyword.iskeyword(s):
        s = "v_" + s
    return s


def fonts_url(title, body):
    fams = []
    for f, weights in ((title, "500;600;700"), (body, "400;500;600;700")):
        fam = f"family={f.replace(' ', '+')}:wght@{weights}"
        if fam.split(":")[0] not in [x.split(":")[0] for x in fams]:
            fams.append(fam)
    return "https://fonts.googleapis.com/css2?" + "&".join(fams) + "&display=swap"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--plan", required=True)
    ap.add_argument("--dest", required=True)
    ap.add_argument("--force", action="store_true", help="écrase un dossier existant")
    a = ap.parse_args()
    plan = json.loads(Path(a.plan).read_text(encoding="utf-8"))

    slug = ident(plan["slug"])
    target = Path(a.dest) / f"{slug}_demo"
    if target.exists():
        if not a.force:
            sys.exit(f"{target} existe déjà (utiliser --force pour l'écraser).")
        shutil.rmtree(target)
    shutil.copytree(BASE, target, ignore=shutil.ignore_patterns("__pycache__", "*.pyc"))
    (target / "__SLUG__").rename(target / slug)

    ident_cfg = plan.get("identity", {})
    lang = plan.get("lang", "fr")
    repl = {
        "__SLUG__": slug,
        "__BRAND__": plan["brand"],
        "__DOMAIN__": plan.get("domain", f"{slug}.fr"),
        "__LANG_CODE__": LANG_CODES.get(lang, lang),
        "__HTML_LANG__": lang,
        "__TIME_ZONE__": plan.get("time_zone", "Europe/Paris"),
        "__UI_LANGUAGE__": {"fr": "francés", "es": "español", "en": "inglés"}.get(lang, lang),
        "__TODAY__": plan.get("today") or date.today().isoformat(),
        "__PORT__": str(plan.get("port", 8765)),
        "__FONTS_URL__": fonts_url(ident_cfg.get("font_title", "Poppins"), ident_cfg.get("font_body", "Montserrat")),
    }
    for f in target.rglob("*"):
        if f.is_file() and f.suffix in TEXT_EXT:
            txt = f.read_text(encoding="utf-8")
            new = txt
            for k, v in repl.items():
                new = new.replace(k, v)
            if new != txt:
                f.write_text(new, encoding="utf-8")

    # Identité visuelle
    cmd = [sys.executable, str(HERE / "tokens.py"), "--out", str(target / "core/static/css/tokens.css"),
           "--brand", ident_cfg.get("brand", "#2F5D62"),
           "--font-title", ident_cfg.get("font_title", "Poppins"),
           "--font-body", ident_cfg.get("font_body", "Montserrat"),
           "--shape", ident_cfg.get("shape", "pill"),
           "--sidebar", ident_cfg.get("sidebar", "dark")]
    if ident_cfg.get("ink"):
        cmd += ["--ink", ident_cfg["ink"]]
    if ident_cfg.get("accent"):
        cmd += ["--accent", ident_cfg["accent"]]
    subprocess.run(cmd, check=True)

    # Modules : stubs, urls, navigation
    home = {"fr": "Accueil", "es": "Inicio", "en": "Home"}.get(lang, "Accueil")
    nav = [f'    {{"label": "{home}", "icon": "house", "url": "dashboard"}},']
    imports, routes = [], []
    for m in plan.get("modules", []):
        mk = ident(m["key"])
        imports.append(mk)
        if m.get("section"):
            nav.append(f"    {{\"section\": {json.dumps(m['section'], ensure_ascii=False)}}},")
        children = []
        views = [f'"""Écrans du module {m["label"]}. Vues fines : données (core.data.{mk}) -> template."""',
                 "from django.shortcuts import render", "", f"from core.data import {mk} as data  # noqa: F401", ""]
        routes.append(f"\n    # {m['label']}")
        for s in m["screens"]:
            sk = ident(s["key"])
            name = f"{mk}_{sk}"
            routes.append(f'    path("{s["url"].lstrip("/")}", {mk}.{sk}, name="{name}"),')
            children.append(f'        {{"label": {json.dumps(s["label"], ensure_ascii=False)}, "url": "{name}", "icon": "{s.get("icon", "circle")}"}},')
            views += ["", f"def {sk}(request):",
                      f'    return render(request, "core/stub.html", {{"title": {json.dumps(s["label"], ensure_ascii=False)}}})', ""]
        (target / "core/views" / f"{mk}.py").write_text("\n".join(views).rstrip() + "\n", encoding="utf-8")
        data_file = target / "core/data" / f"{mk}.py"
        data_file.write_text(f'"""Données fictives du module {m["label"]}."""\n\nfrom core.data.common import USERS, eur, initials, keur  # noqa: F401\n', encoding="utf-8")
        (target / "core/templates" / mk).mkdir(exist_ok=True)
        if len(children) == 1 and not m.get("force_group"):
            c = children[0].strip().rstrip(",")
            entry = json.loads(c)
            nav.append(f'    {{"label": {json.dumps(m["label"], ensure_ascii=False)}, "icon": "{m.get("icon", entry["icon"])}", "url": "{entry["url"]}"}},')
        else:
            nav.append(f'    {{"label": {json.dumps(m["label"], ensure_ascii=False)}, "icon": "{m.get("icon", "folder")}", "children": [')
            nav += children
            nav.append("    ]},")

    urls = target / slug / "urls.py"
    u = urls.read_text(encoding="utf-8")
    u = u.replace("from core.views import auth, dashboard", "from core.views import " + ", ".join(sorted(set(["auth", "dashboard"] + imports))))
    u = u.replace('    path("accueil/", dashboard.home, name="dashboard"),\n',
                  '    path("accueil/", dashboard.home, name="dashboard"),\n' + "\n".join(routes) + "\n")
    urls.write_text(u, encoding="utf-8")

    cp = target / "core/context_processors.py"
    c = cp.read_text(encoding="utf-8")
    c = re.sub(r"NAV = \[\n.*?\n\]", "NAV = [\n" + "\n".join(nav) + "\n]", c, flags=re.S)
    cp.write_text(c, encoding="utf-8")

    print(f"Projet créé : {target}")
    print(f"  {sum(len(m['screens']) for m in plan.get('modules', []))} écrans en stub, {len(plan.get('modules', []))} modules.")
    print("  Étapes suivantes : logo (partials/mark.html, static/img), common.py (BRAND, USERS), dashboard, DESIGN_GUIDE.md.")


if __name__ == "__main__":
    main()
