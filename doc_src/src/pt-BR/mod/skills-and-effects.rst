Sistema de habilidades, cura, dano e efeitos
=============================================


.. epigraph:: Para **autores de mods**: configure habilidades ativas, auras de cura/dano embutidas nas unidades e efeitos de área no campo de batalha (``class effect``) em ``rules.txt``. Do básico ao avançado — leia os capítulos em ordem.


----


Ordem de leitura
----------------


1. **Habilidades ativas** (``class skill``) — golpes acionados pelo jogador ou por gatilho automático
2. **Cura/dano de unidade** (``heal_*`` / ``harm_*``) — clérigos, nuvens venenosas, ritmo de regeneração de vida/mana
3. **Efeitos de batalha** (``class effect``) — muralhas de fogo, auras, ataques em área com debuff
4. **Avançado** — rajadas burst, gatilho automático, tabela de referência de parâmetros de área

A lista completa de palavras-chave oficiais está em ``modding.htm``.


Para **autores de mods**: defina habilidades ativas com ``class skill`` em ``rules.txt``, sem código Python. Exemplo completo no mod oficial **``mods/wuxia/rules.txt``** (demonstração de habilidades wuxia).

Conceitos básicos
-----------------


Use ``class skill`` para definir habilidades, substituindo o antigo ``class ability``:

.. code-block:: text

   def fireball
   class skill
   mana_cost 50
   cost 10 0
   time_cost 30
   effect harm_target 60
   effect_target ask
   effect_range 12
   cooldown 10


As unidades aprendem habilidades via ``can_use_skill``; upgrades continuam usando ``can_use_tech``.

Sistema unificado de habilidades (desde 1.4.4.6)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


A mesma ``class skill`` pode configurar **lançamento manual** e **gatilho automático** ao mesmo tempo. Habilidades aprendidas ficam todas em ``can_use_skill`` da unidade.


+----+----+
| Atributo | Descrição |
+====+====+
| `manual_use 1` | Aparece no menu de comandos; o jogador pode lançar com tecla (padrão `1`) |
+----+----+
| `auto_trigger 1` | Dispara automaticamente em combate quando as condições são atendidas (padrão `0`) |
+----+----+
| `trigger_timing` | Momento do gatilho automático (veja abaixo) |
+----+----+


Ambos podem coexistir: por exemplo, ``manual_use 1`` + ``auto_trigger 1`` significa que o jogador pode lançar manualmente e a habilidade também pode disparar automaticamente em combate com certa probabilidade.

Os campos antigos ``active_trigger_skills``, ``attack_trigger_skills``, ``attack_replace_skills``, ``passive_trigger_skills`` ainda são compatíveis; mods novos devem usar apenas ``can_use_skill`` + ``auto_trigger`` / ``trigger_timing`` na habilidade.

Modos de gatilho de habilidade
------------------------------


Quatro momentos de gatilho automático (trigger_timing)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


É necessário definir ``auto_trigger 1`` e ``trigger_timing``. O valor padrão é ``on_hit``.


+------------------+------+------------+
| `trigger_timing` | Momento | Lista antiga na unidade (ainda compatível) |
+==================+======+============+
| `on_hit` | **Após o atacante acertar um inimigo** (padrão) | `active_trigger_skills` |
+------------------+------+------------+
| `on_attack` | Lançamento adicional **ao iniciar o ataque**; **o ataque normal continua** | `attack_trigger_skills` |
+------------------+------+------------+
| `on_attack_replace` | Lançamento **ao iniciar o ataque**, **substituindo o ataque normal** (se a habilidade disparar, o ataque normal é ignorado) | `attack_replace_skills` |
+------------------+------+------------+
| `on_damaged` | **Ao ser acertado por um inimigo** (passivo) | `passive_trigger_skills` |
+------------------+------+------------+


No gatilho automático, o jogo verifica mana (``mana_cost``), cooldown (``cooldown``), consome mana e entra em cooldown (igual ao lançamento manual). Se a habilidade tiver ``ready``, o gatilho automático também aguarda a preparação antes de aplicar o efeito.

**Atenção**: ``on_hit`` só dispara após o atacante causar dano a um **inimigo**; ``on_damaged`` é disparado pela unidade atingida quando **é acertada por um inimigo**.

