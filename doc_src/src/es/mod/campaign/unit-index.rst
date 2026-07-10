Selectores de índice de unidad en el mapa (``killed_target`` / ``npc_has_item`` / ``unit_lost`` / ``building_lost`` / ``key_unit_killed``)
==========================================================================================================================================

Cuando varias unidades del mismo tipo comparten una casilla, usa :strong:```\<square\> \<index\> \<type\>`` para significar
«la N-ésima unidad de ese tipo en esa casilla» — no «cualquiera de ellas» ni «matar N en total».

Misma sintaxis que :strong:```transfer_units``, ``order`` y ``add_units``. Los índices se asignan al
cargar el mapa / al generar por disparador por ``(square, type)`` y permanecen estables tras moverse la unidad.

----

1. Disparadores
---------------

.. list-table::
   :header-rows: 1

   * - Condición
     - Sintaxis de índice
     - Caso de uso
   * - ``killed_target``
     - ``(killed_target \<index\> \<type\> [enemy|ally])`` o forma con casilla
   * - ``npc_has_item``
     - ``(npc_has_item \<index\> \<type\> \<item\>)`` o forma con casilla
     - Debe dar el objeto a ese PNJ concreto
   * - ``unit_lost``
     - ``(unit_lost \<index\> \<type\>)`` o `` (unit_lost \<square\> \<index\> \<type\>)``
     - Esa unidad amiga de índice de aparición ya no está
   * - ``building_lost``
     - ``(building_lost \<index\> \<type\>)`` o `` (building_lost \<square\> \<index\> \<type\>)``
     - Ese edificio de índice de aparición está destruido
   * - ``key_unit_killed``
     - ``(key_unit_killed \<index\> \<type\>)`` o `` (key_unit_killed \<square\> \<index\> \<type\>)``
     - Esa unidad amiga de índice de aparición fue matada

Las formas heredadas siguen funcionando:

- `(killed_target <unit_id>)` — id global de unidad
- `(killed_target <type> [enemy\|ally])` — cualquier muerte de ese tipo
- `(npc_has_item <NPC_selector> <item> [square])` — tipo/id + casilla actual opcional

----

2. Matar una unidad concreta (``killed_target``)
------------------------------------------------

Completar objetivo solo para la N-ésima unidad
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: text

   computer_only 0 0 c3 3 demo_marker_footman
   
   trigger player1 (killed_target 3 demo_marker_footman enemy) (objective_complete 1)

Solo matar al 3.er ``demo_marker_footman`` generado satisface la condición (agnóstico de casilla).
Forma con casilla: ``(killed_target c3 3 demo_marker_footman enemy)``.

Fallar con muerte incorrecta
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: text

   trigger player1 (killed_target 1 demo_marker_footman enemy) (do (cut_scene 7606) (defeat))
   trigger player1 (killed_target 2 demo_marker_footman enemy) (do (cut_scene 7606) (defeat))
   trigger player1 (killed_target 3 demo_marker_footman enemy) (do (cut_scene 7603) (objective_complete 1))

Matar #1 o #2 → escena + ``defeat``. Matar #3 → completar objetivo 1.

frente a ``has_killed``
~~~~~~~~~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1

   * - Condición
     - Significado
   * - ``(has_killed 3 footman enemy)``
     - Tres footmen enemigos matados en total
   * - ``(killed_target c3 3 footman enemy)``
     - El 3.er footman en C3 fue matado

----

3. Dar a un PNJ concreto (``npc_has_item``)
-------------------------------------------

.. code-block:: text

   computer_only 0 0 neutral b2 3 quest_npc
   short_sword a1
   
   trigger player1 (npc_has_item 3 quest_npc short_sword) (objective_complete 2)

Solo cuenta el 3.er ``quest_npc`` generado (cualquier casilla). Forma con casilla: `` (npc_has_item b2 3 quest_npc short_sword)``.
Consulta `give-to-npc <give-to-npc.htm>`_ para ``give`` / ``receive_items``.

