Sistemas estratégicos RMG: herói e civilização
==============================================

Esta camada integra progressão de herói no estilo Heroes of Might and Magic e
gestão urbana no estilo Civilization em mapas aleatórios (Random Map
Generator, RMG). Continua sendo estratégia em tempo real: rendimentos se
liquidam com o tempo de jogo, sem turnos.


----


1. Como ativar
--------------

Menu principal → **Iniciar jogo → Mapa aleatório**. Todo mapa RMG novo grava
``rmg_strategic_systems 1`` e ativa herói, rendimentos urbanos, cultura, pontos
diplomáticos, tecnologias e políticas.

Mapas feitos à mão e partidas não RMG não ativam essas regras por padrão. Se o
mod não define ``rmg_hero``, o gerador pula o herói sem falhar o carregamento.


----


2. Progressão do herói
----------------------

Cada jogador começa com um ``rmg_hero``:

- Nível 1 inicial, máximo 8.
- Ganha experiência em combate e sobe de nível automaticamente.
- Cada nível aumenta vida, dano corpo a corpo e mana máximo.
- Mana própria; habilidades gastam mana e ela se regenera.
- No máximo um herói RMG por jogador.
- Em **RMG local solo**, nível e experiência máximos são salvos por mod e
  facção e restaurados na próxima partida. Multijogador e replays não leem o
  arquivo local (evita dessincronização).

Perfil do herói entre partidas
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

- Caminho: no diretório de configuração do usuário, ao lado de ``achievements``:
  ``rmg_heroes/<chave_mod>/<facção>.json`` (ex.: ``human.json``).
- Ao fim da partida salva nível e XP máximos; no início da próxima aplica a
  ``rmg_hero``, incluindo habilidades por nível.
- Apenas **mapas aleatórios locais solo** (``TrainingGame``). Campanha,
  multijogador, replay e espectador não usam este arquivo.
- Separado de ``campaign_carryover`` de campanha: ``rmg_hero`` mantém
  ``campaign_carryover 0``; persistência RMG usa JSON dedicado, não
  ``campaigns.ini``.

Árvore de habilidades
~~~~~~~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1

   * - Nível
     - Habilidade
     - Custo de mana
     - Efeito
   * - 2
     - Seta arcano
     - 20
     - Dano mágico a um alvo
   * - 4
     - Redemoinho
     - 35
     - Dano no alcance corpo a corpo
   * - 6
     - Chuva de meteoros
     - 60
     - Dano em área à longa distância

Habilidades desbloqueiam no nível indicado. Selecione o herói e use o menu de
habilidades; mana insuficiente impede o lançamento.


----


3. Expansão urbana e rendimento de casas
----------------------------------------

Prefeitura, fortaleza e castelo contam como cidades. Em mods compatíveis, bases
com **sobrevivência** e **armazenamento de recursos** também.

Cada cidade possui sua casa principal. Selecione a cidade, **Comprar casa**,
depois uma casa principal adjacente ao território atual. Sem ocupação dupla.
Primeira compra: 20 ouro; cada casa extra +10 ouro. Cidade nova reivindica a
casa ao construir.

A cada 60 s, cada cidade viva e cada casa trabalhada paga uma vez.

Rendimento base por cidade
~~~~~~~~~~~~~~~~~~~~~~~~~~

Por tick:

- 6 ouro, 4 madeira, 4 comida, 4 cultura, 1 ponto diplomático.

Bônus de terreno urbano
~~~~~~~~~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1

   * - Terreno
     - Extra
   * - Colina, planalto, rocha alta, passo de montanha
     - +3 ouro
   * - Floresta, floresta densa, pântano
     - +3 madeira
   * - Planície, vila, prado
     - +3 comida
   * - Lago, rio, riacho, vau
     - +1 ouro, +2 comida

Recursos contam para **coleta acumulada** e vitória econômica RMG.

Cidadãos e melhorias de casa
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Comandos **Atribuir cidadão a ouro / madeira / comida / cultura** em casas
próprias. Sem vagas, libera o cidadão mais antigo:

- 1 vaga base; planejamento urbano e administração cívica +1 cada; fortaleza ou
  castelo +1.

Melhorias: **mina** (+3 ouro), **serraria** (+3 madeira), **fazenda** (+3
comida). Custos: mina 15 ouro + 10 madeira; serraria 10 ouro + 15 madeira;
fazenda 10 ouro + 5 madeira + 10 comida.

Rendimento base de casa trabalhada (a cada 60 s): 1 ouro, 1 madeira, 1 comida;
mesmos bônus de terreno; especialização +2 ouro/madeira/comida ou +3 cultura.

Compra: primeira expansão 20 ouro, depois +10 ouro por casa (casa da cidade
grátis).


3.1 Comandos estratégicos de cidade
-----------------------------------

Com prefeitura, fortaleza ou castelo em partida RMG (escolher casa alvo e
confirmar):

.. list-table::
   :header-rows: 1

   * - Comando (voz)
     - Palavra-chave
     - Efeito
   * - Comprar casa (5718)
     - ``rmg_buy_tile``
     - Comprar casa adjacente livre
   * - Atribuir cidadão a ouro (5719)
     - ``rmg_assign_gold``
     - Trabalhar casa própria
   * - Atribuir cidadão a madeira (5720)
     - ``rmg_assign_wood``
     - Especialização madeira
   * - Atribuir cidadão a comida (5721)
     - ``rmg_assign_food``
     - Especialização comida
   * - Atribuir cidadão a cultura (5722)
     - ``rmg_assign_culture``
     - +3 cultura/min nessa casa
   * - Construir mina (5723)
     - ``rmg_build_mine``
     - +3 ouro/tick
   * - Construir serraria (5724)
     - ``rmg_build_lumber_mill``
     - +3 madeira/tick
   * - Construir fazenda (5725)
     - ``rmg_build_farm``
     - +3 comida/tick
   * - Ativar política tradição (5726)
     - ``rmg_switch_tradition``
     - Trocar entre políticas desbloqueadas sem custo de cultura
   * - Ativar política comércio (5727)
     - ``rmg_switch_commerce``
     - Idem
   * - Ativar política diplomacia (5728)
     - ``rmg_switch_diplomacy``
     - Idem