Exemplo 1: dano adicional após acerto (on_hit)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^


Ao disparar contra o **inimigo acertado**, não use `self` em ``effect_target`` (o padrão é a própria unidade). Configuração prática:

.. code-block:: text

   def skill_poison_strike
   class skill
   auto_trigger 1
   manual_use 0
   trigger_timing on_hit
   active_trigger_rate 30
   effect debuffs b_poison
   effect_target ask


No gatilho automático, ``ask`` resolve para o inimigo atualmente atingido. Teste em ``test_wuxia_skills.py``, caso ``skill_proc``.

Exemplo 2: buff adicional ao atacar (on_attack)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^


.. code-block:: text

   def skill_battle_cry
   class skill
   auto_trigger 1
   manual_use 0
   trigger_timing on_attack
   active_trigger_rate 50
   effect buffs b_battle_cry
   effect_target self


Ao iniciar o ataque, 50% de chance de aplicar buff em si mesmo; **o ataque normal desta vez continua**.

Exemplo 3: substituir ataque normal (on_attack_replace)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^


.. code-block:: text

   def skill_flame_strike
   class skill
   auto_trigger 1
   manual_use 1
   trigger_timing on_attack_replace
   active_trigger_rate 100
   effect harm_target mdg
   effect_target ask
   effect_range 1
   mdg 15
   cooldown 3
   mana_cost 10


Ao iniciar o ataque, tenta lançar; se tiver sucesso, **não realiza o ataque normal desta vez**. Pode manter ``manual_use 1`` para o jogador também lançar pelo menu.

Exemplo 4: contra-ataque ao ser atingido (on_damaged)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^


.. code-block:: text

   def skill_thorns
   class skill
   auto_trigger 1
   manual_use 0
   trigger_timing on_damaged
   passive_trigger_rate 30
   effect harm_target 10
   effect_target ask


Ao ser acertado por um inimigo, 30% de chance de causar 10 de dano fixo ao **atacante** (``effect_target ask`` no gatilho passivo resolve para o atacante).

Exemplo 5: manual e automático juntos
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^


.. code-block:: text

   def skill_heal_proc
   class skill
   auto_trigger 1
   manual_use 1
   trigger_timing on_hit
   active_trigger_rate 15
   effect buffs b_small_heal
   effect_target self
   mana_cost 20
   cooldown 8


O jogador pode curar manualmente com a tecla da habilidade; em combate, ao acertar um inimigo, há 15% de chance de disparo automático (ainda consome mana e respeita o cooldown).

Probabilidade de gatilho
~~~~~~~~~~~~~~~~~~~~~~~~



+----+------+----+
| Atributo | Momento aplicável | Descrição |
+====+======+====+
| `active_trigger_rate` | `on_hit`, `on_attack`, `on_attack_replace` | Probabilidade de 1–100 (padrão 100) |
+----+------+----+
| `passive_trigger_rate` | `on_damaged` | Probabilidade de 1–100 (padrão 100) |
+----+------+----+
| `mdg_trigger_rate` | Momentos ativos acima | Se > 0, **tem prioridade em ataque corpo a corpo**, substituindo `active_trigger_rate` |
+----+------+----+
| `rdg_trigger_rate` | Momentos ativos acima | Se > 0, **tem prioridade em ataque à distância**, substituindo `active_trigger_rate` |
+----+------+----+


Exemplo: gatilho ao acertar com 80% corpo a corpo e 40% à distância:

.. code-block:: text

   active_trigger_rate 100
   mdg_trigger_rate 80
   rdg_trigger_rate 40
   trigger_timing on_hit


Condições de gatilho
~~~~~~~~~~~~~~~~~~~~



+----+----+
| Atributo | Descrição |
+====+====+
| `trigger_condition` | Expressão condicional no formato `atributo operador valor` (três palavras, separadas por espaço) |
+----+----+
| `hp_threshold` | Atalho: só dispara quando a porcentagem de vida ≤ limiar (inteiro, ex.: `30` = 30% ou menos) |
+----+----+


A sintaxe de ``trigger_condition`` é a mesma dos buffs. ``hp`` e ``mana`` nas condições são comparados em **porcentagem**:

