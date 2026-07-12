"""Rules-driven configuration for RMG strategic systems (mods/custom maps)."""
from __future__ import annotations

# Fallback defaults when rules are unavailable (unit tests, early import).
_DEFAULTS = {
    "rmg_diplomacy_request_cost": 20,
    "rmg_tile_purchase_base": 20,
    "rmg_tile_purchase_step": 10,
    "rmg_policy_slot_limit": 2,
    "rmg_trade_cooldown": 60,
    "rmg_economic_goal": 3000,
    "rmg_economic_goal_fast": 2000,
    "rmg_economic_goal_macro": 5000,
    "rmg_economic_goal_lanes": 2500,
    "rmg_survival_seconds": 900,
    "rmg_survival_seconds_fast": 600,
    "rmg_exploration_ruin_pairs_small": 1,
    "rmg_exploration_ruin_pairs_medium": 2,
    "rmg_exploration_ruin_pairs_large": 2,
    "rmg_exploration_ruin_pairs_bonus": 1,
    "rmg_strategic_systems": 1,
}

_TRADE_ALIASES = {
    "wood": "resource2",
    "food": "resource3",
}

_FALLBACK_IMPROVEMENTS = {
    "mine": "rmg_tile_mine",
    "lumber_mill": "rmg_tile_lumber_mill",
    "farm": "rmg_tile_farm",
    "trading_post": "rmg_tile_trading_post",
}

_FALLBACK_IMPROVEMENT_YIELDS = {
    "mine": [3, 0, 0, 0, 0],
    "lumber_mill": [0, 3, 0, 0, 0],
    "farm": [0, 0, 3, 0, 0],
    "trading_post": [2, 0, 0, 0, 2],
}

_FALLBACK_TRADES = {
    "resource2": {
        "rmg_trade_pay": [50, 0, 0],
        "rmg_trade_gain": [0, 100, 0],
    },
    "resource3": {
        "rmg_trade_pay": [50, 0, 0],
        "rmg_trade_gain": [0, 0, 100],
    },
    "open_borders": {
        "rmg_trade_diplomacy_cost": 15,
        "rmg_trade_pay": [30, 0, 0],
        "rmg_trade_alliance": 1,
    },
}

_cache: dict | None = None


def invalidate_rmg_rules_cache() -> None:
    global _cache
    _cache = None


def _rules():
    from .definitions import rules

    return rules


def _load_cache() -> dict:
    global _cache
    if _cache is not None:
        return _cache

    try:
        rules = _rules()
        classes = getattr(rules, "classes", {}) or {}
    except Exception:
        classes = {}

    improvements: dict[str, str] = dict(_FALLBACK_IMPROVEMENTS)
    improvement_yields: dict[str, list[int]] = {
        key: list(values) for key, values in _FALLBACK_IMPROVEMENT_YIELDS.items()
    }
    improvement_types: set[str] = set(improvements.values())
    build_orders: dict[str, str] = {
        f"rmg_build_{key}": key for key in improvements
    }

    for type_name, cls in classes.items():
        if not getattr(cls, "rmg_tile_improvement", 0):
            continue
        key = getattr(cls, "rmg_improvement_key", None) or type_name.replace(
            "rmg_tile_", "", 1
        )
        improvements[key] = type_name
        improvement_types.add(type_name)
        build_orders[f"rmg_build_{key}"] = key
        raw = getattr(cls, "rmg_tile_yield", None) or improvement_yields.get(key, [])
        bonus = [int(x) for x in raw]
        while len(bonus) < 5:
            bonus.append(0)
        improvement_yields[key] = bonus[:5]

    trades: dict[str, object] = {}
    for name, cls in classes.items():
        if not getattr(cls, "rmg_trade", 0):
            continue
        trade_id = str(getattr(cls, "rmg_trade_id", None) or name).lower()
        trades[trade_id] = cls

    if not trades:
        trades = {key: SimpleNamespaceTrade(data) for key, data in _FALLBACK_TRADES.items()}

    _cache = {
        "improvements": improvements,
        "improvement_yields": improvement_yields,
        "improvement_types": improvement_types,
        "build_orders": build_orders,
        "trades": trades,
    }
    return _cache


class SimpleNamespaceTrade:
    """Minimal trade definition used when rules are not loaded."""

    def __init__(self, data: dict):
        for key, value in data.items():
            setattr(self, key, value)


def rmg_parameter(name: str, default=None):
    """Read an RMG scalar from ``def parameters`` in rules.txt."""
    if default is None:
        default = _DEFAULTS.get(name, 0)
    try:
        return int(_rules().get("parameters", name, default))
    except Exception:
        return int(default)


def diplomacy_request_cost() -> int:
    return rmg_parameter("rmg_diplomacy_request_cost")


def tile_purchase_base_cost() -> int:
    return rmg_parameter("rmg_tile_purchase_base")


def tile_purchase_step_cost() -> int:
    return rmg_parameter("rmg_tile_purchase_step")


