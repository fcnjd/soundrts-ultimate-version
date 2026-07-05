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

