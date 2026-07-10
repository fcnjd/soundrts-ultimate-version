Guida avanzata alle mod
=======================


Abilità, fazioni, progresso meta, IA — dopo `Primi passi <getting-started.htm>`_. Mappe e campagne hanno guide dedicate.
.. contents::

----

Struttura della cartella mod
----------------------------

``rules.txt`` (nucleo), opzionali ``ai.txt``, ``ui/tts.txt``, ``ui/bindings.txt``, ``ui-xx/``.  
Esempi: ``mods/orc/``, ``mods/starcraft/``, ``mods/crazyMod9beta10/``.

----

Regole: unità e combattimento
-----------------------------

Usa catene ``is_a``; collega le abilità con ``can_use_skill``.
Parole chiave complete: `Manuale di modding <modding.htm>`_.  
Abilità / cure / effetti: `Guida alle abilità <skills-and-effects.htm>`_ oppure `Manuale di modding <modding.htm>`_.

----

UI, tasti rapidi, i18n
----------------------

- `Editor mappatura tasti <hotkey-mapping-editor.htm>`_
- Binding a livelli: `Tasti a livelli <../player/layered-hotkeys.htm>`_
- i18n: `i18n delle mod <mod-i18n.htm>`_ (documento in cinese; lo schema è universale)

----

IA
--

`Tutorial IA <aimaking.htm>`_

----

Meta: achievement, punteggio, carte
-----------------------------------

.. list-table::
   :header-rows: 1

   * - Sistema
     - Doc mod
     - Doc giocatore
   * - Achievement
     - `Sistema achievement <achievement-system.htm>`_
     - `Achievement <../player/achievements.htm>`_
   * - Punteggio
     - `Valutazione punteggio <score-grading-system.htm>`_
     - `Punteggio e voti <../player/score-and-grades.htm>`_
   * - Carte
     - `Carte ritardate <delayed-card-loadout.htm>`_
     - `Carte di loadout <../player/loadout-cards.htm>`_

----

Mappe e campagne (guide separate)
---------------------------------

- `Guida alle mappe <map-guide.htm>`_ → `Manuale di creazione mappe <mapmaking.htm>`_
- `Guida alle campagne <campaign-guide.htm>`_
- `Mappe casuali <randommap.htm>`_

----

Indice
------

- `Manuale di modding <modding.htm>`_
- `Note di rilascio <../relnotes.htm>`_
- `Indice documentazione mod <index.htm>`_

Torna a `Primi passi <getting-started.htm>`_