.. code-block:: text

   trigger_condition hp < 30


Equivalente ao atalho ``hp_threshold 30`` (só dispara com vida ≤ 30%).

**Limitação**: ``trigger_condition`` / ``hp_threshold`` são verificados atualmente nos caminhos ``on_hit`` e ``on_damaged``; ``on_attack`` / ``on_attack_replace`` **não** verificam essas condições.

Preparação (ready)
~~~~~~~~~~~~~~~~~~


.. code-block:: text

   ready 2


Gatilho automático e lançamento manual aguardam ``ready`` segundos antes de executar o ``effect``; no ``style.txt`` da habilidade, ``ready <ID_do_som>`` toca o som no início da preparação.

Diferença entre gatilho automático de habilidade e buff em ataque
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~



+----+------+------+
| Mecanismo | Onde configurar | Uso típico |
+====+======+======+
| `auto_trigger` da habilidade | `class skill` + `can_use_skill` | Lança o efeito completo da habilidade (harm, buff, deploy etc.) |
+----+------+------+
| Buff em ataque | `attack_trigger_buffs` / `attack_replace_buffs` etc. na unidade | Apenas aplica buff/debuff, sem def de habilidade independente |
+----+------+------+
| `is_active` / `is_passive` do buff | `class buff` | O próprio buff se acumula ao atacar/ser atingido |
+----+------+------+


A mesma unidade pode usar gatilho automático de habilidade e buff em ataque ao mesmo tempo; probabilidade e cooldown são avaliados de forma independente.

Alvo e alcance
~~~~~~~~~~~~~~



+----+----+
| Atributo | Descrição |
+====+====+
| `effect_target` | `self` (própria unidade), `ask` (jogador escolhe alvo), `random` (casa aleatória) |
+----+----+
| `effect_range` | Alcance de lançamento (casas); `inf` = infinito |
+----+----+
| `effect_radius` | Raio do centro do efeito (alguns efeitos legados) |
+----+----+


Custo e cooldown
~~~~~~~~~~~~~~~~


``mana_cost``, ``cost`` (recursos), ``time_cost`` (segundos de conjuração), ``cooldown`` (segundos de recarga), ``ready`` (segundos de preparação; no ``style.txt`` da habilidade, ``ready <som>`` toca o efeito sonoro).

Efeitos gerais de habilidade (effect)
-------------------------------------


Sintaxe: ``effect <tipo> [parâmetros…]``

Cada habilidade normalmente tem uma linha ``effect``. O motor suporta os tipos executáveis abaixo (efeitos legados e gerais desde 1.4.4.6):

harm_target — dano em alvo único
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


**Dano verdadeiro fixo** (ignora armadura):

.. code-block:: text

   effect harm_target 60


**Dano pelo pipeline de combate** (armadura, crítico, splash etc.; atributos de combate não nulos na habilidade sobrescrevem o lançador):

.. code-block:: text

   effect harm_target mdg
   effect harm_target rdg


Exemplos wuxia: ``skill_lipi`` (60 fixo), ``skill_lipi_mdg`` (mdg de combate).

harm_area — dano em área
~~~~~~~~~~~~~~~~~~~~~~~~


**Dano verdadeiro fixo**:

.. code-block:: text

   effect harm_area <dano> <raio>


Exemplo (wuxia ``skill_heng_sao``): ``effect harm_area 50 3`` (50 de dano verdadeiro fixo, raio 3).

**Dano em área pelo pipeline de combate**:

.. code-block:: text

   effect harm_area mdg <raio>
   effect harm_area rdg <raio>


O raio pode ser omitido; nesse caso usa ``effect_radius`` da habilidade (padrão 6). A habilidade pode sobrescrever atributos de combate:

.. code-block:: text

   def skill_heng_sao_mdg
   class skill
   effect harm_area mdg 3
   mdg 12
   mdg_splash 6
   mdg_radius 1.5
   mdg_splash_decay_min 0.5
   effect_target ask
   effect_range 8


burst — rajada (habilidade)
~~~~~~~~~~~~~~~~~~~~~~~~~~~


.. code-block:: text

   effect burst mdg <vezes> (interval <seg>) (window <seg>)
   effect burst rdg <vezes> (interval <seg>) (window <seg>)


