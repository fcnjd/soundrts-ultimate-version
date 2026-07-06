import types

from soundrts.clientgameentity import audio as audio_module
from soundrts.clientgameentity.audio import EntityViewAudio


class _FakeStyle:
    def __init__(self, entries, ground=None):
        self.entries = entries
        self.ground = ground or {}

    def get(self, obj, attr, warn_if_not_found=True):
        if attr == "ground":
            return self.ground.get(obj, [])
        return self.entries.get((obj, attr), [])

    def has(self, obj, attr):
        return (obj, attr) in self.entries


class _View(EntityViewAudio):
    def __init__(self, place, x=0, y=0):
        self.type_name = "footman"
        if getattr(place, "objects", None) is None:
            place.objects = []
        if not hasattr(place, "high_ground"):
            place.high_ground = False
        self.place = place
        self.x = x
        self.y = y
        self.airground_type = "ground"
        self.interface = types.SimpleNamespace(
            player=types.SimpleNamespace(allied=[]),
            place=place,
            dobjets={},
        )

    def get_style(self, attr):
        return audio_module.style.get(self.type_name, attr)


def _style(extra=None):
    entries = {
        ("footman", "falling"): ["80051"],
        ("footman", "falling_on_ocean"): ["fallwater"],
        ("footman", "falling_on_water"): ["splash"],
        ("footman", "move"): ["default_step"],
        ("footman", "move_on_ocean"): ["ocean_step"],
        ("footman", "move_on_water"): ["water_step"],
    }
    if extra:
        entries.update(extra)
    return _FakeStyle(entries, ground={"creek": ["water"]})


def test_falling_on_ocean_by_terrain_name(monkeypatch):
    place = types.SimpleNamespace(type_name="ocean")
    monkeypatch.setattr(audio_module, "style", _style())
    view = _View(place)
    assert view._get_falling_sound() == ["fallwater"]


def test_falling_on_water_by_ground_type(monkeypatch):
    place = types.SimpleNamespace(type_name="creek")
    monkeypatch.setattr(audio_module, "style", _style())
    view = _View(place)
    assert view._get_falling_sound() == ["splash"]


def test_falling_on_terrain_name_takes_priority_over_ground(monkeypatch):
    place = types.SimpleNamespace(type_name="creek")
    monkeypatch.setattr(
        audio_module,
        "style",
        _style(
            {
                ("footman", "falling_on_creek"): ["creek_fall"],
                ("footman", "falling_on_water"): ["splash"],
            }
        ),
    )
    view = _View(place)
    assert view._get_falling_sound() == ["creek_fall"]


def test_falling_defaults_when_no_terrain_match(monkeypatch):
    place = types.SimpleNamespace(type_name="plain")
    monkeypatch.setattr(audio_module, "style", _style())
    view = _View(place)
    assert view._get_falling_sound() == ["80051"]


def test_falling_uses_subcell_terrain(monkeypatch):
    place = types.SimpleNamespace(
        type_name="plain",
        type_name_at=lambda x, y: "mountain",
    )
    monkeypatch.setattr(
        audio_module,
        "style",
        _style({("footman", "falling_on_mountain"): ["rock_fall"]}),
    )
    view = _View(place)
    assert view._get_falling_sound() == ["rock_fall"]


def test_move_on_ocean_by_terrain_name(monkeypatch):
    place = types.SimpleNamespace(type_name="ocean")
    monkeypatch.setattr(audio_module, "style", _style())
    view = _View(place)
    assert view._terrain_footstep() == ["ocean_step"]


def test_move_on_water_by_ground_type(monkeypatch):
    place = types.SimpleNamespace(type_name="creek")
    monkeypatch.setattr(audio_module, "style", _style())
    view = _View(place)
    assert view._terrain_footstep() == ["water_step"]


def test_move_on_terrain_name_takes_priority_over_ground(monkeypatch):
    place = types.SimpleNamespace(type_name="creek")
    monkeypatch.setattr(
        audio_module,
        "style",
        _style(
            {
                ("footman", "move_on_creek"): ["creek_step"],
                ("footman", "move_on_water"): ["water_step"],
            }
        ),
    )
    view = _View(place)
    assert view._terrain_footstep() == ["creek_step"]


def test_footstepnoise_uses_move_on_terrain_name(monkeypatch):
    place = types.SimpleNamespace(type_name="ocean", objects=[])
    monkeypatch.setattr(audio_module, "style", _style())
    view = _View(place)
    assert view.footstepnoise() == ["ocean_step"]


