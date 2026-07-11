"""Terrain cover: rules default, map override, editor palette inheritance."""
from __future__ import annotations

import os
from pathlib import Path

import pytest

os.environ.setdefault("SDL_VIDEODRIVER", "dummy")
os.environ.setdefault("SDL_AUDIODRIVER", "dummy")

from soundrts.clientgame import load_palette
from soundrts.definitions import _get_base_classes, rules
from soundrts.lib.editor_palette import apply_palette_to_square
from soundrts.lib.square_terrain_rules import (
    DEFAULT_TERRAIN_COVER,
    parse_terrain_cover_pair,
    resolve_terrain_cover,
    terrain_default_cover,
)
from soundrts.world import World


@pytest.fixture(autouse=True)
def _load_rules():
    rules.load(
        Path("res/rules.txt").read_text(encoding="utf-8"),
        base_classes=_get_base_classes(),
    )


def test_parse_terrain_cover_pair():
    assert parse_terrain_cover_pair([".5", "0"]) == (50, 0)
    assert parse_terrain_cover_pair([".1", "0"]) == (10, 0)


def test_marsh_default_cover_from_rules():
    assert terrain_default_cover("marsh") == (50, 0)
    assert terrain_default_cover("plain") is None


def test_resolve_terrain_cover_priority():
    assert resolve_terrain_cover("marsh", (10, 0)) == (10, 0)
    assert resolve_terrain_cover("marsh", None) == (50, 0)
    assert resolve_terrain_cover(None, None) == DEFAULT_TERRAIN_COVER


def _build_map(text: str):
    world = World([], 42)
    world._parse_map(text)
    world._build_map()
    return world


def test_map_terrain_marsh_uses_rules_cover_without_cover_line():
    world = _build_map(
        """
nb_columns 2
nb_lines 2
nb_players_min 1
nb_players_max 1
starting_squares 2,2
terrain marsh 1,1
"""
    )
    assert world.grid["0,0"].terrain_cover == (50, 0)


def test_map_cover_line_overrides_rules_default():
    world = _build_map(
        """
nb_columns 2
nb_lines 2
nb_players_min 1
nb_players_max 1
starting_squares 2,2
terrain marsh 1,1
cover .1 0 1,1
"""
    )
    assert world.grid["0,0"].terrain_cover == (10, 0)


def test_load_palette_inherits_marsh_cover_from_rules():
    entry = next(e for name, e in load_palette() if name == "marsh")
    assert entry["cover"] == (50, 0)


def test_load_palette_keeps_explicit_forest_cover():
    entry = next(e for name, e in load_palette() if name == "forest")
    assert entry["cover"] == (10, 0)


def test_apply_palette_marsh_matches_rules_cover():
    world = _build_map(
        """
nb_columns 2
nb_lines 2
nb_players_min 1
nb_players_max 1
starting_squares 2,2
"""
    )
    sq = world.grid["0,0"]
    entry = next(e for name, e in load_palette() if name == "marsh")
    apply_palette_to_square(sq, entry)
    assert sq.terrain_cover == (50, 0)