Ou use atraso por golpe:

.. code-block:: text

   effect burst mdg 3 (delays 0 0.2 0.5)


- `interval`: intervalo entre golpes adjacentes (segundos)
- `window`: janela total da rajada (segundos)
- `delays`: lista de atrasos absolutos por golpe; o tamanho deve ser igual ao número de golpes

O dano vem de ``mdg`` / ``rdg`` da habilidade ou do lançador, com atributos de combate completos. Exemplos wuxia: ``skill_jifengci``, ``skill_jifengci_rdg``.

.. epigraph:: **Atenção: `effect burst` de habilidade ≠ rajada de ataque `damage_seq` da unidade.** Veja a seção «Avançado» neste documento e `player/burst-attacks.htm`.


push — empurrão
~~~~~~~~~~~~~~~


.. code-block:: text

   effect push <distância>


Empurra o alvo inimigo para longe do lançador, buscando automaticamente uma casa onde possa ficar. Exemplo wuxia: ``skill_moli_dan`` (``effect push 5``).

buffs / debuffs — aplicar buff ou debuff
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


.. code-block:: text

   effect buffs <nome_buff> [<nome_buff2> …]
   effect debuffs <nome_debuff>


- `effect_target self`: aplica em si mesmo
- `effect_target ask` + `effect_range`: aplica no alvo selecionado

``debuffs`` só afeta inimigos. Exemplo wuxia: ``skill_douzhuan`` → ``effect buffs b_douzhuan``.

**Reflexão de dano**: não existe ``effect reflect`` independente. Configure ``reflect_percent`` (porcentagem) na definição do buff e aplique com ``effect buffs`` da habilidade. Exemplo wuxia: ``reflect_percent 100`` em ``b_douzhuan``.

deploy — implantar efeito de batalha
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


.. code-block:: text

   effect deploy <segundos_vida> [<quantidade>] <nome_tipo class effect>


Coloca uma entidade ``class effect`` na casa alvo (muralha de fogo, zona de cura etc.). Detalhes na seção 3 «Efeitos de batalha».

summon — invocar unidade
~~~~~~~~~~~~~~~~~~~~~~~~


.. code-block:: text

   effect summon <segundos_vida> [<quantidade>] <tipo_unidade> …


Opcional: ``summon_requires_build_field``, ``summon_requires_marked_field``.

Efeitos legados (ainda utilizáveis)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~



+--------+----+
| effect | Descrição |
+========+====+
| `teleportation` | Teleporta unidade aliada para a casa alvo |
+--------+----+
| `recall` | Recolhe unidade aliada da casa alvo até o lançador |
+--------+----+
| `conversion` | Converte unidade inimiga |
+--------+----+
| `raise_dead <seg> <unidade…>` | Ressuscita a partir de cadáver |
+--------+----+
| `resurrection <limite>` | Ressuscita cadáveres aliados |
+--------+----+
| `harm <nível>` | Antigo: gera efeito harm temporário na casa alvo (prefira `harm_target` / `harm_area`) |
+--------+----+


Não executáveis (apenas exibição na UI)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


``effect heal`` e ``effect damage`` só formatam a exibição na tela de atributos; **não** curam nem causam dano ao lançar. Para cura, use ``heal_*`` na unidade, ``class effect`` ou ``effect buffs`` que melhoram atributos de cura.

Filtro de tipo de alvo (harm_target_type)
-----------------------------------------


Válido para ``burst``, ``harm_target``, ``harm_area``, ``push``. Se não configurado, **só afeta inimigos** por padrão (desde 1.4.4.6).

.. code-block:: text

   harm_target_type enemy ground unit -building


- Prefixo `-` em uma tag exclui, ex.: `-building`, `-undead`, `-enemy`
- `harm_target_type` e `target_type` do buff: tags positivas são **AND** (todas devem ser satisfeitas)
- `heal_target_type` e `mdg_targets` / `rdg_targets`: tags positivas são **OR**

Exemplos:

.. code-block:: text

   harm_target_type enemy unit -building
   heal_target_type unit -undead
   mdg_targets ground air -building


Referência mod: wuxia habilidade a habilidade
---------------------------------------------


