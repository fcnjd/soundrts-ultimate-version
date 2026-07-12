"""Runtime strategic systems used by procedural random maps.

The regular SoundRTS resource and upgrade systems remain authoritative.  This
module adds the small amount of per-player state that has no classic RTS
equivalent: culture, diplomacy points, city/tile income and policy modifiers.
"""
from __future__ import annotations

from typing import Iterable, Tuple

from .lib.nofloat import to_int
from . import rmg_rules


CITY_TYPES = frozenset({"townhall", "keep", "castle"})
POLICY_TYPES = frozenset(
    {
        "rmg_policy_tradition",
        "rmg_policy_commerce",
        "rmg_policy_diplomacy",
    }
)
STRATEGIC_RESEARCH_TYPES = (
    "rmg_urban_planning",
    "rmg_civic_administration",
    "rmg_foreign_service",
    "rmg_policy_tradition",
    "rmg_policy_commerce",
    "rmg_policy_diplomacy",
)
# Backward-compatible aliases for tests and external imports.
POLICY_SLOT_LIMIT = 2
DIPLOMACY_REQUEST_COST = 20
TILE_PURCHASE_BASE_COST = 20
TILE_PURCHASE_STEP_COST = 10
TILE_FOCUSES = frozenset({"gold", "wood", "food", "culture"})
TILE_IMPROVEMENTS = frozenset(rmg_rules.improvement_entity_types())
TRADING_POST_GOLD_YIELD = 2
TRADING_POST_DIPLOMACY_YIELD = 2
TRADE_WOOD_GOLD_COST = 50
TRADE_WOOD_AMOUNT = 100
TRADE_FOOD_GOLD_COST = 50
TRADE_FOOD_AMOUNT = 100
OPEN_BORDERS_DIPLOMACY_COST = 15
OPEN_BORDERS_GOLD_COST = 30
TRADE_COOLDOWN_MS = 60000
RMG_TERRITORY_MARKER_TYPE = "rmg_territory_marker"


def initialize_player(player) -> None:
    """Initialize strategic state lazily for old saves and non-RMG tests."""
    if not hasattr(player, "culture_points"):
        player.culture_points = 0
    if not hasattr(player, "diplomacy_points"):
        player.diplomacy_points = 0
    if not hasattr(player, "rmg_city_yield_ticks"):
        player.rmg_city_yield_ticks = 0
    if not hasattr(player, "rmg_claimed_tiles"):
        player.rmg_claimed_tiles = {}
    if not hasattr(player, "rmg_worked_tiles"):
        player.rmg_worked_tiles = {}
    if not hasattr(player, "rmg_tile_workers"):
        player.rmg_tile_workers = {}
    if not hasattr(player, "rmg_worker_auto_gather"):
        player.rmg_worker_auto_gather = {}
    if not hasattr(player, "rmg_assignment_order"):
        player.rmg_assignment_order = []
    if not hasattr(player, "rmg_tile_improvements"):
        player.rmg_tile_improvements = {}
    if not hasattr(player, "rmg_territory_markers"):
        player.rmg_territory_markers = {}
    if not hasattr(player, "rmg_improvement_units"):
        player.rmg_improvement_units = {}
    if not hasattr(player, "rmg_unlocked_policies"):
        player.rmg_unlocked_policies = set()
    if not hasattr(player, "rmg_policy_slots"):
        player.rmg_policy_slots = []


def is_city(unit) -> bool:
    if getattr(unit, "type_name", None) in CITY_TYPES:
        return True
    inherited = getattr(unit, "expanded_is_a", ()) or ()
    if any(name in CITY_TYPES for name in inherited):
        return True
    # Rules-driven fallback for mods (command center, nexus, hatchery, ...).
    return bool(
        getattr(unit, "provides_survival", False)
        and getattr(unit, "storable_resource_types", ())
    )


def cities(player) -> list:
    """Return completed, living city centres controlled by *player*."""
    return [
        unit
        for unit in getattr(player, "units", ())
        if is_city(unit)
        and getattr(unit, "place", None) is not None
        and getattr(unit, "hp", 1) > 0
    ]


def square_for(obj):
    """Resolve a unit, meadow, exit target, or square to its main map square."""
    if obj is None:
        return None
    world = getattr(obj, "world", None)
    squares = getattr(world, "squares", ()) if world is not None else ()
    current = obj
    seen = set()
    while current is not None and id(current) not in seen:
        seen.add(id(current))
        if current in squares:
            return current
        current = getattr(current, "place", None)
    return None


def _square_by_name(world, name):
    for square in getattr(world, "squares", ()) or ():
        if getattr(square, "name", None) == name:
            return square
    return None


def _adjacent_squares(square) -> list:
    result = []
    for exit_obj in getattr(square, "exits", ()) or ():
        other_side = getattr(exit_obj, "other_side", None)
        destination = getattr(other_side, "place", None)
        if destination is not None and destination not in result:
            result.append(destination)
    return result


def tile_owner(world, square_or_name):
    """Return the player owning a strategic tile, if any."""
    name = (
        square_or_name
        if isinstance(square_or_name, str)
        else getattr(square_or_name, "name", None)
    )
    if not name:
        return None
    for player in getattr(world, "players", ()) or ():
        initialize_player(player)
        if name in player.rmg_claimed_tiles:
            return player
    return None


