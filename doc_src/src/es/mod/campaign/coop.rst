# Campañas cooperativas al estilo Age of Empires

Guía completa (1.4.3.9): `../player/campaign-menu.htm <../player/campaign-menu.htm>`_ — navegador de misiones, niveles de dificultad, socios de IA, determinismo, autoría de mapas.

Este motor juega capítulos de campaña en cooperativo como Age of Empires II/III
Definitive Edition: varios jugadores se unen a la misma misión de historia, cada
uno comanda su propia ranura (base/ejército) en un equipo, comparten los
objetivos y las escenas de la misión, y se enfrentan a enemigos que escalan con
la dificultad y el número de jugadores. Las ranuras vacías las ocupa un socio
de IA aliado, así que una sola persona también puede jugar una misión cooperativa en solitario.

Cómo funciona el cooperativo (vista del jugador)
------------------------------------------------

1. Lobby del servidor -> `Campaña cooperativa` -> elige campaña -> elige capítulo ->
   elige dificultad (Fácil / Estándar / Moderada / Difícil / Extrema) -> elige velocidad.
   (Sin paso de tratado: las campañas cooperativas nunca ofrecen tratado.)
2. Otros jugadores se unen al lobby; el anfitrión empieza.
3. La escena introductoria de la misión se reproduce para todos, luego la misión
   corre con sus propios objetivos impulsando la victoria/derrota compartida (no
   «destruir a todos los enemigos»). Las escenas y las actualizaciones de objetivos
   se anuncian a todos los jugadores.
4. Completar el capítulo desbloquea el siguiente (marcador de campaña del anfitrión).

Cómo una campaña declara cooperativo (autor de campaña)
-------------------------------------------------------

Como las tablas de campaña de Age of Empires, el cooperativo se declara en :strong:```campaign.txt``
junto a ``title`` / ``synopsis``. No envíes archivos ``N.coop.txt`` paralelos;
un jugador y cooperativo cargan el mismo mapa de misión ``N.txt``.

.. code-block:: text

   title 7747
   synopsis 7751
   coop_campaign 1
   coop_intro 0
   coop_missions 1-29

.. list-table::
   :header-rows: 1

   * - Campo
     - Significado
   * - ``coop_campaign``
     - ``1`` — la campaña aparece en el menú Campaña cooperativa del servidor
   * - ``coop_intro``
     - Números de capítulo de escena mostrados en el flujo cooperativo (p. ej. prólogo `0`)
   * - ``coop_missions``
     - Números de capítulo de misión jugables en cooperativo (`1-29`, `1 2 3`, etc.)

El motor los analiza en `soundrts/campaign.py <../../../soundrts/campaign.py>`_
(``supports_coop``, ``coop_menu_chapters``, ``coop_mission_chapters``). Las partidas
cooperativas cargan el mapa normal del capítulo vía ``ensure_chapter_map``. Ningún
nombre de campaña está codificado — cualquier mod puede optar mediante su propio ``campaign.txt``.

Cómo un capítulo declara ranuras cooperativas (autor de mapa)
-------------------------------------------------------------

Un capítulo es solo un mapa de campaña. Para hacerlo capaz de cooperativo, autorízalo con
más de una ranura de jugador humano, todas pensadas para el mismo equipo:

.. code-block:: text

   nb_players_min 1            ; allow solo + AI partners
   nb_players_max 2            ; two co-op slots (Player A / Player B)
   ; one starting square per slot, in different places:
   player_start 1 a1 raynor footman footman
   player_start 2 h8 raynor2 footman archer
   ; enemies are computer_only as usual (they form their own "ai" team):
   computer_only e5 ...

Puntos clave:

- ``nb_players_max`` = número de ranuras de jugador cooperativo. El motor asigna a cada
  humano (y a cada socio de IA) una posición de inicio distinta de los inicios de
  jugador del mapa, así que todos obtienen su propia base/ejército.
- ``nb_players_min 1`` permite que un solo humano inicie la misión; el motor rellena las
  ranuras restantes con socios de IA aliados
  (``Game._fill_coop_ai_partners`` en `soundrts/serverroom.py <../../../soundrts/serverroom.py>`_).
- Todas las ranuras humano + socio-IA se fuerzan a un equipo (alianza 1) al
  inicio. Los enemigos declarados con ``computer_only`` forman un equipo separado
  (``populate_map`` los pone en la alianza ``"ai"``), así que siguen siendo hostiles.
- Los disparadores de misión que se dirigen a ``player1``, ``player2``, ... se mapean a los
  jugadores humanos en orden. Las ranuras solo-socio-IA simplemente no son abordadas por esos
  disparadores de historia (solo combaten con las fuerzas de su ranura).

El ``MissionGame`` de un jugador sigue registrando un humano y usa solo el primer spawn.

Herramienta de mantenimiento opcional (solo Raynor)
---------------------------------------------------

`tools/generate_raynor_coop_maps.py <../../../tools/generate_raynor_coop_maps.py>`_ aplica transformaciones de diseño cooperativo (mapa más ancho, segundo jugador espejado, etc.) en :strong:```N.txt`` solo para *The Legend of Raynor*. Otras campañas deben autorar ``campaign.txt`` + ``N.txt`` directamente.

Qué escala con la dificultad / número de jugadores
--------------------------------------------------

Los PV y el daño saliente de las unidades enemigas se escalan de forma determinista (matemática entera,
idéntica en cada cliente) según la dificultad elegida, aumentada además por el
número de jugadores humanos. Consulta
`soundrts/coop_difficulty.py <../../../soundrts/coop_difficulty.py>`_.

Notas de determinismo
---------------------

- Los factores de dificultad se calculan una vez en el servidor y se emiten, así que todos
  los clientes / espectadores / repeticiones reconstruyen un mundo idéntico.
- El traslado entre capítulos ``campaign_flag`` es intencionadamente un no-op en cooperativo
  (el mundo no tiene objeto de campaña local), evitando divergencia de guardado por cliente.
  ``set_map_flag`` / ``map_flag`` dentro de la misión usan estado de mundo sincronizado y funcionan
  con normalidad.

Pruebas
-------

.. code-block:: bash

   python -m pytest soundrts/tests/test_coop_chapter_maps.py -q
   python -m pytest soundrts/tests/test_changelog_1429_coop_campaign_difficulty.py -q
   python -m pytest soundrts/tests/test_changelog_1429c_coop_story_mission.py -q
   python -m pytest soundrts/tests/test_changelog_1429d_coop_player_slots.py -q