Mod de demonstração oficial: ``mods/wuxia/rules.txt``. Mapa de teste: ``mods/wuxia/multi/skills_test.txt``.


+----+-----------+----+
| Habilidade | Tipo de effect | Pontos-chave |
+====+===========+====+
| `skill_jifengci` | `burst mdg` | 5 golpes, intervalo 0,2 s, janela 1 s, alcance corpo a corpo 2 |
+----+-----------+----+
| `skill_jifengci_rdg` | `burst rdg` | Idem, alcance à distância 6 |
+----+-----------+----+
| `skill_heng_sao` | `harm_area 50 3` | 50 de dano verdadeiro fixo, raio 3 |
+----+-----------+----+
| `skill_heng_sao_mdg` | `harm_area mdg 3` | Pipeline de combate + sobrescrita mdg/splash na habilidade |
+----+-----------+----+
| `skill_lipi` | `harm_target 60` | 60 de dano verdadeiro fixo |
+----+-----------+----+
| `skill_lipi_mdg` | `harm_target mdg` | Dano em alvo único pelo pipeline de combate |
+----+-----------+----+
| `skill_douzhuan` | `buffs b_douzhuan` | Buff em si; reflexão via `reflect_percent` do buff |
+----+-----------+----+
| `skill_moli_dan` | `push 5` | Empurrão de 5 casas |
+----+-----------+----+


A unidade portadora ``wuxia_hero`` aprende todas as 8 habilidades via ``can_use_skill``.

Avançado
--------


Diferença entre burst de habilidade e damage_seq da unidade
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~



+----+-------------------+-----------------+
| Item | `effect burst` da habilidade | `damage_seq` da unidade |
+====+===================+=================+
| Onde configurar | Linha `effect` em `class skill` | `damage_seq` na def da unidade |
+----+-------------------+-----------------+
| Como dispara | Lançamento manual ou automático da habilidade | Ataque normal / ataque à distância |
+----+-------------------+-----------------+
| Fonte do dano | `mdg`/`rdg` da habilidade ou lançador + atributos de combate | `mdg`/`rdg` da unidade divididos em vários segmentos |
+----+-------------------+-----------------+
| Sintaxe de segmentos | `burst mdg N (interval X)` | `damage_seq mdg N [(damage …)]` |
+----+-------------------+-----------------+
| Documentação | Este doc + `modding.htm` | `player/burst-attacks.htm` |
+----+-------------------+-----------------+


Ambos usam o pipeline de combate, mas o ponto de configuração e o momento de disparo são totalmente diferentes — não misture a sintaxe.

Livro de habilidades e desbloqueio por upgrade
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


- `level_skills <nível> <habilidade> …`: aprende automaticamente ao subir de nível
- Item `skills` + `learn_level`: aprende ao usar livro de habilidades do inventário
- Detalhes em `modding.htm` e `relnotes.htm` §1.4.4.6

Sons
~~~~


``style.txt`` da habilidade: ``alert`` (selecionada), ``ready`` (preparação), ``triggered`` (efeito aplicado). Buff em ataque: veja ``triggered`` / ``noise loop`` do buff.

Documentação relacionada
------------------------


- Cura/dano embutido na unidade: `HEAL_HARM_自定义功能说明.md` (seção 2 deste documento)
- `class effect` de batalha e deploy: `EFFECT_BUFF_SYSTEM_说明.md` (seção 3 deste documento)
- Lista completa de palavras-chave: `modding.htm`
- Resumo das notas de versão: `relnotes.htm` §1.4.4.6

Para **autores de mods**: configure auras de cura, auras de dano e ritmo de regeneração de vida/mana nas unidades em ``rules.txt``, sem código Python. Use junto com habilidades ativas (``class skill``) e áreas de batalha (``class effect``).

Visão geral
-----------


Desde 1.4.1.7, dano e cura das unidades foram divididos em parâmetros granulares, configuráveis na **def da unidade** ou em **``class effect``**. Parâmetros na unidade indicam efeito contínuo ou periódico de cura/dano ao redor (ou em si mesma).

Parâmetros de dano (harm_*)
---------------------------



