"""Suicide must not leave a nameless fog Tab target; corpse audio path stays intact."""
from __future__ import annotations

import os
import types

import pytest

os.environ.setdefault("SDL_VIDEODRIVER", "dummy")
os.environ.setdefault("SDL_AUDIODRIVER", "dummy")

from soundrts.definitions import rules
from soundrts.lib.resource import res
from soundrts.world import World
from soundrts.worldclient import DirectClient
from soundrts.worldresource import Corpse
from soundrts.clientgame.game_unit_control import _object_choices
from soundrts.clientgame.game_navigation import update_fog_of_war


@pytest.fixture(autouse=True)
def _load_rules():
    res.load_rules_and_ai()


def _world_from_map(text: str):
    world = World([], 42)
    world._parse_map(text)
    world._build_map()
    client = DirectClient("p1", None)
    client.create_player(world)
    return world, client.player


def _sq(world, label: str):
    col = ord(label[0]) - ord("a")
    row = int(label[1]) - 1
    return world.grid[f"{col},{row}"]


def _map_5x5():
    return """
nb_columns 5
nb_lines 5
nb_players_min 1
nb_players_max 1
starting_squares 0,0
starting_resources 100 100
terrain plain a1 a2 a3 a4 a5
terrain plain b1 b2 b3 b4 b5
terrain plain c1 c2 c3 c4 c5
terrain plain d1 d2 d3 d4 d5
terrain plain e1 e2 e3 e4 e5
"""


def _suicide_alone_at_a2(player, world):
    a1 = _sq(world, "a1")
    a2 = _sq(world, "a2")
    th_cls = rules.unit_class("townhall")
    th_cls.collision = 0
    th_cls(player, a1, a1.x, a1.y)
    peasant_cls = rules.unit_class("peasant")
    old_collision = peasant_cls.collision
    peasant_cls.collision = 0
    try:
        peasant = peasant_cls(player, a2, a2.x, a2.y)
    finally:
        peasant_cls.collision = old_collision
    peasant.take_order(["attack", peasant.id], imperative=True, forget_previous=True)
    for _ in range(800):
        if peasant.place is None:
            break
        world.update()
    for _ in range(20):
        world.update()
    return peasant, a2


def _tab_choices(player, world, square):
    iface = types.SimpleNamespace(
        world=world,
        player=player,
        place=square,
        zoom_mode=False,
        zoom=None,
        immersion=False,
        group=[],
        x=square.x / 1000,
        y=square.y / 1000,
        o=90,
        dobjets={},
        memory=set(),
        perception=set(),
        scouted_squares=set(),
        scouted_before_squares=set(),
        scout_info=set(),
        target=None,
        collision_debug=None,
        _side_filter="all",
        _type_filter="all",
        an_order_requiring_a_target_is_selected=False,
    )
    iface.distance = lambda o: 0
    iface.memory = set(player.memory_for_display())
    iface.perception = set(player.perception)
    iface.scouted_squares = set(player.observed_squares)
    iface.scouted_before_squares = set(player.observed_before_squares)
    update_fog_of_war(iface)
    return _object_choices(iface, 1, [])


def test_a2_suicide_tab_has_no_nameless_ghost():
    world, player = _world_from_map(_map_5x5())
    peasant, a2 = _suicide_alone_at_a2(player, world)
    assert peasant.place is None
    choices = _tab_choices(player, world, a2)
    assert choices == []


def test_corpse_memory_not_blocked():
    """Minimal ghost fix must not forbid corpse fog memory (fly buzz audio)."""
    world, player = _world_from_map(_map_5x5())
    _suicide_alone_at_a2(player, world)
    corpse = next(o for o in _sq(world, "a2").objects if isinstance(o, Corpse))
    player._bulk_memorize({corpse})
    assert any(
        getattr(m, "type_name", None) == "corpse"
        or getattr(getattr(m, "initial_model", None), "type_name", None) == "corpse"
        for m in player.memory_for_display()
    )
