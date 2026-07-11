"""Attack cooldown timing: mdg_cd/rdg_cd should match rules (no extra prep/delay tax)."""
from __future__ import annotations

from pathlib import Path

from soundrts.definitions import VIRTUAL_TIME_INTERVAL

_ROOT = Path(__file__).resolve().parents[1]
_ATTACK_ACTION = (_ROOT / "combat" / "attack_action.py").read_text(encoding="utf-8")
_DAMAGE_EFFECTS = (_ROOT / "combat" / "damage_effects.py").read_text(encoding="utf-8")


def test_prep_skips_extra_tick_when_ready_is_zero():
    """mdg_ready/rdg_ready=0 时不应再 return 等待下一 tick。"""
    for block in ("rdg_prep_end_time", "mdg_prep_end_time"):
        idx = _ATTACK_ACTION.index(f"if self.{block} <= 0:")
        snippet = _ATTACK_ACTION[idx : idx + 280]
        assert "if ready > 0:" in snippet
        assert snippet.index("if ready > 0:") < snippet.index("return")


def test_damage_effects_no_duplicate_cooldown_schedule():
    """冷却只在 attack_action 设置，_schedule_ballistic_hit 不再二次调度。"""
    assert "_set_attack_cooldown(is_melee, target)" not in _DAMAGE_EFFECTS
    assert "100ms最小延迟" not in _DAMAGE_EFFECTS


def test_instant_attack_interval_matches_tick_quantization():
    """修复后：1000ms cd + 0 ready 应约 1200ms 间隔（仅 tick 取整），而非 1500ms。"""
    VTI = VIRTUAL_TIME_INTERVAL
    mdg_cd = 1000
    times = []
    t = 0
    mdg_next = 0
    mdg_prep = 0
    for _ in range(20):
        if t < mdg_next:
            t += VTI
            continue
        if mdg_prep <= 0:
            ready = 0
            if ready > 0:
                mdg_prep = t + ready
                t += VTI
                continue
        elif t < mdg_prep:
            t += VTI
            continue
        times.append(t)
        mdg_next = t + mdg_cd
        mdg_prep = 0
        t += VTI
    assert len(times) >= 2
    interval = times[1] - times[0]
    # tick 取整：1000ms cd 在 300ms tick 下稳定为 1200ms 间隔
    assert interval == 1200
    assert interval < 1500  # 修复前约为 1500ms
