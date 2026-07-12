from types import SimpleNamespace

from soundrts.lib.nofloat import PRECISION
from soundrts.rmg_systems import (
    DIPLOMACY_REQUEST_COST,
    OPEN_BORDERS_DIPLOMACY_COST,
    OPEN_BORDERS_GOLD_COST,
    POLICY_SLOT_LIMIT,
    TRADE_FOOD_AMOUNT,
    TRADE_FOOD_GOLD_COST,
    TRADE_WOOD_AMOUNT,
    TRADE_WOOD_GOLD_COST,
    TRADING_POST_DIPLOMACY_YIELD,
    TRADING_POST_GOLD_YIELD,
    TILE_PURCHASE_BASE_COST,
    activate_policy,
    ai_policy_plan,
    assign_citizen,
    buy_tile,
    can_adopt_policy,
    execute_rmg_trade,
    has_rmg_construction_on_square,
    improve_tile,
    register_completed_rmg_improvement,
    spend_diplomacy,
    strategic_tick,
    tile_improvement_diplomacy_yield,
    validate_rmg_build_target,
    worked_tile_yield,
    worker_can_start_rmg_improvement,
)


class _Stats:
    def __init__(self):
        self.gathered = []

    def add(self, key, index, amount):
        self.gathered.append((key, index, amount))


def _city(terrain_name="plain", type_name="townhall"):
    place = SimpleNamespace(terrain_name=terrain_name)
    return SimpleNamespace(
        type_name=type_name,
        expanded_is_a=set(),
        place=place,
        x=0,
        y=0,
        hp=100,
    )


def _player(city_units, upgrades=()):
    return SimpleNamespace(
        units=list(city_units),
        upgrades=list(upgrades),
        resources=[0, 0, 0],
        stats=_Stats(),
    )


class _Square:
    def __init__(self, name, terrain_name):
        self.name = name
        self.terrain_name = terrain_name
        self.id = name
        self.exits = []


def _link(a, b):
    a.exits.append(SimpleNamespace(other_side=SimpleNamespace(place=b)))
    b.exits.append(SimpleNamespace(other_side=SimpleNamespace(place=a)))


def _territory_fixture():
    centre = _Square("0,0", "plain")
    forest = _Square("1,0", "forest")
    _link(centre, forest)
    world = SimpleNamespace(
        squares=[centre, forest],
        players=[],
        terrain={"0,0": "plain", "1,0": "forest"},
        rmg_strategic_systems=True,
    )
    centre.world = world
    forest.world = world
    city = _city()
    city.id = 10
    city.place = centre
    city.world = world
    player = _player([city], upgrades=("rmg_urban_planning",))
    player.world = world
    player.resources = [100 * PRECISION, 100 * PRECISION, 100 * PRECISION]
    world.players.append(player)
    return player, city, centre, forest


def test_city_tick_grants_tile_yields_culture_and_diplomacy(monkeypatch):
    monkeypatch.setattr(
        "soundrts.rmg_systems._terrain_name",
        lambda city: city.place.terrain_name,
    )
    player = _player([_city("plain"), _city("hill")])
    summary = strategic_tick(player)

    assert summary["cities"] == 2
    assert summary["resources"] == (15, 8, 11)
    assert player.resources == [15 * PRECISION, 8 * PRECISION, 11 * PRECISION]
    assert player.culture_points == 8
    assert player.diplomacy_points == 2
    assert len(player.stats.gathered) == 3


def test_city_expansion_and_policies_scale_yields(monkeypatch):
    monkeypatch.setattr("soundrts.rmg_systems._terrain_name", lambda city: "plain")
    player = _player(
        [_city(), _city(), _city()],
        upgrades=("rmg_urban_planning", "rmg_policy_commerce", "rmg_policy_tradition"),
    )
    summary = strategic_tick(player)

    assert summary["cities"] == 3
    assert summary["resources"] == (30, 22, 33)
    assert summary["culture"] == 18


