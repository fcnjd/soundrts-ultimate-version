RMG hero and civilization strategic systems
============================================

This layer adds Heroes of Might and Magic-style hero progression and
Civilization-style city management to SoundRTS random maps (Random Map
Generator, RMG). The game remains real-time strategy: yields and combat
resolve on game time, not turns.


----


1. How to enable
----------------

From the main menu choose **Start a game → Random map** and begin a match.
Every newly generated RMG map writes ``rmg_strategic_systems 1`` and enables
heroes, city yields, culture, diplomacy points, technologies, and policies.

Hand-made maps and non-RMG sessions do not enable these rules by default. If a
mod does not define ``rmg_hero``, the generator skips hero placement without
breaking map load.


----


2. Hero progression
-------------------

Each player starts with one ``rmg_hero``:

- Starts at level 1, maximum level 8.
- Gains experience in combat and levels up automatically.
- Each level increases hit points, melee damage, and mana capacity.
- Heroes have their own mana pool; skills spend mana and mana regenerates.
- At most one RMG hero per player at a time.
- In **local single-player RMG**, the highest level and experience reached are
  saved per mod and faction and restored in the next match. Multiplayer and
  replays do not read local hero saves (avoids client desync).

Cross-match hero profile
~~~~~~~~~~~~~~~~~~~~~~~~

- Save path: under the user config directory, sibling to ``achievements``:
  ``rmg_heroes/<mod_key>/<faction>.json`` (e.g. ``human.json``).
- Written at match end with peak level and XP; applied at the next match start
  to ``rmg_hero``, including unlocked level skills.
- Only **local single-player random maps** (``TrainingGame``). Campaign,
  multiplayer, replay, and spectator modes do not use this file.
- Separate from campaign ``campaign_carryover``: ``rmg_hero`` keeps
  ``campaign_carryover 0`` in rules; RMG persistence uses dedicated JSON, not
  ``campaigns.ini``.

Skill tree
~~~~~~~~~~

.. list-table::
   :header-rows: 1

   * - Level
     - Skill
     - Mana cost
     - Effect
   * - 2
     - Arcane bolt
     - 20
     - Magic damage to one target
   * - 4
     - Whirlwind
     - 35
     - Damage enemies in melee range
   * - 6
     - Meteor shower
     - 60
     - Area damage at long range

Skills unlock automatically at the listed levels. Select the hero and use the
skill command menu; insufficient mana blocks casting.


----


3. City expansion and tile yields
---------------------------------

Town halls, keeps, and castles count as cities. Mod-compatible bases that both
**provide survival** and **store resources** are also treated as cities.

Each city owns its home square as territory. Select a city, use **Purchase
tile**, then pick a main map square adjacent to that city's current territory.
Tiles cannot be double-claimed. The first purchased tile costs 20 gold; each
additional purchase adds 10 gold. A newly built city always claims its home
square.

Every 60 seconds, each living city and each worked tile pays out once.

Base yield per city
~~~~~~~~~~~~~~~~~~~

Each city pays per tick:

- 6 gold
- 4 wood
- 4 food
- 4 culture
- 1 diplomacy point

City terrain bonus
~~~~~~~~~~~~~~~~~~

The city's RMG terrain adds to the base yield:

.. list-table::
   :header-rows: 1

   * - Terrain
     - Extra yield
   * - Hill, plateau, high rocky plain, mountain pass
     - +3 gold
   * - Forest, dense forest, marsh
     - +3 wood
   * - Plain, town, meadows
     - +3 food
   * - Lake, river, creek, ford
     - +1 gold, +2 food

Resource yields count toward **total gathered** and can satisfy RMG economic
victory. After each tick the local player hears city count, culture total, and
diplomacy total.

Citizens and tile improvements
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Select a city and use **Assign citizen to gold / wood / food / culture**, then
pick an owned tile. If citizen slots are full, the oldest assignment is
released:

- 1 base slot per city.
- Urban planning and civic administration each add 1 slot.
- Keep or castle adds 1 more slot.

