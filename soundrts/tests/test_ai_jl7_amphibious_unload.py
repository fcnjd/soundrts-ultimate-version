"""jl7 + nightmare AI: packed boats parked at the enemy shore must unload."""
from __future__ import annotations

import os
import sys
import types
import warnings
from pathlib import Path

import pytest

os.environ.setdefault("SDL_VIDEODRIVER", "dummy")
os.environ.setdefault("SDL_AUDIODRIVER", "dummy")

saved_argv = sys.argv
sys.argv = [saved_argv[0] if saved_argv else "pytest"]
with warnings.catch_warnings():
    warnings.simplefilter("ignore")
    from soundrts.definitions import rules
    from soundrts.lib.resource import res
    from soundrts.world import World
    from soundrts.worldclient import DirectClient, DummyClient
    from soundrts.worldplayercomputer import Computer
    from soundrts.worldplayercomputer_water import find_amphibious_crossing

sys.argv = saved_argv

ROOT = Path(__file__).resolve().parents[2]
JL7 = ROOT / "res" / "multi" / "jl7.txt"


@pytest.fixture(autouse=True)
def load_rules():
    res.load_rules_and_ai()


def _load_jl7_world():
    world = World([], 42)
    world._parse_map(JL7.read_text(encoding="utf-8"))
    world._build_map()
    return world


def _populate_jl7_nightmare():
    world = _load_jl7_world()
    human = DirectClient("p1", None)
    human.faction = rules.factions[0]
    human.alliance = "1"
    ai_client = DummyClient("nightmare")
    ai_client.faction = rules.factions[0]
    ai_client.alliance = "2"
    world.populate_map([human, ai_client], random_starts=False)
    world._update_buckets()
    comp = next(p for p in world.players if isinstance(p, Computer))
    comp.AI_type = "nightmare"
    return world, comp


def _order_keywords(unit):
    out = []
    for o in unit.orders:
        if isinstance(o, (list, tuple)):
            out.append(o[0])
        else:
            out.append(getattr(o, "keyword", o))
    return out


def test_jl7_amphibious_crossing_reaches_enemy_start():
    world, comp = _populate_jl7_nightmare()
    ai_start = world.grid[world.players_starts[1][1][0][0]]
    enemy_start = world.grid[world.players_starts[0][1][0][0]]
    route = find_amphibious_crossing(ai_start, enemy_start, comp)
    assert route is not None
    _load_land, _load_water, unload_water, unload_land = route
    assert unload_land is enemy_start or unload_land in enemy_start.neighbors
    assert unload_water in unload_land.strict_neighbors


def test_jl7_send_amphibious_issues_unload_all():
    world, comp = _populate_jl7_nightmare()
    ai_start = world.grid[world.players_starts[1][1][0][0]]
    enemy_start = world.grid[world.players_starts[0][1][0][0]]
    route = find_amphibious_crossing(ai_start, enemy_start, comp)
    assert route is not None
    load_land, load_water, _unload_water, _unload_land = route

    footman = types.SimpleNamespace(
        airground_type="ground",
        speed=1,
        place=ai_start,
        orders=[],
        is_inside=False,
        transport_volume=1,
        cancel_all_orders=lambda: footman.orders.clear(),
        take_order=lambda cmd, **kw: footman.orders.append(cmd),
    )
    boat = types.SimpleNamespace(
        airground_type="water",
        transport_capacity=8,
        speed=1,
        place=load_water,
        orders=[],
        is_inside=False,
        inside=types.SimpleNamespace(objects=[]),
        cancel_all_orders=lambda: boat.orders.clear(),
        take_order=lambda cmd, **kw: boat.orders.append(cmd),
    )
    comp.units = [footman, boat]
    sent = comp._send_ground_units_amphibious([footman], enemy_start)
    assert sent == [footman]
    assert "unload_all" in _order_keywords(boat)
    assert ["load_all", load_land.id] in boat.orders


def test_jl7_nightmare_unloads_packed_boat_parked_at_enemy_door():
    """Regression: boat full of soldiers idling next to the player's shore.

    `_try_transport_assaults` ignores cargo (soldiers are is_inside), so without an
    explicit unload pass the nightmare AI never issues unload_all.
    """
    world, comp = _populate_jl7_nightmare()
    ai_start = world.grid[world.players_starts[1][1][0][0]]
    enemy_start = world.grid[world.players_starts[0][1][0][0]]
    route = find_amphibious_crossing(ai_start, enemy_start, comp)
    assert route is not None
    _load_land, _load_water, unload_water, unload_land = route

    footman = types.SimpleNamespace(
        airground_type="ground",
        speed=1,
        place=None,
        orders=[],
        is_inside=True,
        transport_volume=1,
    )
    boat = types.SimpleNamespace(
        airground_type="water",
        transport_capacity=8,
        speed=1,
        place=unload_water,
        orders=[],
        is_inside=False,
        inside=types.SimpleNamespace(objects=[footman]),
        cancel_all_orders=lambda: boat.orders.clear(),
        take_order=lambda cmd, **kw: boat.orders.append(cmd),
    )
    assert unload_land in unload_water.strict_neighbors
    comp.units = [boat, footman]
    comp._enemy_presence = [enemy_start]
    # No idle ground soldiers outside — this is the stuck "parked at the door" state.
    assert comp._idle_ground_assault_units() == []

    comp._try_amphibious_landings()

    assert ["unload_all", unload_land.id] in boat.orders or any(
        isinstance(o, list) and o[0] == "unload_all" for o in boat.orders
    )
    keywords = _order_keywords(boat)
    assert "unload_all" in keywords


def test_try_unload_idle_loaded_transport_skips_empty_boat():
    world, comp = _populate_jl7_nightmare()
    enemy_start = world.grid[world.players_starts[0][1][0][0]]
    water = next(
        n for n in enemy_start.strict_neighbors if getattr(n, "is_water", False)
    )
    boat = types.SimpleNamespace(
        airground_type="water",
        transport_capacity=8,
        speed=1,
        place=water,
        orders=[],
        is_inside=False,
        inside=types.SimpleNamespace(objects=[]),
        cancel_all_orders=lambda: boat.orders.clear(),
        take_order=lambda cmd, **kw: boat.orders.append(cmd),
    )
    comp.units = [boat]
    comp._enemy_presence = [enemy_start]
    comp._try_unload_idle_loaded_transports()
    assert boat.orders == []