def test_third_policy_replaces_oldest_slot():
    player = _player(
        [_city()],
        upgrades=("rmg_policy_tradition", "rmg_policy_commerce"),
    )
    assert POLICY_SLOT_LIMIT == 2
    assert can_adopt_policy(player, "rmg_policy_tradition")
    assert can_adopt_policy(player, "rmg_policy_diplomacy")
    activate_policy(player, "rmg_policy_diplomacy")
    assert player.rmg_policy_slots == [
        "rmg_policy_commerce",
        "rmg_policy_diplomacy",
    ]
    assert "rmg_policy_tradition" not in player.upgrades


def test_unlocked_policy_hidden_from_research_menu():
    from soundrts.worldorders.production import ResearchOrder
    from soundrts.worldorders.strategic import RmgSwitchTraditionOrder

    player = _player(
        [_city()],
        upgrades=("rmg_policy_tradition", "rmg_policy_commerce"),
    )
    player.culture_points = 200
    can_adopt_policy(player, "rmg_policy_diplomacy")
    activate_policy(player, "rmg_policy_diplomacy")
    assert "rmg_policy_tradition" in player.rmg_unlocked_policies
    assert "rmg_policy_tradition" not in player.upgrades

    city = player.units[0]
    city.player = player
    city.orders = []
    city.world = SimpleNamespace(rmg_strategic_systems=True)
    city.can_research = (
        "rmg_policy_tradition",
        "rmg_policy_commerce",
        "rmg_policy_diplomacy",
    )

    assert not ResearchOrder.additional_condition(city, "rmg_policy_tradition")
    assert not ResearchOrder.additional_condition(city, "rmg_policy_commerce")
    assert RmgSwitchTraditionOrder.is_allowed(city)


def test_pending_policy_cannot_be_queued_twice():
    player = _player([_city()])
    player.units[0].orders = [
        SimpleNamespace(
            type=SimpleNamespace(
                type_name="rmg_policy_tradition",
                rmg_policy=1,
            )
        ),
        SimpleNamespace(
            type=SimpleNamespace(
                type_name="rmg_policy_commerce",
                rmg_policy=1,
            )
        ),
    ]
    assert not can_adopt_policy(player, "rmg_policy_commerce")
    assert can_adopt_policy(player, "rmg_policy_diplomacy")


def test_tile_purchase_citizen_assignment_and_improvement_affect_yield(monkeypatch):
    player, city, _centre, forest = _territory_fixture()
    player.observed_squares = set()
    player.observed_before_squares = set()
    player.strictly_observed_before_squares = set()
    worker = SimpleNamespace(
        id=20,
        type_name="peasant",
        is_rmg_worker=True,
        place=forest,
        hp=10,
        orders=[],
        auto_gather=True,
        take_order=lambda order: None,
        player=player,
        world=player.world,
    )
    player.units.append(worker)

    def spawn_entity(owner, type_name, square):
        entity = SimpleNamespace(
            id=30,
            type_name=type_name,
            place=square,
            hp=150,
            delete=lambda: None,
            player=owner,
        )
        owner.units.append(entity)
        return entity

    monkeypatch.setattr(
        "soundrts.rmg_systems._spawn_rmg_entity", spawn_entity
    )

    assert buy_tile(player, city, forest)
    assert player.rmg_claimed_tiles["1,0"] == city.id
    assert forest in player.observed_squares
    assert forest in player.strictly_observed_before_squares
    assert assign_citizen(player, city, forest, "wood")
    assert player.rmg_tile_workers["1,0"] == worker.id
    assert worker.auto_gather is False
    # City instant build is retired; peasant construction must complete first.
    assert improve_tile(player, city, forest, "lumber_mill") is False
    assert worker_can_start_rmg_improvement(worker, "rmg_tile_lumber_mill")
    assert validate_rmg_build_target(worker, "rmg_tile_lumber_mill", forest) is None

    building = SimpleNamespace(
        id=30,
        type_name="rmg_tile_lumber_mill",
        place=forest,
        player=player,
        world=player.world,
    )
    assert register_completed_rmg_improvement(building)
    assert player.rmg_improvement_units["1,0"] == 30
    assert player.rmg_tile_improvements["1,0"] == "lumber_mill"
    # Completion auto-binds the on-site peasant if the tile had no worker.
    assert player.rmg_tile_workers.get("1,0") == worker.id
    assert player.rmg_worked_tiles.get("1,0") == "wood"

    summary = strategic_tick(player)
    # City centre 8/6/9 after urban planning; worked forest adds 1/8/1.
    assert summary["resources"] == (9, 14, 10)


