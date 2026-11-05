"""Parcours de toutes les pages de la démo : statut HTTP, erreurs JS/console, débordement
horizontal, modales qui s'ouvrent, liens morts. Les pages sont découvertes dans les urls Django.

python tools/smoke.py [--base http://127.0.0.1:8765] [--shots DOSSIER] [--only /prefixe/]
Code de sortie 1 s'il reste des problèmes.
"""
import argparse
import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))


def discover_pages():
    """Toutes les routes sans paramètre, connexion d'abord."""
    settings_mod = next(p.parent.name for p in ROOT.glob("*/settings.py"))
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", f"{settings_mod}.settings")
    import django
    from django.urls import URLPattern, URLResolver, get_resolver

    django.setup()
    pages = []

    def walk(patterns, prefix=""):
        for p in patterns:
            route = prefix + str(p.pattern)
            if isinstance(p, URLResolver):
                walk(p.url_patterns, route)
            elif isinstance(p, URLPattern) and "<" not in route and not route.startswith("^"):
                cb = getattr(p.callback, "view_class", None)
                if cb and cb.__name__ == "RedirectView":
                    continue
                if any(k in route for k in ("deconnexion", "logout", "salir")):
                    continue
                pages.append("/" + route)

    walk(get_resolver().url_patterns)
    pages.sort(key=lambda r: (not any(k in r for k in ("connexion", "login")), r))
    return pages


def launch(pw):
    try:
        return pw.chromium.launch(headless=True)
    except Exception:
        for exe in (r"C:\Program Files\Google\Chrome\Application\chrome.exe",
                    "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
                    "/usr/bin/google-chrome"):
            if os.path.exists(exe):
                return pw.chromium.launch(executable_path=exe, headless=True)
        raise SystemExit("Aucun Chromium : lancer `python -m playwright install chromium`.")


DEAD_LINKS_JS = """() => [...document.querySelectorAll('a[href="#"], a:not([href])')]
  .filter(a => a.offsetParent && !a.closest('[data-toast],[data-open],[data-tab],[data-filter],[data-menu],[data-popover]')
              && !a.matches('[data-toast],[data-open],[data-tab],[data-filter],[data-menu],[data-popover]')
              && !a.onclick)
  .map(a => (a.textContent || a.getAttribute('aria-label') || '').trim().slice(0, 30))"""


def main():
    from playwright.sync_api import sync_playwright

    ap = argparse.ArgumentParser()
    ap.add_argument("--base", default=os.environ.get("DEMO_BASE", "http://127.0.0.1:8765"))
    ap.add_argument("--shots")
    ap.add_argument("--only")
    a = ap.parse_args()
    pages = [p for p in discover_pages() if not a.only or p.startswith(a.only)]
    if a.shots:
        os.makedirs(a.shots, exist_ok=True)

    problems = 0
    with sync_playwright() as pw:
        b = launch(pw)
        for w, h in ((1440, 900), (390, 844)):
            pg = b.new_page(viewport={"width": w, "height": h})
            errs = []
            pg.on("pageerror", lambda e: errs.append(str(e)))
            pg.on("console", lambda m: errs.append(m.text) if m.type == "error" else None)
            for path in pages:
                errs.clear()
                r = pg.goto(a.base + path, wait_until="networkidle")
                pg.wait_for_timeout(400)
                over = pg.evaluate("document.documentElement.scrollWidth - innerWidth")
                dead = pg.evaluate(DEAD_LINKS_JS)
                opened = failed = 0
                if w == 1440:
                    openers = pg.locator("[data-open]:visible")
                    for i in range(openers.count()):
                        try:
                            openers.nth(i).click(timeout=1500)
                            pg.wait_for_timeout(150)
                            if pg.evaluate("!!document.querySelector('dialog[open]')"):
                                opened += 1
                                pg.keyboard.press("Escape")
                                pg.wait_for_timeout(120)
                            else:
                                failed += 1
                        except Exception:
                            pass
                bad = r.status != 200 or over > 1 or errs or failed or dead
                problems += bool(bad)
                extra = []
                if errs:
                    extra.append("ERR: " + " | ".join(errs[:3]))
                if failed:
                    extra.append(f"modales KO={failed}")
                if dead:
                    extra.append(f"liens morts={dead[:4]}")
                print(f"{'KO' if bad else 'ok'} {w:>4} {path:<34} status={r.status} overflow={over} modales={opened} {' '.join(extra)}")
                if a.shots:
                    name = path.strip("/").replace("/", "_") or "root"
                    pg.screenshot(path=f"{a.shots}/{w}_{name}.png", full_page=(w == 1440))
            pg.close()
        b.close()
    print("PROBLEMES :", problems)
    sys.exit(1 if problems else 0)


if __name__ == "__main__":
    main()