----

4. Proteger una unidad o edificio amigo concreto (derrota)
----------------------------------------------------------

Solo el footman #3 puede morir
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: text

   player ... a1 3 footman raynor
   
   trigger player1 (unit_lost a1 3 footman) (defeat)
   trigger player1 (key_unit_killed a1 3 footman) (defeat)

Solo el primer ayuntamiento (índice global de aparición)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: text

   player ... b1 townhall raynor ...   ; chapter 2 base at B1 works too
   
   trigger player1 (building_lost 1 townhall) (defeat)

El índice global cuenta el orden de aparición por jugador por tipo, independientemente de la casilla:
- 1.er ayuntamiento generado = ayuntamiento 1 (ya sea en A1 o B1)
- 2.º generado = ayuntamiento 2; destruir #2 no falla este disparador

Para la N-ésima unidad específica de casilla, usa ``(building_lost a1 1 townhall)``.

frente a formas heredadas
~~~~~~~~~~~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1

   * - Condición
     - Significado
   * - ``(unit_lost footman)``
     - Todos los footmen del jugador han desaparecido
   * - ``(unit_lost a1 3 footman)``
     - Solo el 3.er footman en A1 ha desaparecido
   * - ``(building_lost townhall)``
     - Todos los ayuntamientos del jugador están destruidos
   * - ``(building_lost a1 1 townhall)``
     - Solo el 1.er ayuntamiento en A1 está destruido

----

5. Múltiples objetivos y escenas
--------------------------------

Los objetivos primarios pueden terminarse en cualquier orden. Cada ``cut_scene`` en ``objective_complete``
debe describir solo ese objetivo — no digas «todos los objetivos completos» en una rama;
la victoria se ejecuta automáticamente cuando todos los objetivos primarios están hechos.

Bien:

.. code-block:: text

   trigger player1 (killed_target c3 3 demo_marker_footman enemy)
       (do (cut_scene 7603) (objective_complete 1))
   
   trigger player1 (npc_has_item b2 3 quest_npc short_sword)
       (do (cut_scene 7604) (objective_complete 2))

Mal: texto de escena 7604 afirmando que ambos objetivos están hechos cuando el jugador aún puede necesitar matar al footman #3.

----

6. Demo: The Legend of Raynor capítulo 28
-----------------------------------------

Archivo: ``res/single/The Legend of Raynor/28.txt``

.. list-table::
   :header-rows: 1

   * - Área
     - Contenido
   * - A1
     - footman + peasant, ``short_sword`` en el suelo
   * - C3
     - 3 ``demo_marker_footman`` enemigos
   * - B2
     - 3 ``quest_npc`` neutrales

Objetivo 1: matar al 3.er footman en C3 (muerte incorrecta → derrota).  
Objetivo 2: dar ``short_sword`` al 3.er PNJ en B2.

----

7. Código y pruebas
-------------------

.. list-table::
   :header-rows: 1

   * - Función
     - Ruta
   * - Asignar índice al generar
     - ``triggers.py`` — ``\_assign_map_select_slot``
   * - Seguimiento de muertes
     - ``record_unit_killed`` → ``\_killed_map_slots`` / ``\_units_killed_by``
   * - Condiciones
     - ``lang_killed_target``, ``lang_npc_has_item``, ``lang_unit_lost``, ``lang_building_lost``, ``lang_key_unit_killed``
   * - Prueba de mapa
     - `test_give_item_to_npc.py::test_chapter_28_map_select_index_triggers`
   * - Pruebas de pérdida
     - ``test_map_select_loss_triggers.py``

.. code-block:: text

   python -m pytest soundrts/tests/test_give_item_to_npc.py::test_chapter_28_map_select_index_triggers -q
   python -m pytest soundrts/tests/test_map_select_loss_triggers.py -q