def test_move_on_bridge_deck_resolves_wood_not_water(monkeypatch):
    place = types.SimpleNamespace(
        type_name="river",
        _bridge_terrain_voice="bridge_deck",
        fixed_terrain=True,
        objects=[],
    )
    monkeypatch.setattr(
        audio_module,
        "style",
        _FakeStyle(
            {
                ("footman", "move"): ["default_step"],
                ("footman", "move_on_wood"): ["wood_step"],
                ("footman", "move_on_water"): ["water_step"],
            },
            ground={"bridge_deck": ["wood"], "river": ["water"]},
        ),
    )
    view = _View(place)
    assert view._terrain_footstep() == ["wood_step"]
    assert view.footstepnoise() == ["wood_step"]


def test_move_on_lake_bridge_overrides_type_name_at(monkeypatch):
    place = types.SimpleNamespace(
        type_name="lake",
        type_name_at=lambda x, y: "lake",
        fixed_terrain=True,
        _bridge_terrain_voice="bridge_deck",
        objects=[],
    )
    monkeypatch.setattr(
        audio_module,
        "style",
        _FakeStyle(
            {
                ("footman", "move"): ["default_step"],
                ("footman", "move_on_wood"): ["wood_step"],
                ("footman", "move_on_water"): ["water_step"],
            },
            ground={
                "bridge_deck": ["wood"],
                "lake": ["water"],
                "big_bridge": ["wood"],
            },
        ),
    )
    view = _View(place)
    assert view._terrain_sound_keys() == ["bridge_deck", "wood"]
    assert view._terrain_footstep() == ["wood_step"]


def test_move_on_meadow_overrides_plain_gravel():
    """水泥/砾石底图上铺 meadow：走 building_land 层，不走底图 gravel。"""
    from soundrts.lib.resource import res

    res.load_rules_and_ai()
    place = types.SimpleNamespace(
        type_name="plain",
        type_name_at=lambda x, y: "plain",
        high_ground=False,
        objects=[
            types.SimpleNamespace(
                type_name="meadow",
                is_a_building_land=True,
                is_an_exit=False,
            )
        ],
    )
    view = _View(place)
    assert view._overlay_terrain_voices(place) == ["meadows"]
    keys = view._terrain_sound_keys()
    assert keys == ["meadows", "grass"]
    assert "plain" not in keys
    assert "gravel" not in keys
    assert view._terrain_footstep() == audio_module.style.get("footman", "move_on_grass")
    assert view.footstepnoise() == audio_module.style.get("footman", "move_on_grass")


def test_building_site_remembered_meadow_uses_grass():
    """施工中 meadow 已从格上移除，site.building_land 仍应提供 meadows 覆盖层。"""
    from soundrts.lib.resource import res

    res.load_rules_and_ai()
    meadow = types.SimpleNamespace(
        type_name="meadow",
        is_a_building_land=True,
        is_an_exit=False,
    )
    site = types.SimpleNamespace(
        type_name="buildingsite",
        building_land=meadow,
    )
    place = types.SimpleNamespace(
        type_name="plain",
        type_name_at=lambda x, y: "plain",
        high_ground=False,
        objects=[site],
    )
    view = _View(place)
    assert view._overlay_terrain_voices(place) == ["meadows"]
    keys = view._terrain_sound_keys()
    assert keys == ["meadows", "grass"]
    assert "plain" not in keys
    assert "gravel" not in keys
    assert view._terrain_footstep() == audio_module.style.get("footman", "move_on_grass")


def test_move_on_meadows_explicit_ground_grass(monkeypatch):
    """覆盖层 def 上写 ground grass 时，不依赖 meadow 对象反查。"""
    place = types.SimpleNamespace(
        type_name="plain",
        type_name_at=lambda x, y: "plain",
        high_ground=False,
        objects=[
            types.SimpleNamespace(
                type_name="meadow",
                is_a_building_land=True,
                is_an_exit=False,
            )
        ],
    )
    monkeypatch.setattr(
        audio_module,
        "style",
        _FakeStyle(
            {
                ("footman", "move"): ["default_step"],
                ("footman", "move_on_grass"): ["grass_step"],
                ("footman", "move_on_gravel"): ["gravel_step"],
            },
            ground={"meadows": ["grass"], "plain": ["gravel"], "meadow": ["grass"]},
        ),
    )
    view = _View(place)
    assert view._terrain_footstep() == ["grass_step"]
    assert "gravel" not in view._terrain_sound_keys()


def test_plain_without_overlay_uses_base_terrain(monkeypatch):
    place = types.SimpleNamespace(
        type_name="plain",
        type_name_at=lambda x, y: "plain",
        high_ground=False,
        objects=[],
    )
    monkeypatch.setattr(
        audio_module,
        "style",
        _FakeStyle(
            {
                ("footman", "move"): ["default_step"],
                ("footman", "move_on_gravel"): ["gravel_step"],
            },
            ground={"plain": ["gravel"]},
        ),
    )
    view = _View(place)
    assert view._overlay_terrain_voices(place) == []
    assert view._terrain_sound_keys() == ["plain", "gravel"]
    assert view._terrain_footstep() == ["gravel_step"]

