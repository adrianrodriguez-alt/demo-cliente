"""Capture d'écran d'une page de la démo, avec erreurs JS affichées (ERR:).

python tools/shot.py <chemin> <sortie.png> [--w 1440] [--h 900] [--full]
                     [--click CSS]... [--hover CSS] [--base URL]
Ex. : python tools/shot.py /accueil/ out.png --full
      python tools/shot.py /commercial/prospects/ m.png --click "[data-open=m-new]"
"""
import argparse
import os
import sys

from playwright.sync_api import sync_playwright

sys.path.insert(0, os.path.dirname(__file__))
from smoke import launch  # noqa: E402

p = argparse.ArgumentParser()
p.add_argument("path")
p.add_argument("out")
p.add_argument("--w", type=int, default=1440)
p.add_argument("--h", type=int, default=900)
p.add_argument("--full", action="store_true")
p.add_argument("--hover")
p.add_argument("--click", action="append", default=[])
p.add_argument("--base", default=os.environ.get("DEMO_BASE", "http://127.0.0.1:8765"))
a = p.parse_args()

with sync_playwright() as pw:
    b = launch(pw)
    pg = b.new_page(viewport={"width": a.w, "height": a.h})
    errors = []
    pg.on("pageerror", lambda e: errors.append(str(e)))
    pg.on("console", lambda m: errors.append(m.text) if m.type == "error" else None)
    pg.goto(a.base + a.path, wait_until="networkidle")
    pg.wait_for_timeout(900)
    for c in a.click:
        pg.click(c)
        pg.wait_for_timeout(500)
    if a.hover:
        pg.hover(a.hover)
        pg.wait_for_timeout(600)
    pg.screenshot(path=a.out, full_page=a.full)
    for e in errors:
        print("ERR:", e)
    b.close()
