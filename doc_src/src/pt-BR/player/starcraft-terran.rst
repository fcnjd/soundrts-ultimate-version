# Mod StarCraft: complementos Terran e recombinar

Mod: ative ``mods = starcraft`` em ``SoundRTS.ini``.

Este guia cobre complementos Tech Lab / Reactor: construir, destacar no lift-off, recombinar voando e a diferença entre **terreno de construção** (permissão para construir) e alinhamento de slot (reatachar).

Mapas StarCraft usam **build sites** (``build_site``, terreno de quadrado ``build_sites``) em vez de **meadows** clássicos. Abaixo, "terreno de construção" significa qualquer objeto ``class building_land``; neste mod isso costuma ser ``build_site``.


----


1. Conceitos
-------------



.. list-table::
   :header-rows: 1

   * - Termo
     - Significado
   * - Host
     - Barracks, Factory ou Starport (``can_have_addon``)
   * - Complemento
     - Tech Lab ou Reactor (``is_addon 1``), construído no slot lateral do host
   * - Slot
     - Cerca de 3,5 tiles a leste do host (``addon_offset_x``, padrão 3500 unidades internas)
   * - Terreno de construção
     - Objeto ``class building_land`` no quadrado (``build_site`` neste mod); edifícios Terran terrestres devem consumir um para pousar
   * - Recombinar
     - Após lift-off o complemento fica no chão; outro host pousa com o slot alinhado e reanexa automaticamente o complemento órfão



Tech Lab concede por host, ex.:

- Barracks + Tech Lab → Marauder
- Factory + Tech Lab → Siege Tank
- Starport + Tech Lab → Medivac

Reactor usa ``addon_train_multiplier 2``.


----


2. Construir um complemento
----------------------


1. Selecione um host existente (ex. Barracks), não terreno vazio.
2. Construa Tech Lab ou Reactor no menu.
3. O complemento se auto-constrói no lado do host (``self_constructs 1``); não usa seu próprio slot de terreno de construção.

Mapa de teste: ``terran_addon_test``.


----


3. Lift-off
-------------


Barracks / Factory / Starport podem mudar para forma voadora (``can_change_to flying_*``):

1. Selecione o edifício terrestre → change_to → variante voadora.
2. O host deixa o chão; o complemento permanece e é destacado.
3. Terreno de construção é restaurado onde o edifício estava: **o mesmo tipo que o edifício consumiu ao ser construído** (``build_site`` neste mod). Se o mapa só gera build sites (``nb_build_site_by_square``, ``building_land build_site``, etc.), lift-off deixa um build site — você **não** precisa de ``default_building_land build_site`` nas regras do mod para isso.

Um quadrado pode ter vários patches (ex. Barracks e Factory cada um faz lift-off uma vez → dois build sites). Em starts com apenas um patch no mapa, a Factory pode começar sem terreno de construção; patches aparecem na posição de lift-off de cada edifício.


----


4. Pouso normal vs pouso de recombinar
----------------------------------


4.1 Duas verificações separadas
~~~~~~~~~~~~~~~~~~~~~~~~



.. list-table::
   :header-rows: 1

   * - Etapa
     - Decide
     - Não decide
   * - Pouso
     - Qual objeto de terreno de construção é consumido; host (x, y)
     - Reanexar
   * - Reanexar
     - Tech Lab órfão anexa ao host
     - Qual patch foi usado



Terreno de construção = permissão para pousar (qualquer ``class building_land`` no quadrado; nomes de API como ``find_meadow_near_xy`` são históricos).  
Slot = geometria: complemento em ``(host.x + 3500, host.y)``; reanexar exige alinhamento de slot dentro de ~2,5 tiles de distância Manhattan.

Você pode ver a Factory em um "patch central" enquanto treinamento de Tank funciona: slot alinhado, não porque o edifício está na grama sob o lab.

4.2 Pouso normal (patch do próprio lift-off)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


1. Tab no terreno de construção deixado quando aquele edifício fez lift-off (build site neste mod).
2. Backspace (``go`` padrão), aguarde até chegar.
3. change_to forma terrestre.

O edifício pousa ali e não assume um Tech Lab órfão. Se um complemento órfão compatível permanecer no quadrado, você ouve: *Go to the Tech Lab first, then land to reattach the addon* (TTS 7350).

4.3 Pouso de recombinar (assumir Tech Lab órfão)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


1. Construa Tech Lab na Barracks, lift-off da Barracks (lab fica).
2. Lift-off da Factory, voe até aquele quadrado.
3. Tab no Tech Lab (não em um patch de terreno de construção).
4. Backspace go — alvo vira o slot de pouso (~3,5 tiles a oeste do lab), não o centro do lab.
5. change_to Factory.

Resultado:

- Factory aparece nas coordenadas do slot;
- O objeto de terreno de construção mais próximo no quadrado é consumido (muitas vezes um patch central);
- Slot alinha com o lab → reanexação automática → Tank (etc.) disponível.

Mapa de teste: ``terran_recombine_test``; campanha ``sc_build_tests`` capítulo 4.


----


5. Referência rápida
--------------------



.. list-table::
   :header-rows: 1

   * - Objetivo
     - Tab
     - Após go
     - resultado change_to
   * - Pousar no ponto de lift-off
     - build site do lift-off
     - Backspace
     - Sem reanexar, sem Tank
   * - Assumir Tech Lab órfão
     - Tech Lab
     - Backspace (voa até o slot)
     - Reanexar, Tank disponível



Com vários patches, a voz do Tab pode dizer "build site" para todos — use direção; para recombinar, Tab no lab.


----


6. FAQ
--------


Por que posso treinar Tank quando o lab não tem patch perto, só patches centrais?

Ir até o Tech Lab voa você até o slot. O pouso coloca a Factory nas coordenadas do slot, mas apaga o objeto de terreno de construção mais próximo (muitas vezes um central). Reanexar verifica distância do lab até ``factory.x + 3500``, não qual patch foi usado.

Por que pouso central costumava reanexar?

Lógica antiga encaixava pouso em qualquer lugar do quadrado dentro de ~5,5 m do lab. Agora: vá ao patch do seu próprio lift-off → pouso no lugar; recombinar exige ir ao Tech Lab.

Slot alinhado mas parece longe do lab?

O lab fica no lado do host (~3,5 tiles de deslocamento), não sob o centro do host — layout estilo SC2.


----


7. Autores de mods (rules.txt)
----------------------------



.. list-table::
   :header-rows: 1

   * - Palavra-chave
     - Função
   * - ``can_have_addon``
     - Tipos de complemento permitidos no host
   * - ``is_addon 1``
     - Edifício complemento
   * - ``addon_host_types``
     - Quais hosts aceitam este complemento
   * - ``addon_grants_train_\<host\>``
     - Opções extras de treino quando anexado
   * - ``addon_grants_research``
     - Pesquisa extra quando anexado
   * - ``addon_train_multiplier``
     - Multiplicador do Reactor
   * - ``can_change_to`` / ``ground_form``
     - Formas de lift / pouso
   * - ``change_time``
     - Tempo de morph
   * - ``nb_build_site_by_square``
     - Preenche cada quadrado com ``build_site``; veja ``mod/mapmaking.rst`` e ``mod/building-land-terrain.htm``



Veja também ``mods/starcraft/readme.txt``.  
Referência do autor: seção *Build fields, addons & lift-off* de ``mod/modding.rst``.
