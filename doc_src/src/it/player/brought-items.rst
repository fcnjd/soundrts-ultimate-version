# Portare un oggetto a una casella e consegna narrativa (``has_brought_item`` + ``remove_item``)

Due trigger usati insieme:

- ``has_brought_item`` (condizione): un'unità del giocatore porta un oggetto a una casella
- ``remove_item`` (azione): rimuove e distrugge l'oggetto dall'inventario (consegna narrativa «hand-in»)

Tipico: porta una pozione di mana al santuario → cut scene → la pozione scompare → obiettivo completato.

Esempio: The Legend of Raynor cap. 18 (`18.txt <../../../res/single/The Legend of Raynor/18.txt>`_).


----


1. Confronto con altri trigger sugli oggetti
---------------------------------------------



.. list-table::
   :header-rows: 1

   * - Trigger
     - Rileva / effetto
     - Posizione dell'oggetto
     - Caso d'uso
   * - ``has_item``
     - il giocatore possiede l'oggetto
     - inventario di qualsiasi unità
     - trovato / raccolto
   * - ``has_brought_item``
     - oggetto portato alla casella
     - unità su quella casella
     - consegna arrivando (senza depositare)
   * - ``find``
     - oggetto a terra
     - lasciato sulla casella
     - piazzare l'oggetto; sintassi: casella prima ``(find c3 mana_potion)``
   * - ``npc_has_item``
     - l'NPC ha ricevuto l'oggetto
     - inventario NPC / ``received_items``
     - dare a un NPC
   * - ``remove_item``
     - distruggi dall'inventario
     - —
     - consegna narrativa automatica



----


2. Condizione: ``has_brought_item``
--------------------------------------


.. code-block:: text

   (has_brought_item <square> <item_type> [count])


- Casella: es. ``c3``, `"3,3"`
- Tipo di oggetto: es. ``mana_potion``
- Quantità: opzionale, predefinita `1`

Vera quando almeno un'unità viva del giocatore su quella casella ha abbastanza dell'oggetto in inventario.

- Mani vuote sulla casella → falsa
- Oggetto altrove, unità non sulla casella → falsa
- Portato alla casella → vera (non serve depositarlo)


----


3. Azione: ``remove_item``
------------------------------


.. code-block:: text

   (remove_item <item_type> [square] [count])


- Senza casella: rimuove da tutte le unità vive del giocatore
- Con casella: solo le unità su quella casella
- Quantità: opzionale, predefinita `1`

L'oggetto viene distrutto (come se fosse consumato). Abbinalo a ``cut_scene`` per la narrazione.


----


4. Esempio completo (cap. 18)
-------------------------------


.. code-block:: text

   trigger player1 (has_brought_item c3 mana_potion)
       (do (cut_scene 7560) (remove_item mana_potion c3) (objective_complete 1))



Concatena più azioni con ``do``. Non usare ``if`` per tre azioni in fila.

Flusso: raccogli la pozione → cammina fino al santuario c3 → condizione vera → cut scene → oggetto rimosso → obiettivo 1 completato.


----


5. Confronto con dare-a-NPC
-----------------------------



.. list-table::
   :header-rows: 1

   * - Metodo
     - Quando
   * - ``npc_has_item`` + ``give`` del giocatore
     - ricevente NPC fisico
   * - ``has_brought_item`` + ``remove_item``
     - arrivo-e-consegna, senza NPC, storia automatica



----


6. File correlati
------------------



.. list-table::
   :header-rows: 1

   * - Contenuto
     - Percorso
   * - Implementazione
     - ``soundrts/worldplayerbase/triggers.py``
   * - Mappa di esempio
     - `res/single/The Legend of Raynor/18.txt`
   * - Trovare un oggetto
     - [find-item-objective.md](find-item-objective.htm)
   * - Dare a un NPC
     - [give-to-npc.md](give-to-npc.htm)
