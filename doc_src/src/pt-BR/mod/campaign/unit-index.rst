Seletores de índice de unidade no mapa (``killed_target`` / ``npc_has_item`` / ``unit_lost`` / ``building_lost`` / ``key_unit_killed``)
=======================================================================================================================================


Quando várias unidades do mesmo tipo compartilham uma casa, use
:strong:```\<square\> \<index\> \<type\>`` para significar "a N-ésima unidade
desse tipo naquela casa" — não "qualquer uma delas" nem "matar N no total".

Mesma sintaxe que :strong:```transfer_units``, ``order`` e ``add_units``.
Índices são atribuídos no carregamento do mapa / spawn por gatilho por
``(square, type)`` e permanecem estáveis após a unidade se mover.


----


1. Gatilhos
-----------



.. list-table::
   :header-rows: 1

   * - Condição
     - Sintaxe de índice
     - Caso de uso
   * - ``killed_target``
     - ``(killed_target \<index\> \<type\> [enemy|ally])`` ou forma com casa
   * - ``npc_has_item``
     - ``(npc_has_item \<index\> \<type\> \<item\>)`` ou forma com casa
     - Deve dar o item àquele NPC específico
   * - ``unit_lost``
     - ``(unit_lost \<index\> \<type\>)`` ou `` (unit_lost \<square\> \<index\> \<type\>)``
     - Aquela unidade aliada de índice spawnada sumiu
   * - ``building_lost``
     - ``(building_lost \<index\> \<type\>)`` ou `` (building_lost \<square\> \<index\> \<type\>)``
     - Aquele edifício de índice spawnado foi destruído
   * - ``key_unit_killed``
     - ``(key_unit_killed \<index\> \<type\>)`` ou `` (key_unit_killed \<square\> \<index\> \<type\>)``
     - Aquela unidade aliada de índice spawnada foi morta



Formas legadas ainda funcionam:

- `(killed_target <unit_id>)` — id global da unidade
- `(killed_target <type> [enemy\|ally])` — qualquer abate daquele tipo
- `(npc_has_item <NPC_selector> <item> [square])` — tipo/id + casa atual
  opcional


----


2. Matar uma unidade específica (``killed_target``)
---------------------------------------------------


Completar objetivo apenas para a N-ésima unidade
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


.. code-block:: text

   computer_only 0 0 c3 3 demo_marker_footman
   
   trigger player1 (killed_target 3 demo_marker_footman enemy) (objective_complete 1)


Apenas matar o 3º ``demo_marker_footman`` spawnado satisfaz a condição
(independente da casa).
Forma com casa: ``(killed_target c3 3 demo_marker_footman enemy)``.

Falha em abate errado
~~~~~~~~~~~~~~~~~~~~~


.. code-block:: text

   trigger player1 (killed_target 1 demo_marker_footman enemy) (do (cut_scene 7606) (defeat))
   trigger player1 (killed_target 2 demo_marker_footman enemy) (do (cut_scene 7606) (defeat))
   trigger player1 (killed_target 3 demo_marker_footman enemy) (do (cut_scene 7603) (objective_complete 1))


Matar #1 ou #2 → cut scene + ``defeat``. Matar #3 → completa objetivo 1.

vs ``has_killed``
~~~~~~~~~~~~~~~~~



.. list-table::
   :header-rows: 1

   * - Condição
     - Significado
   * - ``(has_killed 3 footman enemy)``
     - Três footman inimigos mortos no total
   * - ``(killed_target c3 3 footman enemy)``
     - O 3º footman em C3 foi morto




----


3. Dar a um NPC específico (``npc_has_item``)
---------------------------------------------


.. code-block:: text

   computer_only 0 0 neutral b2 3 quest_npc
   short_sword a1
   
   trigger player1 (npc_has_item 3 quest_npc short_sword) (objective_complete 2)