def refresh_territory(player) -> None:
    """Claim every city centre and discard state for tiles no longer owned."""
    initialize_player(player)
    world = getattr(player, "world", None)
    if world is None:
        return
    valid_city_ids = {getattr(city, "id", None) for city in cities(player)}
    for city in cities(player):
        square = square_for(city)
        if square is None:
            continue
        owner = tile_owner(world, square)
        if owner in (None, player):
            player.rmg_claimed_tiles[square.name] = getattr(city, "id", None)
    stale = [
        name
        for name, city_id in player.rmg_claimed_tiles.items()
        if city_id not in valid_city_ids or _square_by_name(world, name) is None
    ]
    for name in stale:
        player.rmg_claimed_tiles.pop(name, None)
        _release_tile_worker(player, name)
        _remove_tracked_entity(player, player.rmg_territory_markers, name)
        _remove_tracked_entity(player, player.rmg_improvement_units, name)
        player.rmg_tile_improvements.pop(name, None)
        clear_rmg_construction_sites(player, name)
    player.rmg_assignment_order = [
        name
        for name in player.rmg_assignment_order
        if name in player.rmg_worked_tiles
    ]
    _reconcile_workers(player)
    _sync_territory_entities(player)


def tile_purchase_cost(player) -> int:
    initialize_player(player)
    purchased = max(0, len(player.rmg_claimed_tiles) - len(cities(player)))
    return rmg_rules.tile_purchase_base_cost() + purchased * rmg_rules.tile_purchase_step_cost()


def _improvement_entity_map():
    return rmg_rules.improvement_entity_types()


def _spawn_improvement_entity(player, improvement_key: str, square):
    type_name = _improvement_entity_map().get(improvement_key)
    if type_name is None:
        return None
    return _spawn_rmg_entity(player, type_name, square)


def _entity_by_id(player, entity_id):
    if entity_id is None:
        return None
    getter = getattr(player, "get_object_by_id", None)
    if callable(getter):
        try:
            entity = getter(entity_id)
            if entity is not None:
                return entity
        except Exception:
            pass
    for entity in getattr(player, "units", ()) or ():
        if getattr(entity, "id", None) == entity_id:
            return entity
    return None


def _remove_tracked_entity(player, registry, square_name) -> None:
    entity_id = registry.pop(square_name, None)
    entity = _entity_by_id(player, entity_id)
    if entity is not None and getattr(entity, "place", None) is not None:
        entity.delete()


def _spawn_rmg_entity(player, type_name: str, square):
    """Spawn a completed, zero-cost RMG map entity and return it."""
    add_unit = getattr(player, "add_unit", None)
    if not callable(add_unit):
        return None
    from .definitions import rules

    entity_type = rules.unit_class(type_name)
    if entity_type is None:
        return None
    before = {getattr(unit, "id", None) for unit in getattr(player, "units", ())}
    try:
        add_unit(entity_type, square)
    except Exception:
        return None
    spawned = [
        unit
        for unit in getattr(player, "units", ())
        if getattr(unit, "id", None) not in before
        and getattr(unit, "type_name", None) == type_name
    ]
    if not spawned:
        return None
    entity = max(spawned, key=lambda unit: getattr(unit, "id", 0))
    entity.rmg_tile_square_name = getattr(square, "name", None)
    return entity


def _sync_territory_entities(player) -> None:
    """Keep territory markers and improvement buildings in sync with state."""
    world = getattr(player, "world", None)
    if world is None or not getattr(world, "rmg_strategic_systems", False):
        return

    claimed = set(player.rmg_claimed_tiles)
    for name in list(player.rmg_territory_markers):
        marker = _entity_by_id(player, player.rmg_territory_markers[name])
        if name not in claimed:
            _remove_tracked_entity(player, player.rmg_territory_markers, name)
        elif marker is None or getattr(marker, "place", None) is None:
            player.rmg_territory_markers.pop(name, None)
    for name in claimed:
        if name in player.rmg_territory_markers:
            continue
        square = _square_by_name(world, name)
        marker = _spawn_rmg_entity(player, RMG_TERRITORY_MARKER_TYPE, square)
        if marker is not None:
            player.rmg_territory_markers[name] = marker.id

    for name, entity_id in list(player.rmg_improvement_units.items()):
        entity = _entity_by_id(player, entity_id)
        if name not in player.rmg_tile_improvements:
            _remove_tracked_entity(player, player.rmg_improvement_units, name)
        elif entity is None or getattr(entity, "place", None) is None:
            # A destroyed improvement stops producing and does not respawn.
            player.rmg_improvement_units.pop(name, None)
            player.rmg_tile_improvements.pop(name, None)

    # Old saves have abstract improvement state but no entity registry.
    for name, improvement in list(player.rmg_tile_improvements.items()):
        if name in player.rmg_improvement_units or name not in claimed:
            continue
        square = _square_by_name(world, name)
        entity = _spawn_rmg_entity(
            player, _improvement_entity_map()[improvement], square
        )
        if entity is not None:
            entity.rmg_improvement = improvement
            player.rmg_improvement_units[name] = entity.id


def is_claimed_square(player, square) -> bool:
    if square is None:
        return False
    initialize_player(player)
    name = getattr(square, "name", None)
    return bool(name and name in player.rmg_claimed_tiles)


def claimed_squares(player) -> list:
    """Return main-map squares owned by *player* in RMG strategic mode."""
    world = getattr(player, "world", None)
    if world is None or not getattr(world, "rmg_strategic_systems", False):
        return []
    initialize_player(player)
    squares = []
    for name in player.rmg_claimed_tiles:
        square = _square_by_name(world, name)
        if square is not None:
            squares.append(square)
    return squares