def policy_slot_limit() -> int:
    return rmg_parameter("rmg_policy_slot_limit")


def trade_cooldown_ms(trade_cls=None) -> int:
    if trade_cls is not None:
        seconds = getattr(trade_cls, "rmg_trade_cooldown", None)
        if seconds is not None:
            return max(0, int(seconds)) * 1000
    return rmg_parameter("rmg_trade_cooldown") * 1000


def normalize_trade_kind(trade_kind: str):
    kind = str(trade_kind or "").lower()
    kind = _TRADE_ALIASES.get(kind, kind)
    if kind in _load_cache()["trades"]:
        return kind
    return None


def trade_kinds() -> frozenset[str]:
    return frozenset(_load_cache()["trades"].keys())


def trade_class(trade_kind: str):
    kind = normalize_trade_kind(trade_kind)
    if kind is None:
        return None
    return _load_cache()["trades"].get(kind)


def trade_pay_visible(trade_cls) -> list[int]:
    raw = getattr(trade_cls, "rmg_trade_pay", None) or []
    result = [int(x) for x in raw]
    while len(result) < 3:
        result.append(0)
    return result[:3]


def trade_gain_visible(trade_cls) -> list[int]:
    raw = getattr(trade_cls, "rmg_trade_gain", None) or []
    result = [int(x) for x in raw]
    while len(result) < 3:
        result.append(0)
    return result[:3]


def improvement_entity_types() -> dict[str, str]:
    return dict(_load_cache()["improvements"])


def improvement_type_names() -> frozenset[str]:
    return frozenset(_load_cache()["improvement_types"])


def build_order_improvements() -> dict[str, str]:
    return dict(_load_cache()["build_orders"])


def build_keyword_for_improvement(improvement_key: str) -> str:
    for keyword, key in _load_cache()["build_orders"].items():
        if key == improvement_key:
            return keyword
    return f"rmg_build_{improvement_key}"


def default_work_focus_for_improvement(improvement_key: str) -> str:
    """Pick gold/wood/food/culture focus from ``rmg_tile_yield`` bonuses."""
    bonus = improvement_yield_bonus(improvement_key)
    labels = ("gold", "wood", "food", "culture")
    best_index = 0
    best_value = bonus[0] if bonus else 0
    for index in range(1, min(4, len(bonus))):
        if bonus[index] > best_value:
            best_value = bonus[index]
            best_index = index
    return labels[best_index]


def improvement_entity_type(improvement_key: str) -> str | None:
    return improvement_entity_types().get(improvement_key)


def improvement_for_entity_type(type_name: str):
    for key, entity_type in improvement_entity_types().items():
        if entity_type == type_name:
            return key
    return None


def improvement_yield_bonus(improvement_key: str) -> list[int]:
    if not improvement_key:
        return [0, 0, 0, 0, 0]
    return list(_load_cache()["improvement_yields"].get(improvement_key, [0, 0, 0, 0, 0]))


def improvement_menu_cost(improvement_key: str, nb_types: int) -> tuple:
    from .definitions import rules

    type_name = improvement_entity_types().get(improvement_key)
    if not type_name:
        return (0,) * nb_types
    cls = rules.unit_class(type_name)
    if cls is None:
        return (0,) * nb_types
    costs = list(getattr(cls, "cost", None) or [])
    while len(costs) < nb_types:
        costs.append(0)
    return tuple(costs[:nb_types])


def economic_goal(template: str = "standard", spec_override: int | None = None) -> int:
    if spec_override is not None:
        return max(1, int(spec_override))
    key = f"rmg_economic_goal_{template}"
    try:
        rules = _rules()
        per_template = rules.get("parameters", key, None)
        if per_template is not None:
            return max(1, int(per_template))
    except Exception:
        pass
    if key in _DEFAULTS:
        return _DEFAULTS[key]
    return rmg_parameter("rmg_economic_goal", 3000)


def survival_seconds(template: str = "standard", spec_override: int | None = None) -> int:
    if spec_override is not None:
        return max(1, int(spec_override))
    key = "rmg_survival_seconds_fast" if template == "fast" else "rmg_survival_seconds"
    return rmg_parameter(key, _DEFAULTS.get(key, 900))


def exploration_ruin_pairs(
    size: str = "medium",
    exploration_mode: bool = False,
    spec_override: int | None = None,
) -> int:
    if spec_override is not None:
        return max(0, int(spec_override))
    size_key = size if size in ("small", "medium", "large") else "medium"
    param = f"rmg_exploration_ruin_pairs_{size_key}"
    base = rmg_parameter(param, _DEFAULTS.get(param, 2))
    if exploration_mode:
        base += rmg_parameter(
            "rmg_exploration_ruin_pairs_bonus",
            _DEFAULTS.get("rmg_exploration_ruin_pairs_bonus", 1),
        )
    return max(0, base)


def strategic_systems_enabled(spec_override: bool | None = None) -> bool:
    if spec_override is not None:
        return bool(spec_override)
    return bool(rmg_parameter("rmg_strategic_systems", 1))
