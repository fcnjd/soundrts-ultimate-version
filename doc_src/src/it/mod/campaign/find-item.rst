# Vittoria per oggetto trovato (trigger ``has_item``)

Progettare obiettivi in cui raccogliere un oggetto completa lo scopo.

Condizione centrale: :strong:```has_item`` — il giocatore detiene l'oggetto nell'inventario di un'unità viva?


----


1. Panoramica
---------------



.. list-table::
   :header-rows: 1

   * - Parte
     - Nome
     - Ruolo
   * - Campo unità
     - ``class item``
     - oggetto raccoglibile
   * - Ordine predefinito
     - ``pickup``
     - clic destro su oggetto a terra
   * - Condizione
     - ``has_item``
     - il giocatore detiene il tipo di oggetto



Flusso: piazzare oggetto → pickup → ``(has_item …)`` → `` (objective_complete N)`` → vittoria quando tutti gli obiettivi sono fatti.


Non impostare ``consume_on_pickup 1`` (default 0). Se consumato al pickup, ``has_item`` non diventa mai vero.


----


2. ``has_item``
-------------------


.. code-block:: text

   (has_item <item_type> [count])


Conta gli oggetti negli inventari di tutte le unità vive del giocatore.

.. code-block:: text

   (has_item lost_amulet)
   (has_item lost_amulet 2)



.. list-table::
   :header-rows: 1

   * - Condizione
     - Controlla
   * - ``has``
     - conteggio unità possedute
   * - ``has_item``
     - oggetti in inventario
   * - ``has_brought_item``
     - portato su una casella
   * - ``npc_has_item``
     - PNG ha ricevuto l'oggetto
   * - ``find``
     - oggetto a terra sulla casella




----


3. Definire l'oggetto missione
--------------------------------


.. code-block:: text

   def lost_amulet
   class item


Il raccoglitore deve avere ``inventory_capacity \> 0`` (peasant, footman, …).


----


4. Piazzare sulla mappa
-------------------------


.. code-block:: text

   lost_amulet c3
   lost_amulet 2 c3



----


5. Esempio (cap. 17)
----------------------


Vedi `17.txt <../../../res/single/The Legend of Raynor/17.txt>`_:

.. code-block:: text

   trigger player1 (timer 0) (add_objective 1 "find the lost amulet")
   trigger player1 (has_item lost_amulet) (objective_complete 1)



----


6. Composto: cap. 20 (trasporto + uso in inventario)
------------------------------------------------------


`mystery_treasure <../../../res/single/The Legend of Raynor/20.txt>`_: raccogliere → ``has_brought_item b2`` → usare al santuario (``use_square b2``) → ricompensa in oro.


----


7. Composto: cap. 22 (lasciare + raccogliere monete)
-----------------------------------------------------


`sealed_treasure <../../../res/single/The Legend of Raynor/22.txt>`_: lasciare in b2 → ``find`` + ``remove_ground_item`` → spawn ``gold_coin`` → raccoglierle tutte.


----


8. Composto: cap. 23 (lasciare = consegnare)
---------------------------------------------


`war_supplies <../../../res/single/The Legend of Raynor/23.txt>`_: ``has_item`` poi ``find c3 war_supplies`` dopo il drop.


.. list-table::
   :header-rows: 1

   * - Capitolo
     - Oggetto
     - Consegna
   * - 20
     - ``mystery_treasure``
     - trasporto + uso in inventario
   * - 22
     - ``sealed_treasure``
     - lasciare, aprire, raccogliere monete
   * - 23
     - ``war_supplies``
     - lasciare alla stazione




----


9. Cap. 24–27
---------------


Raccogliere ``secret_letter`` in ``b1`` (stesso flusso di ``has_item``), poi dare al leader (``npc_has_item``). Vedi `campaign-northern-arc.htm <campaign-secret-letter-alliance.htm>`_.


----


10. Implementazione
---------------------


- ``lang_has_item`` in ``soundrts/worldplayerbase/triggers.py``
- Esempio: `res/single/The Legend of Raynor/17.txt`, ``rules.txt`` (``lost_amulet``)
