# Mod StarCraft: complementos Terran y recombinar

Mod: activa ``mods = starcraft`` en ``SoundRTS.ini``.

Esta guía cubre los complementos Tech Lab / Reactor: construir, despegar y desprender, recombinar en vuelo, y la diferencia entre **suelo edificable** (permiso de construcción) y alineación de ranura (reattach).

Los mapas StarCraft usan **sitios de construcción** (``build_site``, terreno de casilla ``build_sites``) en lugar de **prados** clásicos. Abajo, «suelo edificable» significa cualquier objeto ``class building_land``; en este mod suele ser ``build_site``.

----

1. Conceptos
------------

.. list-table::
   :header-rows: 1

   * - Término
     - Significado
   * - Anfitrión
     - Barracks, Factory o Starport (``can_have_addon``)
   * - Complemento
     - Tech Lab o Reactor (``is_addon 1``), construido en la ranura lateral del anfitrión
   * - Ranura
     - Unos 3,5 baldosas al este del anfitrión (``addon_offset_x``, por defecto 3500 unidades internas)
   * - Suelo edificable
     - Un objeto ``class building_land`` en la casilla (``build_site`` en este mod); los edificios Terran terrestres deben consumir uno para aterrizar
   * - Recombinar
     - Tras el despegue el complemento permanece en el suelo; otro anfitrión aterriza con la ranura alineada y reatacha automáticamente el complemento huérfano

Tech Lab concede por anfitrión, p. ej.:

- Barracks + Tech Lab → Marauder
- Factory + Tech Lab → Siege Tank
- Starport + Tech Lab → Medivac

Reactor usa ``addon_train_multiplier 2``.

----

2. Construir un complemento
---------------------------

1. Selecciona un anfitrión existente (p. ej. Barracks), no suelo desnudo.
2. Construye Tech Lab o Reactor desde el menú.
3. El complemento se autoconstruye en el lado del anfitrión (``self_constructs 1``); no usa su propia ranura de suelo edificable.

Mapa de prueba: ``terran_addon_test``.

----

3. Despegue
-----------

Barracks / Factory / Starport pueden cambiar a forma voladora (``can_change_to flying_*``):

1. Selecciona el edificio terrestre → change_to → variante voladora.
2. El anfitrión deja el suelo; el complemento permanece y se desprende.
3. Se restaura el suelo edificable donde estaba el anfitrión: **el mismo tipo que el edificio consumió al construirse** (``build_site`` en este mod). Si el mapa solo genera sitios de construcción (``nb_build_site_by_square``, ``building_land build_site``, etc.), el despegue deja un sitio de construcción — **no** necesitas ``default_building_land build_site`` en las reglas del mod para eso.

Una casilla puede tener varios parches (p. ej. Barracks y Factory despegan una vez cada uno → dos sitios de construcción). En inicios con un solo parche de mapa, la Factory puede empezar sin suelo edificable; los parches aparecen en la posición de despegue de cada edificio.

----

4. Aterrizaje normal frente a aterrizaje de recombinación
---------------------------------------------------------

4.1 Dos comprobaciones separadas
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1

   * - Paso
     - Decide
     - No decide
   * - Aterrizaje
     - Qué objeto de suelo edificable se consume; anfitrión (x, y)
     - Reattach
   * - Reattach
     - El Tech Lab huérfano se adjunta al anfitrión
     - Qué parche se usó

Suelo edificable = permiso para aterrizar (cualquier ``class building_land`` en la casilla; nombres de API como ``find_meadow_near_xy`` son históricos).  
Ranura = geometría: complemento en ``(host.x + 3500, host.y)``; el reattach requiere alineación de ranura dentro de ~2,5 baldosas de distancia Manhattan.

Puedes ver la Factory en un «parche central» mientras el entrenamiento de Tank funciona: la ranura está alineada, no porque el edificio esté sobre hierba bajo el lab.

