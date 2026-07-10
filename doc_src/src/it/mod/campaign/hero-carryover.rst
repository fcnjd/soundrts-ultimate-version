Trasporto eroi di campagna (guidato dalle rules)
=================================================


Le campagne single-player possono far persistere un eroe designato tra i capitoli. Tutto si configura in :strong:```rules.txt`` / ``campaign.txt`` — nessun nome unità hard-coded. In cooperativo gli eroi non persistono (sincronizzazione di rete).

Panoramica giocatore: `../player/campaign-and-co-op-improvements <../player/campaign-and-co-op-improvements.htm>`_ §2.1.1.

Cinese: `../../zh/mod/战役跨章英雄携带说明 <../../zh/mod/战役跨章英雄携带说明.htm>`_.


----


1. Tre meccanismi inter-capitolo
---------------------------------



.. list-table::
   :header-rows: 1

   * - Meccanismo
     - Dove
     - Cosa porta
     - Uso tipico
   * - ``campaign_carryover``
     - campi unità in ``rules.txt``
     - Livello+XP, inventario (split opzionale)
     - Crescita eroe RPG
   * - ``campaign_flag``
     - trigger di mappa
     - Booleani di storia
     - Alleanze, missioni secondarie
   * - ``add_inventory_item``
     - trigger di mappa
     - Oggetti specifici
     - Gettoni, chiavi




----


2. Campi ``rules.txt``
--------------------------


Impostare sulla def eroe radice (le varianti via ``is_a`` ereditano).


.. list-table::
   :header-rows: 1

   * - Campo
     - Default
     - Significato
   * - ``campaign_carryover``
     - ``0``
     - ``1`` = abilita salvataggio inter-capitolo
   * - ``campaign_carryover_id``
     - nome def
     - prefisso ``campaigns.ini`` `hero_<id>_`
   * - ``campaign_carryover_stats``
     - ``1`` con carryover attivo
     - Livello + XP
   * - ``campaign_carryover_inventory``
     - ``1`` con carryover attivo
     - Oggetti nello zaino



Esempi
~~~~~~


Carryover completo (default):

.. code-block:: text

   def my_hero
   is_a knight
   campaign_carryover 1
   inventory_capacity 8
   max_level 20
   xp_threshold_growth linear 100 50
   hp_max_per_level 20


(``xp_thresholds 200 500 1000`` esplicito funziona ancora.)

``Livello / XP iniziali (``level`` / ``xp``):``

Come nella sezione Heroes di ``mod/modding.rst`` (incluso ``xp_threshold_growth`` da 1.4.4.7):


.. list-table::
   :header-rows: 1

   * - Campo
     - Significato
   * - ``level``
     - Livello iniziale (default `1`). Valori `> 1` applicano i `*_per_level` cumulativi e ``level_skills`` allo spawn.
   * - ``xp``
     - XP cumulativa iniziale opzionale.
   * - ``level 0``
     - Inizia sotto il livello 1; lo stato mostra livello 0 e XP verso `xp_thresholds[0]`.



Il ripristino inter-capitolo sovrascrive i default della mappa; il livello salvato si combina con ``hero_min_level``, poi i bonus cumulativi vengono riapplicati.

Solo stats (niente inventario):

.. code-block:: text

   campaign_carryover 1
   campaign_carryover_inventory 0


Solo inventario (niente stats):

.. code-block:: text

   campaign_carryover 1
   campaign_carryover_stats 0


Niente carryover: omettere ``campaign_carryover 1``.


----


3. ``campaign.txt``: livello minimo
---------------------------------------


.. code-block:: text

   hero_min_level 13:2 16:3 19:4


Coppie capitolo:livello; il livello ripristinato è ``max(salvato, minimo)``.


----


4. File di salvataggio (``user/campaigns.ini``)
--------------------------------------------------


.. code-block:: ini

   hero_raynor_xp = 1200
   hero_raynor_level = 3
   hero_raynor_inventory = sword,health_potion
   flags = ch24_garrek_token


Aggiornato solo in vittoria; un nuovo tentativo dopo una sconfitta non sovrascrive.


----


5. Codice
---------


- `soundrts/campaign_hero.py <../../../soundrts/campaign_hero.py>`_
- `soundrts/tests/test_campaign_hero.py <../../../soundrts/tests/test_campaign_hero.py>`_


----


6. Cooperativo
--------------


Nessun ripristino/salvataggio eroe; anche ``campaign_flag`` è un no-op deterministico in cooperativo.
