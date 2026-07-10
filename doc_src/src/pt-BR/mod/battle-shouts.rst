Gritos de batalha (áudio de combate em camadas)
===============================================

Compilação só de escaramuça (sem formações de legião). Três camadas: **fundo do campo de batalha**, **voz da unidade**, **destaques de eventos**. Reprodução escalonada com cooldowns.

Código: ``battle_shout_audio.py``, ``combat.py``, ``formation_sound_queue.py``. Testes: ``test_battle_shout_audio.py``.

Gatilhos: qualquer lado tem ≥ **5** unidades lutando no quadrado. Cooldowns: 10 s global, 6 s por quadrado; 4 s para gritos de carga/crítico.

``style.txt``::

  def walking_unit
  shouts 1854

Referência completa (chinês): ``zh/mod/battle-shouts.rst``.
