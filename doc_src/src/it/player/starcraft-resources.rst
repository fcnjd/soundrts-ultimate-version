Mod StarCraft — minerali e vespene
===================================


Mod: ``mods/starcraft`` (``mods = starcraft`` in ``SoundRTS.ini``).

Risorse
--------


- Minerali (``resource1``): premi Z
- Vespene (``resource2``): premi X

Sintassi della mappa:

.. code-block:: text

   mineral_field 1500 a1
   geyser 1 e1


Strutture del gas
------------------


Assimilator / Extractor / Refinery devono essere costruiti su un geyser (Tab sul geyser, poi costruisci). Costruire su terreno edificabile riproduce «non puoi costruire lì».

Dopo il completamento:

1. La struttura produce automaticamente (``auto_production``): ogni ``production_time`` secondi aggiunge ``production_qty`` di vespene nell'edificio (predefinito 18 s / 8 unità)
2. I lavoratori raccolgono dall'edificio del gas (``can_gather assimilator``, ecc.) e trasportano ``extraction_qty`` per viaggio (predefinito 8)
3. Il vespene viene depositato al Nexus / Hatchery / Command Center (``storable_resource_types resource1 resource2``)

Usa auto_production per il gas, non auto_cultivate in stile fattoria (le fattorie ripartono solo quando il deposito è vuoto).

Schermata attributi
--------------------


Seleziona una struttura del gas e premi V per sentire requires deposit (nome del tipo di deposito, es. geyser). Tempo e quantità di produzione usano le voci di attributo di produzione già esistenti.

Riferimento alle regole: ``mod/modding.rst`` (Economy and Deposits & gas).

Mappa di test: ``mods/starcraft/multi/sc_resources_test.txt``.
