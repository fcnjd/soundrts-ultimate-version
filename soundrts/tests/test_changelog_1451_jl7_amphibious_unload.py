"""审计：1.4.5.1 — 电脑运输船停门口不卸兵修复的发行说明。"""
from __future__ import annotations

from pathlib import Path


def _source(*path_parts):
    return (
        Path(__file__).resolve().parents[2].joinpath(*path_parts).read_text(encoding="utf-8")
    )


def _section_after_heading(text: str, heading: str) -> str:
    start = text.index(heading)
    rest = text[start + len(heading) :]
    next_idx = rest.find("\n1.4.")
    return rest if next_idx == -1 else rest[:next_idx]


def _assert_jl7_unload_documented(section: str) -> None:
    assert "_try_unload_idle_loaded_transports" in section
    assert "test_ai_jl7_amphibious_unload.py" in section
    assert "unload_all" in section
    assert "jl7" in section


def test_zh_relnotes_1451_documents_jl7_amphibious_unload_fix():
    src = _source("doc_src", "src", "zh", "relnotes.rst")
    section = _section_after_heading(src, "1.4.5.1")
    assert "运输船装满士兵停在敌方门口却不卸兵" in section
    _assert_jl7_unload_documented(section)


def test_en_relnotes_1451_documents_jl7_amphibious_unload_fix():
    src = _source("doc_src", "src", "en", "relnotes.rst")
    section = _section_after_heading(src, "1.4.5.1")
    assert "transport boats park loaded at the enemy shore without unloading" in section
    _assert_jl7_unload_documented(section)


def test_es_relnotes_1451_documents_jl7_amphibious_unload_fix():
    src = _source("doc_src", "src", "es", "relnotes.rst")
    section = _section_after_heading(src, "1.4.5.1")
    assert "barcos de transporte de la IA aparcan cargados" in section
    _assert_jl7_unload_documented(section)


def test_it_relnotes_1451_documents_jl7_amphibious_unload_fix():
    src = _source("doc_src", "src", "it", "relnotes.rst")
    section = _section_after_heading(src, "1.4.5.1")
    assert "navi da trasporto del computer restano cariche" in section
    _assert_jl7_unload_documented(section)


def test_pt_br_relnotes_1451_documents_jl7_amphibious_unload_fix():
    src = _source("doc_src", "src", "pt-BR", "relnotes.rst")
    section = _section_after_heading(src, "1.4.5.1")
    assert "barcos de transporte do computador estacionam carregados" in section
    _assert_jl7_unload_documented(section)