def apply_territory_vision(player) -> None:
    """Owned RMG tiles stay fully visible to their owner."""
    squares = claimed_squares(player)
    if not squares:
        return
    observed = getattr(player, "observed_squares", None)
    if observed is None:
        player.observed_squares = set()
        observed = player.observed_squares
    before = getattr(player, "observed_before_squares", None)
    if before is None:
        player.observed_before_squares = set()
        before = player.observed_before_squares
    strict_before = getattr(player, "strictly_observed_before_squares", None)
    if strict_before is None:
        player.strictly_observed_before_squares = set()
        strict_before = player.strictly_observed_before_squares
    cover = getattr(player, "_vision_cover_counts", None)
    if cover is None:
        player._vision_cover_counts = {}
        cover = player._vision_cover_counts
    for square in squares:
        observed.add(square)
        before.add(square)
        strict_before.add(square)
        if cover.get(square, 0) <= 0:
            cover[square] = 1


def menu_resource_cost(keyword: str, unit) -> tuple:
    """Return internal resource costs for RMG city command menu display."""
    from .definitions import MAX_NB_OF_RESOURCE_TYPES

    zero = (0,) * MAX_NB_OF_RESOURCE_TYPES
    if keyword == "rmg_buy_tile":
        player = getattr(unit, "player", None)
        gold = tile_purchase_cost(player) if player is not None else rmg_rules.tile_purchase_base_cost()
        costs = list(zero)
        costs[0] = to_int(str(gold))
        return tuple(costs)
    improvement = rmg_rules.build_order_improvements().get(keyword)
    if improvement is not None:
        return rmg_rules.improvement_menu_cost(improvement, len(zero))
    return zero


def _pay_visible_resources(player, visible_costs) -> bool:
    resources = getattr(player, "resources", ())
    internal = [to_int(str(max(0, amount))) for amount in visible_costs]
    if any(index >= len(resources) or resources[index] < amount for index, amount in enumerate(internal)):
        return False
    for index, amount in enumerate(internal):
        resources[index] -= amount
    return True


def buy_tile(player, city, target) -> bool:
    """Buy an unowned tile adjacent to this city's existing territory."""
    initialize_player(player)
    refresh_territory(player)
    target_square = square_for(target)
    city_square = square_for(city)
    world = getattr(player, "world", None)
    city_id = getattr(city, "id", None)
    if target_square is None or city_square is None or world is None:
        return False
    if tile_owner(world, target_square) is not None:
        return False
    city_tiles = {
        name for name, owner_city_id in player.rmg_claimed_tiles.items()
        if owner_city_id == city_id
    }
    adjacent_names = {
        getattr(adjacent, "name", None)
        for name in city_tiles
        for adjacent in _adjacent_squares(_square_by_name(world, name))
    }
    if target_square.name not in adjacent_names:
        return False
    if not _pay_visible_resources(player, (tile_purchase_cost(player), 0, 0)):
        return False
    player.rmg_claimed_tiles[target_square.name] = city_id
    apply_territory_vision(player)
    _sync_territory_entities(player)
    return True


def citizen_slots(player, city) -> int:
    upgrades = set(getattr(player, "upgrades", ()) or ())
    slots = 1
    if "rmg_urban_planning" in upgrades:
        slots += 1
    if "rmg_civic_administration" in upgrades:
        slots += 1
    if getattr(city, "type_name", "") in {"keep", "castle"}:
        slots += 1
    return slots


def _is_worker(unit) -> bool:
    """True for peasants / workers, including client EntityView proxies.

    Order menus run on client EntityView objects, which are not ``Worker``
    instances. Unwrap ``.model`` and also accept ``class worker`` / flag.
    """
    if unit is None:
        return False
    model = getattr(unit, "model", None)
    if model is not None and model is not unit:
        unit = model
    if bool(getattr(unit, "is_rmg_worker", False)):
        return True
    try:
        from .worldunit.worldworker import Worker

        if isinstance(unit, Worker):
            return True
    except Exception:
        pass
    classes = getattr(unit, "class", None) or ()
    if isinstance(classes, str):
        classes = (classes,)
    return "worker" in classes


def _release_tile_worker(player, square_name: str) -> None:
    worker_id = player.rmg_tile_workers.pop(square_name, None)
    player.rmg_worked_tiles.pop(square_name, None)
    if square_name in player.rmg_assignment_order:
        player.rmg_assignment_order.remove(square_name)
    worker = _entity_by_id(player, worker_id)
    if worker is not None:
        previous = player.rmg_worker_auto_gather.pop(worker_id, None)
        if previous is not None:
            worker.auto_gather = previous


def _reconcile_workers(player) -> None:
    for square_name, worker_id in list(player.rmg_tile_workers.items()):
        worker = _entity_by_id(player, worker_id)
        if (
            worker is None
            or getattr(worker, "place", None) is None
            or getattr(worker, "hp", 1) <= 0
            or not _is_worker(worker)
        ):
            _release_tile_worker(player, square_name)


def _available_worker(player, square, current_worker_id=None):
    assigned = set(player.rmg_tile_workers.values())
    candidates = []
    for worker in getattr(player, "units", ()) or ():
        worker_id = getattr(worker, "id", None)
        if (
            not _is_worker(worker)
            or getattr(worker, "place", None) is None
            or getattr(worker, "hp", 1) <= 0
            or (worker_id in assigned and worker_id != current_worker_id)
            or (
                bool(getattr(worker, "orders", ()))
                and worker_id != current_worker_id
            )
        ):
            continue
        candidates.append(worker)
    if not candidates:
        return None
    return min(
        candidates,
        key=lambda worker: (
            square_for(worker) is not square,
            bool(getattr(worker, "orders", ())),
            getattr(worker, "id", 0),
        ),
    )