+----+----+
| Atributo | Descrição |
+====+====+
| `harm_level` | Quantidade de dano por tick (valor direto, 1 = 1 ponto) |
+----+----+
| `harm_cd` | Intervalo entre danos (segundos); armazenado internamente em ms, ex.: 7,5 s como `7.5` |
+----+----+
| `harm_ready` | Atraso antes do primeiro dano (segundos) |
+----+----+
| `harm_range` | Distância de ação (da unidade ao alvo) |
+----+----+
| `harm_radius` | Raio de ação centrado no alvo |
+----+----+
| `harm_target_type` | Tags de filtro de alvo |
+----+----+


Exemplo (nuvem venenosa na unidade):

.. code-block:: text

   def poison_aura_unit
   class soldier
   harm_level 2
   harm_cd 3
   harm_radius 4
   harm_target_type enemy unit -building


Comportamento de harm_target_type
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


- **Desde 1.4.4.6**: em habilidades, se `harm_target_type` não estiver configurado, o padrão é **só inimigos**.
- Pode usar `enemy`, `allied`, `ground`, `air`, `unit`, `building` etc.; prefixo `-` exclui, ex.: `-building`, `-undead`.
- Tags positivas são **AND** (todas devem ser satisfeitas).
- Sem tags diplomáticas como `enemy` / `allied`, auras harm antigas de unidade podem não distinguir aliados de inimigos; mods novos devem definir explicitamente `harm_target_type enemy …`.

Parâmetros de cura (heal_*)
---------------------------



+----+----+
| Atributo | Descrição |
+====+====+
| `heal_level` | Quantidade de cura por tick |
+----+----+
| `heal_cd` | Intervalo entre curas (segundos) |
+----+----+
| `heal_ready` | Atraso antes da primeira cura |
+----+----+
| `heal_range` | Distância de ação |
+----+----+
| `heal_radius` | Raio de ação |
+----+----+
| `heal_target_type` | Filtro de alvo; tags positivas são **OR** |
+----+----+


Exemplo (aura de cura estilo clérigo):

.. code-block:: text

   def priest
   class soldier
   heal_level 3
   heal_cd 2
   heal_radius 5
   heal_target_type allied unit -undead


Regeneração de vida e mana (regen)
----------------------------------



+----+----+
| Atributo | Descrição |
+====+====+
| `hp_regen` | Regeneração de vida por segundo |
+----+----+
| `hp_regen_cd` | Intervalo do tick de regeneração |
+----+----+
| `hp_regen_ready` | Atraso antes da primeira regeneração |
+----+----+
| `mana_regen` | Regeneração de mana por segundo |
+----+----+
| `mana_regen_cd` | Intervalo de regeneração de mana |
+----+----+
| `mana_regen_ready` | Atraso antes da primeira regeneração de mana |
+----+----+


Melhorar cura/dano via buff
---------------------------


Buffs podem alterar ``heal_level``, ``heal_cd``, ``heal_radius`` ou ``harm_level`` etc. (buff multiatributo). Exemplo:

.. code-block:: text

   def HealEnhancementBuff
   class buff
   stat heal_level heal_cd heal_radius
   v 1 1500 6
   duration 300
   temporary 1


- `v 1` em `heal_level` = +1 ponto real de cura
- `v 1500` em `heal_cd` = cooldown de 1,5 s (milissegundos)
- `v 6` em `heal_radius` = +6 de alcance

Aplicação por habilidade: ``effect buffs HealEnhancementBuff``.

Relação com class effect
------------------------


Entidades ``class effect`` usam os mesmos parâmetros ``harm_*`` / ``heal_*``, colocadas no campo por ``effect deploy`` de habilidades. Detalhes em ``EFFECT_BUFF_SYSTEM_说明.md``.

Diferença dos effects de habilidade
-----------------------------------



+----+----+
| Forma | Uso |
+====+====+
| `harm_*` / `heal_*` da unidade | Aura permanente ou periódica na unidade |
+----+----+
| `class effect` + `deploy` | Área temporária no campo (muralha de fogo, luz sagrada etc.) |
+----+----+
| `effect harm_target` / `harm_area` | Dano pontual/rajada de habilidade ativa |
+----+----+
| `effect buffs` | Altera indiretamente atributos heal/harm via buff |
+----+----+


