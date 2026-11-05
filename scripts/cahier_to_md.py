"""Convertit le cahier des charges renvoyé par Koralya (get_cahier) en Markdown lisible.

python cahier_to_md.py <entrée> <sortie.md>

<entrée> peut être :
  - le fichier JSON sauvegardé par l'outil MCP quand la réponse est trop longue
    ({"result": {"contenido": "<html…>", "formato": "html", …}}) ;
  - un JSON {"contenido": …} ;
  - un fichier .html ou .md brut.
Bibliothèque standard uniquement.
"""
import html
import json
import re
import sys
from html.parser import HTMLParser


class MD(HTMLParser):
    BLOCK = {"p", "div", "h1", "h2", "h3", "h4", "h5", "h6", "li", "tr", "blockquote", "section"}

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.out = []
        self.line = []
        self.lists = []
        self.table = None
        self.row = None
        self.cell = None
        self.prefix = ""

    # --- utilitaires
    def _text(self, t):
        target = self.cell if self.cell is not None else self.line
        target.append(t)

    def _flush(self):
        txt = re.sub(r"[ \t ]+", " ", "".join(self.line)).strip()
        if txt:
            self.out.append(self.prefix + txt)
        self.line, self.prefix = [], ""

    # --- balises
    def handle_starttag(self, tag, attrs):
        if tag in ("table",):
            self._flush()
            self.table = []
        elif tag == "tr" and self.table is not None:
            self.row = []
        elif tag in ("td", "th") and self.row is not None:
            self.cell = []
        elif tag in ("ul", "ol"):
            self._flush()
            self.lists.append([tag, 0])
        elif tag == "li":
            self._flush()
            depth = len(self.lists) - 1
            kind = self.lists[-1] if self.lists else ["ul", 0]
            kind[1] += 1
            bullet = f"{kind[1]}." if kind[0] == "ol" else "-"
            self.prefix = "  " * max(depth, 0) + bullet + " "
        elif re.fullmatch(r"h[1-6]", tag):
            self._flush()
            self.prefix = "#" * int(tag[1]) + " "
        elif tag in ("strong", "b"):
            self._text("**")
        elif tag in ("em", "i"):
            self._text("*")
        elif tag == "br":
            if self.cell is not None:
                self.cell.append(" ")
            else:
                self._flush()
        elif tag in self.BLOCK and self.cell is None:
            self._flush()

    def handle_endtag(self, tag):
        if tag in ("td", "th") and self.cell is not None:
            self.row.append(re.sub(r"\s+", " ", "".join(self.cell)).strip().replace("|", "\\|"))
            self.cell = None
        elif tag == "tr" and self.row is not None:
            if any(self.row):
                self.table.append(self.row)
            self.row = None
        elif tag == "table" and self.table is not None:
            rows = self.table
            self.table = None
            if rows:
                n = max(len(r) for r in rows)
                rows = [r + [""] * (n - len(r)) for r in rows]
                self.out.append("")
                self.out.append("| " + " | ".join(rows[0]) + " |")
                self.out.append("|" + "---|" * n)
                for r in rows[1:]:
                    self.out.append("| " + " | ".join(r) + " |")
                self.out.append("")
        elif tag in ("ul", "ol"):
            self._flush()
            if self.lists:
                self.lists.pop()
        elif tag in ("strong", "b"):
            self._text("**")
        elif tag in ("em", "i"):
            self._text("*")
        elif (tag in self.BLOCK or re.fullmatch(r"h[1-6]", tag)) and self.cell is None:
            self._flush()

    def handle_data(self, data):
        if data.strip() or (self.line and data):
            self._text(data.replace("\n", " "))

    def markdown(self):
        self._flush()
        text = "\n\n".join(l if not l.startswith(("|", "-", "  ")) and not re.match(r"\d+\. ", l) else l for l in self.out)
        # les lignes de liste / tableau consécutives ne doivent pas être séparées par une ligne vide
        text = re.sub(r"\n\n(?=(\||- |  |\d+\. ))", "\n", text)
        text = text.replace("****", "")
        return re.sub(r"\n{3,}", "\n\n", text).strip() + "\n"


def load(path):
    raw = open(path, encoding="utf-8").read()
    meta = {}
    try:
        data = json.loads(raw)
        data = data.get("result", data)
        meta = {k: v for k, v in data.items() if k not in ("contenido", "versiones")}
        raw = data["contenido"]
        fmt = data.get("formato", "html")
    except (json.JSONDecodeError, AttributeError, KeyError):
        fmt = "md" if path.endswith(".md") else "html"
    return raw, fmt, meta


def main():
    src, dst = sys.argv[1], sys.argv[2]
    raw, fmt, meta = load(src)
    if fmt == "html" or "<p" in raw[:2000]:
        p = MD()
        p.feed(raw)
        body = p.markdown()
    else:
        body = html.unescape(raw)
    head = ""
    if meta:
        head = (f"<!-- Cahier des charges · client {meta.get('cliente', '?')} · statut {meta.get('status', '?')}"
                f" · version {meta.get('version_mostrada', meta.get('current_version', '?'))} · maj {meta.get('updated_at', '?')} -->\n\n")
    with open(dst, "w", encoding="utf-8") as f:
        f.write(head + body)
    print(f"{dst} : {len(body):,} caractères, {body.count(chr(10)):,} lignes")


if __name__ == "__main__":
    main()