Worked tiles pay terrain-based yields and can build a **mine**, **lumber
mill**, or **farm** for +3 gold, +3 wood, or +3 food per tick. Costs: mine
15 gold + 10 wood; lumber mill 10 gold + 15 wood; farm 10 gold + 5 wood + 10
food.

Worked tile base yield (every 60 s, before improvements and focus):

- 1 gold, 1 wood, 1 food per tile.
- Same terrain bonuses as the city table above.
- Citizen focus: +2 gold, +2 wood, +2 food, or +3 culture (culture focus does
  not add the +2 resource bonus).

Purchase cost: first expansion 20 gold, then +10 gold per tile bought (city
home square is free).


3.1 City strategic commands
---------------------------

With a town hall, keep, or castle selected in an RMG match, the command menu
includes (select target square, then confirm):

.. list-table::
   :header-rows: 1

   * - Command (voice)
     - Keyword
     - Effect
   * - Purchase tile (5718)
     - ``rmg_buy_tile``
     - Buy an adjacent unowned main square
   * - Assign citizen to gold (5719)
     - ``rmg_assign_gold``
     - Work a owned tile for gold
   * - Assign citizen to wood (5720)
     - ``rmg_assign_wood``
     - Work for wood
   * - Assign citizen to food (5721)
     - ``rmg_assign_food``
     - Work for food
   * - Assign citizen to culture (5722)
     - ``rmg_assign_culture``
     - +3 culture per minute on that tile
   * - Build mine (5723)
     - ``rmg_build_mine``
     - +3 gold per tick on that tile
   * - Build lumber mill (5724)
     - ``rmg_build_lumber_mill``
     - +3 wood per tick
   * - Build farm (5725)
     - ``rmg_build_farm``
     - +3 food per tick
   * - Activate tradition policy (5726)
     - ``rmg_switch_tradition``
     - Switch among unlocked policies at no culture cost
   * - Activate commerce policy (5727)
     - ``rmg_switch_commerce``
     - Same
   * - Activate diplomacy policy (5728)
     - ``rmg_switch_diplomacy``
     - Same

Policy switch commands appear only for researched policies that are not
currently active. Invalid targets announce command failure.


----


4. Technology tree
------------------

Research at any city:

.. list-table::
   :header-rows: 1

   * - Technology
     - Requires
     - Effect
   * - Urban planning
     - —
     - +2 gold, wood, and food per city per tick
   * - Civic administration
     - Urban planning
     - +2 culture per city per tick
   * - Foreign service
     - Civic administration
     - +1 diplomacy point per city per tick

Technologies cost normal gold, wood, and food. Non-RMG games hide ``rmg_``
research entries.


----


5. Culture and policy cards
---------------------------

Culture is an in-match strategic stat (not shown on the resource bar). Cities
generate culture each minute; adopting a policy spends culture once.

Policy cards
~~~~~~~~~~~~

.. list-table::
   :header-rows: 1

   * - Policy
     - Culture cost
     - Requires
     - Effect
   * - Tradition
     - 40
     - Urban planning
     - +50% culture yield
   * - Commerce
     - 80
     - Civic administration
     - +25% city gold, wood, and food
   * - Diplomacy
     - 120
     - Foreign service
     - Double diplomacy point yield

At most **two** policies are active. Researching a third unlocks it and
**replaces the oldest active** policy. After that, any city can **Activate
tradition / commerce / diplomacy policy** to switch among unlocked policies
for free; replaced policies stay unlocked.

Policies appear in research only when you have enough culture.

Computer players pick fixed combinations by situation and research
prerequisites in order (urban planning → policy → civic administration → …):

.. list-table::
   :header-rows: 1

   * - AI / situation
     - Preferred pair
   * - Aggressive (``aggressive`` / ``rush`` / ``hard`` …)
     - Commerce + tradition
   * - Standard with ≥ 2 enemies
     - Diplomacy + commerce
   * - Other
     - Tradition + commerce

AI skips policies outside its plan and does not queue the same policy while
culture is insufficient.


----


6. Diplomacy points
-------------------

Cities generate diplomacy points each minute; foreign service and the diplomacy
policy increase output.

In RMG with strategic systems, **sending an alliance request** costs 20
diplomacy points:

