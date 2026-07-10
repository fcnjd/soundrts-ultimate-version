#! .venv\Scripts\python.exe
import os
import shutil
from os.path import join, relpath, splitext

from docutils import core
from docutils.utils import SystemMessage

import rules2doc

SRC = "doc_src/src"

_SETTINGS = {
    "halt_level": 5,
    "exit_status_level": 5,
    "report_level": 4,
    "input_encoding": "utf-8",
    "output_encoding": "utf-8",
}


def _publish_one(src_path, dest_path):
    os.makedirs(os.path.dirname(dest_path), exist_ok=True)
    core.publish_file(
        source_path=src_path,
        writer_name="html",
        destination_path=dest_path,
        settings_overrides=_SETTINGS,
    )


def _publish_rst(lang, dest_pkg):
    """Build RST under doc_src into HTML under doc/{lang}/ only."""
    p = join(SRC, lang)
    dp = join(dest_pkg, lang)
    os.makedirs(dp, exist_ok=True)
    for root, _dirs, files in os.walk(p):
        for n in files:
            if not n.endswith(".rst"):
                continue
            src_path = join(root, n)
            rel = relpath(src_path, p)
            htm_rel = splitext(rel)[0] + ".htm"
            _publish_one(src_path, join(dp, htm_rel))
    if lang in ("en", "pt-BR", "es", "it"):
        with open(join(p, "stats.inc"), "w", encoding="utf-8") as f:
            f.write(rules2doc.stats)


def build(dest="."):
    DEST = join(dest, "doc")
    os.makedirs(DEST, exist_ok=True)

    # Prefer RST sources for all supported languages. Fall back to legacy
    # doc_src/src/{lang}/htm copies only when no RST tree is present.
    rst_langs = ("en", "zh", "es", "it", "pt-BR")
    for lang in rst_langs:
        lang_src = join(SRC, lang)
        has_rst = False
        if os.path.isdir(lang_src):
            for _root, _dirs, files in os.walk(lang_src):
                if any(n.endswith(".rst") for n in files):
                    has_rst = True
                    break
        if has_rst:
            if lang in ("en", "pt-BR", "es", "it"):
                # Keep units stats include in sync when present in English.
                en_stats = join(SRC, "en", "stats.inc")
                lang_stats = join(lang_src, "stats.inc")
                if lang != "en" and os.path.isfile(en_stats):
                    shutil.copyfile(en_stats, lang_stats)
            try:
                _publish_rst(lang, DEST)
            except (UnicodeError, SystemMessage):
                if lang == "pt-BR":
                    pt_br = join(DEST, "pt-BR")
                    os.makedirs(pt_br, exist_ok=True)
                    en_units = join(DEST, "en", "units.htm")
                    if os.path.isfile(en_units):
                        shutil.copyfile(en_units, join(pt_br, "units.htm"))
                else:
                    raise
        elif lang in ("es", "it"):
            p = join(SRC, lang, "htm")
            dp = join(DEST, lang)
            os.makedirs(dp, exist_ok=True)
            if os.path.isdir(p):
                for n in os.listdir(p):
                    shutil.copyfile(join(p, n), join(dp, n))


if __name__ == "__main__":
    build()