**Não existe** effect executável ``effect heal``; use um dos três métodos acima para cura.

Crescimento por upgrade
-----------------------


Unidades podem ter ``heal_cd_per_level``, ``harm_radius_per_level`` e outros ``*_per_level`` que se acumulam ao subir de nível. Detalhes em ``relnotes.htm`` §1.4.4.6.

Referência rápida de parâmetros
-------------------------------



+----+----+----+
| Dano | Cura | Significado |
+====+====+====+
| `harm_level` | `heal_level` | Valor por tick |
+----+----+----+
| `harm_cd` | `heal_cd` | Intervalo |
+----+----+----+
| `harm_ready` | `heal_ready` | Atraso inicial |
+----+----+----+
| `harm_range` | `heal_range` | Distância |
+----+----+----+
| `harm_radius` | `heal_radius` | Raio |
+----+----+----+
| `harm_target_type` | `heal_target_type` | Filtro de alvo |
+----+----+----+


Para **autores de mods**: configure efeitos de área no campo com ``class effect``, buffs e debuffs com ``class buff`` / ``class debuff``; aplique via ``effect deploy`` ou ``effect buffs`` / ``debuffs`` em habilidades. Sem código Python.

Efeitos de batalha (class effect)
---------------------------------


Desde 1.4.1.7, entidades ``class effect`` podem causar dano em área, cura ou carregar debuff continuamente no mapa.

Exemplo de zona de dano
~~~~~~~~~~~~~~~~~~~~~~~


.. code-block:: text

   def exorcism
   class effect
   harm_level 2
   harm_cd 7.5
   harm_radius 6
   harm_target_type undead
   debuffs b_slow


Exemplo de zona de cura
~~~~~~~~~~~~~~~~~~~~~~~


.. code-block:: text

   def holy_ground
   class effect
   heal_level 5
   heal_cd 3
   heal_radius 4
   heal_target_type allied unit


Descrição dos parâmetros
~~~~~~~~~~~~~~~~~~~~~~~~


Parâmetros de dano e cura são os mesmos de ``harm_*`` / ``heal_*`` na unidade (seção 2 «Cura/dano de unidade»). ``class effect`` também aceita ``decay`` (segundos de vida; deploy pode especificar pela habilidade).

Implantação por habilidade
~~~~~~~~~~~~~~~~~~~~~~~~~~


.. code-block:: text

   def skill_blizzard
   class skill
   effect deploy 8 blizzard_fx
   effect_target ask
   effect_range 10


Sintaxe: ``effect deploy <seg> [<quantidade>] <nome_tipo_effect>``

Diferente de ``effect summon``: deploy só gera ``class effect``, não unidades. Opcional: ``summon_requires_build_field`` / ``summon_requires_marked_field`` (ex.: tumor de creep).

Exemplos embutidos em ``res/rules.txt`` (clérigo com ``effect deploy`` + ``class effect`` de exorcismo).

Buff e Debuff (class buff / class debuff)
-----------------------------------------


Sintaxe básica
~~~~~~~~~~~~~~


.. code-block:: text

   def b_slow
   class debuff
   stat speed
   v -2
   duration 10
   temporary 1
   stack 1



+----+----+
| Atributo | Descrição |
+====+====+
| `stat` | Atributos afetados (pode haver vários) |
+----+----+
| `v` | Bônus fixo |
+----+----+
| `dv` | Variação por segundo (com `dt`) |
+----+----+
| `percentage` | Bônus percentual |
+----+----+
| `duration` | Duração (segundos) |
+----+----+
| `temporary` | `1` = removido ao morrer |
+----+----+
| `stack` | Camadas empilháveis |
+----+----+
| `target_type` | Condições para ser alvo do buff (lógica AND) |
+----+----+
| `buff_radius` | Raio da aura (buff tipo aura) |
+----+----+


Aplicar buff por habilidade
~~~~~~~~~~~~~~~~~~~~~~~~~~~


.. code-block:: text

   def skill_douzhuan
   class skill
   effect buffs b_douzhuan
   effect_target self


.. code-block:: text

   def skill_curse
   class skill
   effect debuffs b_slow
   effect_target ask
   effect_range 8


