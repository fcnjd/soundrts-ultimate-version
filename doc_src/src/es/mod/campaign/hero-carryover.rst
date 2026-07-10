Traslado de héroes de campaña (dirigido por reglas)
===================================================

Las campañas de un jugador pueden conservar un héroe designado entre capítulos. Todo se configura en :strong:```rules.txt`` / ``campaign.txt`` — sin nombres de unidad codificados. El cooperativo no conserva héroes (sincronización de red).

Resumen para jugadores: `../player/campaign-menu <../player/campaign-menu.htm>`_.

----

1. Tres mecanismos entre capítulos
----------------------------------

.. list-table::
   :header-rows: 1

   * - Mecanismo
     - Dónde
     - Qué lleva
     - Uso típico
   * - ``campaign_carryover``
     - campos de unidad en ``rules.txt``
     - Nivel+XP, inventario (división opcional)
     - crecimiento de héroe RPG
   * - ``campaign_flag``
     - disparadores de mapa
     - booleanos de historia
     - alianzas, misiones secundarias
   * - ``add_inventory_item``
     - disparadores de mapa
     - objetos concretos
     - fichas, llaves

----

2. Campos de ``rules.txt``
--------------------------

Establécelos en la def raíz del héroe (las variantes vía ``is_a`` heredan).

.. list-table::
   :header-rows: 1

   * - Campo
     - Por defecto
     - Significado
   * - ``campaign_carryover``
     - ``0``
     - ``1`` = activar guardado entre capítulos
   * - ``campaign_carryover_id``
     - nombre de la def
     - prefijo `hero_<id>_` en ``campaigns.ini``
   * - ``campaign_carryover_stats``
     - ``1`` con carryover activo
     - Nivel + XP
   * - ``campaign_carryover_inventory``
     - ``1`` con carryover activo
     - Objetos de la mochila

Ejemplos
~~~~~~~~

Traslado completo (por defecto):

.. code-block:: text

   def my_hero
   is_a knight
   campaign_carryover 1
   inventory_capacity 8
   max_level 20
   xp_threshold_growth linear 100 50
   hp_max_per_level 20

(``xp_thresholds 200 500 1000`` explícito sigue funcionando.)

``Nivel / XP iniciales (``level`` / ``xp``):``

Igual que la sección Heroes en ``mod/modding.rst`` (incluido ``xp_threshold_growth`` desde 1.4.4.7):

.. list-table::
   :header-rows: 1

   * - Campo
     - Significado
   * - ``level``
     - Nivel inicial (por defecto `1`). Valores `> 1` aplican `*_per_level` acumulativos y ``level_skills`` al aparecer.
   * - ``xp``
     - XP acumulada inicial opcional.
   * - ``level 0``
     - Empezar por debajo del nivel 1; el estado muestra nivel 0 y XP hacia `xp_thresholds[0]`.

La restauración entre capítulos anula los valores por defecto del mapa; el nivel guardado se combina con ``hero_min_level``, luego se reaplica las bonificaciones acumulativas.

Solo estadísticas (sin inventario):

.. code-block:: text

   campaign_carryover 1
   campaign_carryover_inventory 0

Solo inventario (sin estadísticas):

.. code-block:: text

   campaign_carryover 1
   campaign_carryover_stats 0

Sin traslado: omite ``campaign_carryover 1``.

----

3. ``campaign.txt``: nivel mínimo
---------------------------------

.. code-block:: text

   hero_min_level 13:2 16:3 19:4

Pares capítulo:nivel; el nivel restaurado es ``max(saved, minimum)``.

----

4. Archivo de guardado (``user/campaigns.ini``)
-----------------------------------------------

.. code-block:: ini

   hero_raynor_xp = 1200
   hero_raynor_level = 3
   hero_raynor_inventory = sword,health_potion
   flags = ch24_garrek_token

Se actualiza solo al ganar; reintentar tras una derrota no sobrescribe.

----

5. Código
---------

- `soundrts/campaign_hero.py <../../../soundrts/campaign_hero.py>`_
- `soundrts/tests/test_campaign_hero.py <../../../soundrts/tests/test_campaign_hero.py>`_

----

6. Cooperativo
--------------

Sin restauración/guardado de héroe; ``campaign_flag`` también es un no-op determinista en cooperativo.
