Mod StarCraft: creep Zerg e tumores da Queen
============================================


Mod: ative ``mods = starcraft`` em ``SoundRTS.ini``.

Palavras-chave de regras: ``mod/modding.rst`` (Build fields). Guias Terran/Protoss: `starcraft-terran.htm <starcraft-terran.htm>`_, `starcraft-resources.htm <starcraft-resources.htm>`_.


----


1. Duas propriedades de raio
----------------------------


Defina uma por provedor de creep/psi; mantenha a outra em 0.


.. list-table::
   :header-rows: 1

   * - Propriedade
     - Alcance
     - Notas
   * - ``build_field_radius``
     - passos BFS em tiles a partir do quadrado do edifício
     - Quadrados discretos; estilo legado
   * - ``build_field_radius_m``
     - Metros a partir de ``(x, y)`` do edifício
     - Mesma escala do alcance de ataque; um quadrado do mapa ≈ 12 m



Padrões do mod StarCraft:


.. list-table::
   :header-rows: 1

   * - Edifício
     - Raio
   * - Hatchery
     - ``build_field_radius_m 12``
   * - Creep tumor
     - ``build_field_radius_m 4``
   * - Nexus
     - `18 m`
   * - Pylon
     - `12 m`




----


2. Creep vivo vs creep marcado
------------------------------



.. list-table::
   :header-rows: 1

   * - Tipo
     - Significado
   * - Vivo
     - Emitido agora por Hatchery/tumor em pé (você ouve creep ao se mover perto)
   * - Marcado
     - Pintura persistente do quadrado + espalhamento (``build_field_persists``, ``build_field_spreads``)



- Edifícios Zerg precisam de um quadrado marcado (``requires_build_field_on_square 1``).
- Entrar em creep marcado visível pode anunciar o rótulo do campo.
- Após a morte da Hatchery, o creep marcado permanece; ainda é possível construir nele.

Hatcheries com raio em metros também pintam marcas quando ``build_field_persists`` / ``build_field_spreads`` está definido — senão você poderia ouvir creep vivo mas receber "não é possível construir aqui".


----


3. Espalhamento
---------------


``build_field_spreads 1`` — a cada segundo de jogo, as marcas de creep expandem uma camada para quadrados adjacentes (``build_field_spread_squares N`` para espalhar mais rápido).

Mapa de teste: ``mods/starcraft/multi/zerg_creep_test.txt``.


----


4. Tumores de creep da Queen (estilo SC2)
-----------------------------------------


Treine a Queen no Queen's Nest (requer Spawning Pool).


.. list-table::
   :header-rows: 1

   * - Habilidade
     - Custo
     - Alcance
     - Regra de alvo
   * - Spawn creep tumor
     - 25 mana, 20 s de cast
     - 11
     - Quadrado com creep vivo ou marcado
   * - Extend creep tumor (no tumor)
     - 12 s de cast
     - 8
     - Quadrado só com creep marcado



- Spawn coloca um edifício ``creep_tumor`` invisível no quadrado alvo.
- Cada tumor fornece 4 m de creep e se espalha como o creep da Hatchery.
- Extend encadeia tumores rumo a locais de construção distantes (não pode pular para a borda só-viva — precisa esperar o espalhamento/marca).

Mapa de teste: ``mods/starcraft/multi/zerg_creep_tumor_test.txt``.

Atributos do modder em ``class skill``:

.. code-block:: text

   summon_requires_build_field creep
   summon_requires_marked_field 1    ; extend only



----


5. Checklist rápido
-------------------


1. Hatchery pinta creep → espere o espalhamento ou use tumores da Queen para alcançar quadrados distantes.
2. Construa estruturas Zerg só em creep marcado (F9/objetivos não relacionados).
3. Spire / pool / extractor em creep remanescente após a morte da Hatchery — ``zerg_creep_test`` passo 2.
