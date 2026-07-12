Gestione audio (refactor P0–P2)
================================

SoundRTS 1.4.5.1 refactorizza il motore audio client in tre fasi. **P0 / P1 / P2 sono fasi di refactor** (struttura → UX → rifinitura), **non** i tre livelli di urla di battaglia, né il valore numerico ``priority`` di ``psounds.play()`` per la preempt delle casse.

Le urla di battaglia a livelli (``shout_bg`` / ``shout_unit`` / ``shout_event``) sono in :doc:`battle-shouts`.

.. contents::

Architettura
------------

::

  clientmain → clientmedia.init_media()
    ├─ sound.init()           pygame.mixer, canale 0 riservato alla voce
    ├─ sounds.load_default()  indicizza SFX in ui/, decodifica on demand
    └─ voice.init()           coda voce + TTS

  Runtime:
    canale 0      → voce UI / narrazione (VoiceChannel)
    canali 1..N   → SFX di gioco (SoundManager / psounds)
    stream music  → musica di sottofondo (pygame.mixer.music)

Moduli principali:

+---------------------------+------------------------------------------+
| Modulo                    | Ruolo                                    |
+===========================+==========================================+
| ``lib/sound.py``          | mix, pan stereo, canali, stato BGM       |
| ``lib/sound_cache.py``    | indice a livelli, lazy load, preload     |
| ``lib/music_resolver.py`` | lookup menu/gioco/battaglia/vittoria/sconfitta |
| ``lib/battle_music.py``   | state machine musica di combattimento    |
| ``lib/voice.py``          | coda voce parlata                        |
| ``clientmedia.py``        | punti di regolazione volume              |

P0 — refactor strutturale
-------------------------

**Obiettivi**: ridurre il monolite ``sound.py``, controllare la memoria al cambio mod, correggere lo stato mutabile a livello di classe.

**Modulo risolutore musica (``music_resolver.py``)**

- Centralizza ``find_music_file()`` e la ricerca nei pacchetti mappa/campagna.
- Helper condivisi: ``find_map_or_campaign_asset()``, ``get_active_context()``, ``clear_music_cache()``.
- ``play_game_music``, ``play_battle_music`` e gli stinger vittoria/sconfitta condividono la stessa catena di lookup.

**Riciclo esplicito cache SFX (``sound_cache.clear_decoded()``)**

- Su ``load_default()`` al cambio mod/campagna/mappa: ``psounds.stop()``, azzera timestamp di rate-limit, ricostruisce i livelli.

**Fix stato istanza**

- ``SoundSource``, ``LoopingSoundSource``, ``SoundManager`` spostano ``channel``, ``_sources``, ``_start_time`` in ``__init__``.

**Test**: ``test_music_resolver.py``

P1 — UX e prestazioni
---------------------

**Volume SFX di gioco separato (``sfx_volume``)**

- Chiave config ``audio/sfx_volume`` (default 0.5) in ``SoundRTS.ini``.
- **Voce/UI** usa ``main_volume``; **SFX di battaglia** (passi, combattimento, ambience in loop) usa ``sfx_volume``.
- In partita: ``cmd_sfx_volume``; regolabile da menu e in match.

**Attesa voce non bloccante**

- ``voice._say_now()`` / ``flush()`` usano ``pygame.event.pump()`` + ``Clock.tick(30)`` invece di ``time.sleep(0.1)``.

**Fallback musica menu unificato**

- ``_play_menu_music_with_fallback()`` unifica la logica duplicata in selezione campagna, creazione partita e lobby server.

**Test**: ``test_audio_settings.py``, ``test_voice_pump.py``

P2 — rifinitura
---------------

**P2a — ambiente smussato**

- ``ambient_volume()`` usa un LFO lento basato sulla posizione (~8 s) invece di ``random.random()`` per frame.

**P2b — controller musica di battaglia (``battle_music.py``)**

- Centralizza controlli nemici in visione e ingresso/uscita BGM di combattimento.
- Sostituisce la logica sparsa in ``combat.py``, ``game_display.py``, ``game_navigation.py``.

**P2c — pulizia ``music_resolver``**

- Rimuove rami irraggiungibili; aggiunge test di lookup.

**P2d — SFX multiformato e preload a caldo**

Gli SFX di gioco sotto ``ui/`` supportano:

- ``.ogg`` (preferito)
- ``.wav``
- ``.mp3``

Se più formati condividono lo stesso stem, vince ``.ogg``. Gli ID possono essere scritti come ``footstep``, ``footstep.wav`` o ``1029.mp3``.

Preload a caldo: thread in background legge i byte; il thread principale decodifica con ``tick_preload()`` (thread safety pygame). Opzionale in ``parameters.txt``::

  preload_sounds 4303,4304
  preload_decode_per_tick 6

**Test**: ``test_ambient_stereo_volume.py``, ``test_battle_music.py``, ``test_sfx_formats.py``

Volumi e tasti rapidi
---------------------

+------------------+----------------------------+----------------------------------+
| Volume           | Chiave config              | Regolazione tipica               |
+==================+============================+==================================+
| Voce / UI        | ``audio/main_volume``      | opzionale (screen reader esterni)|
+------------------+----------------------------+----------------------------------+
| SFX di gioco     | ``audio/sfx_volume``       | Home su / End giù               |
+------------------+----------------------------+----------------------------------+
| Musica           | ``audio/music_volume``     | Alt+Home / Alt+End               |
+------------------+----------------------------+----------------------------------+

Per autori di mod
-----------------

- Mettere gli SFX in ``ui/`` o ``mods/<mod>/ui/``.
- ``.ogg`` resta consigliato per le dimensioni; ``.wav`` / ``.mp3`` funzionano senza conversione.
- Se ``ui/tts.txt`` definisce già lo stesso ID come testo, quell'ID non viene caricato come audio.

**Da non confondere con i livelli di urla**

+----------------------+--------------------------------+---------------------------+
| Concetto             | Significato                    | Documento                 |
+======================+================================+===========================+
| Refactor P0–P2       | moduli, volume, formati        | questa pagina             |
+----------------------+--------------------------------+---------------------------+
| Livelli urla         | ``shout_bg`` / unità / evento  | :doc:`battle-shouts`      |
+----------------------+--------------------------------+---------------------------+
| Intero priority      | preempt in ``psounds.play``    | ``lib/sound.py``          |

Bozze precedenti delle note di rilascio 1.4.5.1 descrivevano P0–P2 come livelli di priorità ambientale/combattimento/avvisi; le note di rilascio sono state corrette.
