"""Unit ``*_on_terrain`` percent modifiers (``.5`` -> 50% of base)."""
from __future__ import annotations

import soundrts.worldunit  # noqa: F401

from soundrts.combat.attack_action import AttackActionMixin
from soundrts.combat.damage_calculation import DamageCalculationMixin
from soundrts.lib.nofloat import PRECISION
from soundrts.lib.square_terrain_rules import (
    parse_percent_points,
    stat_percent_delta,
    terrain_list_stat_percent_delta,
)


class _MarshPlace:
    type_name = "marsh"

    def type_name_at(self, x, y):
        return "marsh"


class _Attacker(DamageCalculationMixin, AttackActionMixin):
    def __init__(self):
        self.mdg = 6 * PRECISION
        self.rdg = 4 * PRECISION
        self.mdg_cd = int(2 * PRECISION)
        self.rdg_cd = int(1.5 * PRECISION)
        self.mdg_vs = {}
        self.rdg_vs = {}
        self.mdg_on_terrain = ("marsh", "-.25")
        self.rdg_on_terrain = ("marsh", ".5")
        self.mdg_cd_on_terrain = ("marsh", ".25")
        self.rdg_cd_on_terrain = ("marsh", ".2")
        self.place = _MarshPlace()
        self.x = 0
        self.y = 0


def test_parse_percent_points():
    assert parse_percent_points(".25") == 25
    assert parse_percent_points("-.5") == -50


def test_stat_percent_delta():
    base = 8 * PRECISION
    assert stat_percent_delta("-.25", base) == base * (-25) // 100


def test_terrain_list_stat_percent_delta():
    assert terrain_list_stat_percent_delta(
        "marsh", ("marsh", "-.25", "forest", ".5"), 8 * PRECISION
    ) == 8 * PRECISION * (-25) // 100


def test_mdg_on_terrain_percent():
    attacker = _Attacker()
    target = type(
        "T",
        (),
        {"type_name": "footman", "expanded_is_a": (), "_armor_instance": None, "armor": None},
    )()
    base = 6 * PRECISION
    assert attacker._get_melee_damage_vs(target) == base + base * (-25) // 100


def test_rdg_on_terrain_percent():
    attacker = _Attacker()
    target = type(
        "T",
        (),
        {"type_name": "footman", "expanded_is_a": (), "_armor_instance": None, "armor": None},
    )()
    base = 4 * PRECISION
    assert attacker._get_ranged_damage_vs(target) == base + base * 50 // 100


def test_mdg_cd_on_terrain_percent():
    attacker = _Attacker()
    base_cd = int(2 * PRECISION)
    assert attacker._get_melee_cd_on_terrain() == base_cd * 25 // 100


def test_rdg_cd_on_terrain_percent():
    attacker = _Attacker()
    base_cd = int(1.5 * PRECISION)
    assert attacker._get_ranged_cd_on_terrain() == base_cd * 20 // 100
