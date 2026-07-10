Interfaccia inventario ed equipaggiamento
==========================================


Come le unità usano l'inventario (zaino), la schermata equipaggiamento e il modello oggetto dello stesso tipo in ``rules.txt`` (un tipo può essere sia oggetto raccoglibile sia arma/armatura equipaggiabile).


----


1. Panoramica
--------------



.. list-table::
   :header-rows: 1

   * - Schermata
     - Scorciatoia
     - Mostra
   * - Attributi
     - `Alt+V`
     - tutte le statistiche
   * - Zaino
     - `Shift+V`
     - tutti gli oggetti in inventario
   * - Equipaggiamento
     - `Ctrl+V`
     - armi e armature (equipaggiamento da inventario + integrato)



Una sola schermata alla volta. Seleziona esattamente un'unità amica.

Zaino vs equipaggiamento
~~~~~~~~~~~~~~~~~~~~~~~~~


- Zaino: equipaggia/usa/lascia cadere qualsiasi oggetto.
- Equipaggiamento: solo armi e armature. L'equipaggiamento integrato è etichettato «built-in weapon / built-in armor» (sola lettura).

Equipaggiamento misto integrato + oggetto
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


Quando un'unità ha sia equipaggiamento ``class weapon``/``class armor`` sia ``class item`` (es. ``weapons bow sword``):


.. list-table::
   :header-rows: 1

   * - Regola
     - Significato
   * - Priorità allo spawn
     - L'integrato è sempre equipaggiato per primo; l'equipaggiamento oggetto va nello zaino
   * - ``spawn_weapons_equipped 1`` (predefinito)
     - Le armi oggetto restano nello zaino e non si possono equipaggiare manualmente
   * - ``spawn_weapons_equipped 0``
     - Le armi oggetto nello zaino si possono equipaggiare
   * - Cambio
     - Solo integrato ↔ integrato; solo oggetto ↔ oggetto; nessun cambio incrociato
   * - Armatura
     - Stesso con ``spawn_armor_equipped``



Se l'unità ha solo equipaggiamento oggetto, i flag di spawn controllano l'equipaggiamento silenzioso alla creazione (predefinito attivo).


----


2. Controlli del giocatore
---------------------------


Apertura
~~~~~~~~~


- Esattamente 1 unità amica selezionata.
- Zaino: inventario non vuoto.
- Equipaggiamento: almeno un'arma o armatura (integrata o in inventario).

Nello zaino / equipaggiamento
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~



.. list-table::
   :header-rows: 1

   * - Tasto
     - Azione
   * - Frecce
     - oggetto precedente / successivo
   * - ``g``
     - leggi l'introduzione dell'oggetto (da ``style.txt``)
   * - ``Enter``
     - equipaggia arma / indossa armatura / usa consumabile
   * - ``Shift+Enter``
     - togli arma o armatura
   * - ``Delete``
     - lascia cadere (conferma, poi Enter)
   * - ``Shift+Delete``
     - lascia cadere senza conferma
   * - ``Esc``
     - chiudi / annulla il drop



Mondo
~~~~~~


- Raccolta: ``pickup`` (clic destro predefinito).
- Drop: ``drop`` o Delete nell'interfaccia.
- Dare: ``give`` — vedi `give-to-npc.md <give-to-npc.htm>`_.


----


3. Due sistemi di equipaggiamento
----------------------------------


3.1 Arma / armatura integrata (classico)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


.. code-block:: text

   def footman
   weapons sword          ; class weapon
   armor footman_armor    ; class armor


Non è nello zaino. La schermata equipaggiamento la mostra come built-in; non si può togliere né lasciare cadere dall'interfaccia.

3.2 Equipaggiamento da oggetto nello zaino (modello stesso tipo)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


.. code-block:: text

   def sword
   class item
   equippable_as_weapon 1
   mdg 3.5
   ...


Le statistiche si applicano mentre è equipaggiato; vengono rimosse al disequipaggiamento. Vedi ``res/rules.txt`` per gli esempi ``sword``, ``footman_armor``.


