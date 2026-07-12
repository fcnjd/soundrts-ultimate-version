Gerenciamento de áudio (refatoração P0–P2)
==========================================

O SoundRTS 1.4.5.1 refatora o motor de áudio do cliente em três fases. **P0 / P1 / P2 são etapas de refatoração** (estrutura → experiência → polimento), **não** as três camadas de gritos de batalha, nem o valor numérico ``priority`` de ``psounds.play()`` para preempt de canais.

Gritos de batalha em camadas (``shout_bg`` / ``shout_unit`` / ``shout_event``) estão em :doc:`battle-shouts`.

.. contents::

Arquitetura
-----------

::

  clientmain → clientmedia.init_media()
    ├─ sound.init()           pygame.mixer, canal 0 reservado para voz
    ├─ sounds.load_default()  indexa SFX em ui/, decodifica sob demanda
    └─ voice.init()           fila de voz + TTS

  Em execução:
    canal 0      → voz da interface / narração (VoiceChannel)
    canais 1..N  → SFX do jogo (SoundManager / psounds)
    stream music → música de fundo (pygame.mixer.music)

Módulos principais:

+---------------------------+------------------------------------------+
| Módulo                    | Função                                   |
+===========================+==========================================+
| ``lib/sound.py``          | mixagem, pan estéreo, canais, estado BGM |
| ``lib/sound_cache.py``    | índice em camadas, lazy load, preload    |
| ``lib/music_resolver.py`` | busca menu/jogo/batalha/vitória/derrota  |
| ``lib/battle_music.py``   | máquina de estados da música de combate  |
| ``lib/voice.py``          | fila de voz da interface                 |
| ``clientmedia.py``        | pontos de ajuste de volume               |

P0 — refatoração estrutural
---------------------------

**Objetivos**: reduzir o monólito ``sound.py``, controlar memória ao trocar de mod e corrigir estado mutável em nível de classe.

**Módulo resolvedor de música (``music_resolver.py``)**

- Centraliza ``find_music_file()`` e busca em pacotes de mapa/campanha.
- Helpers compartilhados: ``find_map_or_campaign_asset()``, ``get_active_context()``, ``clear_music_cache()``.
- ``play_game_music``, ``play_battle_music`` e stingers de vitória/derrota compartilham a mesma cadeia de busca.

**Reciclagem explícita do cache SFX (``sound_cache.clear_decoded()``)**

- Em ``load_default()`` ao trocar mod/campanha/mapa: ``psounds.stop()``, limpa timestamps de rate-limit, reconstrói camadas.

**Correção de estado de instância**

- ``SoundSource``, ``LoopingSoundSource``, ``SoundManager`` movem ``channel``, ``_sources``, ``_start_time`` para ``__init__``.

**Testes**: ``test_music_resolver.py``

P1 — experiência e desempenho
-----------------------------

**Volume SFX de jogo separado (``sfx_volume``)**

- Chave de config ``audio/sfx_volume`` (padrão 0.5) em ``SoundRTS.ini``.
- **Voz/interface** usa ``main_volume``; **SFX de batalha** (passos, combate, ambiente em loop) usa ``sfx_volume``.
- Em partida: ``cmd_sfx_volume``; ajustável no menu e durante a partida.

**Espera de voz sem bloqueio**

- ``voice._say_now()`` / ``flush()`` usam ``pygame.event.pump()`` + ``Clock.tick(30)`` em vez de ``time.sleep(0.1)``.

**Fallback de música de menu unificado**

- ``_play_menu_music_with_fallback()`` unifica a lógica duplicada no seletor de campanha, criação de partida e lobby do servidor.

**Testes**: ``test_audio_settings.py``, ``test_voice_pump.py``

P2 — polimento
--------------

**P2a — ambiente suavizado**

- ``ambient_volume()`` usa LFO lento baseado em posição (~8 s) em vez de ``random.random()`` por frame.

**P2b — controlador de música de batalha (``battle_music.py``)**

- Centraliza checagens de inimigos na visão e entrada/saída de BGM de combate.
- Substitui lógica espalhada em ``combat.py``, ``game_display.py``, ``game_navigation.py``.

**P2c — limpeza do ``music_resolver``**

- Remove ramos inalcançáveis; adiciona testes de busca.

**P2d — SFX multiformato e preload a quente**

SFX de jogo em ``ui/`` suportam:

- ``.ogg`` (preferido)
- ``.wav``
- ``.mp3``

Quando vários formatos compartilham o mesmo stem, ``.ogg`` vence. IDs podem ser escritos como ``footstep``, ``footstep.wav`` ou ``1029.mp3``.

Preload a quente: thread em segundo plano lê bytes; thread principal decodifica com ``tick_preload()`` (thread safety do pygame). Opcional em ``parameters.txt``::

  preload_sounds 4303,4304
  preload_decode_per_tick 6

**Testes**: ``test_ambient_stereo_volume.py``, ``test_battle_music.py``, ``test_sfx_formats.py``

Volumes e atalhos
-----------------

+------------------+----------------------------+----------------------------------+
| Volume           | Chave de config            | Ajuste habitual                  |
+==================+============================+==================================+
| Voz / interface  | ``audio/main_volume``      | opcional (leitores externos)     |
+------------------+----------------------------+----------------------------------+
| SFX do jogo      | ``audio/sfx_volume``       | Home aumentar / End diminuir     |
+------------------+----------------------------+----------------------------------+
| Música           | ``audio/music_volume``     | Alt+Home / Alt+End               |
+------------------+----------------------------+----------------------------------+

Para autores de mods
--------------------

- Coloque SFX em ``ui/`` ou ``mods/<mod>/ui/``.
- ``.ogg`` ainda é recomendado pelo tamanho; ``.wav`` / ``.mp3`` funcionam sem conversão.
- Se ``ui/tts.txt`` já define o mesmo ID como texto, esse ID não é carregado como áudio.

**Não confundir com camadas de gritos**

+----------------------+--------------------------------+---------------------------+
| Conceito             | Significado                    | Documento                 |
+======================+================================+===========================+
| Refatoração P0–P2    | módulos, volume, formatos      | esta página               |
+----------------------+--------------------------------+---------------------------+
| Camadas de gritos    | ``shout_bg`` / unidade / evento | :doc:`battle-shouts`    |
+----------------------+--------------------------------+---------------------------+
| Inteiro priority     | preempt em ``psounds.play``    | ``lib/sound.py``          |

Rascunhos anteriores das notas de versão 1.4.5.1 descreviam P0–P2 como camadas de prioridade ambiental/combate/alertas; as notas de versão já foram corrigidas.
