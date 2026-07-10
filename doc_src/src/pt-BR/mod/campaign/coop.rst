Campanhas cooperativas estilo Age of Empires
============================================


Guia completo (1.4.3.9): `../player/campaign-and-co-op-improvements.md <../player/campaign-and-co-op-improvements.htm>`_ — navegador de missões, níveis de dificuldade, parceiros IA, determinismo, autoria de mapas.

Versão em chinês: `../../zh/player/战役与合作战役改进说明.md <../../zh/player/战役与合作战役改进说明.htm>`_

Este motor executa capítulos de campanha de forma cooperativa como Age of
Empires II/III Definitive Edition: vários jogadores entram na mesma missão de
história, cada um comanda seu próprio slot (base/exército) na mesma equipe,
compartilham objetivos e cut scenes da missão e enfrentam inimigos que escalam
com dificuldade e número de jogadores. Slots vazios são assumidos por um
parceiro IA aliado, então uma pessoa também pode jogar missão cooperativa solo.

Como funciona o cooperativo (visão do jogador)
----------------------------------------------


1. Lobby do servidor -> `Co-op campaign` -> escolher campanha -> escolher
   capítulo -> escolher dificuldade (Easy / Standard / Moderate / Hard /
   Extreme) -> escolher velocidade.
   (Sem etapa de trégua: campanhas cooperativas nunca oferecem trégua.)
2. Outros jogadores entram no lobby; o anfitrião inicia.
3. A cut scene intro da missão toca para todos, depois a missão roda com seus
   próprios objetivos dirigindo vitória/derrota compartilhada (não "destruir
   todos os inimigos"). Cut scenes e atualizações de objetivo são anunciadas a
   todos os jogadores.
4. Completar o capítulo desbloqueia o próximo (marcador de campanha do
   anfitrião).

Como uma campanha declara cooperativo (autor de campanha)
---------------------------------------------------------


Como tabelas de campanha do Age of Empires, o cooperativo é declarado em
:strong:```campaign.txt`` junto de ``title`` / ``synopsis``. Não envie arquivos
``N.coop.txt`` paralelos; um jogador e cooperativo carregam o mesmo mapa de
missão ``N.txt``.

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
     - ``1`` — campanha aparece no menu Co-op campaign do servidor
   * - ``coop_intro``
     - Números de capítulo de cut scene mostrados no fluxo cooperativo (por
       exemplo prólogo `0`)
   * - ``coop_missions``
     - Números de capítulo jogáveis em cooperativo (`1-29`, `1 2 3` etc.)



O motor interpreta isso em `soundrts/campaign.py <../../../soundrts/campaign.py>`_
(``supports_coop``, ``coop_menu_chapters``, ``coop_mission_chapters``). Partidas
cooperativas carregam o mapa normal do capítulo via ``ensure_chapter_map``. Nenhum
nome de campanha é fixo no código — qualquer mod pode aderir via seu próprio
``campaign.txt``.

Como um capítulo declara slots cooperativos (autor de mapa)
-----------------------------------------------------------


Um capítulo é apenas um mapa de campanha. Para torná-lo cooperativo, crie com
mais de um slot de jogador humano, todos na mesma equipe:

.. code-block:: text

   nb_players_min 1            ; permite solo + parceiros IA
   nb_players_max 2            ; dois slots cooperativos (Jogador A / Jogador B)
   ; uma casa inicial por slot, em lugares diferentes:
   player_start 1 a1 raynor footman footman
   player_start 2 h8 raynor2 footman archer
   ; inimigos são computer_only como de costume (formam equipe "ai" própria):
   computer_only e5 ...


Pontos-chave:

- ``nb_players_max`` = número de slots cooperativos. O motor atribui a cada
  humano (e cada parceiro IA) uma posição inicial distinta dos starts do mapa,
  para todos terem base/exército próprios.
- ``nb_players_min 1`` permite um humano solo iniciar a missão; o motor preenche
  slots restantes com parceiros IA aliados
  (``Game._fill_coop_ai_partners`` em `soundrts/serverroom.py <../../../soundrts/serverroom.py>`_).
- Todos os slots humanos + parceiros IA são forçados à mesma equipe (aliança 1)
  no início. Inimigos declarados com ``computer_only`` formam equipe separada
  (``populate_map`` os coloca na aliança ``"ai"``), permanecendo hostis.
- Gatilhos de missão que endereçam ``player1``, ``player2``, ... mapeiam para
  os humanos em ordem. Slots só de parceiro IA simplesmente não são
  endereçados por esses gatilhos de história (apenas lutam com as forças do
  slot).

``MissionGame`` de um jogador ainda registra um humano e usa apenas o primeiro
spawn.

Ferramenta de manutenção opcional (apenas Raynor)
-------------------------------------------------


`tools/generate_raynor_coop_maps.py <../../../tools/generate_raynor_coop_maps.py>`_ aplica
transformações de layout cooperativo (mapa mais largo, segundo jogador
espelhado etc.) em :strong:```N.txt`` apenas para *The Legend of Raynor*.
Outras campanhas devem criar ``campaign.txt`` + ``N.txt`` diretamente.

O que escala com dificuldade / número de jogadores
--------------------------------------------------


HP de unidades inimigas e dano causado escalam deterministicamente (matemática
inteira, idêntica em todo cliente) pela dificuldade escolhida, aumentados
ainda pelo número de jogadores humanos. Veja
`soundrts/coop_difficulty.py <../../../soundrts/coop_difficulty.py>`_.

Notas de determinismo
---------------------


- Fatores de dificuldade são calculados uma vez no servidor e transmitidos,
  para todos os clientes / espectadores / replays reconstruírem um mundo
  idêntico.
- Carry-over ``campaign_flag`` entre capítulos é intencionalmente no-op em
  cooperativo (o mundo não tem objeto de campanha local), evitando divergência
  de save por cliente. ``set_map_flag`` / ``map_flag`` na missão usam estado
  sincronizado do mundo e funcionam normalmente.

Testes
------


.. code-block:: bash

   python -m pytest soundrts/tests/test_coop_chapter_maps.py -q
   python -m pytest soundrts/tests/test_changelog_1429_coop_campaign_difficulty.py -q
   python -m pytest soundrts/tests/test_changelog_1429c_coop_story_mission.py -q
   python -m pytest soundrts/tests/test_changelog_1429d_coop_player_slots.py -q
