"""Génère tokens.css (identité visuelle d'un client) à partir de quelques décisions.

Usage :
  python tokens.py --brand "#F07D00" --out core/static/css/tokens.css
                   [--ink "#1E1D1D"] [--font-title Poppins] [--font-body Montserrat]
                   [--shape pill|soft|sharp] [--sidebar dark|light|brand]

--brand    couleur principale (logo / charte). Une gamme 50→900 est calculée en OKLCH.
--ink      neutre le plus sombre. Par défaut : un anthracite légèrement teinté par la marque.
--accent   couleur secondaire facultative (ex. marque orange + accent bleu). Sert aux graphiques,
           badges .accent et éléments secondaires ; jamais à un 2e bouton principal.
           Sans accent, --accent-* = les neutres (graphiques « encre + marque »).
--shape    pill = boutons capsule ; soft = coins arrondis 10 px ; sharp = coins 4 px.
--sidebar  dark = barre latérale foncée (ink-900) ; light = blanche ; brand = couleur de marque.

Si le client a une charte avec ses propres tokens, n'utilise pas ce script : recopie ses
valeurs dans tokens.css en gardant les NOMS de variables ci-dessous (app.css en dépend).
"""
import argparse
import math

# ---------- Conversions sRGB <-> OKLab ----------

def _hex_to_rgb(h):
    h = h.lstrip("#")
    if len(h) == 3:
        h = "".join(c * 2 for c in h)
    return tuple(int(h[i:i + 2], 16) / 255 for i in (0, 2, 4))


def _lin(c):
    return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4


def _delin(c):
    return 12.92 * c if c <= 0.0031308 else 1.055 * c ** (1 / 2.4) - 0.055


def _rgb_to_oklch(rgb):
    r, g, b = (_lin(c) for c in rgb)
    l = (0.4122214708 * r + 0.5363325363 * g + 0.0514459929 * b) ** (1 / 3)
    m = (0.2119034982 * r + 0.6806995451 * g + 0.1073969566 * b) ** (1 / 3)
    s = (0.0883024619 * r + 0.2817188376 * g + 0.6299787005 * b) ** (1 / 3)
    L = 0.2104542553 * l + 0.7936177850 * m - 0.0040720468 * s
    a = 1.9779984951 * l - 2.4285922050 * m + 0.4505937099 * s
    bb = 0.0259040371 * l + 0.7827717662 * m - 0.8086757660 * s
    return L, math.hypot(a, bb), math.degrees(math.atan2(bb, a)) % 360


def _oklch_to_rgb(L, C, H):
    a, b = C * math.cos(math.radians(H)), C * math.sin(math.radians(H))
    l = (L + 0.3963377774 * a + 0.2158037573 * b) ** 3
    m = (L - 0.1055613458 * a - 0.0638541728 * b) ** 3
    s = (L - 0.0894841775 * a - 1.2914855480 * b) ** 3
    r = 4.0767416621 * l - 3.3077115913 * m + 0.2309699292 * s
    g = -1.2684380046 * l + 2.6097574011 * m - 0.3413193965 * s
    bl = -0.0041960863 * l - 0.7034186147 * m + 1.7076147010 * s
    return r, g, bl


def _in_gamut(rgb):
    return all(-1e-4 <= c <= 1 + 1e-4 for c in rgb)


def _oklch_hex(L, C, H):
    # réduit la chroma jusqu'à rentrer dans le gamut sRGB
    while C > 0 and not _in_gamut(_oklch_to_rgb(L, C, H)):
        C -= 0.002
    r, g, b = (_delin(min(max(c, 0), 1)) for c in _oklch_to_rgb(L, max(C, 0), H))
    return "#{:02X}{:02X}{:02X}".format(round(r * 255), round(g * 255), round(b * 255))


def _luminance(hexc):
    r, g, b = (_lin(c) for c in _hex_to_rgb(hexc))
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def contrast(a, b):
    la, lb = sorted((_luminance(a), _luminance(b)), reverse=True)
    return (la + 0.05) / (lb + 0.05)


def _rgba(hexc, alpha):
    r, g, b = (round(c * 255) for c in _hex_to_rgb(hexc))
    return f"rgba({r},{g},{b},{alpha})"


