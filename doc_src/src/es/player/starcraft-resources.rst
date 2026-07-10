Mod StarCraft — minerales y vespeno
===================================

Mod: ``mods/starcraft`` (``mods = starcraft`` en ``SoundRTS.ini``).

Recursos
--------

- Minerales (``resource1``): pulsa Z
- Vespeno (``resource2``): pulsa X

Sintaxis de mapa:

.. code-block:: text

   mineral_field 1500 a1
   geyser 1 e1

Estructuras de gas
------------------

Assimilator / Extractor / Refinery deben construirse sobre un geyser (Tab en el geyser, luego construir). Construir en suelo edificable reproduce «no se puede construir ahí».

Tras completarse:

1. La estructura produce automáticamente (``auto_production``): cada ``production_time`` segundos añade ``production_qty`` de vespeno al edificio (por defecto 18 s / 8 unidades)
2. Los trabajadores recolectan del edificio de gas (``can_gather assimilator``, etc.) y transportan ``extraction_qty`` por viaje (por defecto 8)
3. El vespeno se almacena en el Nexus / Hatchery / Command Center (``storable_resource_types resource1 resource2``)

Usa auto_production para el gas, no auto_cultivate al estilo de granjas (las granjas solo se reinician cuando el almacén está vacío).

Pantalla de atributos
---------------------

Selecciona una estructura de gas y pulsa V para oír que requiere depósito (nombre del tipo de depósito, p. ej. geyser). El tiempo y la cantidad de producción usan las entradas de atributo de producción existentes.

Referencia de reglas: ``mod/modding.rst`` (Economy and Deposits & gas).

Mapa de prueba: ``mods/starcraft/multi/sc_resources_test.txt``.
