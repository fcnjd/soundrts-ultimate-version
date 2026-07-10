Mod StarCraft — minerais e vespene
==================================


Mod: ``mods/starcraft`` (``mods = starcraft`` em ``SoundRTS.ini``).

Recursos
--------


- Minerais (``resource1``): pressione Z
- Vespene (``resource2``): pressione X

Sintaxe de mapa:

.. code-block:: text

   mineral_field 1500 a1
   geyser 1 e1


Estruturas de gás
-----------------


Assimilator / Extractor / Refinery devem ser construídos sobre um geyser (Tab no geyser, depois construir). Construir em terreno edificável toca “não é possível construir ali”.

Após a conclusão:

1. A estrutura produz automaticamente (``auto_production``): a cada ``production_time`` segundos adiciona ``production_qty`` de vespene no edifício (padrão 18 s / 8 unidades)
2. Trabalhadores coletam do edifício de gás (``can_gather assimilator``, etc.) e carregam ``extraction_qty`` por viagem (padrão 8)
3. Vespene é armazenado no Nexus / Hatchery / Command Center (``storable_resource_types resource1 resource2``)

Use auto_production para gás, não auto_cultivate estilo fazenda (fazendas só reiniciam quando o armazenamento está vazio).

Tela de atributos
-----------------


Selecione uma estrutura de gás e pressione V para ouvir requires deposit (nome do tipo de depósito, ex.: geyser). Tempo e quantidade de produção usam as entradas de atributo de produção existentes.

Referência de regras: ``mod/modding.rst`` (Economy e Deposits & gas).

Mapa de teste: ``mods/starcraft/multi/sc_resources_test.txt``.