def assign_citizen(player, city, target, focus: str) -> bool:
    """Dispatch a real worker to an owned tile and assign its specialization."""
    if focus not in TILE_FOCUSES:
        return False
    initialize_player(player)
    refresh_territory(player)
    square = square_for(target)
    city_id = getattr(city, "id", None)
    if square is None or player.rmg_claimed_tiles.get(square.name) != city_id:
        return False
    current = [
        name for name in player.rmg_assignment_order
        if player.rmg_claimed_tiles.get(name) == city_id
        and name in player.rmg_worked_tiles
    ]
    existing_worker_id = player.rmg_tile_workers.get(square.name)
    worker = _available_worker(player, square, existing_worker_id)
    if worker is None:
        return False
    if square.name in current:
        player.rmg_assignment_order.remove(square.name)
    elif len(current) >= citizen_slots(player, city):
        evicted = current[0]
        _release_tile_worker(player, evicted)
    if existing_worker_id is not None and existing_worker_id != worker.id:
        _release_tile_worker(player, square.name)
    player.rmg_worked_tiles[square.name] = focus
    player.rmg_tile_workers[square.name] = worker.id
    player.rmg_assignment_order.append(square.name)
    if worker.id not in player.rmg_worker_auto_gather:
        player.rmg_worker_auto_gather[worker.id] = bool(
            getattr(worker, "auto_gather", False)
        )
    worker.auto_gather = False
    if square_for(worker) is not square:
        target_id = getattr(square, "id", None)
        if target_id is None:
            _release_tile_worker(player, square.name)
            return False
        worker.take_order(["go", target_id])
    return True


def improve_tile(player, city, target, improvement: str) -> bool:
    """Deprecated city instant-build path; improvements now use peasant BuildOrder."""
    return False


def is_rmg_improvement_type(type_name_or_cls) -> bool:
    if type_name_or_cls is None:
        return False
    if isinstance(type_name_or_cls, str):
        return type_name_or_cls in rmg_rules.improvement_type_names()
    name = getattr(type_name_or_cls, "type_name", None) or getattr(
        type_name_or_cls, "__name__", None
    )
    return name in rmg_rules.improvement_type_names()


def improvement_for_entity_type(type_name: str):
    return rmg_rules.improvement_for_entity_type(type_name)


def assigned_square_name_for_worker(player, worker):
    initialize_player(player)
    worker_id = getattr(worker, "id", None)
    if worker_id is None:
        return None
    for square_name, assigned_id in player.rmg_tile_workers.items():
        if assigned_id == worker_id:
            return square_name
    return None


def _is_rmg_building_site(unit) -> bool:
    if getattr(unit, "type_name", None) != "buildingsite":
        return False
    site_type = getattr(unit, "type", None)
    return is_rmg_improvement_type(site_type)


def rmg_construction_sites_on_square(player, square) -> list:
    if square is None:
        return []
    result = []
    for unit in getattr(player, "units", ()) or ():
        if not _is_rmg_building_site(unit):
            continue
        if square_for(unit) is square:
            result.append(unit)
    return result


def has_rmg_construction_on_square(player, square) -> bool:
    return bool(rmg_construction_sites_on_square(player, square))


def clear_rmg_construction_sites(player, square_name: str) -> None:
    """Remove unfinished RMG building sites when a tile is lost."""
    world = getattr(player, "world", None)
    square = _square_by_name(world, square_name) if world is not None else None
    if square is None:
        return
    for site in list(rmg_construction_sites_on_square(player, square)):
        try:
            site.delete()
        except Exception:
            pass


def worker_can_start_rmg_improvement(worker, type_name=None) -> bool:
    """True when a peasant may see RMG improvement builds (classic RTS menu)."""
    player = getattr(worker, "player", None)
    world = getattr(worker, "world", None) or getattr(player, "world", None)
    if player is None or not getattr(world, "rmg_strategic_systems", False):
        return False
    if not _is_worker(worker):
        return False
    if type_name is not None and not is_rmg_improvement_type(type_name):
        return False
    return True


def validate_rmg_build_target(worker, type_name, target):
    """Return an impossibility reason, or None when the RMG build target is valid.

    Target must be an owned claimed tile without a finished improvement or site.
    The peasant does not need a prior city assignment and may still be en route.
    """
    player = getattr(worker, "player", None)
    world = getattr(worker, "world", None) or getattr(player, "world", None)
    if player is None or not getattr(world, "rmg_strategic_systems", False):
        return "cannot_build_here"
    if not is_rmg_improvement_type(type_name):
        return "cannot_build_here"
    if not _is_worker(worker):
        return "cannot_build_here"
    initialize_player(player)
    square = square_for(target)
    if square is None and hasattr(target, "find_free_space_for"):
        square = target
    if square is None:
        return "cannot_build_here"
    if player.rmg_claimed_tiles.get(getattr(square, "name", None)) is None:
        return "cannot_build_here"
    if square.name in player.rmg_tile_improvements:
        return "cannot_build_here"
    if has_rmg_construction_on_square(player, square):
        return "cannot_build_here"
    return None


def _default_focus_for_improvement(improvement: str) -> str:
    return rmg_rules.default_work_focus_for_improvement(improvement)


def _ensure_builder_works_completed_tile(player, building, square) -> None:
    """If the tile has no stationed worker, bind a peasant already on the square."""
    name = getattr(square, "name", None)
    if not name:
        return
    existing = _entity_by_id(player, player.rmg_tile_workers.get(name))
    if (
        existing is not None
        and getattr(existing, "place", None) is not None
        and getattr(existing, "hp", 1) > 0
        and square_for(existing) is square
    ):
        return
    builder = None
    for unit in getattr(player, "units", ()) or ():
        if not _is_worker(unit):
            continue
        if square_for(unit) is not square:
            continue
        if getattr(unit, "hp", 1) <= 0:
            continue
        builder = unit
        break
    if builder is None:
        return
    improvement = getattr(building, "rmg_improvement", None) or player.rmg_tile_improvements.get(
        name
    )
    focus = player.rmg_worked_tiles.get(name) or _default_focus_for_improvement(
        improvement or "mine"
    )
    previous = player.rmg_tile_workers.get(name)
    if previous is not None and previous != builder.id:
        _release_tile_worker(player, name)
    player.rmg_worked_tiles[name] = focus
    player.rmg_tile_workers[name] = builder.id
    if name in player.rmg_assignment_order:
        player.rmg_assignment_order.remove(name)
    player.rmg_assignment_order.append(name)
    if builder.id not in player.rmg_worker_auto_gather:
        player.rmg_worker_auto_gather[builder.id] = bool(
            getattr(builder, "auto_gather", False)
        )
    builder.auto_gather = False