# ---------- Gammes ----------

STEPS = [50, 100, 200, 300, 400, 500, 600, 700, 800, 900]
# Luminosité relative à la couleur de base : vers le blanc (fraction de l'écart) pour 50→400,
# vers le noir (facteur multiplicatif) pour 600→900. Ainsi la gamme reste monotone
# que la marque soit claire (jaune) ou foncée (bleu marine).
LIGHT_F = [0.92, 0.80, 0.60, 0.40, 0.18]
DARK_F = [0.84, 0.72, 0.59, 0.46]
BRAND_C = [0.12, 0.25, 0.45, 0.70, 0.90, 1.0, 0.95, 0.85, 0.72, 0.58]
INK_L = [0.978, 0.948, 0.893, 0.81, 0.68, 0.53, 0.45, 0.385, 0.315, 0.24]


def brand_ramp(base):
    L, C, H = _rgb_to_oklch(_hex_to_rgb(base))
    lights = [L + (1 - L) * f for f in LIGHT_F]
    darks = [L * f for f in DARK_F]
    out = {}
    for step, l, k in zip(STEPS, lights + [None] + darks, BRAND_C):
        out[step] = base.upper() if l is None else _oklch_hex(l, C * k, H)
    return out


def ink_ramp(brand, ink=None):
    _, _, H = _rgb_to_oklch(_hex_to_rgb(brand))
    chroma = 0.006  # neutres à peine teintés par la marque : plus « vivants » qu'un gris pur
    if ink:
        Lk, Ck, Hk = _rgb_to_oklch(_hex_to_rgb(ink))
        H, chroma = Hk, min(Ck, 0.02)
    out = {s: _oklch_hex(l, chroma, H) for s, l in zip(STEPS, INK_L)}
    if ink:
        out[900] = ink.upper()
    return out


SHAPES = {
    #        btn     nav     badge   card   field  modal  check
    "pill": ("999px", "999px", "999px", "20px", "12px", "24px", "7px"),
    "soft": ("10px", "10px", "8px", "14px", "10px", "18px", "5px"),
    "sharp": ("4px", "4px", "4px", "6px", "4px", "8px", "3px"),
}