----


4. Árvore tecnológica
---------------------

.. list-table::
   :header-rows: 1

   * - Tecnologia
     - Requisito
     - Efeito
   * - Planejamento urbano
     - —
     - +2 ouro, madeira e comida por cidade/tick
   * - Administração cívica
     - Planejamento urbano
     - +2 cultura por cidade/tick
   * - Serviço exterior
     - Administração cívica
     - +1 ponto diplomático por cidade/tick


----


5. Cultura e cartas de política
-------------------------------

Cultura é estatística estratégica da partida; políticas a consomem ao adotar.

.. list-table::
   :header-rows: 1

   * - Política
     - Cultura
     - Requisito
     - Efeito
   * - Tradição
     - 40
     - Planejamento urbano
     - +50% cultura
   * - Comércio
     - 80
     - Administração cívica
     - +25% ouro, madeira e comida urbanos
   * - Diplomacia
     - 120
     - Serviço exterior
     - Dobro de pontos diplomáticos

Máximo **duas** políticas ativas. A terceira substitui a mais antiga. Depois
**Ativar tradição / comércio / diplomacia** troca grátis entre desbloqueadas.

IA escolhe pares fixos: agressiva → comércio + tradição; ≥2 inimigos →
diplomacia + comércio; resto → tradição + comércio.


----


6. Pontos diplomáticos
----------------------

Cidades geram pontos a cada minuto. **Enviar pedido de aliança** custa 20
pontos em RMG estratégico (aceitar/recusar/sair grátis; cooldown 60 s).


6.1 Consultar cultura e diplomacia
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Cultura e diplomacia **não** usam a barra de recursos (Z / X / Shift+Z). Em
partidas RMG com ``rmg_strategic_systems``:

.. list-table::
   :header-rows: 1

   * - Método
     - Ação
   * - Atalhos globais
     - **B** cultura atual; **Shift+B** pontos de diplomacia
   * - Atributos da cidade
     - Cidade própria, atributos (Alt+V): **U** cultura, **Y** diplomacia
   * - Voz periódica
     - A cada 60 s ``rmg_strategic_tick`` anuncia cidades, cultura e diplomacia
   * - Alertas de mudança
     - Com alertas de recursos ativos, mudanças de cultura/diplomacia também são anunciadas

Fora de RMG, **B** / **Shift+B** apenas emitem aviso.


----


7. Compatibilidade com mods
---------------------------

Arquitetura do gameplay RMG
~~~~~~~~~~~~~~~~~~~~~~~~~~~

Mapas aleatórios combinam **framework do motor** (gerador, quatro modos de
vitória, API de triggers, sistemas estratégicos estilo Civ opcionais) com
**dados de regras e templates**. Valores padrão e ativação dos sistemas
estratégicos ficam em ``def parameters`` do ``rules.txt``; templates
``cfg/randommap/*.txt`` sobrescrevem por partida. Mods estendem o RMG via
regras/templates, sem Python. ``map.txt`` manual permite vitórias totalmente
livres.

Parâmetros globais (``def parameters``)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Inclui ``rmg_diplomacy_request_cost``, ``rmg_tile_purchase_*``,
``rmg_policy_slot_limit``, ``rmg_trade_cooldown``, ``rmg_economic_goal*``,
``rmg_survival_seconds*``, ``rmg_exploration_ruin_pairs_*``,
``rmg_strategic_systems``.

Melhorias de casa (``rmg_tile_*``), comércio (``rmg_trade_*``), vitória por
template (``default_victory_mode``, ``survival_seconds``,
``exploration_ruin_pairs``, ``strategic_systems 0``) e bloco
``victory_triggers`` — ver ``res/randommap/example.txt`` e
``player/rmg-strategic-systems.htm`` (inglês/chinês completos).

Outras notas
~~~~~~~~~~~~

- ``rmg_hero`` necessário para herói inicial.
- Bases com ``provides_survival`` e ``storable_resource_types`` = cidade.
- Cidades recebem tecnologia e políticas RMG dinamicamente; mapas não RMG filtram pesquisa ``rmg_``.
- ``can_research`` é armazenado como ``_rules_can_research``; ``effective_can_research()`` injeta ``rmg_*`` só em mapas RMG.

Atributos: ``culture_cost``, ``rmg_policy 1``. Triggers: ``rmg_strategic_tick``,
``rmg_has_culture``, ``rmg_has_diplomacy``, ``rmg_grant_culture``,
``rmg_grant_diplomacy``.


----


8. Implementação
----------------

``soundrts/rmg_systems.py``, ``rmg_progress.py``, ``worldorders/strategic.py``,
``randommap.py``, ``worldplayercomputer.py``, ``game.py``,
``clientgame/game_resources.py``, ``attributes/basic_attributes.py``,
``res/rules.txt``, voz 5702–5728 e status cultura/diplomacia 5716–5717,
testes ``test_rmg_systems.py``.


----


9. Limites atuais
-----------------

Sem turnos Civ5, crescimento populacional, manutenção de estradas ou UI
diplomática. Território por casa RMG sem alterar passagem de unidades. Herói
entre partidas apenas em RMG local solo.