def test_rmg_improvement_build_is_visible_and_targets_claimed_tiles():
    from soundrts.worldorders.production import BuildOrder

    player, city, centre, forest = _territory_fixture()
    worker = SimpleNamespace(
        id=22,
        type_name="peasant",
        is_rmg_worker=True,
        place=centre,
        hp=10,
        orders=[],
        auto_gather=True,
        take_order=lambda order: None,
        player=player,
        world=player.world,
        can_build=("rmg_tile_mine", "rmg_tile_lumber_mill", "rmg_tile_farm"),
    )
    player.units.append(worker)
    # Menu is visible on any peasant in RMG maps, even before buying/assigning.
    assert worker_can_start_rmg_improvement(worker, "rmg_tile_mine")
    assert BuildOrder.additional_condition(worker, "rmg_tile_mine")
    # But the target must be an owned claimed tile.
    assert validate_rmg_build_target(worker, "rmg_tile_mine", forest) == "cannot_build_here"

    assert buy_tile(player, city, forest)
    assert validate_rmg_build_target(worker, "rmg_tile_mine", forest) is None
    assert validate_rmg_build_target(worker, "rmg_tile_mine", centre) is None or (
        centre.name in player.rmg_claimed_tiles
    )
    # City centre square is claimed by the city itself.
    assert centre.name in player.rmg_claimed_tiles
    assert validate_rmg_build_target(worker, "rmg_tile_mine", centre) is None

    player.rmg_tile_improvements["1,0"] = "mine"
    assert validate_rmg_build_target(worker, "rmg_tile_mine", forest) == "cannot_build_here"


def test_rmg_build_menu_visible_on_client_entity_view_proxy():
    """Classic A menu runs on EntityView, which is not a Worker instance."""
    from soundrts.worldorders.production import BuildOrder

    player, _city, centre, _forest = _territory_fixture()
    player.forbidden_techs = []
    player.check_count_limit = lambda _t: True
    model = SimpleNamespace(
        id=22,
        type_name="peasant",
        place=centre,
        hp=10,
        orders=[],
        player=player,
        world=player.world,
        can_build=("rmg_tile_mine", "rmg_tile_lumber_mill", "rmg_tile_farm"),
        **{"class": ["worker"]},
    )
    # Mimic EntityView: not a Worker, attributes proxied via .model / __dict__.
    view = SimpleNamespace(
        model=model,
        type_name=model.type_name,
        player=player,
        world=player.world,
        orders=[],
        can_build=model.can_build,
        **{"class": ["worker"]},
    )
    assert worker_can_start_rmg_improvement(view, "rmg_tile_mine")
    assert BuildOrder.additional_condition(view, "rmg_tile_mine")
    assert "build rmg_tile_mine" in BuildOrder.menu(view)


def test_rmg_construction_site_blocks_repeat_build_and_yield():
    player, city, _centre, forest = _territory_fixture()
    worker = SimpleNamespace(
        id=23,
        type_name="peasant",
        is_rmg_worker=True,
        place=forest,
        hp=10,
        orders=[],
        player=player,
        world=player.world,
        auto_gather=True,
        take_order=lambda order: None,
    )
    site_type = SimpleNamespace(type_name="rmg_tile_mine", __name__="rmg_tile_mine")
    site = SimpleNamespace(
        id=40,
        type_name="buildingsite",
        type=site_type,
        place=forest,
        player=player,
        world=player.world,
    )
    player.units.extend([worker, site])
    assert buy_tile(player, city, forest)
    assert has_rmg_construction_on_square(player, forest)
    assert worker_can_start_rmg_improvement(worker, "rmg_tile_mine")
    assert validate_rmg_build_target(worker, "rmg_tile_mine", forest) == "cannot_build_here"
    assert assign_citizen(player, city, forest, "gold")
    summary = strategic_tick(player)
    # Construction site is not a finished improvement; no +3 gold yet.
    # City 8/6/9 + forest gold focus 3/3/1 = 11/9/10.
    assert summary["resources"] == (11, 9, 10)


