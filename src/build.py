"""Monta a página a partir de src/page.html e dos dados em src/data.

Uso: python3 src/build.py [--artifact CAMINHO]
Gera index.html e publicada/icsmp-iegm.html. Com --artifact, grava também
o corpo da página (sem doctype/head) para publicar no claude.ai.
"""
import json, pathlib, sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
SRC = ROOT / "src"
HEAD = ('<!doctype html>\n<html lang="pt-BR">\n<head>\n<meta charset="utf-8">\n'
        '<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">\n'
        '</head>\n<body>\n')

def main():
    page = (SRC / "page.html").read_text(encoding="utf-8")
    rev05 = json.loads((SRC / "data" / "rev05.json").read_text(encoding="utf-8"))
    regional = json.loads((SRC / "data" / "regional.json").read_text(encoding="utf-8"))
    body = (page.replace("/*DATA*/[]", json.dumps(rev05, ensure_ascii=False))
                .replace("/*REGIONAL*/[]", json.dumps(regional, ensure_ascii=False, separators=(",", ":"))))
    full = HEAD + body + "</body>\n</html>\n"
    (ROOT / "index.html").write_text(full, encoding="utf-8")
    (ROOT / "publicada" / "icsmp-iegm.html").write_text(full, encoding="utf-8")
    if "--artifact" in sys.argv:
        pathlib.Path(sys.argv[sys.argv.index("--artifact") + 1]).write_text(body, encoding="utf-8")

if __name__ == "__main__":
    main()