4.2 Aterrizaje normal (propio parche de despegue)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

1. Tab el suelo edificable dejado cuando ese edificio despegó (sitio de construcción en este mod).
2. Retroceso (``go`` por defecto), espera hasta la llegada.
3. change_to forma terrestre.

El edificio aterriza ahí y no se hace cargo de un Tech Lab huérfano. Si queda un complemento huérfano compatible en la casilla, oyes: *Ve primero al Tech Lab, luego aterriza para reatachar el complemento* (TTS 7350).

4.3 Aterrizaje de recombinación (tomar Tech Lab huérfano)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

1. Construye Tech Lab en Barracks, despega Barracks (el lab se queda).
2. Despega Factory, vuela a esa casilla.
3. Tab el Tech Lab (no un parche de suelo edificable).
4. Retroceso go — el objetivo se convierte en la ranura de aterrizaje (~3,5 baldosas al oeste del lab), no el centro del lab.
5. change_to Factory.

Resultado:

- Factory aparece en las coordenadas de la ranura;
- Se consume el objeto de suelo edificable más cercano de la casilla (a menudo un parche central);
- La ranura se alinea con el lab → reattach automático → Tank (etc.) disponible.

Mapa de prueba: ``terran_recombine_test``; campaña ``sc_build_tests`` capítulo 4.

----

5. Referencia rápida
--------------------

.. list-table::
   :header-rows: 1

   * - Objetivo
     - Tab
     - Tras go
     - Resultado de change_to
   * - Aterrizar en el punto de despegue
     - Sitio de construcción del despegue
     - Retroceso
     - Sin reattach, sin Tank
   * - Tomar Tech Lab huérfano
     - Tech Lab
     - Retroceso (vuela a la ranura)
     - Reattach, Tank disponible

Con varios parches, la voz de Tab puede decir «build site» para todos — usa la dirección; para recombinar, Tab el lab.

----

6. Preguntas frecuentes
-----------------------

¿Por qué puedo entrenar Tank cuando el lab no tiene parche cerca, solo parches centrales?

Ir al Tech Lab te hace volar a la ranura. Aterrizar coloca la Factory en la ranura (x,y) pero elimina el objeto de suelo edificable más cercano (a menudo uno central). El reattach comprueba la distancia del lab a ``factory.x + 3500``, no qué parche se usó.

¿Por qué el aterrizaje central solía reatachar?

La lógica antigua ajustaba el aterrizaje en cualquier punto de la casilla a ~5,5 m del lab. Ahora: ve a tu propio parche de despegue → aterriza en el sitio; recombinar requiere ir al Tech Lab.

¿Ranura alineada pero parece lejos del lab?

El lab está en el lado del anfitrión (~3,5 baldosas de desplazamiento), no bajo el centro del anfitrión — diseño estilo SC2.

----

7. Autores de mods (rules.txt)
------------------------------

.. list-table::
   :header-rows: 1

   * - Palabra clave
     - Función
   * - ``can_have_addon``
     - Tipos de complemento permitidos en el anfitrión
   * - ``is_addon 1``
     - Edificio complemento
   * - ``addon_host_types``
     - Qué anfitriones aceptan este complemento
   * - ``addon_grants_train_\<host\>``
     - Opciones de entrenamiento extra al estar adjunto
   * - ``addon_grants_research``
     - Investigación extra al estar adjunto
   * - ``addon_train_multiplier``
     - Multiplicador del Reactor
   * - ``can_change_to`` / ``ground_form``
     - Formas de despegue / aterrizaje
   * - ``change_time``
     - Tiempo de morph
   * - ``nb_build_site_by_square``
     - Rellenar automáticamente cada casilla con ``build_site``; ver ``mod/mapmaking.rst`` y ``mod/building-land-terrain.htm``

Véase también ``mods/starcraft/readme.txt``.  
Referencia del autor: ``mod/modding.rst`` sección *Build fields, addons & lift-off*.
