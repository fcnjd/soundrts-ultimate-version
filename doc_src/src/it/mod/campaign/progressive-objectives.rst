Obiettivi di campagna progressivi (``register_objective``)
============================================================


Per mappe single-player che rivelano gli obiettivi uno alla volta (completa l'obiettivo 1, poi senti l'obiettivo 2).

Riferimento ufficiale ai trigger: ``mod/mapmaking.rst`` (Register_objective).


----


1. Problema
-------------


Ogni ``add_objective`` fa due cose:

1. Mostra l'obiettivo in F9 e riproduce la voce «nuovo obiettivo».
2. Aggiunge quel numero all'insieme dei requisiti di vittoria.

Se una mappa chiama solo ``add_objective 1`` all'inizio e ``add_objective 2`` dopo che l'obiettivo 1 è completato, completare l'obiettivo 1 faceva vincere subito la missione — perché l'obiettivo 2 non esisteva ancora nell'insieme dei requisiti, oppure la vecchia logica trattava «tutti gli obiettivi visibili fatti» come vittoria.


----


2. Soluzione: ``register_objective``
----------------------------------------


Registra tutti i numeri primari in anticipo senza mostrarli:

.. code-block:: text

   trigger player1 (timer 0) (do (register_objective 1 2 3) (add_objective 1 7001))
   trigger player1 (has barracks) (do (objective_complete 1) (add_objective 2 7002))
   trigger player1 (has 10 footman) (objective_complete 2)
   trigger player1 (has townhall) (objective_complete 3)



.. list-table::
   :header-rows: 1

   * - Azione
     - F9 / voce
     - Insieme vittoria
   * - ``register_objective 1 2 3``
     - No
     - Aggiunge 1, 2, 3 a ``\_required_objective_numbers``
   * - ``add_objective 1 …``
     - Sì
     - Aggiunge anche 1 (se non già registrato)
   * - ``objective_complete 1``
     - Rimuove l'obiettivo 1 da F9
     - Aggiunge 1 a ``\_completed_objective_numbers``



La vittoria scatta quando ``\_required_objective_numbers`` ⊆ ``\_completed_objective_numbers`` (``soundrts/worldplayerbase/base.py`` — ``\_all_required_objectives_done``).


----


3. Numerazione F9 e voce
--------------------------


Quando più di un obiettivo primario è registrato o visibile:

- F9 mostra «Primary objective N:» poi la descrizione (due punti dopo il numero).
- Con un solo obiettivo primario, il numero è omesso.

Il motore scansiona i trigger della mappa al caricamento (``collect_planned_objective_numbers`` in ``soundrts/objective_announce.py``) così i numeri sono corretti anche quando le chiamate ``add_objective`` vivono in trigger ``timer 0`` separati.

Gli obiettivi opzionali (``add_secondary_objective``) usano una numerazione indipendente con le stesse regole.


----


4. Esempi in questo repository
--------------------------------



.. list-table::
   :header-rows: 1

   * - Mappa
     - Schema
   * - ``mods/starcraft/single/sc_build_tests/1.txt``
     - 2 obiettivi Protoss a catena
   * - ``mods/starcraft/single/sc_late_game/1.txt``
     - 6 obiettivi late-game a catena




----


5. Test
---------


.. code-block:: bash

   python -m pytest soundrts/tests/test_campaign_alliance_transfer_triggers.py -k register_objective -q
   python -m pytest soundrts/tests/test_objective_announce.py -q
   python -m pytest soundrts/tests/test_cmd_objectives.py -q