def register_completed_rmg_improvement(building) -> bool:
    """Register a finished RMG tile improvement and announce success."""
    type_name = getattr(building, "type_name", None)
    improvement = improvement_for_entity_type(type_name)
    if improvement is None:
        return False
    player = getattr(building, "player", None)
    if player is None:
        return False
    initialize_player(player)
    square = square_for(building)
    if square is None or square.name not in player.rmg_claimed_tiles:
        return False
    building.rmg_improvement = improvement
    building.rmg_tile_square_name = square.name
    player.rmg_tile_improvements[square.name] = improvement
    player.rmg_improvement_units[square.name] = getattr(building, "id", None)
    _ensure_builder_works_completed_tile(player, building, square)
    keyword = rmg_rules.build_keyword_for_improvement(improvement)
    announce_strategic_order_success(player, keyword, type_name=type_name)
    return True


RMG_ORDER_SUCCESS_MESSAGES = {
    "rmg_buy_tile": "RMG_TILE_PURCHASED",
    "rmg_assign_gold": "RMG_CITIZEN_ASSIGNED",
    "rmg_assign_wood": "RMG_CITIZEN_ASSIGNED",
    "rmg_assign_food": "RMG_CITIZEN_ASSIGNED",
    "rmg_assign_culture": "RMG_CITIZEN_ASSIGNED",
    "rmg_build_mine": "RMG_MINE_BUILT",
    "rmg_build_lumber_mill": "RMG_LUMBER_MILL_BUILT",
    "rmg_build_farm": "RMG_FARM_BUILT",
    "rmg_build_trading_post": "RMG_TRADING_POST_BUILT",
}
RMG_ORDERS_WITH_YIELD_HINT = frozenset(
    {
        "rmg_buy_tile",
        "rmg_assign_gold",
        "rmg_assign_wood",
        "rmg_assign_food",
        "rmg_assign_culture",
    }
)


def announce_strategic_order_success(player, keyword: str, type_name=None) -> None:
    """Tell the local human player that an abstract RMG tile action succeeded."""
    if not getattr(player, "is_local_human", lambda: False)():
        return
    from . import msgparts as mp
    from .definitions import rules, style

    message_name = RMG_ORDER_SUCCESS_MESSAGES.get(keyword)
    if message_name is not None:
        msg = list(getattr(mp, message_name, []))
    elif type_name:
        title = style.get("parameters", type_name, warn_if_not_found=False)
        if not title:
            cls = rules.unit_class(type_name)
            title = style.get("parameters", getattr(cls, "type_name", type_name), warn_if_not_found=False)
        msg = list(title) if title else []
    else:
        return
    if not msg:
        return
    if keyword in RMG_ORDERS_WITH_YIELD_HINT:
        msg += mp.COMMA + mp.RMG_YIELD_EVERY_MINUTE
    player.send_voice_important(msg)


def format_yield_announcement(summary: dict) -> list:
    """Build a voice message for one strategic tick's visible gains."""
    from . import msgparts as mp
    from .definitions import style
    from .lib.msgs import nb2msg

    msg = mp.RMG_CITY_YIELD + mp.COMMA
    resources = summary.get("resources", ())
    and_index = len(msg)
    for index, amount in enumerate(resources):
        if amount <= 0:
            continue
        if len(msg) > and_index + 1:
            msg += style.get("parameters", "and")
        resource_title = style.get("parameters", f"resource{index + 1}_title")
        if resource_title:
            msg += nb2msg(int(amount)) + resource_title
    culture = int(summary.get("culture", 0) or 0)
    if culture > 0:
        if len(msg) > and_index + 1:
            msg += style.get("parameters", "and")
        msg += nb2msg(culture) + mp.RMG_CULTURE
    diplomacy = int(summary.get("diplomacy", 0) or 0)
    if diplomacy > 0:
        if len(msg) > and_index + 1:
            msg += style.get("parameters", "and")
        msg += nb2msg(diplomacy) + mp.RMG_DIPLOMACY_POINTS
    return msg


def _terrain_name(city) -> str:
    place = getattr(city, "place", None)
    if place is None:
        return ""
    # Buildings can temporarily expose their own ``square_terrain`` (town),
    # while RMG yield must use the underlying generated map tile.
    world = getattr(city, "world", None)
    map_terrain = getattr(world, "terrain", None)
    place_name = getattr(place, "name", None)
    if isinstance(map_terrain, dict) and place_name in map_terrain:
        return map_terrain[place_name] or ""
    try:
        from .lib.square_terrain_rules import terrain_name_at_square

        return terrain_name_at_square(
            place, getattr(city, "x", None), getattr(city, "y", None)
        ) or ""
    except Exception:
        return getattr(place, "terrain_name", "") or ""


def tile_yield_for_city(city) -> Tuple[int, int, int]:
    """Visible gold/wood/food produced by one city each strategic tick."""
    result = [6, 4, 4]
    terrain = _terrain_name(city)
    if terrain in {"hill", "plateau", "high_rocky_plain", "mountain_pass"}:
        result[0] += 3
    elif terrain in {"forest", "dense_forest", "marsh"}:
        result[1] += 3
    elif terrain in {"plain", "town", "meadows"}:
        result[2] += 3
    elif terrain in {"lake", "river", "creek", "ford"}:
        result[0] += 1
        result[2] += 2
    return tuple(result)


