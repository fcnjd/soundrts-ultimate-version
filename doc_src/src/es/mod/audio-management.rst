Gestión de audio (refactorización P0–P2)
=========================================

SoundRTS 1.4.5.1 refactoriza el motor de audio del cliente en tres fases. **P0 / P1 / P2 son etapas de refactorización** (estructura → experiencia → pulido), **no** las tres capas de gritos de batalla, ni el valor numérico ``priority`` de ``psounds.play()`` para la preempción de canales.

Los gritos de batalla por capas (``shout_bg`` / ``shout_unit`` / ``shout_event``) están en :doc:`battle-shouts`.

.. contents::

Arquitectura
------------

::

  clientmain → clientmedia.init_media()
    ├─ sound.init()           pygame.mixer, canal 0 reservado para voz
    ├─ sounds.load_default()  indexa SFX en ui/, decodifica bajo demanda
    └─ voice.init()           cola de voz + TTS

  En ejecución:
    canal 0      → voz de interfaz / narración (VoiceChannel)
    canales 1..N → SFX del juego (SoundManager / psounds)
    flujo music  → música de fondo (pygame.mixer.music)

Módulos principales:

+---------------------------+------------------------------------------+
| Módulo                    | Función                                  |
+===========================+==========================================+
| ``lib/sound.py``          | mezcla, panorámica, canales, estado BGM  |
| ``lib/sound_cache.py``    | índice por capas, carga perezosa, precarga |
| ``lib/music_resolver.py`` | búsqueda menú/juego/batalla/victoria/derrota |
| ``lib/battle_music.py``   | máquina de estados música de combate     |
| ``lib/voice.py``          | cola de voz de la interfaz             |
| ``clientmedia.py``        | puntos de ajuste de volumen              |

P0 — refactorización estructural
--------------------------------

**Objetivos**: reducir el monolito ``sound.py``, controlar la memoria al cambiar de mod y corregir el estado mutable a nivel de clase.

**Módulo de resolución musical (``music_resolver.py``)**

- Centraliza ``find_music_file()`` y la búsqueda en paquetes de mapa/campaña.
- Helpers compartidos: ``find_map_or_campaign_asset()``, ``get_active_context()``, ``clear_music_cache()``.
- ``play_game_music``, ``play_battle_music`` y los stingers de victoria/derrota comparten la misma cadena de búsqueda.

**Reciclaje explícito de caché SFX (``sound_cache.clear_decoded()``)**

- En ``load_default()`` al cambiar mod/campaña/mapa: ``psounds.stop()``, limpiar marcas de tiempo de limitación, reconstruir capas.

**Corrección de estado de instancia**

- ``SoundSource``, ``LoopingSoundSource``, ``SoundManager`` mueven ``channel``, ``_sources``, ``_start_time`` a ``__init__``.

**Pruebas**: ``test_music_resolver.py``

P1 — experiencia y rendimiento
------------------------------

**Volumen SFX independiente (``sfx_volume``)**

- Clave de configuración ``audio/sfx_volume`` (predeterminado 0.5) en ``SoundRTS.ini``.
- **Voz/interfaz** usa ``main_volume``; **SFX de batalla** (pasos, combate, ambiente en bucle) usa ``sfx_volume``.
- En partida: ``cmd_sfx_volume``; ajustable en menú y durante la partida.

**Espera de voz sin bloqueo**

- ``voice._say_now()`` / ``flush()`` usan ``pygame.event.pump()`` + ``Clock.tick(30)`` en lugar de ``time.sleep(0.1)``.

**Fallback de música de menú unificado**

- ``_play_menu_music_with_fallback()`` fusiona la lógica duplicada en selector de campaña, creación de partida y lobby del servidor.

**Pruebas**: ``test_audio_settings.py``, ``test_voice_pump.py``

P2 — pulido
-----------

**P2a — ambiente suavizado**

- ``ambient_volume()`` usa un LFO lento basado en posición (~8 s) en lugar de ``random.random()`` por fotograma.

**P2b — controlador de música de combate (``battle_music.py``)**

- Centraliza comprobaciones de enemigos en visión y entrada/salida de BGM de combate.
- Sustituye la lógica dispersa en ``combat.py``, ``game_display.py``, ``game_navigation.py``.

**P2c — limpieza de ``music_resolver``**

- Elimina ramas inalcanzables; añade pruebas de búsqueda.

**P2d — SFX multiformato y precarga en caliente**

Los SFX del juego bajo ``ui/`` admiten:

- ``.ogg`` (preferido)
- ``.wav``
- ``.mp3``

Si varios formatos comparten el mismo stem, gana ``.ogg``. Los ID pueden escribirse como ``footstep``, ``footstep.wav`` o ``1029.mp3``.

Precarga en caliente: un hilo en segundo plano lee bytes; el hilo principal decodifica con ``tick_preload()`` (seguridad de hilos de pygame). Opcional en ``parameters.txt``::

  preload_sounds 4303,4304
  preload_decode_per_tick 6

**Pruebas**: ``test_ambient_stereo_volume.py``, ``test_battle_music.py``, ``test_sfx_formats.py``

Volúmenes y atajos
------------------

+------------------+----------------------------+----------------------------------+
| Volumen          | Clave de config            | Ajuste habitual                  |
+==================+============================+==================================+
| Voz / interfaz   | ``audio/main_volume``      | opcional (lectores externos)     |
+------------------+----------------------------+----------------------------------+
| SFX del juego    | ``audio/sfx_volume``       | Home subir / End bajar           |
+------------------+----------------------------+----------------------------------+
| Música           | ``audio/music_volume``     | Alt+Home / Alt+End               |
+------------------+----------------------------+----------------------------------+

Para autores de mods
--------------------

- Coloque los SFX en ``ui/`` o ``mods/<mod>/ui/``.
- Se recomienda ``.ogg`` por tamaño; ``.wav`` / ``.mp3`` funcionan sin conversión.
- Si ``ui/tts.txt`` ya define el mismo ID como texto, ese ID no se carga como sonido.

**No confundir con las capas de gritos**

+----------------------+--------------------------------+---------------------------+
| Concepto             | Significado                    | Documento                 |
+======================+================================+===========================+
| Refactor P0–P2       | módulos, volumen, formatos     | esta página               |
+----------------------+--------------------------------+---------------------------+
| Capas de gritos      | ``shout_bg`` / unidad / evento | :doc:`battle-shouts`      |
+----------------------+--------------------------------+---------------------------+
| Entero priority      | preempción en ``psounds.play`` | ``lib/sound.py``          |

Borradores anteriores de las notas de la versión 1.4.5.1 describían P0–P2 como capas de prioridad ambiental/combate/alertas; las notas de la versión ya están corregidas.
