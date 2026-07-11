"""审计：1.4.5.1 — 近战/远程攻击冷却偏慢修复的发行说明。"""
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


def test_zh_relnotes_1451_documents_attack_cooldown_fix():
    src = _source("doc_src", "src", "zh", "relnotes.rst")
    section = _section_after_heading(src, "1.4.5.1")
    assert "mdg_cd" in section
    assert "rdg_cd" in section
    assert "test_attack_cooldown_timing.py" in section
    assert "charge_mdg_cd" in section


def test_en_relnotes_1451_documents_attack_cooldown_fix():
    src = _source("doc_src", "src", "en", "relnotes.rst")
    section = _section_after_heading(src, "1.4.5.1")
    assert "mdg_cd" in section
    assert "rdg_cd" in section
    assert "test_attack_cooldown_timing.py" in section
    assert "charge_mdg_cd" in section


def test_es_relnotes_1451_documents_attack_cooldown_fix():
    src = _source("doc_src", "src", "es", "relnotes.rst")
    section = _section_after_heading(src, "1.4.5.1")
    assert "mdg_cd" in section
    assert "test_attack_cooldown_timing.py" in section


def test_it_relnotes_1451_documents_attack_cooldown_fix():
    src = _source("doc_src", "src", "it", "relnotes.rst")
    section = _section_after_heading(src, "1.4.5.1")
    assert "mdg_cd" in section
    assert "test_attack_cooldown_timing.py" in section


def test_pt_br_relnotes_1451_documents_attack_cooldown_fix():
    src = _source("doc_src", "src", "pt-BR", "relnotes.rst")
    section = _section_after_heading(src, "1.4.5.1")
    assert "mdg_cd" in section
    assert "test_attack_cooldown_timing.py" in section
