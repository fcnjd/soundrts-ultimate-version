Primi passi con le mod
======================


La tua prima patch e la prima unità funzionante — non ancora mappe o campagne. Continua con: `Guida avanzata alle mod <advanced.htm>`_.
-------------------------------------------------------------------------------------------------------------------------------

Cosa modifichi
--------------

Una mod è una cartella di file di testo. Salva, ricarica la mappa o riavvia il gioco.

.. list-table::
   :header-rows: 1

   * - File
     - Ruolo
   * - ``rules.txt``
     - Unità, tecnologia, abilità (questa guida)
   * - ``style.txt`` + ``ui/tts.txt``
     - Nomi e battute vocali
   * - ``ai.txt``
     - Strategia del computer (più avanti)

Riferimento alle parole chiave: `Manuale di modding <modding.htm>`_.

----

Passo 1: cartella e attivazione
-------------------------------

Metti la mod in ``user/mods/mymod/``. Attivala in ``user/SoundRTS.ini``:

.. code-block:: ini

   mods = mymod

Le mod successive nell’elenco sovrascrivono quelle precedenti. Scorciatoia di sviluppo: ``python soundrts.py --mods=mymod``

----

Passo 2: prova in due righe
---------------------------

``user/mods/mymod/rules.txt``:

.. code-block:: text

   def peasant
   decay 20

I contadini spariscono dopo circa 20 secondi — la mod è caricata.

Mod solo audio: copia ``mods/soundpack/`` oppure usa Opzioni → soundpack.

----

Passo 3: leggere rules.txt
--------------------------

.. code-block:: text

   def my_soldier
   class soldier
   is_a footman
   hp 120
   mdg 8

- ``def`` — inizia una definizione
- ``class`` — soldier, building, skill, …
- ``is_a`` — eredita, poi sovrascrivi i campi
- ``clear`` in cima al file — sostituisce i valori predefiniti invece di fare patch

Fazioni: ``def orc_faction`` + ``class faction``.

----

Passo 4: i nomi che i giocatori sentono
---------------------------------------

.. code-block:: text

   ; ui/style.txt — title 7801
   ; ui/tts.txt — 7801 Heavy Infantry

Vedi `i18n delle mod <mod-i18n.htm>`_ (documento in cinese; lo schema è universale).

----

Passo 5: test
-------------

Partita singola contro il computer; Ctrl+Shift+F2 rivela la mappa (solo, unico umano).  
Log: ``user/tmp/client.log``

Significato dei campi lato giocatore: `Inventario <../player/inventory.htm>`_ · `Comportamenti predefiniti <../player/unit-default-behavior.htm>`_

----

E dopo?
--------

.. list-table::
   :header-rows: 1

   * - Obiettivo
     - Leggi
   * - Mod completa, abilità, fazioni
     - `Guida avanzata <advanced.htm>`_ · `Manuale di modding <modding.htm>`_
   * - Prima mappa
     - `Guida alle mappe <map-guide.htm>`_
   * - Campagna
     - `Guida alle campagne <campaign-guide.htm>`_
   * - Note di rilascio
     - `Note di rilascio <../relnotes.htm>`_

Torna all’`Indice documentazione mod <index.htm>`_
