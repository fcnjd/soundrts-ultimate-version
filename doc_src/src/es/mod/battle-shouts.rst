Gritos de batalla (audio de combate por capas)
==============================================

Compilación solo escaramuza (sin formaciones de legión). Tres capas: **fondo del campo de batalla**, **voz de unidad**, **destacados de eventos**. Reproducción escalonada con tiempos de reutilización.

Código: ``battle_shout_audio.py``, ``combat.py``, ``formation_sound_queue.py``. Pruebas: ``test_battle_shout_audio.py``.

Disparadores: cualquiera de los bandos tiene ≥ **5** unidades combatiendo en la casilla. Tiempos de reutilización: 10 s global, 6 s por casilla; 4 s para gritos de carga/crítico.

``style.txt``::

  def walking_unit
  shouts 1854

Referencia completa (chino): ``zh/mod/battle-shouts.rst``.
