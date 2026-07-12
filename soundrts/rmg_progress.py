"""Local, cross-match progression for the single-player RMG hero."""

from __future__ import annotations

import json
import os

from .lib.log import warning
from .paths import CONFIG_DIR_PATH, current_mod_key


def hero_progress_path(faction=None) -> str:
    directory = os.path.join(CONFIG_DIR_PATH, "rmg_heroes", current_mod_key())
    try:
        os.makedirs(directory, exist_ok=True)
    except OSError:
        pass
    key = str(faction or "_default").replace("/", "_").replace("\\", "_")
    return os.path.join(directory, f"{key}.json")


def load_hero_progress(faction=None) -> dict:
    path = hero_progress_path(faction)
    if not os.path.isfile(path):
        return {"level": 1, "xp": 0}
    try:
        with open(path, encoding="utf-8") as stream:
            data = json.load(stream)
    except (OSError, json.JSONDecodeError, TypeError):
        warning("couldn't read RMG hero progress: %s", path)
        return {"level": 1, "xp": 0}
    return {
        "level": max(1, int(data.get("level", 1) or 1)),
        "xp": max(0, int(data.get("xp", 0) or 0)),
    }


def save_hero_progress(player) -> bool:
    heroes = [
        unit
        for unit in getattr(player, "units", ()) or ()
        if getattr(unit, "type_name", None) == "rmg_hero"
    ]
    peak_level = int(getattr(player, "rmg_hero_peak_level", 1) or 1)
    peak_xp = int(getattr(player, "rmg_hero_peak_xp", 0) or 0)
    if not heroes and peak_level <= 1 and peak_xp <= 0:
        return False
    hero = (
        max(heroes, key=lambda unit: (getattr(unit, "level", 1), getattr(unit, "xp", 0)))
        if heroes
        else None
    )
    faction = getattr(player, "faction", None)
    previous = load_hero_progress(faction)
    current = {
        "level": max(previous["level"], peak_level, int(getattr(hero, "level", 1) or 1)),
        "xp": max(previous["xp"], peak_xp, int(getattr(hero, "xp", 0) or 0)),
    }
    path = hero_progress_path(faction)
    try:
        tmp = path + ".tmp"
        with open(tmp, "w", encoding="utf-8") as stream:
            json.dump(current, stream, ensure_ascii=False, indent=2)
            stream.write("\n")
        os.replace(tmp, path)
    except OSError:
        warning("couldn't write RMG hero progress: %s", path)
        return False
    return True


def apply_hero_progress(player) -> bool:
    progress = load_hero_progress(getattr(player, "faction", None))
    player.rmg_hero_peak_level = progress["level"]
    player.rmg_hero_peak_xp = progress["xp"]
    changed = False
    for hero in getattr(player, "units", ()) or ():
        if getattr(hero, "type_name", None) != "rmg_hero":
            continue
        from .level_up_stats import apply_level_up_to

        apply_level_up_to(hero, progress["level"], notify=False)
        hero.xp = max(int(getattr(hero, "xp", 0) or 0), progress["xp"])
        changed = True
    return changed