Apenas o 3º ``quest_npc`` spawnado conta (qualquer casa). Forma com casa:
`` (npc_has_item b2 3 quest_npc short_sword)``.
Veja `give-to-npc <give-to-npc.htm>``_ para ``give`` / ``receive_items``.


----


4. Proteger unidade ou edifício aliado específico (derrota)
-----------------------------------------------------------


Apenas footman #3 pode morrer
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


.. code-block:: text

   player ... a1 3 footman raynor
   
   trigger player1 (unit_lost a1 3 footman) (defeat)
   trigger player1 (key_unit_killed a1 3 footman) (defeat)


Apenas a primeira prefeitura (índice global de spawn)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


.. code-block:: text

   player ... b1 townhall raynor ...   ; base do capítulo 2 em B1 também funciona
   
   trigger player1 (building_lost 1 townhall) (defeat)


Índice global conta ordem de spawn por jogador por tipo, independente da casa:
- 1ª prefeitura spawnada = prefeitura 1 (em A1 ou B1)
- 2ª spawnada = prefeitura 2; destruir #2 não falha este gatilho

Para N-ésima unidade específica da casa, use ``(building_lost a1 1 townhall)``.

vs formas legadas
~~~~~~~~~~~~~~~~~



.. list-table::
   :header-rows: 1

   * - Condição
     - Significado
   * - ``(unit_lost footman)``
     - Todos os footman do jogador sumiram
   * - ``(unit_lost a1 3 footman)``
     - Apenas o 3º footman em A1 sumiu
   * - ``(building_lost townhall)``
     - Todas as prefeituras do jogador foram destruídas
   * - ``(building_lost a1 1 townhall)``
     - Apenas a 1ª prefeitura em A1 foi destruída




----


5. Múltiplos objetivos e cut scenes
-----------------------------------


Objetivos primários podem ser concluídos em qualquer ordem. Cada ``cut_scene``
em ``objective_complete`` deve descrever apenas aquele objetivo — não diga
"todos os objetivos concluídos" em um ramo;
a vitória roda automaticamente quando todo objetivo primário estiver feito.

Bom:

.. code-block:: text

   trigger player1 (killed_target c3 3 demo_marker_footman enemy)
       (do (cut_scene 7603) (objective_complete 1))
   
   trigger player1 (npc_has_item b2 3 quest_npc short_sword)
       (do (cut_scene 7604) (objective_complete 2))


Ruim: texto da cut scene 7604 dizendo que ambos objetivos estão feitos quando
o jogador ainda precisa matar footman #3.


----


6. Demo: The Legend of Raynor capítulo 28
-----------------------------------------


Arquivo: ``res/single/The Legend of Raynor/28.txt``


.. list-table::
   :header-rows: 1

   * - Área
     - Conteúdo
   * - A1
     - footman + peasant, ``short_sword`` no chão
   * - C3
     - 3 ``demo_marker_footman`` inimigos
   * - B2
     - 3 ``quest_npc`` neutros



Objetivo 1: matar o 3º footman em C3 (abate errado → derrota).  
Objetivo 2: dar ``short_sword`` ao 3º NPC em B2.


----


7. Código e testes
------------------



.. list-table::
   :header-rows: 1

   * - Função
     - Caminho
   * - Atribuir índice no spawn
     - ``triggers.py`` — ``\_assign_map_select_slot``
   * - Rastreamento de abates
     - ``record_unit_killed`` → ``\_killed_map_slots`` / ``\_units_killed_by``
   * - Condições
     - ``lang_killed_target``, ``lang_npc_has_item``, ``lang_unit_lost``,
       ``lang_building_lost``, ``lang_key_unit_killed``
   * - Teste de mapa
     - `test_give_item_to_npc.py::test_chapter_28_map_select_index_triggers`
   * - Testes de perda
     - ``test_map_select_loss_triggers.py``



.. code-block:: text

   python -m pytest soundrts/tests/test_give_item_to_npc.py::test_chapter_28_map_select_index_triggers -q
   python -m pytest soundrts/tests/test_map_select_loss_triggers.py -q