def test_classic_map_hides_rmg_improvement_builds():
    from soundrts.worldorders.production import BuildOrder

    worker = SimpleNamespace(
        id=1,
        type_name="peasant",
        is_rmg_worker=True,
        place=SimpleNamespace(name="a1"),
        player=SimpleNamespace(
            world=SimpleNamespace(rmg_strategic_systems=False),
            rmg_tile_workers={},
            rmg_claimed_tiles={},
            rmg_tile_improvements={},
            units=[],
        ),
        world=SimpleNamespace(rmg_strategic_systems=False),
        can_build=("rmg_tile_mine",),
    )
    assert not BuildOrder.additional_condition(worker, "rmg_tile_mine")


def test_rmg_tile_work_requires_a_real_worker_on_the_tile():
    player, city, _centre, forest = _territory_fixture()
    assert buy_tile(player, city, forest)
    assert not assign_citizen(player, city, forest, "gold")

    worker = SimpleNamespace(
        id=21,
        type_name="peasant",
        is_rmg_worker=True,
        place=forest,
        hp=10,
        orders=[],
        auto_gather=True,
        take_order=lambda order: None,
    )
    worker.world = player.world
    player.units.append(worker)
    assert assign_citizen(player, city, forest, "gold")

    worker.place = _centre
    summary = strategic_tick(player)
    # The city still produces, but the unattended tile does not.
    assert summary["resources"] == (8, 6, 9)


def test_ai_uses_dedicated_policy_combinations():
    aggressive = SimpleNamespace(AI_type="aggressive", true_enemies=[])
    diplomatic = SimpleNamespace(AI_type="standard", true_enemies=[1, 2])
    assert ai_policy_plan(aggressive) == (
        "rmg_policy_commerce",
        "rmg_policy_tradition",
    )
    assert ai_policy_plan(diplomatic) == (
        "rmg_policy_diplomacy",
        "rmg_policy_commerce",
    )


def test_rmg_city_orders_are_registered_and_hidden_outside_rmg():
    from soundrts.worldorders import ORDERS_DICT

    city = _city()
    city.world = SimpleNamespace(rmg_strategic_systems=True)
    city.player = SimpleNamespace(
        rmg_unlocked_policies=set(), rmg_policy_slots=[]
    )
    for keyword in (
        "rmg_buy_tile",
        "rmg_assign_gold",
        "rmg_switch_commerce",
    ):
        assert keyword in ORDERS_DICT
    assert "rmg_build_farm" not in ORDERS_DICT
    assert ORDERS_DICT["rmg_buy_tile"].menu(city) == ["rmg_buy_tile"]
    city.world.rmg_strategic_systems = False
    assert ORDERS_DICT["rmg_buy_tile"].menu(city) == []


def test_rmg_city_orders_are_indexed_for_command_menu():
    from soundrts.clientgameorder import get_orders_list, update_orders_list
    from soundrts.definitions import style
    from soundrts.lib.resource import res

    res.load_style()
    update_orders_list()
    indexed = {cls.keyword for cls in get_orders_list()}
    for keyword in (
        "rmg_buy_tile",
        "rmg_assign_gold",
        "rmg_switch_commerce",
    ):
        assert keyword in indexed
    assert "rmg_build_farm" not in indexed
    assert style.has("rmg_buy_tile", "index")
    assert not style.has("rmg_build_farm", "index")


def test_rmg_city_orders_show_resource_costs_in_menu():
    from soundrts.clientgameorder import OrderTypeView
    from soundrts.lib.nofloat import PRECISION
    from soundrts.lib.resource import res
    from soundrts.rmg_systems import menu_resource_cost

    res.load_style()
    player, city, _centre, _forest = _territory_fixture()
    city.player = player

    buy_view = OrderTypeView("rmg_buy_tile", city)
    assert buy_view.cost[0] == 20 * PRECISION
    assert "129" in "".join(str(part) for part in buy_view.full_comment)

    assert menu_resource_cost("rmg_build_mine", city)[:3] == (
        15 * PRECISION,
        10 * PRECISION,
        0,
    )
    assert menu_resource_cost("rmg_assign_gold", city) == (0,) * 10
    assert OrderTypeView("rmg_assign_gold", city).full_comment == []

    player.rmg_claimed_tiles = {"0,0": city.id, "1,0": city.id}
    from soundrts.rmg_systems import initialize_player

    initialize_player(player)
    assert menu_resource_cost("rmg_buy_tile", city)[0] == 30 * PRECISION


