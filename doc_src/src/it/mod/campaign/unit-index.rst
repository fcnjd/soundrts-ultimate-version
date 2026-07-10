Selettori indice unità mappa (``killed_target`` / ``npc_has_item`` / ``unit_lost`` / ``building_lost`` / ``key_unit_killed``)
===============================================================================================================================


Quando più unità dello stesso tipo condividono una casella, usare :strong:```\<casella\> \<indice\> \<tipo\>`` per indicare
«la N-esima unità di quel tipo in quella casella» — non «una qualsiasi di esse» né «ucciderne N in totale».

Stessa sintassi di :strong:```transfer_units``, ``order`` e ``add_units``. Gli indici sono assegnati al
caricamento della mappa / allo spawn da trigger per ``(casella, tipo)`` e restano stabili dopo lo spostamento.


----


1. Trigger
----------



.. list-table::
   :header-rows: 1

   * - Condizione
     - Sintassi indice
     - Caso d'uso
   * - ``killed_target``
     - ``(killed_target \<indice\> \<tipo\> [enemy|ally])`` o forma con casella
   * - ``npc_has_item``
     - ``(npc_has_item \<indice\> \<tipo\> \<oggetto\>)`` o forma con casella
     - Bisogna consegnare l'oggetto a quel PNG specifico
   * - ``unit_lost``
     - ``(unit_lost \<indice\> \<tipo\>)`` o `` (unit_lost \<casella\> \<indice\> \<tipo\>)``
     - Quell'unità alleata con indice di spawn è scomparsa
   * - ``building_lost``
     - ``(building_lost \<indice\> \<tipo\>)`` o `` (building_lost \<casella\> \<indice\> \<tipo\>)``
     - Quell'edificio con indice di spawn è stato distrutto
   * - ``key_unit_killed``
     - ``(key_unit_killed \<indice\> \<tipo\>)`` o `` (key_unit_killed \<casella\> \<indice\> \<tipo\>)``
     - Quell'unità alleata con indice di spawn è stata uccisa



Le forme legacy funzionano ancora:

- `(killed_target <unit_id>)` — id unità globale
- `(killed_target <type> [enemy\|ally])` — qualsiasi uccisione di quel tipo
- `(npc_has_item <NPC_selector> <item> [square])` — tipo/id + casella corrente opzionale


----


2. Uccidere un'unità specifica (``killed_target``)
----------------------------------------------------


Completare l'obiettivo solo per la N-esima unità
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


.. code-block:: text

   computer_only 0 0 c3 3 demo_marker_footman
   
   trigger player1 (killed_target 3 demo_marker_footman enemy) (objective_complete 1)


Solo uccidere il 3° ``demo_marker_footman`` spawnato soddisfa la condizione (indipendente dalla casella).
Forma con casella: ``(killed_target c3 3 demo_marker_footman enemy)``.

Fallire se si uccide quello sbagliato
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


.. code-block:: text

   trigger player1 (killed_target 1 demo_marker_footman enemy) (do (cut_scene 7606) (defeat))
   trigger player1 (killed_target 2 demo_marker_footman enemy) (do (cut_scene 7606) (defeat))
   trigger player1 (killed_target 3 demo_marker_footman enemy) (do (cut_scene 7603) (objective_complete 1))


Uccidere #1 o #2 → cut scene + ``defeat``. Uccidere #3 → completa l'obiettivo 1.

vs ``has_killed``
~~~~~~~~~~~~~~~~~



.. list-table::
   :header-rows: 1

   * - Condizione
     - Significato
   * - ``(has_killed 3 footman enemy)``
     - Tre fanti nemici uccisi in totale
   * - ``(killed_target c3 3 footman enemy)``
     - Il 3° fante in C3 è stato ucciso



----


3. Consegnare a un PNG specifico (``npc_has_item``)
-----------------------------------------------------


.. code-block:: text

   computer_only 0 0 neutral b2 3 quest_npc
   short_sword a1
   
   trigger player1 (npc_has_item 3 quest_npc short_sword) (objective_complete 2)