----


4. Spawn dell'equipaggiamento nello zaino
------------------------------------------


Allo spawn:

- `weapons <name>`: se il tipo è ``class item`` + ``equippable_as_weapon 1`` → istanza nello zaino; equipaggiamento silenzioso se non c'è arma integrata e ``spawn_weapons_equipped 1``.
- `armor <name>`: stesso per l'armatura.

Esempio di fante con spada oggetto + armatura oggetto: entrambe nello zaino, entrambe equipaggiate di default, visibili in Shift+V e Ctrl+V.

.. code-block:: text

   spawn_weapons_equipped 0/1   ; default 1
   spawn_armor_equipped 0/1     ; default 1


Arciere misto
~~~~~~~~~~~~~~


.. code-block:: text

   def archer
   weapons bow sword


- ``bow`` = ``class weapon`` → integrato, sempre equipaggiato.
- ``sword`` = ``class item`` → zaino; con il flag di spawn predefinito, la spada non si può equipaggiare mentre l'arco è integrato.

Imposta ``spawn_weapons_equipped 0`` per consentire l'equipaggiamento manuale della spada (ancora nessun cambio diretto arco↔spada).

Requisiti
~~~~~~~~~~



.. list-table::
   :header-rows: 1

   * - Campo
     - Nota
   * - ``inventory_capacity``
     - deve essere > 0
   * - ``transport_volume``
     - spazio per oggetto (predefinito 1); la capacità conta gli oggetti, non il volume




----


5. Lista di controllo per autori
---------------------------------


Solo integrato
~~~~~~~~~~~~~~~


.. code-block:: text

   def my_unit
   weapons short_sword
   armor light_armor


Raccoglibile, equipaggiabile, rimovibile
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


1. Definisci l'oggetto con ``equippable_as_weapon 1`` o ``equippable_as_armor 1``.
2. Unità: ``inventory_capacity`` + ``weapons my_sword``.
3. ``style.txt``: ``title``, ``intro``.

Consumabili
~~~~~~~~~~~~


.. code-block:: text

   def health_potion
   class item
   buffs heal


Usa con Enter nello zaino (``use_item``), non nella schermata equipaggiamento.


----


6. Ordini del server
---------------------



.. list-table::
   :header-rows: 1

   * - Ordine
     - Argomenti
     - 
   * - ``equip_weapon``
     - id oggetto
     - 
   * - ``unequip_weapon``
     - id oggetto
     - 
   * - ``equip_armor``
     - id oggetto
     - 
   * - ``unequip_armor``
     - id oggetto
     - 
   * - ``use_item``
     - id oggetto
     - 
   * - ``drop``
     - id oggetto
     - 



I trasferimenti di inventario al potenziamento/morfosi avvengono tramite ``transfer_inventory_to``.


----


7. FAQ
-------


D: Zaino vuoto sul fante?  
Un ``class weapon`` integrato non entra nello zaino finché il tipo non è ``class item`` con logica di spawn-in-inventario.

D: «Built-in armor» e non si può togliere?  
È ancora ``class armor``; aggiungi ``class item`` + ``equippable_as_armor 1``.

D: Stesso nome per oggetto e arma?  
Sì (modello stesso tipo): es. ``sword`` come oggetto per zaino/spawn; ``bow`` resta puro ``class weapon``.


----


8. File correlati
------------------



.. list-table::
   :header-rows: 1

   * - File
     - 
   * - ``res/ui/bindings.txt``
     - Shift+V, Ctrl+V
   * - ``soundrts/attributes/inventory_screen.py``
     - interfaccia zaino
   * - ``soundrts/attributes/equipment_screen.py``
     - interfaccia equipaggiamento
   * - ``soundrts/worldunit/worldbase.py``
     - logica di spawn / equipaggiamento
   * - ``res/rules.txt``
     - esempi



Vedi anche `give-to-npc <give-to-npc.htm>`_, `find-item-objective <find-item-objective.htm>`_.
