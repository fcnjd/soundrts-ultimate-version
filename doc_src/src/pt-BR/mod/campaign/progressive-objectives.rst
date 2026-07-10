Objetivos progressivos de campanha (``register_objective``)
===========================================================


Para mapas single-player que revelam metas uma de cada vez (complete a meta 1, depois ouça a meta 2).

Referência oficial de gatilhos: ``mod/mapmaking.rst`` (Register_objective).


----


1. Problema
-----------


Cada ``add_objective`` faz duas coisas:

1. Mostra a meta em F9 e toca a voz de “novo objetivo”.
2. Adiciona esse número ao conjunto de requisitos de vitória.

Se um mapa só chama ``add_objective 1`` no início e ``add_objective 2`` depois que a meta 1 completa, completar a meta 1 costumava vencer a missão imediatamente — porque a meta 2 ainda não existia no conjunto de requisitos, ou a lógica antiga tratava “todos os objetivos visíveis feitos” como vitória.


----


2. Solução: ``register_objective``
----------------------------------


Registre todos os números primários de antemão sem exibi-los:

.. code-block:: text

   trigger player1 (timer 0) (do (register_objective 1 2 3) (add_objective 1 7001))
   trigger player1 (has barracks) (do (objective_complete 1) (add_objective 2 7002))
   trigger player1 (has 10 footman) (objective_complete 2)
   trigger player1 (has townhall) (objective_complete 3)



.. list-table::
   :header-rows: 1

   * - Ação
     - F9 / voz
     - Conjunto de vitória
   * - ``register_objective 1 2 3``
     - Não
     - Adiciona 1, 2, 3 a ``\_required_objective_numbers``
   * - ``add_objective 1 …``
     - Sim
     - Também adiciona 1 (se ainda não registrado)
   * - ``objective_complete 1``
     - Remove a meta 1 de F9
     - Adiciona 1 a ``\_completed_objective_numbers``



A vitória ocorre quando ``\_required_objective_numbers`` ⊆ ``\_completed_objective_numbers`` (``soundrts/worldplayerbase/base.py`` — ``\_all_required_objectives_done``).


----


3. Numeração em F9 e na voz
---------------------------


Quando mais de um objetivo primário está registrado ou visível:

- F9 mostra "Primary objective N:" e depois a descrição (dois-pontos após o número).
- Com apenas um objetivo primário, o número é omitido.

O motor varre os gatilhos do mapa no carregamento (``collect_planned_objective_numbers`` em ``soundrts/objective_announce.py``) para que os números fiquem corretos mesmo quando as chamadas ``add_objective`` estão em gatilhos ``timer 0`` separados.

Objetivos opcionais (``add_secondary_objective``) usam numeração independente com as mesmas regras.


----


4. Exemplos neste repositório
-----------------------------



.. list-table::
   :header-rows: 1

   * - Mapa
     - Padrão
   * - ``mods/starcraft/single/sc_build_tests/1.txt``
     - 2 metas Protoss encadeadas
   * - ``mods/starcraft/single/sc_late_game/1.txt``
     - 6 metas de late-game encadeadas



----


5. Testes
---------


.. code-block:: bash

   python -m pytest soundrts/tests/test_campaign_alliance_transfer_triggers.py -k register_objective -q
   python -m pytest soundrts/tests/test_objective_announce.py -q
   python -m pytest soundrts/tests/test_cmd_objectives.py -q