Solo il 3° ``quest_npc`` spawnato conta (qualsiasi casella). Forma con casella: `` (npc_has_item b2 3 quest_npc short_sword)``.
Vedi `give-to-npc <give-to-npc.htm>`_ per ``give`` / ``receive_items``.


----


4. Proteggere un'unità o un edificio alleato specifico (sconfitta)
--------------------------------------------------------------------


Solo il fante #3 può morire
~~~~~~~~~~~~~~~~~~~~~~~~~~~~


.. code-block:: text

   player ... a1 3 footman raynor
   
   trigger player1 (unit_lost a1 3 footman) (defeat)
   trigger player1 (key_unit_killed a1 3 footman) (defeat)


Solo il primo municipio (indice di spawn globale)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


.. code-block:: text

   player ... b1 townhall raynor ...   ; chapter 2 base at B1 works too
   
   trigger player1 (building_lost 1 townhall) (defeat)


L'indice globale conta l'ordine di spawn per giocatore e per tipo, indipendentemente dalla casella:
- 1° municipio spawnato = municipio 1 (sia in A1 sia in B1)
- 2° spawnato = municipio 2; distruggere #2 non fa fallire questo trigger

Per la N-esima unità specifica di una casella, usare ``(building_lost a1 1 townhall)``.

vs forme legacy
~~~~~~~~~~~~~~~~



.. list-table::
   :header-rows: 1

   * - Condizione
     - Significato
   * - ``(unit_lost footman)``
     - Tutti i fanti del giocatore sono scomparsi
   * - ``(unit_lost a1 3 footman)``
     - Solo il 3° fante in A1 è scomparso
   * - ``(building_lost townhall)``
     - Tutti i municipi del giocatore sono distrutti
   * - ``(building_lost a1 1 townhall)``
     - Solo il 1° municipio in A1 è distrutto




----


5. Obiettivi multipli e cut scene
-----------------------------------


Gli obiettivi primari possono essere completati in qualsiasi ordine. Ogni ``cut_scene`` su ``objective_complete``
deve descrivere solo quell'obiettivo — non dire «tutti gli obiettivi completati» in un ramo;
la vittoria scatta automaticamente quando ogni obiettivo primario è fatto.

Bene:

.. code-block:: text

   trigger player1 (killed_target c3 3 demo_marker_footman enemy)
       (do (cut_scene 7603) (objective_complete 1))
   
   trigger player1 (npc_has_item b2 3 quest_npc short_sword)
       (do (cut_scene 7604) (objective_complete 2))


Male: testo della cut scene 7604 che afferma che entrambi gli obiettivi sono fatti mentre il giocatore potrebbe ancora dover uccidere il fante #3.


----


6. Demo: The Legend of Raynor capitolo 28
-------------------------------------------


File: ``res/single/The Legend of Raynor/28.txt``


.. list-table::
   :header-rows: 1

   * - Area
     - Contenuto
   * - A1
     - footman + peasant, ``short_sword`` a terra
   * - C3
     - 3 ``demo_marker_footman`` nemici
   * - B2
     - 3 ``quest_npc`` neutrali



Obiettivo 1: uccidere il 3° fante in C3 (uccisione sbagliata → sconfitta).  
Obiettivo 2: dare ``short_sword`` al 3° PNG in B2.


----


7. Codice e test
-----------------



.. list-table::
   :header-rows: 1

   * - Ruolo
     - Percorso
   * - Assegna indice allo spawn
     - ``triggers.py`` — ``\_assign_map_select_slot``
   * - Tracciamento uccisioni
     - ``record_unit_killed`` → ``\_killed_map_slots`` / ``\_units_killed_by``
   * - Condizioni
     - ``lang_killed_target``, ``lang_npc_has_item``, ``lang_unit_lost``, ``lang_building_lost``, ``lang_key_unit_killed``
   * - Test mappa
     - `test_give_item_to_npc.py::test_chapter_28_map_select_index_triggers`
   * - Test perdite
     - ``test_map_select_loss_triggers.py``



.. code-block:: text

   python -m pytest soundrts/tests/test_give_item_to_npc.py::test_chapter_28_map_select_index_triggers -q
   python -m pytest soundrts/tests/test_map_select_loss_triggers.py -q