def test_rmg_policy_research_shows_culture_cost_in_menu():
    from soundrts import msgparts as mp
    from soundrts.clientgameorder import OrderTypeView
    from soundrts.lib.resource import res

    res.load_rules_and_ai()
    res.load_style()
    player, city, _centre, _forest = _territory_fixture()
    city.player = player
    city.orders = []
    player.has = lambda name: name in player.upgrades
    player.upgrades = ["rmg_urban_planning"]

    tradition_view = OrderTypeView("research rmg_policy_tradition", city)
    assert mp.RMG_CULTURE[0] in tradition_view.full_comment
    assert any(part == 1000040 or part == 40 for part in tradition_view.full_comment)

    commerce_view = OrderTypeView("research rmg_policy_commerce", city)
    assert mp.RMG_CULTURE[0] in commerce_view.full_comment
    assert any(part == 1000080 or part == 80 for part in commerce_view.full_comment)
    player.upgrades.append("rmg_civic_administration")
    commerce_view = OrderTypeView("research rmg_policy_commerce", city)
    assert mp.RMG_CULTURE[0] in commerce_view.full_comment
    assert any(part == 1000080 or part == 80 for part in commerce_view.full_comment)


def test_strategic_order_success_and_yield_announcements():
    from soundrts import msgparts as mp
    from soundrts.lib.resource import res
    from soundrts.rmg_systems import (
        announce_strategic_order_success,
        format_yield_announcement,
    )
    from soundrts.worldorders import ORDERS_DICT

    res.load_style()
    player, city, _centre, forest = _territory_fixture()
    city.player = player
    city.world.rmg_strategic_systems = True
    forest.id = 99
    player.is_local_human = lambda: True
    player.send_voice_important = lambda msg: setattr(
        player, "_last_voice", list(msg)
    )

    order = ORDERS_DICT["rmg_buy_tile"](city, [forest.id])
    announce_strategic_order_success(player, order.keyword)
    assert mp.RMG_TILE_PURCHASED[0] in player._last_voice
    assert mp.RMG_YIELD_EVERY_MINUTE[0] in player._last_voice

    announce_strategic_order_success(player, "rmg_build_mine")
    assert mp.RMG_MINE_BUILT[0] in player._last_voice
    assert mp.RMG_YIELD_EVERY_MINUTE[0] not in player._last_voice

    msg = format_yield_announcement(
        {"resources": (9, 14, 10), "culture": 8, "diplomacy": 2}
    )
    assert mp.RMG_CITY_YIELD[0] in msg
    assert mp.RMG_CULTURE[0] in msg
    assert mp.RMG_DIPLOMACY_POINTS[0] in msg



def test_rmg_hero_progress_persists_between_matches(monkeypatch, tmp_path):
    from soundrts import rmg_progress

    monkeypatch.setattr(rmg_progress, "CONFIG_DIR_PATH", str(tmp_path))
    monkeypatch.setattr(rmg_progress, "current_mod_key", lambda: "base")
    finished_hero = SimpleNamespace(type_name="rmg_hero", level=5, xp=420)
    old_player = SimpleNamespace(
        faction="human", units=[finished_hero], rmg_hero_peak_level=5,
        rmg_hero_peak_xp=420,
    )
    assert rmg_progress.save_hero_progress(old_player)

    new_hero = SimpleNamespace(
        type_name="rmg_hero", level=1, max_level=8, xp=0,
        _apply_level_skills_up_to=lambda level, notify=False: None,
    )
    new_player = SimpleNamespace(faction="human", units=[new_hero])
    assert rmg_progress.apply_hero_progress(new_player)
    assert (new_hero.level, new_hero.xp) == (5, 420)


def test_alliance_request_cost_is_announced_for_rmg_cities():
    from soundrts import msgparts as mp
    from soundrts.lib.resource import res
    from soundrts.rmg_systems import alliance_request_cost, diplomacy_cost_msg

    res.load_style()
    city = _city()
    city.place = SimpleNamespace()
    player = _player([city])
    player.world = SimpleNamespace(rmg_strategic_systems=True)
    assert alliance_request_cost(player) == DIPLOMACY_REQUEST_COST

    player.world.rmg_strategic_systems = False
    assert alliance_request_cost(player) == 0

    msg = diplomacy_cost_msg(DIPLOMACY_REQUEST_COST)
    assert mp.RMG_DIPLOMACY_POINTS[0] in msg
    assert any(part == 1000020 or part == 20 for part in msg)


