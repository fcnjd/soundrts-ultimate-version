Guía avanzada de mods
=====================

Habilidades, facciones, progreso meta, IA — después de `Primeros pasos <getting-started.htm>`_. Mapas y campañas tienen sus propias guías.
.. contents::

----

Estructura de la carpeta del mod
--------------------------------

``rules.txt`` (núcleo), opcionales ``ai.txt``, ``ui/tts.txt``, ``ui/bindings.txt``, ``ui-xx/``.  
Ejemplos: ``mods/orc/``, ``mods/starcraft/``, ``mods/crazyMod9beta10/``.

----

Reglas: unidades y combate
--------------------------

Usa cadenas ``is_a``; adjunta habilidades con ``can_use_skill``.
Palabras clave completas: `Manual de modding <modding.htm>`_.  
Habilidades / curación / efectos: `Guía de habilidades <skills-and-effects.htm>`_ o `Manual de modding <modding.htm>`_.

----

IU, teclas rápidas, i18n
------------------------

- `Editor de teclas rápidas <hotkey-mapping-editor.htm>`_
- Enlaces por capas: `Teclas rápidas por capas <../player/layered-hotkeys.htm>`_
- i18n: `Internacionalización de mods <mod-i18n.htm>`_

----

IA

`Tutorial de IA <aimaking.htm>`_

----

Meta: logros, puntuación, cartas
--------------------------------

.. list-table::
   :header-rows: 1

   * - Sistema
     - Doc del mod
     - Doc del jugador
   * - Logros
     - `Sistema de logros <achievement-system.htm>`_
     - `Logros <../player/achievements.htm>`_
   * - Puntuación
     - `Sistema de notas <score-grading-system.htm>`_
     - `Puntuación y notas <../player/score-and-grades.htm>`_
   * - Cartas
     - `Cartas diferidas <delayed-card-loadout.htm>`_
     - `Cartas de carga <../player/loadout-cards.htm>`_

----

Mapas y campañas (guías aparte)
-------------------------------

- `Guía de mapas <map-guide.htm>`_ → `Manual de creación de mapas <mapmaking.htm>`_
- `Guía de campañas <campaign-guide.htm>`_
- `Mapas aleatorios <randommap.htm>`_

----

Índice
------

- `Manual de modding <modding.htm>`_
- `Notas de la versión <../relnotes.htm>`_
- `Índice de docs de mods <index.htm>`_

Volver a `Primeros pasos <getting-started.htm>`_