def _is_policy_type(type_name: str) -> bool:
    if type_name in POLICY_TYPES:
        return True
    try:
        from .definitions import rules

        policy_type = rules.unit_class(type_name)
        return bool(getattr(policy_type, "rmg_policy", 0))
    except Exception:
        return False


def active_policies(player) -> set[str]:
    initialize_player(player)
    legacy = [
        name
        for name in (getattr(player, "upgrades", ()) or ())
        if _is_policy_type(name)
    ]
    for name in legacy:
        if name not in player.rmg_unlocked_policies:
            player.rmg_unlocked_policies.add(name)
        if name not in player.rmg_policy_slots and len(player.rmg_policy_slots) < rmg_rules.policy_slot_limit():
            player.rmg_policy_slots.append(name)
    return set(player.rmg_policy_slots)


def pending_policies(player) -> set[str]:
    result: set[str] = set()
    for unit in getattr(player, "units", ()) or ():
        for order in getattr(unit, "orders", ()) or ():
            policy_type = getattr(order, "type", None)
            name = getattr(policy_type, "type_name", None)
            if name and _is_policy_type(name):
                result.add(name)
    return result


def can_adopt_policy(player, policy_name: str) -> bool:
    if not _is_policy_type(policy_name):
        return True
    initialize_player(player)
    active_policies(player)
    # A newly completed policy replaces the oldest active slot.  Known inactive
    # policies can later be switched back without paying their culture cost again.
    return policy_name not in pending_policies(player)


def activate_policy(player, policy_name: str) -> bool:
    """Unlock and activate a policy, replacing the oldest occupied slot."""
    if not _is_policy_type(policy_name):
        return False
    initialize_player(player)
    player.rmg_unlocked_policies.add(policy_name)
    if policy_name in player.rmg_policy_slots:
        return True
    if len(player.rmg_policy_slots) >= rmg_rules.policy_slot_limit():
        removed = player.rmg_policy_slots.pop(0)
        while removed in getattr(player, "upgrades", ()):
            player.upgrades.remove(removed)
    player.rmg_policy_slots.append(policy_name)
    if policy_name not in getattr(player, "upgrades", ()):
        player.upgrades.append(policy_name)
    return True


def switch_policy(player, policy_name: str) -> bool:
    initialize_player(player)
    if policy_name not in player.rmg_unlocked_policies:
        return False
    return activate_policy(player, policy_name)


def _sum_yields(city_units: Iterable) -> list[int]:
    result = [0, 0, 0]
    for city in city_units:
        for index, amount in enumerate(tile_yield_for_city(city)):
            result[index] += amount
    return result


def _terrain_name_for_square(world, square) -> str:
    terrain = getattr(world, "terrain", None)
    name = getattr(square, "name", None)
    if isinstance(terrain, dict) and name in terrain:
        return terrain[name] or ""
    return getattr(square, "terrain_name", "") or ""


def worked_tile_yield(player, square_name: str) -> Tuple[int, int, int, int]:
    """Gold, wood, food and culture from one on-site worker."""
    world = getattr(player, "world", None)
    square = _square_by_name(world, square_name) if world is not None else None
    terrain = _terrain_name_for_square(world, square) if square is not None else ""
    result = [1, 1, 1, 0]
    if terrain in {"hill", "plateau", "high_rocky_plain", "mountain_pass"}:
        result[0] += 2
    elif terrain in {"forest", "dense_forest", "marsh"}:
        result[1] += 2
    elif terrain in {"plain", "town", "meadows"}:
        result[2] += 2
    elif terrain in {"lake", "river", "creek", "ford"}:
        result[0] += 1
        result[2] += 1
    focus = player.rmg_worked_tiles.get(square_name)
    if focus == "gold":
        result[0] += 2
    elif focus == "wood":
        result[1] += 2
    elif focus == "food":
        result[2] += 2
    elif focus == "culture":
        result[3] += 3
    improvement = player.rmg_tile_improvements.get(square_name)
    if improvement:
        bonus = rmg_rules.improvement_yield_bonus(improvement)
        for index in range(4):
            result[index] += bonus[index]
    return tuple(result)


def tile_improvement_diplomacy_yield(player, square_name: str) -> int:
    """Extra diplomacy from a worked tile improvement (rules-driven)."""
    improvement = player.rmg_tile_improvements.get(square_name)
    if not improvement:
        return 0
    worker = _entity_by_id(player, player.rmg_tile_workers.get(square_name))
    square = _square_by_name(getattr(player, "world", None), square_name)
    if (
        worker is None
        or getattr(worker, "place", None) is None
        or getattr(worker, "hp", 1) <= 0
        or square_for(worker) is not square
    ):
        return 0
    bonus = rmg_rules.improvement_yield_bonus(improvement)
    return bonus[4] if len(bonus) > 4 else 0