def test_diplomacy_points_are_spent_atomically():
    player = _player([_city()])
    player.diplomacy_points = DIPLOMACY_REQUEST_COST - 1
    assert not spend_diplomacy(player)
    assert player.diplomacy_points == DIPLOMACY_REQUEST_COST - 1

    player.diplomacy_points += 1
    assert spend_diplomacy(player)
    assert player.diplomacy_points == 0


def test_strategic_research_is_only_exposed_on_rmg_cities():
    from soundrts.lib.resource import res
    from soundrts.world_build_rules import effective_can_research

    res.load_rules_and_ai()

    class _City:
        can_research = ("hunting_techniques", "rmg_urban_planning")
        provides_survival = True
        storable_resource_types = ("resource1",)

    host = _City()
    host.attached_addons = []
    host.world = SimpleNamespace(rmg_strategic_systems=False)
    assert effective_can_research(host) == ("hunting_techniques",)

    host.world.rmg_strategic_systems = True
    research = effective_can_research(host)
    assert "rmg_urban_planning" in research
    assert "rmg_policy_tradition" in research


def test_townhall_can_research_property_respects_rmg_flag():
    from soundrts.definitions import rules
    from soundrts.lib.resource import res

    res.load_rules_and_ai()
    cls = rules.unit_class("townhall")
    assert "can_research" not in cls.__dict__
    assert "_rules_can_research" in cls.__dict__

    inst = object.__new__(cls)
    inst.attached_addons = []
    inst.world = SimpleNamespace(rmg_strategic_systems=False)
    assert inst.can_research == ("hunting_techniques",)
    assert not any(name.startswith("rmg_") for name in inst.can_research)

    inst.world.rmg_strategic_systems = True
    research = inst.can_research
    assert "hunting_techniques" in research
    assert "rmg_urban_planning" in research
    assert "rmg_policy_tradition" in research


def test_strategic_tts_entries_exist():
    from pathlib import Path

    root = Path(__file__).resolve().parents[2]
    for relative in ("res/ui/tts.txt", "res/ui-zh/tts.txt"):
        text = (root / relative).read_text(encoding="utf-8")
        for message_id in range(5702, 5729):
            assert f"\n{message_id} " in "\n" + text


def test_culture_and_diplomacy_status_helpers():
    from types import SimpleNamespace

    from soundrts.clientgame import game_resources

    interface = SimpleNamespace(
        world=SimpleNamespace(rmg_strategic_systems=True),
        player=SimpleNamespace(culture_points=12, diplomacy_points=5),
    )
    assert game_resources.strategic_systems_active(interface)
    assert game_resources.culture_points(interface) == 12
    assert game_resources.diplomacy_points(interface) == 5

    interface.world.rmg_strategic_systems = False
    assert not game_resources.strategic_systems_active(interface)


def test_city_attributes_include_strategic_points():
    from types import SimpleNamespace

    from soundrts import msgparts as mp
    from soundrts.attributes.basic_attributes import BasicAttributes

    player = SimpleNamespace(
        culture_points=30,
        diplomacy_points=7,
        _is_pure_spectator=False,
    )
    interface = SimpleNamespace(
        world=SimpleNamespace(rmg_strategic_systems=True),
        player=player,
    )
    unit = SimpleNamespace(
        type_name="townhall",
        player=player,
        model=SimpleNamespace(type_name="townhall"),
    )

    attrs = []
    BasicAttributes(SimpleNamespace(interface=interface)).add_strategic_player_attributes(
        unit, attrs
    )
    assert len(attrs) == 2
    assert attrs[0][0] == "u" and attrs[0][1] == mp.RMG_CULTURE
    assert attrs[1][0] == "y" and attrs[1][1] == mp.RMG_DIPLOMACY_POINTS

    interface.world.rmg_strategic_systems = False
    attrs = []
    BasicAttributes(SimpleNamespace(interface=interface)).add_strategic_player_attributes(
        unit, attrs
    )
    assert attrs == []


