Objetivos progresivos de campaña (``register_objective``)
=========================================================

Para mapas de un jugador que revelan metas de una en una (completar meta 1, luego oír meta 2).

Referencia oficial de disparadores: ``mod/mapmaking.rst`` (Register_objective).

----

1. Problema
-----------

Cada ``add_objective`` hace dos cosas:

1. Muestra la meta en F9 y reproduce la voz de «nuevo objetivo».
2. Añade ese número al conjunto de requisitos de victoria.

Si un mapa solo llama ``add_objective 1`` al inicio y ``add_objective 2`` tras completar la meta 1, completar la meta 1 solía ganar la misión de inmediato — porque aún no existía la meta 2 en el conjunto de requisitos, o la lógica antigua trataba «todos los objetivos visibles hechos» como victoria.

----

2. Solución: ``register_objective``
-----------------------------------

Registra todos los números primarios por adelantado sin mostrarlos:

.. code-block:: text

   trigger player1 (timer 0) (do (register_objective 1 2 3) (add_objective 1 7001))
   trigger player1 (has barracks) (do (objective_complete 1) (add_objective 2 7002))
   trigger player1 (has 10 footman) (objective_complete 2)
   trigger player1 (has townhall) (objective_complete 3)

.. list-table::
   :header-rows: 1

   * - Acción
     - F9 / voz
     - Conjunto de victoria
   * - ``register_objective 1 2 3``
     - No
     - Añade 1, 2, 3 a ``\_required_objective_numbers``
   * - ``add_objective 1 …``
     - Sí
     - También añade 1 (si no estaba ya registrado)
   * - ``objective_complete 1``
     - Quita la meta 1 de F9
     - Añade 1 a ``\_completed_objective_numbers``

La victoria se produce cuando ``\_required_objective_numbers`` ⊆ ``\_completed_objective_numbers`` (``soundrts/worldplayerbase/base.py`` — ``\_all_required_objectives_done``).

----

3. Numeración de F9 y voz
-------------------------

Cuando hay más de un objetivo primario registrado o visible:

- F9 muestra «Objetivo primario N:» y luego la descripción (dos puntos tras el número).
- Con un solo objetivo primario, se omite el número.

El motor escanea los disparadores del mapa al cargar (``collect_planned_objective_numbers`` en ``soundrts/objective_announce.py``) para que los números sean correctos aunque las llamadas a ``add_objective`` vivan en disparadores ``timer 0`` separados.

Los objetivos opcionales (``add_secondary_objective``) usan numeración independiente con las mismas reglas.

----

4. Ejemplos en este repositorio
-------------------------------

.. list-table::
   :header-rows: 1

   * - Mapa
     - Patrón
   * - ``mods/starcraft/single/sc_build_tests/1.txt``
     - 2 metas Protoss encadenadas
   * - ``mods/starcraft/single/sc_late_game/1.txt``
     - 6 metas de final de partida encadenadas

----

5. Pruebas
----------

.. code-block:: bash

   python -m pytest soundrts/tests/test_campaign_alliance_transfer_triggers.py -k register_objective -q
   python -m pytest soundrts/tests/test_objective_announce.py -q
   python -m pytest soundrts/tests/test_cmd_objectives.py -q