def strategic_tick(player) -> dict:
    """Apply one minute of city yields and return a deterministic summary."""
    initialize_player(player)
    refresh_territory(player)
    city_units = cities(player)
    if not city_units:
        return {
            "cities": 0,
            "resources": (0, 0, 0),
            "culture": 0,
            "diplomacy": 0,
        }

    upgrades = set(getattr(player, "upgrades", ()) or ())
    yields = _sum_yields(city_units)
    culture = len(city_units) * 4
    diplomacy = max(1, len(city_units))
    for square_name in list(player.rmg_worked_tiles):
        if square_name not in player.rmg_claimed_tiles:
            continue
        worker = _entity_by_id(
            player, player.rmg_tile_workers.get(square_name)
        )
        square = _square_by_name(getattr(player, "world", None), square_name)
        if (
            worker is None
            or getattr(worker, "place", None) is None
            or getattr(worker, "hp", 1) <= 0
            or square_for(worker) is not square
        ):
            continue
        tile_yield = worked_tile_yield(player, square_name)
        for index in range(3):
            yields[index] += tile_yield[index]
        culture += tile_yield[3]
        diplomacy += tile_improvement_diplomacy_yield(player, square_name)

    if "rmg_urban_planning" in upgrades:
        yields = [amount + len(city_units) * 2 for amount in yields]
    if "rmg_civic_administration" in upgrades:
        culture += len(city_units) * 2
    if "rmg_foreign_service" in upgrades:
        diplomacy += len(city_units)

    policies = active_policies(player)
    if "rmg_policy_commerce" in policies:
        yields = [(amount * 125) // 100 for amount in yields]
    if "rmg_policy_tradition" in policies:
        culture = (culture * 150) // 100
    if "rmg_policy_diplomacy" in policies:
        diplomacy *= 2

    resources = getattr(player, "resources", ())
    for index, visible_amount in enumerate(yields):
        if index >= len(resources):
            break
        amount = to_int(str(visible_amount))
        resources[index] += amount
        stats = getattr(player, "stats", None)
        if stats is not None and hasattr(stats, "add"):
            stats.add("gathered", index, amount)

    player.culture_points += culture
    player.diplomacy_points += diplomacy
    player.rmg_city_yield_ticks += 1
    return {
        "cities": len(city_units),
        "resources": tuple(yields),
        "culture": culture,
        "diplomacy": diplomacy,
    }


def spend_diplomacy(player, amount: int | None = None) -> bool:
    initialize_player(player)
    if amount is None:
        amount = rmg_rules.diplomacy_request_cost()
    amount = max(0, int(amount))
    if player.diplomacy_points < amount:
        return False
    player.diplomacy_points -= amount
    return True


def alliance_request_cost(player) -> int:
    """Diplomacy points charged to send an alliance request, or 0 if free."""
    world = getattr(player, "world", None)
    if not getattr(world, "rmg_strategic_systems", False):
        return 0
    if not cities(player):
        return 0
    return rmg_rules.diplomacy_request_cost()


def diplomacy_cost_msg(amount: int):
    """Voice/menu fragments for a diplomacy-point cost."""
    from . import msgparts as mp
    from .definitions import style
    from .lib.msgs import nb2msg

    amount = max(0, int(amount))
    if amount <= 0:
        return []
    return style.get("parameters", "requires") + nb2msg(amount) + mp.RMG_DIPLOMACY_POINTS


def ai_policy_plan(player) -> tuple[str, ...]:
    """Return a deterministic policy combination tailored to this AI."""
    ai_type = str(getattr(player, "AI_type", "") or "").lower()
    if any(word in ai_type for word in ("aggressive", "rush", "hard")):
        return ("rmg_policy_commerce", "rmg_policy_tradition")
    enemies = getattr(player, "true_enemies", None)
    if enemies is None:
        checker = getattr(player, "player_is_an_enemy", None)
        enemies = [
            other
            for other in getattr(getattr(player, "world", None), "players", ()) or ()
            if other is not player
            and not getattr(other, "neutral", False)
            and (not callable(checker) or checker(other))
        ]
    enemy_count = len(enemies)
    if enemy_count >= 2:
        return ("rmg_policy_diplomacy", "rmg_policy_commerce")
    return ("rmg_policy_tradition", "rmg_policy_commerce")


def ai_research_priority(player, available: Iterable[str]) -> list[str]:
    plan = ai_policy_plan(player)
    available = [
        name
        for name in available
        if not _is_policy_type(name) or name in plan
    ]
    strategic_order = ["rmg_urban_planning"]
    if "rmg_policy_tradition" in plan:
        strategic_order.append("rmg_policy_tradition")
    strategic_order.append("rmg_civic_administration")
    if "rmg_policy_commerce" in plan:
        strategic_order.append("rmg_policy_commerce")
    strategic_order.append("rmg_foreign_service")
    if "rmg_policy_diplomacy" in plan:
        strategic_order.append("rmg_policy_diplomacy")
    rank = {name: index for index, name in enumerate(strategic_order)}
    return sorted(available, key=lambda name: (rank.get(name, len(rank)), available.index(name)))


def _trade_cooldown_key(target_id, trade_kind: str) -> str:
    return f"{trade_kind}:{target_id}"


def _trade_on_cooldown(player, target_id, trade_kind: str, trade_cls) -> bool:
    cooldowns = getattr(player, "_rmg_trade_cooldowns", None)
    if not isinstance(cooldowns, dict):
        return False
    last = cooldowns.get(_trade_cooldown_key(target_id, trade_kind), -10**9)
    world = getattr(player, "world", None)
    now = getattr(world, "time", 0) if world is not None else 0
    return now - last < rmg_rules.trade_cooldown_ms(trade_cls)


def _mark_trade_cooldown(player, target_id, trade_kind: str) -> None:
    cooldowns = getattr(player, "_rmg_trade_cooldowns", None)
    if not isinstance(cooldowns, dict):
        cooldowns = {}
        player._rmg_trade_cooldowns = cooldowns
    world = getattr(player, "world", None)
    cooldowns[_trade_cooldown_key(target_id, trade_kind)] = getattr(
        world, "time", 0
    )


def _player_is_trade_target_ok(buyer, target) -> bool:
    if target is None or target is buyer:
        return False
    if getattr(target, "neutral", False):
        return False
    if getattr(target, "is_human", False):
        return False
    checker = getattr(buyer, "player_is_an_enemy", None)
    if callable(checker) and checker(target):
        return False
    try:
        if target in getattr(buyer, "allied", []):
            return True
    except Exception:
        pass
    return True


def _transfer_visible_resources(from_player, to_player, gold=0, wood=0, food=0) -> bool:
    from_resources = getattr(from_player, "resources", ())
    to_resources = getattr(to_player, "resources", ())
    amounts = [gold, wood, food]
    internal = [to_int(str(max(0, amount))) for amount in amounts]
    if any(index >= len(from_resources) or from_resources[index] < amount for index, amount in enumerate(internal)):
        return False
    for index, amount in enumerate(internal):
        if amount <= 0:
            continue
        from_resources[index] -= amount
        if index < len(to_resources):
            to_resources[index] += amount
    return True


def _form_alliance_between(a, b) -> None:
    """Align alliance ids for *a* and *b* using the same rules as accept."""
    aid_self = getattr(a.client, "alliance", None)
    aid_t = getattr(b.client, "alliance", None)
    affected_before = {aid_self, aid_t}
    _UNSET = (None, "None", "ai")
    if aid_self in _UNSET and aid_t in _UNSET:
        used = {getattr(p.client, "alliance", None) for p in a.world.players}
        new_id = 1
        while new_id in used:
            new_id += 1
        a.client.alliance = new_id
        b.client.alliance = new_id
    elif aid_self in _UNSET:
        a.client.alliance = aid_t
    elif aid_t in _UNSET:
        b.client.alliance = aid_self
    else:
        try:
            nid = min(int(aid_self), int(aid_t))
        except Exception:
            nid = aid_self
        a.client.alliance = nid
        b.client.alliance = nid
    affected_after = {getattr(a.client, "alliance", None), getattr(b.client, "alliance", None)}
    affected_ids = set(x for x in affected_before | affected_after if x not in [None, "None"])
    for p in a.world.players:
        if getattr(p.client, "alliance", None) in affected_ids or p in (a, b):
            try:
                p.update_alliance()
            except Exception:
                pass


def normalize_trade_kind(trade_kind: str):
    return rmg_rules.normalize_trade_kind(trade_kind)


def execute_rmg_trade(buyer, target, trade_kind: str) -> str:
    """Attempt a simplified RMG trade with an AI faction.

    Trade offers are defined in rules.txt (``rmg_trade 1`` upgrades).
    Returns a result token: ``success``, ``declined``, ``already_allied``,
    ``not_enough_diplomacy``, ``not_enough_gold``, ``cooldown``, ``invalid``.
    """
    from . import msgparts as mp

    world = getattr(buyer, "world", None)
    if not getattr(world, "rmg_strategic_systems", False):
        return "invalid"
    if not cities(buyer):
        return "invalid"
    trade_kind = rmg_rules.normalize_trade_kind(trade_kind)
    trade_cls = rmg_rules.trade_class(trade_kind) if trade_kind else None
    if trade_cls is None:
        return "invalid"
    if not _player_is_trade_target_ok(buyer, target):
        return "declined"
    if _trade_on_cooldown(buyer, target.id, trade_kind, trade_cls):
        return "cooldown"

    try:
        already_ally = target in getattr(buyer, "allied", [])
    except Exception:
        already_ally = False

    pay = rmg_rules.trade_pay_visible(trade_cls)
    while len(pay) < 3:
        pay.append(0)

    if getattr(trade_cls, "rmg_trade_alliance", 0):
        if already_ally:
            return "already_allied"
        diplomacy_cost = max(0, int(getattr(trade_cls, "rmg_trade_diplomacy_cost", 0) or 0))
        if diplomacy_cost and not spend_diplomacy(buyer, diplomacy_cost):
            return "not_enough_diplomacy"
        if not _transfer_visible_resources(
            buyer, target, gold=pay[0], wood=pay[1], food=pay[2]
        ):
            if diplomacy_cost:
                buyer.diplomacy_points += diplomacy_cost
            return "not_enough_gold"
        _form_alliance_between(buyer, target)
        buyer._ally_requests_from.discard(target.id)
        target._ally_requests_from.discard(buyer.id)
        _mark_trade_cooldown(buyer, target.id, trade_kind)
        if buyer.is_local_human():
            buyer.send_voice_important(mp.RMG_OPEN_BORDERS_ESTABLISHED + target.name)
        return "success"

    gain = rmg_rules.trade_gain_visible(trade_cls)
    while len(gain) < 3:
        gain.append(0)
    resource_index = next((index for index, amount in enumerate(gain) if amount > 0), None)
    if resource_index is None:
        return "invalid"
    resource_amount = gain[resource_index]
    target_resources = getattr(target, "resources", ())
    if (
        resource_index >= len(target_resources)
        or target_resources[resource_index] < to_int(str(resource_amount))
    ):
        return "declined"
    if not _transfer_visible_resources(
        buyer, target, gold=pay[0], wood=pay[1], food=pay[2]
    ):
        return "not_enough_gold"
    transfer = [0, 0, 0]
    transfer[resource_index] = resource_amount
    if not _transfer_visible_resources(
        target, buyer, gold=transfer[0], wood=transfer[1], food=transfer[2]
    ):
        _transfer_visible_resources(target, buyer, gold=pay[0], wood=pay[1], food=pay[2])
        return "declined"
    _mark_trade_cooldown(buyer, target.id, trade_kind)
    if buyer.is_local_human():
        from .definitions import style
        from .lib.msgs import nb2msg

        resource_title = style.get("parameters", f"resource{resource_index + 1}_title")
        buyer.send_voice_important(
            mp.RMG_TRADE_SUCCESS
            + nb2msg(resource_amount)
            + resource_title
            + target.name
        )
    return "success"
