"""审计：1.4.5.1 — 已占领建筑强制攻击仍触发占领命令修复的发行说明。"""
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


def _assert_capture_after_occupied_documented(section: str) -> None:
    assert "should_capture_on_contact" in section
    assert "test_capture_default_order.py" in section
    assert "test_imperative_attack_on_captured_barracks_deals_damage_not_capture" in section


def test_zh_relnotes_1451_documents_capture_after_occupied_fix():
    src = _source("doc_src", "src", "zh", "relnotes.rst")
    section = _section_after_heading(src, "1.4.5.1")
    assert "已占领建筑被强制攻击时仍触发占领命令" in section
    _assert_capture_after_occupied_documented(section)


def test_en_relnotes_1451_documents_capture_after_occupied_fix():
    src = _source("doc_src", "src", "en", "relnotes.rst")
    section = _section_after_heading(src, "1.4.5.1")
    assert "force attack on already-captured building still triggers capture" in section
    _assert_capture_after_occupied_documented(section)


def test_es_relnotes_1451_documents_capture_after_occupied_fix():
    src = _source("doc_src", "src", "es", "relnotes.rst")
    section = _section_after_heading(src, "1.4.5.1")
    assert "ataque forzado a edificio ya capturado" in section
    _assert_capture_after_occupied_documented(section)


def test_it_relnotes_1451_documents_capture_after_occupied_fix():
    src = _source("doc_src", "src", "it", "relnotes.rst")
    section = _section_after_heading(src, "1.4.5.1")
    assert "attacco forzato a edificio già catturato" in section
    _assert_capture_after_occupied_documented(section)


def test_pt_br_relnotes_1451_documents_capture_after_occupied_fix():
    src = _source("doc_src", "src", "pt-BR", "relnotes.rst")
    section = _section_after_heading(src, "1.4.5.1")
    assert "ataque forçado a edificio já capturado" in section
    _assert_capture_after_occupied_documented(section)
