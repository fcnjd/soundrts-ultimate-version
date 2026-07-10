Mod StarCraft: creep Zerg y tumores de la Reina
===============================================

Mod: activa ``mods = starcraft`` en ``SoundRTS.ini``.

Palabras clave de reglas: ``mod/modding.rst`` (Build fields). Guías Terran/Protoss: `starcraft-terran.htm <starcraft-terran-addons.htm>`_, `starcraft-resources.htm <starcraft-resources-vespene.htm>`_.

----

1. Dos propiedades de radio
---------------------------

Establece una por proveedor de creep/psi; deja la otra en 0.

.. list-table::
   :header-rows: 1

   * - Propiedad
     - Alcance
     - Notas
   * - ``build_field_radius``
     - Pasos BFS de casilla desde la casilla del edificio
     - Casillas discretas; estilo heredado
   * - ``build_field_radius_m``
     - Metros desde el ``(x, y)`` del edificio
     - Misma escala que el alcance de ataque; una casilla del mapa ≈ 12 m

Valores por defecto del mod StarCraft:

.. list-table::
   :header-rows: 1

   * - Edificio
     - Radio
   * - Hatchery
     - ``build_field_radius_m 12``
   * - Creep tumor
     - ``build_field_radius_m 4``
   * - Nexus
     - `18 m`
   * - Pylon
     - `12 m`

----

2. Creep vivo frente a creep marcado
------------------------------------

.. list-table::
   :header-rows: 1

   * - Tipo
     - Significado
   * - Vivo
     - Emitido actualmente por un Hatchery/tumor en pie (oyes creep al moverte cerca)
   * - Marcado
     - Pintura persistente de casilla + expansión (``build_field_persists``, ``build_field_spreads``)

- Los edificios Zerg necesitan una casilla marcada (``requires_build_field_on_square 1``).
- Al entrar en creep marcado visible se puede anunciar la etiqueta del campo.
- Tras la muerte del Hatchery, el creep marcado permanece; aún puedes construir sobre él.

Los Hatchery de radio en metros también pintan marcas cuando ``build_field_persists`` / ``build_field_spreads`` está activo — de lo contrario podrías oír creep vivo pero recibir «no se puede construir aquí».

----

3. Expansión
------------

``build_field_spreads 1`` — cada segundo de juego, las marcas de creep se expanden una capa a las casillas adyacentes (``build_field_spread_squares N`` para expansión más rápida).

Mapa de prueba: ``mods/starcraft/multi/zerg_creep_test.txt``.

----

4. Tumores de creep de la Reina (estilo SC2)
--------------------------------------------

Entrena Queen desde Queen's Nest (requiere Spawning Pool).

.. list-table::
   :header-rows: 1

   * - Habilidad
     - Coste
     - Alcance
     - Regla de objetivo
   * - Spawn creep tumor
     - 25 maná, 20 s de lanzamiento
     - 11
     - Casilla con creep vivo o marcado
   * - Extend creep tumor (en tumor)
     - 12 s de lanzamiento
     - 8
     - Casilla solo con creep marcado

- Spawn coloca un edificio invisible ``creep_tumor`` en la casilla objetivo.
- Cada tumor proporciona 4 m de creep y se expande como el creep del Hatchery.
- Extend encadena tumores hacia sitios de construcción lejanos (no puede saltar al borde solo-vivo — hay que esperar a la expansión/marca).

Mapa de prueba: ``mods/starcraft/multi/zerg_creep_tumor_test.txt``.

Atributos de modder en ``class skill``:

.. code-block:: text

   summon_requires_build_field creep
   summon_requires_marked_field 1    ; extend only

----

5. Lista rápida
---------------

1. El Hatchery pinta creep → espera la expansión o usa tumores de la Reina para alcanzar casillas lejanas.
2. Construye estructuras Zerg solo sobre creep marcado (F9/objetivos no relacionados).
3. Spire / pool / extractor sobre creep residual tras la muerte del Hatchery — ``zerg_creep_test`` paso 2.