def test_trading_post_improvement_adds_gold_and_diplomacy_yield():
    player, city, _centre, forest = _territory_fixture()
    player.observed_squares = set()
    player.observed_before_squares = set()
    player.strictly_observed_before_squares = set()
    worker = SimpleNamespace(
        id=24,
        type_name="peasant",
        is_rmg_worker=True,
        place=forest,
        hp=10,
        orders=[],
        auto_gather=False,
        take_order=lambda order: None,
        player=player,
        world=player.world,
    )
    player.units.append(worker)
    assert buy_tile(player, city, forest)
    assert assign_citizen(player, city, forest, "gold")
    building = SimpleNamespace(
        id=31,
        type_name="rmg_tile_trading_post",
        place=forest,
        hp=150,
        delete=lambda: None,
        player=player,
        world=player.world,
    )
    player.units.append(building)
    assert register_completed_rmg_improvement(building)
    assert player.rmg_tile_improvements["1,0"] == "trading_post"

    gold, wood, food, culture = worked_tile_yield(player, "1,0")
    assert gold >= TRADING_POST_GOLD_YIELD
    assert tile_improvement_diplomacy_yield(player, "1,0") == TRADING_POST_DIPLOMACY_YIELD

    summary = strategic_tick(player)
    assert summary["diplomacy"] >= 1 + TRADING_POST_DIPLOMACY_YIELD


def test_execute_rmg_trade_wood_transfers_resources():
    buyer = _player([_city()])
    buyer.world = SimpleNamespace(rmg_strategic_systems=True, time=100000)
    buyer.is_local_human = lambda: False
    buyer.resources = [200 * PRECISION, 0, 0]
    buyer.allied = [buyer]
    buyer.player_is_an_enemy = lambda other: False
    buyer._ally_requests_from = set()
    buyer._rmg_trade_cooldowns = {}
    buyer.units[0].world = buyer.world

    seller = _player([_city()])
    seller.world = buyer.world
    seller.id = 2
    seller.is_human = False
    seller.neutral = False
    seller.resources = [0, 500 * PRECISION, 500 * PRECISION]
    seller.allied = [seller]
    seller._ally_requests_from = set()

    result = execute_rmg_trade(buyer, seller, "resource2")
    assert result == "success"
    assert buyer.resources[0] == (200 - TRADE_WOOD_GOLD_COST) * PRECISION
    assert buyer.resources[1] == TRADE_WOOD_AMOUNT * PRECISION
    assert seller.resources[1] == (500 - TRADE_WOOD_AMOUNT) * PRECISION


def test_execute_rmg_trade_open_borders_forms_alliance():
    buyer = _player([_city()])
    buyer.world = SimpleNamespace(rmg_strategic_systems=True, time=100000, players=[])
    buyer.id = 1
    buyer.is_local_human = lambda: False
    buyer.resources = [100 * PRECISION, 0, 0]
    buyer.diplomacy_points = OPEN_BORDERS_DIPLOMACY_COST + 5
    buyer.allied = [buyer]
    buyer.player_is_an_enemy = lambda other: False
    buyer._ally_requests_from = set()
    buyer._rmg_trade_cooldowns = {}
    buyer.client = SimpleNamespace(alliance=None)
    buyer.update_alliance = lambda: None
    buyer.units[0].world = buyer.world

    target = _player([_city()])
    target.world = buyer.world
    target.id = 2
    target.is_human = False
    target.neutral = False
    target.allied = [target]
    target._ally_requests_from = set()
    target.client = SimpleNamespace(alliance="ai")
    target.update_alliance = lambda: None

    buyer.world.players = [buyer, target]

    result = execute_rmg_trade(buyer, target, "open_borders")
    assert result == "success"
    assert buyer.resources[0] == (100 - OPEN_BORDERS_GOLD_COST) * PRECISION
    assert buyer.diplomacy_points == 5
    assert buyer.client.alliance == target.client.alliance
    assert buyer.client.alliance not in (None, "None", "ai")