- No points spent if you cannot afford it.
- Points are deducted only when the request is sent.
- Accept, decline, withdraw, or leave an alliance is free.
- The 60-second cooldown per target still applies.
- Nomadic or city-less mod setups are not blocked by diplomacy costs.

Neutral creeps cannot join diplomacy.


6.1 Viewing culture and diplomacy
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Culture and diplomacy **do not** use the main resource bar (Z / X / Shift+Z) or
stay announced like wood or food. On RMG matches with ``rmg_strategic_systems``:

.. list-table::
   :header-rows: 1

   * - Method
     - Action
   * - Global hotkeys
     - **B** — current culture; **Shift+B** — current diplomacy points
   * - City attributes
     - Select your town hall / keep / castle, open attributes (Alt+V), **U** for culture, **Y** for diplomacy
   * - Periodic voice
     - Every 60 s ``rmg_strategic_tick`` still reports city count, culture total, diplomacy total
   * - Change alerts
     - If resource-change alerts are enabled, culture/diplomacy changes are voiced too

On non-RMG maps, **B** / **Shift+B** only beep.


----


7. Mod compatibility
--------------------

RMG gameplay architecture
~~~~~~~~~~~~~~~~~~~~~~~~~~~

Random maps combine an **engine framework** (generator, four victory modes,
trigger API, optional Civ-style strategic systems) with **rules and template
data**. Default values and whether strategic systems are enabled live in
``rules.txt`` ``def parameters``; ``cfg/randommap/*.txt`` templates override
them per skirmish setup. Mods extend RMG by editing rules and templates—no
Python changes. Hand-written ``map.txt`` files allow fully custom victory
conditions.

Strategic numbers, tile improvements, diplomatic trades, and victory goals are
all rule-driven in ``rules.txt``.

Global parameters (``def parameters``)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1

   * - Key
     - Default
     - Meaning
   * - ``rmg_diplomacy_request_cost``
     - 20
     - Diplomacy spent to send an alliance request
   * - ``rmg_tile_purchase_base``
     - 20
     - Gold for the first purchased tile
   * - ``rmg_tile_purchase_step``
     - 10
     - Extra gold per additional purchased tile
   * - ``rmg_policy_slot_limit``
     - 2
     - Active policy cards at once
   * - ``rmg_trade_cooldown``
     - 60
     - Default diplomatic trade cooldown (seconds)
   * - ``rmg_economic_goal``
     - 3000
     - Economic victory: total ``resource1`` gathered
   * - ``rmg_economic_goal_fast`` / ``_macro`` / ``_lanes``
     - 2000 / 5000 / 2500
     - Per-template economic goals
   * - ``rmg_survival_seconds``
     - 900
     - Survival hold time (seconds, non-fast templates)
   * - ``rmg_survival_seconds_fast``
     - 600
     - Survival hold time for fast template
   * - ``rmg_exploration_ruin_pairs_small`` / ``_medium`` / ``_large``
     - 1 / 2 / 2
     - Symmetric ancient-ruin *pairs* (each pair = two mirrored ruins)
   * - ``rmg_exploration_ruin_pairs_bonus``
     - 1
     - Extra pairs when exploration victory mode is selected
   * - ``rmg_strategic_systems``
     - 1
     - Enable Civ-style RMG systems on generated maps

Tile improvements (``rmg_tile_*`` buildings)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

On any RMG tile building:

- ``rmg_tile_improvement 1`` — marks a strategic tile improvement
- ``rmg_improvement_key mine`` — short internal key (optional; default strips ``rmg_tile_`` prefix)
- ``rmg_tile_yield 3 0 0 0 0`` — per 60 s while a worker is on tile: gold / wood / food / culture / diplomacy

Build cost and time still use normal ``cost`` / ``time_cost``.

Diplomatic trades (``rmg_trade_*`` upgrades)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Built-in example:

.. code-block:: text

   def rmg_trade_resource2
   class upgrade
   rmg_trade 1
   rmg_trade_id resource2
   rmg_trade_pay 50 0 0
   rmg_trade_gain 0 100 0

- ``rmg_trade_id`` — wire token (``resource1`` / ``resource2`` / ``resource3`` recommended)
- ``rmg_trade_pay`` — visible resources paid by buyer
- ``rmg_trade_gain`` — visible resources received from AI
- ``rmg_trade_diplomacy_cost`` — extra diplomacy cost (optional)
- ``rmg_trade_alliance 1`` — alliance on success (open-borders style)
- ``rmg_trade_cooldown 90`` — per-trade cooldown override (seconds, optional)

F12 hotkeys still map to ``resource2`` / ``resource3`` / ``open_borders``; new
trades need ``diplomacy_bindings.txt`` entries and
``diplomacy trade <rmg_trade_id> <player>``.

Victory modes and custom challenges (``cfg/randommap/*.txt``)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Per-template overrides (example):

.. code-block:: text

   random_map_template
   name space_survival
   extends fast
   title space survival
   default_victory_mode survival
   survival_seconds 1200
   exploration_ruin_pairs 2
   economic_goal 8000
   strategic_systems 0

- ``default_victory_mode`` — auto-select victory mode when this template is chosen
- ``strategic_systems 0`` — disable culture/diplomacy/tile purchase (pure RTS, e.g. sci-fi reskin)
- Command centres need not be ``townhall``: any building with ``provides_survival 1`` and ``storable_resource_types``

**Fifth and custom victory modes** — ``victory_triggers`` block (full trigger lines):

.. code-block:: text

   victory_triggers
   trigger players (timer 60 60) (if (has_gathered 5000 resource2) (victory))
   end_victory_triggers

The generator writes your victory triggers and still adds ``no_building_left`` /
``no_unit_left`` defeat triggers. See ``res/randommap/example.txt``.

Other compatibility notes
~~~~~~~~~~~~~~~~~~~~~~~~~

Rule-driven behaviour:

- ``rmg_hero`` must exist for a starting hero.
- Non-standard command centres with ``provides_survival`` and
  ``storable_resource_types`` count as cities.
- Cities gain RMG tech and policy research dynamically.
- Non-RMG maps filter ``rmg_`` research.
- Rules store building ``can_research`` as ``_rules_can_research`` so ``Building.can_research`` ``@property`` works; ``townhall`` no longer lists ``rmg_*`` in rules—``effective_can_research()`` injects them on RMG maps only.
- Mods with fewer than three resources only get yields for existing slots.

Key rule fields:

.. code-block:: text

   culture_cost 40
   rmg_policy 1

Map triggers may also use:

.. code-block:: text

   (rmg_strategic_tick)
   (rmg_has_culture 100)
   (rmg_has_diplomacy 20)
   (rmg_grant_culture 25)
   (rmg_grant_diplomacy 10)


----


8. Implementation
-----------------

- Strategic runtime: ``soundrts/rmg_systems.py``
- City commands: ``soundrts/worldorders/strategic.py``
- Cross-match hero saves: ``soundrts/rmg_progress.py``
- RMG map hook: ``soundrts/randommap.py``
- Map flag: ``soundrts/world/world_map.py``
- Culture on research: ``soundrts/worldorders/production.py``
- Diplomacy spend: ``soundrts/worldplayerbase/base.py``
- AI policy order: ``soundrts/worldplayercomputer.py``
- Hero save hooks: ``soundrts/game.py``
- Triggers: ``soundrts/worldplayerbase/triggers.py``
- Rules: ``res/rules.txt``
- Voice/style: ``res/ui/style.txt``, ``res/ui/tts.txt``, ``res/ui-zh/tts.txt`` (5702–5728; culture/diplomacy status 5716–5717)
- Culture/diplomacy UI: ``soundrts/clientgame/game_resources.py``, ``soundrts/attributes/basic_attributes.py``
- Tests: ``soundrts/tests/test_rmg_systems.py``, ``soundrts/tests/test_randommap.py``


----


9. Current boundaries
---------------------

Still real-time minute ticks — no Civ5 turns, citizen population growth, road
maintenance, or diplomacy UI. Territory is tracked per RMG main square and
does not change unit movement rights. Cross-match hero growth applies only to
local single-player random maps, not multiplayer.
