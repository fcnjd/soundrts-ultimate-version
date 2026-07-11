"""Rules metadata for ``class terrain`` definitions (not a map entity)."""


class TerrainRules:
    is_a = ()
    expanded_is_a = ()
    is_dynamic = 1
    is_high_ground = 0
    is_water = 0
    is_ground = 1
    is_air = 1
    height = 0
    blocks_path = 0
    passable_units = ()  # unset in rules -> use is_ground/is_air/is_water
    speed = ()  # optional ground/air multipliers, e.g. .5 1
    cover = ()  # optional ground/air cover, e.g. .5 0
    speed_vs = ()  # unit-specific speed multipliers, e.g. knight .25 archer .5
    cover_vs = ()  # unit-specific ranged cover, e.g. archer .25
    dodge_vs = ()  # unit-specific dodge, e.g. archer .1 (= +10%)
    mdg_vs = ()  # unit-specific melee damage %, e.g. knight -.33 (= -33%)
    rdg_vs = ()  # unit-specific ranged damage %
    mdg_cd_vs = ()  # unit-specific melee cooldown %, e.g. knight .5 (= +50% cd)
    rdg_cd_vs = ()  # unit-specific ranged cooldown %
    rmg_terrain = 0
    rmg_border = 0
    rmg_water = 0
    rmg_ford = 0
