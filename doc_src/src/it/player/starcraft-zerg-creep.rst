Mod StarCraft: creep Zerg e tumori della Regina
================================================


Mod: attiva ``mods = starcraft`` in ``SoundRTS.ini``.

Parole chiave delle regole: ``mod/modding.rst`` (Build fields). Guide Terran/Protoss: `starcraft-terran.htm <starcraft-terran-addons.htm>`_, `starcraft-resources.htm <starcraft-resources-vespene.htm>`_.


----


1. Due proprietà di raggio
---------------------------


Impostane una per ogni fornitore di creep/psi; lascia l'altra a 0.


.. list-table::
   :header-rows: 1

   * - Proprietà
     - Portata
     - Note
   * - ``build_field_radius``
     - passi BFS in caselle dalla casella dell'edificio
     - Caselle discrete; stile legacy
   * - ``build_field_radius_m``
     - Metri dalla posizione ``(x, y)`` dell'edificio
     - Stessa scala del raggio d'attacco; una casella di mappa ≈ 12 m



Valori predefiniti del mod StarCraft:


.. list-table::
   :header-rows: 1

   * - Edificio
     - Raggio
   * - Hatchery
     - ``build_field_radius_m 12``
   * - Creep tumor
     - ``build_field_radius_m 4``
   * - Nexus
     - `18 m`
   * - Pylon
     - `12 m`




----


2. Creep vivo vs creep marcato
--------------------------------



.. list-table::
   :header-rows: 1

   * - Tipo
     - Significato
   * - Vivo
     - Emesso attualmente da un Hatchery/tumore in piedi (senti il creep muovendoti nelle vicinanze)
   * - Marcato
     - Vernice persistente sulla casella + diffusione (``build_field_persists``, ``build_field_spreads``)



- Gli edifici Zerg richiedono una casella marcata (``requires_build_field_on_square 1``).
- Entrare su creep marcato visibile può annunciare l'etichetta del campo.
- Dopo la morte dell'Hatchery, il creep marcato resta; puoi ancora costruirci sopra.

Gli Hatchery a raggio metrico verniciano anche i segni quando ``build_field_persists`` / ``build_field_spreads`` è impostato — altrimenti potresti sentire il creep vivo ma ricevere «non puoi costruire qui».


----


3. Diffusione
--------------


``build_field_spreads 1`` — ogni secondo di gioco, i segni di creep si espandono di un livello verso le caselle adiacenti (``build_field_spread_squares N`` per una diffusione più rapida).

Mappa di test: ``mods/starcraft/multi/zerg_creep_test.txt``.


----


4. Tumori di creep della Regina (stile SC2)
---------------------------------------------


Addestra la Queen dal Queen's Nest (richiede Spawning Pool).


.. list-table::
   :header-rows: 1

   * - Abilità
     - Costo
     - Portata
     - Regola del bersaglio
   * - Spawn creep tumor
     - 25 mana, 20 s di lancio
     - 11
     - Casella con creep vivo o marcato
   * - Extend creep tumor (sul tumore)
     - 12 s di lancio
     - 8
     - Solo casella con creep marcato



- Spawn piazza un edificio invisibile ``creep_tumor`` sulla casella bersaglio.
- Ogni tumore fornisce 4 m di creep e si diffonde come il creep dell'Hatchery.
- Extend concatena i tumori verso siti di costruzione lontani (non puoi saltare sul bordo solo-vivo — bisogna attendere diffusione/marca).

Mappa di test: ``mods/starcraft/multi/zerg_creep_tumor_test.txt``.

Attributi del modder su ``class skill``:

.. code-block:: text

   summon_requires_build_field creep
   summon_requires_marked_field 1    ; extend only



----


5. Lista di controllo rapida
-----------------------------


1. L'Hatchery vernicia il creep → attendi la diffusione o usa i tumori della Queen per raggiungere caselle lontane.
2. Costruisci strutture Zerg solo su creep marcato (F9/obiettivi non c'entrano).
3. Spire / pool / extractor sul creep residuo dopo la morte dell'Hatchery — passo 2 di ``zerg_creep_test``.
