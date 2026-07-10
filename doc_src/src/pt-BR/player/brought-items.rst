Levar item ao quadrado e entrega narrativa (``has_brought_item`` + ``remove_item``)
===================================================================================

Dois gatilhos usados juntos:

- ``has_brought_item`` (condição): unidade do jogador carrega um item até um quadrado
- ``remove_item`` (ação): remove e destrói o item do inventário (entrega narrativa)

Típico: levar poção de mana ao santuário → cut scene → poção some → objetivo completo.

Exemplo: The Legend of Raynor cap. 18 (`18.txt <../../../res/single/The Legend of Raynor/18.txt>`_).


----


1. vs outros gatilhos de item
-----------------------------



.. list-table::
   :header-rows: 1

   * - Gatilho
     - Detecta / efeito
     - Local do item
     - Caso de uso
   * - ``has_item``
     - jogador possui o item
     - inventário de qualquer unidade
     - encontrado / pegou
   * - ``has_brought_item``
     - item carregado no quadrado
     - unidades naquele quadrado
     - entregar chegando (sem dropar)
   * - ``find``
     - objeto no chão
     - dropado no quadrado
     - colocar item; sintaxe: quadrado primeiro ``(find c3 mana_potion)``
   * - ``npc_has_item``
     - NPC recebeu o item
     - inventário do NPC / ``received_items``
     - dar ao NPC
   * - ``remove_item``
     - destruir do inventário
     - —
     - entrega narrativa automática



----


2. Condição: ``has_brought_item``
---------------------------------



.. code-block:: text

   (has_brought_item <square> <item_type> [count])


- Quadrado: ex. ``c3``, `"3,3"`
- Tipo de item: ex. ``mana_potion``
- Contagem: opcional, padrão `1`

Verdadeiro quando pelo menos uma unidade viva do jogador naquele quadrado possui o suficiente do item no inventário.

- Mãos vazias no quadrado → falso
- Item em outro lugar, unidade fora do quadrado → falso
- Carregado até o quadrado → verdadeiro (não precisa dropar)


----


3. Ação: ``remove_item``
------------------------



.. code-block:: text

   (remove_item <item_type> [square] [count])


- Sem quadrado: remove de todas as unidades vivas do jogador
- Com quadrado: só unidades naquele quadrado
- Contagem: opcional, padrão `1`

O item é destruído (como consumir). Combine com ``cut_scene`` para a narrativa.


----


4. Exemplo completo (cap. 18)
-----------------------------



.. code-block:: text

   trigger player1 (has_brought_item c3 mana_potion)
       (do (cut_scene 7560) (remove_item mana_potion c3) (objective_complete 1))



Encadeie várias ações com ``do``. Não use ``if`` para três ações em sequência.

Fluxo: pegar poção → andar até o santuário em c3 → condição verdadeira → cut scene → item removido → objetivo 1 concluído.


----


5. vs dar ao NPC
----------------



.. list-table::
   :header-rows: 1

   * - Método
     - Quando
   * - ``npc_has_item`` + ``give`` do jogador
     - receptor NPC físico
   * - ``has_brought_item`` + ``remove_item``
     - chegar e entregar, sem NPC, história automática



----


6. Arquivos relacionados
------------------------



.. list-table::
   :header-rows: 1

   * - Conteúdo
     - Caminho
   * - Implementação
     - ``soundrts/worldplayerbase/triggers.py``
   * - Mapa de exemplo
     - `res/single/The Legend of Raynor/18.txt`
   * - Encontrar item
     - `find-item <../mod/campaign/find-item.htm>`_
   * - Dar ao NPC
     - `give-to-npc <../mod/campaign/give-to-npc.htm>`_