Ataques também podem carregar: ``buffs`` / ``debuffs`` na def da unidade, ou via ``attack_trigger_buffs`` etc.

Reflexão de dano (reflect_percent)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


**Não há** palavra-chave ``effect reflect``. Configure na buff:

.. code-block:: text

   def b_douzhuan
   class buff
   duration 8
   temporary 1
   reflect_percent 100


Depois aplique com ``effect buffs b_douzhuan``. O mod wuxia «Dou Zhuan Xing Yi» segue esse padrão.

``reflect_percent`` é porcentagem inteira (100 = reflexão total).

Buff multiatributo
~~~~~~~~~~~~~~~~~~


Um buff pode afetar vários atributos ao mesmo tempo:

.. code-block:: text

   def HealEnhancementBuff
   class buff
   stat heal_level heal_cd heal_radius
   v 1 1500 6
   duration 300
   temporary 1


Regras de correspondência de valores:

- Número de atributos = número de valores: correspondência um a um
- Valores insuficientes: repete o último valor
- Um único valor: aplica a todos os atributos

Atributos de valor direto (``v 1`` = 1 ponto): ``hp``, ``mdg``, ``rdg``, ``heal_level``, ``harm_level``, ``heal_radius``, ``harm_radius``, ``speed`` e mais de 20 outros.

Atributos de tempo (milissegundos): ``heal_cd``, ``harm_cd``, ``mdg_cd``, ``rdg_cd`` etc.

Buff com gatilho
~~~~~~~~~~~~~~~~


.. code-block:: text

   def CombatStanceBuff
   class buff
   stat mdg rdg
   v 30 25
   duration 100
   temporary 1
   is_active 1
   mdg_trigger_rate 80



+----+----+
| Modo | Atributo |
+====+====+
| Após acertar ataque | Padrão |
+----+----+
| Ao iniciar ataque | `is_active 1` |
+----+----+
| Ao sofrer ataque | `is_passive 1` + `trigger_condition` + `passive_trigger_rate` |
+----+----+


Sons do buff (style.txt)
~~~~~~~~~~~~~~~~~~~~~~~~


.. code-block:: text

   def b_douzhuan
   triggered douzhuan_proc
   noise loop douzhuan_hum


- `triggered`: toca no momento da aplicação
- `noise loop`: em loop durante a duração
- `noise repeat <intervalo> <som…>`: repete no intervalo

Filtro de tipo de alvo (target_type)
------------------------------------


A sintaxe de ``target_type`` em buff/debuff é igual a ``harm_target_type``; várias condições em **AND**. Suporta exclusão ``-tag``:

.. code-block:: text

   target_type unit -undead -building


Relação com o sistema de habilidades
------------------------------------



+-----------+----+
| effect de habilidade | Função |
+===========+====+
| `effect deploy` | Coloca `class effect` |
+-----------+----+
| `effect buffs` / `debuffs` | Aplica buff no alvo |
+-----------+----+
| `effect harm_target` / `harm_area` | Dano direto (sem entidade effect) |
+-----------+----+


Palavras-chave completas de habilidade em ``GENERIC_SKILL_SYSTEM.md`` (seção 1).

Referência rápida
-----------------


Buff de melhoria de cura
~~~~~~~~~~~~~~~~~~~~~~~~


.. code-block:: text

   def heal_aura_buff
   class buff
   stack 1
   stat heal_level heal_cd heal_radius
   v 1 1500 6
   temporary 1
   duration 10
   target_type self


Buff de melhoria de dano
~~~~~~~~~~~~~~~~~~~~~~~~


.. code-block:: text

   def harm_aura_buff
   class buff
   stack 1
   stat harm_level harm_cd harm_radius
   v 2 -1000 4
   temporary 1
   duration 15
   target_type self


Exemplos mais completos de buff multiatributo em ``MULTI_ATTRIBUTE_BUFF_说明.md <MULTI_ATTRIBUTE_BUFF_说明.htm>``_. Reflexão de dano usa o atributo ``reflect_percent`` do buff (porcentagem inteira, 100 = total), aplicado por ``effect buffs``; não há ``effect reflect`` independente. Exemplo wuxia: ``b_douzhuan``.
