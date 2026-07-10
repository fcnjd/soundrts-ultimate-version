Herói entre capítulos da campanha (orientado por rules)
=======================================================


Campanhas single-player podem persistir um herói designado entre capítulos. Tudo é configurado em :strong:```rules.txt`` / ``campaign.txt`` — sem nomes de unidade fixos no código. Cooperativo não persiste heróis (sincronização de rede).

Visão do jogador: `menu de campanha <../../player/campaign-menu.htm>`_.


----


1. Três mecanismos entre capítulos
----------------------------------



.. list-table::
   :header-rows: 1

   * - Mecanismo
     - Onde
     - Carrega
     - Uso típico
   * - ``campaign_carryover``
     - campos de unidade em ``rules.txt``
     - Nível+XP, inventário (opcionalmente separado)
     - crescimento de herói RPG
   * - ``campaign_flag``
     - gatilhos de mapa
     - booleanos de história
     - alianças, missões secundárias
   * - ``add_inventory_item``
     - gatilhos de mapa
     - itens específicos
     - tokens, chaves




----


2. Campos de ``rules.txt``
--------------------------


Defina na def raiz do herói (variantes via ``is_a`` herdam).


.. list-table::
   :header-rows: 1

   * - Campo
     - Padrão
     - Significado
   * - ``campaign_carryover``
     - ``0``
     - ``1`` = ativar save entre capítulos
   * - ``campaign_carryover_id``
     - nome da def
     - prefixo em ``campaigns.ini``: `hero_<id>_`
   * - ``campaign_carryover_stats``
     - ``1`` com carryover ligado
     - Nível + XP
   * - ``campaign_carryover_inventory``
     - ``1`` com carryover ligado
     - Itens da mochila



Exemplos
~~~~~~~~


Carryover completo (padrão):

.. code-block:: text

   def my_hero
   is_a knight
   campaign_carryover 1
   inventory_capacity 8
   max_level 20
   xp_threshold_growth linear 100 50
   hp_max_per_level 20


(``xp_thresholds 200 500 1000`` explícito ainda funciona.)

Nível / XP iniciais (``level`` / ``xp``):

Igual à seção Heroes em ``mod/modding.rst`` (incluindo ``xp_threshold_growth`` desde 1.4.4.7):


.. list-table::
   :header-rows: 1

   * - Campo
     - Significado
   * - ``level``
     - Nível inicial (padrão `1`). Valores `> 1` aplicam `*_per_level` cumulativos e ``level_skills`` no spawn.
   * - ``xp``
     - XP cumulativo inicial opcional.
   * - ``level 0``
     - Começar abaixo do nível 1; o status mostra nível 0 e XP rumo a `xp_thresholds[0]`.



A restauração entre capítulos sobrescreve os padrões do mapa; o nível salvo é combinado com ``hero_min_level``, depois os bônus cumulativos são reaplicados.

Só stats (sem inventário):

.. code-block:: text

   campaign_carryover 1
   campaign_carryover_inventory 0


Só inventário (sem stats):

.. code-block:: text

   campaign_carryover 1
   campaign_carryover_stats 0


Sem carryover: omita ``campaign_carryover 1``.


----


3. ``campaign.txt``: nível mínimo
---------------------------------



.. code-block:: text

   hero_min_level 13:2 16:3 19:4


Pares capítulo:nível; o nível restaurado é ``max(saved, minimum)``.


----


4. Arquivo de save (``user/campaigns.ini``)
------------------------------------------



.. code-block:: ini

   hero_raynor_xp = 1200
   hero_raynor_level = 3
   hero_raynor_inventory = sword,health_potion
   flags = ch24_garrek_token


Atualizado só na vitória; tentar de novo após derrota não sobrescreve.


----


5. Código
---------


- `soundrts/campaign_hero.py <../../../soundrts/campaign_hero.py>`_
- `soundrts/tests/test_campaign_hero.py <../../../soundrts/tests/test_campaign_hero.py>`_


----


6. Cooperativo
--------------


Sem restauração/save de herói; ``campaign_flag`` também é no-op determinístico no cooperativo.
