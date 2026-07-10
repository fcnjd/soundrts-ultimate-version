Interface de inventário e equipamento
=========================


Como as unidades usam inventário (mochila), a tela de equipamento e o modelo de item do mesmo tipo em ``rules.txt`` (um tipo pode ser item coletável e arma/armadura equipável).


----


1. Visão geral
-------------



.. list-table::
   :header-rows: 1

   * - Tela
     - Atalho
     - Mostra
   * - Atributos
     - `Alt+V`
     - todos os atributos
   * - Mochila
     - `Shift+V`
     - todos os itens do inventário
   * - Equipamento
     - `Ctrl+V`
     - armas e armaduras (equipamento do inventário + integrado)



Apenas uma tela por vez. Selecione exatamente uma unidade aliada.

Mochila vs equipamento
~~~~~~~~~~~~~~~~~~~~~~


- Mochila: equipar/usar/soltar qualquer item.
- Equipamento: apenas armas e armaduras. Equipamento integrado rotulado "built-in weapon / built-in armor" (somente leitura).

Equipamento integrado + itens misturados
~~~~~~~~~~~~~~~~~~~~~~~~~~~


Quando uma unidade tem equipamento ``class weapon``/``class armor`` e ``class item`` (ex.: ``weapons bow sword``):


.. list-table::
   :header-rows: 1

   * - Regra
     - Significado
   * - Prioridade no spawn
     - Integrado sempre equipado primeiro; itens vão para a mochila
   * - ``spawn_weapons_equipped 1`` (padrão)
     - Armas-item ficam na mochila e não podem ser equipadas manualmente
   * - ``spawn_weapons_equipped 0``
     - Armas-item na mochila podem ser equipadas
   * - Troca
     - Integrado ↔ integrado apenas; item ↔ item apenas; sem troca cruzada
   * - Armadura
     - Mesmo com ``spawn_armor_equipped``



Se a unidade tem apenas equipamento-item, as flags de spawn controlam equipamento silencioso na criação (padrão ligado).


----


2. Controles do jogador
--------------------


Abrir
~~~~~


- Exatamente 1 unidade aliada selecionada.
- Mochila: inventário não vazio.
- Equipamento: pelo menos uma arma ou armadura (integrada ou no inventário).

Na mochila / equipamento
~~~~~~~~~~~~~~~~~~~~~~~~



.. list-table::
   :header-rows: 1

   * - Tecla
     - Ação
   * - Setas
     - item anterior / próximo
   * - ``g``
     - ler introdução do item (de ``style.txt``)
   * - ``Enter``
     - equipar arma / vestir armadura / usar consumível
   * - ``Shift+Enter``
     - desequipar arma ou armadura
   * - ``Delete``
     - soltar (confirmar com Enter)
   * - ``Shift+Delete``
     - soltar sem confirmar
   * - ``Esc``
     - fechar / cancelar soltar



Mundo
~~~~~~


- Coletar: ``pickup`` (clique direito padrão).
- Soltar: ``drop`` ou Delete na interface.
- Dar: ``give`` — veja `give-to-npc.md <give-to-npc.htm>`_.


----


3. Dois sistemas de equipamento
--------------------------


3.1 Arma / armadura integrada (clássico)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


.. code-block:: text

   def footman
   weapons sword          ; class weapon
   armor footman_armor    ; class armor


Não entra na mochila. A tela de equipamento mostra como integrado; não pode desequipar ou soltar pela interface.

3.2 Equipamento-item na mochila (modelo do mesmo tipo)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


.. code-block:: text

   def sword
   class item
   equippable_as_weapon 1
   mdg 3.5
   ...


Atributos aplicam enquanto equipado; removidos ao desequipar. Veja ``res/rules.txt`` para exemplos ``sword``, ``footman_armor``.


----


4. Gerar equipamento na mochila
-----------------------------


No spawn:

- `weapons <name>`: se o tipo é ``class item`` + ``equippable_as_weapon 1`` → instância na mochila; equipamento silencioso se não houver arma integrada e ``spawn_weapons_equipped 1``.
- `armor <name>`: o mesmo para armadura.

Exemplo footman com espada-item + armadura-item: ambos na mochila, ambos equipados por padrão, visíveis em Shift+V e Ctrl+V.

.. code-block:: text

   spawn_weapons_equipped 0/1   ; padrão 1
   spawn_armor_equipped 0/1     ; padrão 1


Arqueiro misto
~~~~~~~~~~~~~


.. code-block:: text

   def archer
   weapons bow sword


- ``bow`` = ``class weapon`` → integrado, sempre equipado.
- ``sword`` = ``class item`` → mochila; com flag de spawn padrão, espada não pode ser equipada enquanto arco é integrado.

Defina ``spawn_weapons_equipped 0`` para permitir equipar espada manualmente (ainda sem troca direta arco↔espada).

Requisitos
~~~~~~~~~~~~~



.. list-table::
   :header-rows: 1

   * - Campo
     - Nota
   * - ``inventory_capacity``
     - deve ser > 0
   * - ``transport_volume``
     - espaço por item (padrão 1); capacidade conta itens, não volume




----


5. Checklist do autor
---------------------


Somente integrado
~~~~~~~~~~~~~~


.. code-block:: text

   def my_unit
   weapons short_sword
   armor light_armor


Coletável, equipável, removível
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


1. Defina item com ``equippable_as_weapon 1`` ou ``equippable_as_armor 1``.
2. Unidade: ``inventory_capacity`` + ``weapons my_sword``.
3. ``style.txt``: ``title``, ``intro``.

Consumíveis
~~~~~~~~~~~~


.. code-block:: text

   def health_potion
   class item
   buffs heal


Use com Enter na mochila (``use_item``), não na tela de equipamento.


----


6. Ordens do servidor
------------------



.. list-table::
   :header-rows: 1

   * - Ordem
     - Args
     - 
   * - ``equip_weapon``
     - id do item
     - 
   * - ``unequip_weapon``
     - id do item
     - 
   * - ``equip_armor``
     - id do item
     - 
   * - ``unequip_armor``
     - id do item
     - 
   * - ``use_item``
     - id do item
     - 
   * - ``drop``
     - id do item
     - 



Inventário transfere em upgrade/morph via ``transfer_inventory_to``.


----


7. FAQ
--------


P: Mochila vazia no footman?  
Arma integrada ``class weapon`` não entra na mochila até o tipo ser ``class item`` com lógica de spawn para inventário.

P: "Built-in armor" e não consigo desequipar?  
Ainda é ``class armor``; adicione ``class item`` + ``equippable_as_armor 1``.

P: Mesmo nome para item e arma?  
Sim (modelo do mesmo tipo): ex. ``sword`` como item para mochila/spawn; ``bow`` permanece ``class weapon`` puro.


----


8. Arquivos relacionados
------------------



.. list-table::
   :header-rows: 1

   * - Arquivo
     - 
   * - ``res/ui/bindings.txt``
     - Shift+V, Ctrl+V
   * - ``soundrts/attributes/inventory_screen.py``
     - interface da mochila
   * - ``soundrts/attributes/equipment_screen.py``
     - interface de equipamento
   * - ``soundrts/worldunit/worldbase.py``
     - lógica de spawn / equipar
   * - ``res/rules.txt``
     - exemplos



Veja também `give-to-npc <give-to-npc.htm>`_, `find-item-objective <find-item-objective.htm>`_.
