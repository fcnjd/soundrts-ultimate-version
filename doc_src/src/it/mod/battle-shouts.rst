Urla di battaglia (audio di combattimento a livelli)
====================================================

Build solo skirmish (senza formazioni legione). Tre livelli: **sfondo del campo di battaglia**, **voce delle unità**, **evidenziazioni degli eventi**. Riproduzione scaglionata con cooldown.

**Nota**: questi «tre livelli» non sono le **fasi P0–P2 di refactor del motore audio**; vedi :doc:`audio-management`.

Codice: ``battle_shout_audio.py``, ``combat.py``, ``formation_sound_queue.py``. Test: ``test_battle_shout_audio.py``.

Attivazione: almeno una delle due parti ha ≥ **5** unità in combattimento nella casella. Cooldown: 10 s globali, 6 s per casella; 4 s per urla di evento carica/critico.

``style.txt``::

  def walking_unit
  shouts 1854

Questo documento è il riferimento completo in italiano.
