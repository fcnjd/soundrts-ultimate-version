Vitória por encontrar item (gatilho ``has_item``)
=================================================


Projete objetivos em que pegar um item completa a meta.

Condição central: :strong:```has_item`` — o jogador possui o item no inventário de alguma unidade viva?


----


1. Visão geral
--------------



.. list-table::
   :header-rows: 1

   * - Parte
     - Nome
     - Função
   * - Campo de unidade
     - ``class item``
     - item coletável
   * - Ordem padrão
     - ``pickup``
     - clique direito no item no chão
   * - Condição
     - ``has_item``
     - jogador possui o tipo de item



Fluxo: colocar item → pickup → ``(has_item …)`` → `` (objective_complete N)`` → vitória quando todos os objetivos estiverem feitos.


Não defina ``consume_on_pickup 1`` (padrão 0). Se consumido ao pegar, ``has_item`` nunca fica verdadeiro.


----


2. ``has_item``
---------------


.. code-block:: text

   (has_item <item_type> [count])


Conta itens nos inventários de todas as unidades vivas do jogador.

.. code-block:: text

   (has_item lost_amulet)
   (has_item lost_amulet 2)



.. list-table::
   :header-rows: 1

   * - Condição
     - Verifica
   * - ``has``
     - contagem de unidades possuídas
   * - ``has_item``
     - itens no inventário
   * - ``has_brought_item``
     - carregado até o quadrado
   * - ``npc_has_item``
     - NPC recebeu o item
   * - ``find``
     - item no chão no quadrado




----


3. Definir item de missão
-------------------------


.. code-block:: text

   def lost_amulet
   class item


Quem pega precisa de ``inventory_capacity \> 0`` (peasant, footman, …).


----


4. Colocar no mapa
------------------


.. code-block:: text

   lost_amulet c3
   lost_amulet 2 c3



----


5. Exemplo (cap. 17)
--------------------


Veja `17.txt <../../../res/single/The Legend of Raynor/17.txt>`_:

.. code-block:: text

   trigger player1 (timer 0) (add_objective 1 "find the lost amulet")
   trigger player1 (has_item lost_amulet) (objective_complete 1)



----


6. Composto: cap. 20 (carregar + usar no inventário)
----------------------------------------------------


`mystery_treasure <../../../res/single/The Legend of Raynor/20.txt>`_: pegar → ``has_brought_item b2`` → usar no santuário (``use_square b2``) → recompensa em ouro.


----


7. Composto: cap. 22 (dropar + coletar moedas)
---------------------------------------------


`sealed_treasure <../../../res/single/The Legend of Raynor/22.txt>`_: dropar em b2 → ``find`` + ``remove_ground_item`` → spawn ``gold_coin`` → pegar todas.


----


8. Composto: cap. 23 (dropar = entregar)
---------------------------------------


`war_supplies <../../../res/single/The Legend of Raynor/23.txt>`_: ``has_item`` e depois ``find c3 war_supplies`` após o drop.


.. list-table::
   :header-rows: 1

   * - Capítulo
     - Item
     - Entrega
   * - 20
     - ``mystery_treasure``
     - carregar + uso no inventário
   * - 22
     - ``sealed_treasure``
     - dropar, abrir, coletar moedas
   * - 23
     - ``war_supplies``
     - dropar na estação




----


9. Caps. 24–27
--------------


Pegue ``secret_letter`` em ``b1`` (mesmo fluxo de ``has_item``), depois entregue ao líder (``npc_has_item``). Veja `arco do Norte <../../player/campaign-northern-arc.htm>`_.


----


10. Implementação
-----------------


- ``lang_has_item`` em ``soundrts/worldplayerbase/triggers.py``
- Exemplo: `res/single/The Legend of Raynor/17.txt`, ``rules.txt`` (``lost_amulet``)