def test_worker_can_build_trading_post_on_rmg_map():
    from soundrts.worldorders.production import BuildOrder

    player, _city, centre, _forest = _territory_fixture()
    worker = SimpleNamespace(
        id=25,
        type_name="peasant",
        place=centre,
        hp=10,
        orders=[],
        player=player,
        world=player.world,
        can_build=("rmg_tile_trading_post",),
        **{"class": ["worker"]},
    )
    assert worker_can_start_rmg_improvement(worker, "rmg_tile_trading_post")
    assert BuildOrder.additional_condition(worker, "rmg_tile_trading_post")


def test_cmd_diplomacy_trade_resource2_does_not_misparse_kind_as_target_id():
    """``diplomacy trade resource2 <id>`` uses engine resource slot names on the wire."""
    from types import SimpleNamespace

    from soundrts.worldplayerbase.base import Player

    seller = SimpleNamespace(
        id=2,
        is_human=False,
        neutral=False,
        resources=[0, 500 * PRECISION, 500 * PRECISION],
        allied=[],
        _ally_requests_from=set(),
        player_is_an_enemy=lambda other: False,
    )
    buyer = Player.__new__(Player)
    city = SimpleNamespace(
        type_name="townhall",
        expanded_is_a=set(),
        place=SimpleNamespace(name="0,0"),
        hp=100,
    )
    buyer.units = [city]
    buyer.resources = [200 * PRECISION, 0, 0]
    buyer.diplomacy_points = 0
    buyer.allied = [buyer]
    buyer._ally_requests_from = set()
    buyer._rmg_trade_cooldowns = {}
    buyer.is_local_human = lambda: False
    buyer.world = SimpleNamespace(
        rmg_strategic_systems=True,
        time=100000,
        players=[buyer, seller],
        alliances_locked=False,
    )
    buyer.id = 1
    buyer.player_is_an_enemy = lambda other: False
    buyer.send_voice_important = lambda msg: None
    buyer._resolve_player_by_id = lambda pid: seller if str(pid) == "2" else None
    buyer._alliances_locked_now = lambda: False

    buyer.cmd_diplomacy(["trade", "resource2", "2"])
    assert buyer.resources[0] == (200 - TRADE_WOOD_GOLD_COST) * PRECISION
    assert buyer.resources[1] == TRADE_WOOD_AMOUNT * PRECISION


def test_execute_rmg_trade_accepts_legacy_wood_alias():
    buyer = _player([_city()])
    buyer.world = SimpleNamespace(rmg_strategic_systems=True, time=100000)
    buyer.is_local_human = lambda: False
    buyer.resources = [200 * PRECISION, 0, 0]
    buyer.allied = [buyer]
    buyer.player_is_an_enemy = lambda other: False
    buyer._ally_requests_from = set()
    buyer._rmg_trade_cooldowns = {}
    buyer.units[0].world = buyer.world

    seller = _player([_city()])
    seller.world = buyer.world
    seller.id = 2
    seller.is_human = False
    seller.neutral = False
    seller.resources = [0, 500 * PRECISION, 500 * PRECISION]
    seller.allied = [seller]
    seller._ally_requests_from = set()

    assert execute_rmg_trade(buyer, seller, "wood") == "success"
    assert buyer.resources[1] == TRADE_WOOD_AMOUNT * PRECISION


def test_rmg_rules_load_from_rules_txt():
    from soundrts import rmg_rules
    from soundrts.lib.resource import res

    res.load_rules_and_ai()
    assert rmg_rules.diplomacy_request_cost() == DIPLOMACY_REQUEST_COST
    assert rmg_rules.tile_purchase_base_cost() == TILE_PURCHASE_BASE_COST
    assert "trading_post" in rmg_rules.improvement_entity_types()
    assert rmg_rules.improvement_yield_bonus("trading_post") == [
        TRADING_POST_GOLD_YIELD,
        0,
        0,
        0,
        TRADING_POST_DIPLOMACY_YIELD,
    ]
    assert rmg_rules.default_work_focus_for_improvement("farm") == "food"
    assert rmg_rules.normalize_trade_kind("resource2") == "resource2"
    trade = rmg_rules.trade_class("resource2")
    assert rmg_rules.trade_pay_visible(trade)[0] == TRADE_WOOD_GOLD_COST
    assert rmg_rules.trade_gain_visible(trade)[1] == TRADE_WOOD_AMOUNT