def build(a):
    b = brand_ramp(a.brand)
    k = ink_ramp(a.brand, a.ink)
    on_brand = k[900] if contrast(b[500], k[900]) >= contrast(b[500], "#FFFFFF") else "#FFFFFF"
    btn, nav, badge, card, field, modal, check = SHAPES[a.shape]
    acc = brand_ramp(a.accent) if a.accent else k
    acc_main = acc[500] if a.accent else k[900]
    on_accent = k[900] if contrast(acc_main, k[900]) >= contrast(acc_main, "#FFFFFF") else "#FFFFFF"

    if a.sidebar == "light":
        side = dict(bg="#FFFFFF", fg=k[700], strong=k[900], muted=k[400], hover=k[50], hover2=k[100],
                    accent=b[500], active_bg=b[50], active_fg=b[800], border=f"1px solid {k[100]}",
                    login_bg=b[50], login_fg=k[900])
    elif a.sidebar == "brand":
        side_bg = b[700] if contrast(b[700], "#FFFFFF") >= 4.5 else b[800]
        side = dict(bg=side_bg, fg=_rgba("#FFFFFF", .82), strong="#FFFFFF", muted=_rgba("#FFFFFF", .55),
                    hover=_rgba("#FFFFFF", .08), hover2=_rgba("#FFFFFF", .12), accent="#FFFFFF",
                    active_bg="#FFFFFF", active_fg=b[800], border="0", login_bg=side_bg, login_fg="#FFFFFF")
    else:
        side = dict(bg=k[900], fg=k[200], strong="#FFFFFF", muted=k[500], hover=_rgba("#FFFFFF", .06),
                    hover2=_rgba("#FFFFFF", .09), accent=b[500], active_bg=b[500], active_fg=on_brand, border="0",
                    login_bg=k[900], login_fg="#FFFFFF")

    ramp = lambda name, r: "\n".join(f"  --{name}-{s}: {r[s]};" for s in STEPS)
    shadow_ink = _rgba(k[900], "{a}")
    sh = lambda a_: shadow_ink.format(a=a_)

    return f"""/* =========================================================================
   Tokens de l'identité client. SEUL fichier à modifier pour changer la marque.
   Généré par tokens.py (--brand {a.brand} --accent {a.accent} --shape {a.shape} --sidebar {a.sidebar})
   Texte sur la couleur de marque : {on_brand} (contraste {contrast(b[500], on_brand):.1f}:1)
   ========================================================================= */
:root {{
  /* Marque */
{ramp("brand", b)}
  --on-brand: {on_brand};

  /* Neutres (encre) */
{ramp("ink", k)}

  /* Accent (secondaire) */
{ramp("accent", acc)}
  --accent: {acc_main};  --on-accent: {on_accent};

  /* États */
  --success: #1E9E6A;  --success-bg: #E6F6EF;  --success-fg: #137A50;  --success-border: #C6EADB;
  --warning: #A87400;  --warning-bg: #FFF6D9;  --warning-fg: #7D5600;  --warning-bar: #E5A100;
  --danger:  #D93A3A;  --danger-bg:  #FDECEC;  --danger-fg:  #B82727;  --danger-border: #F6CCCC;  --danger-bg-hover: #FBD9D9;
  --info:    #2F7FD1;  --info-bg:    #E8F1FB;  --info-fg:    #1F63AB;  --info-border: #CFE1F6;

  /* Surfaces */
  --surface: #FFFFFF;  --bg: #FFFFFF;  --bg-alt: {k[50]};
  --text: {k[800]};  --border: {k[100]};
  --topbar-bg: {_rgba(k[50], .86)};
  --backdrop: {sh(.42)};

  /* Barre latérale */
  --sidebar-bg: {side['bg']};  --sidebar-fg: {side['fg']};  --sidebar-fg-strong: {side['strong']};
  --sidebar-muted: {side['muted']};  --sidebar-hover: {side['hover']};  --sidebar-hover-strong: {side['hover2']};
  --sidebar-accent: {side['accent']};  --sidebar-border: {side['border']};
  --nav-active-bg: {side['active_bg']};  --nav-active-fg: {side['active_fg']};
  --login-art-bg: {side['login_bg']};  --login-art-fg: {side['login_fg']};

  /* Formes */
  --radius-btn: {btn};  --radius-nav: {nav};  --radius-badge: {badge};  --radius-pill: 999px;
  --radius-card: {card};  --radius-field: {field};  --radius-modal: {modal};  --radius-check: {check};

  /* Ombres & focus */
  --shadow-1: 0 1px 2px {sh(.06)}, 0 1px 1px {sh(.04)};
  --shadow-2: 0 4px 14px -4px {sh(.12)}, 0 2px 4px {sh(.05)};
  --shadow-3: 0 18px 40px -12px {sh(.22)}, 0 4px 10px {sh(.06)};
  --shadow-brand: 0 10px 24px -8px {_rgba(b[500], .55)};
  --btn-base: inset 0 -3px 0 {_rgba(b[900], .18)};
  --btn-pressed: inset 0 2px 0 {_rgba(b[900], .22)};
  --focus-ring: 0 0 0 3px #FFFFFF, 0 0 0 5.5px {b[500]};

  /* Typographie & mouvement */
  --font-title: "{a.font_title}", system-ui, sans-serif;
  --font-body: "{a.font_body}", system-ui, sans-serif;
  --ease: cubic-bezier(.2,.8,.2,1);
  --duration: 160ms;

  /* Mise en page */
  --sidebar-w: 248px;
  --page-pad: 32px;
}}
"""


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--brand", required=True)
    ap.add_argument("--ink")
    ap.add_argument("--accent")
    ap.add_argument("--font-title", default="Poppins")
    ap.add_argument("--font-body", default="Montserrat")
    ap.add_argument("--shape", choices=SHAPES, default="pill")
    ap.add_argument("--sidebar", choices=("dark", "light", "brand"), default="dark")
    ap.add_argument("--out", required=True)
    args = ap.parse_args()
    css = build(args)
    with open(args.out, "w", encoding="utf-8") as f:
        f.write(css)
    print(f"tokens.css écrit : {args.out}")
