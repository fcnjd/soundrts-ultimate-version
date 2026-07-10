Sistema de habilidades, tratamiento, daños y efectos.
=====================================================

.. epigraph:: Para **Autores de mods**: configure habilidades activas, auras de curación/daño basadas en unidades y efectos del área del campo de batalla (`class effect`) en `rules.txt`. De lo menos profundo a lo más profundo, se recomienda leer capítulo por capítulo.

----

orden de lectura
----------------

1. **Habilidades activas** (`class skill`): movimientos activados por los botones del jugador o automáticamente
2. **Unidad de curación/daño** (`heal_*` / `harm_*`) — Sacerdote, Nube venenosa, Ritmo de regeneración de vida/maná
3. **Efecto de campo de batalla** (`class effect`): muro de fuego, halo, ataque a distancia con desventaja
4. **Avanzado**: ráfaga combinada, disparo automático, tabla de comparación de parámetros de rango

Consulte también ``modding.htm`` para obtener la lista oficial de palabras clave.

Para **Autores de mods**: use ``class skill`` para definir habilidades activas en ``rules.txt``, no se requiere código fuente Python. Para ver un ejemplo completo, consulte el mod oficial **``mods/wuxia/rules.txt``** (Demostración de habilidades en artes marciales).

Conceptos básicos
-----------------

Utilice ``class skill`` para definir habilidades, reemplazando la versión anterior ``class ability``:

.. code-block:: text

   def fireball
   class skill
   mana_cost 50
   cost 10 0
   time_cost 30
   effect harm_target 60
   effect_target ask
   effect_range 12
   cooldown 10

Las unidades aprenden habilidades a través de ``can_use_skill``; las actualizaciones todavía usan ``can_use_tech``.

Sistema de habilidades unificado (de 1.4.4.6)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

El mismo ``class skill`` se puede configurar con **disparo manual** y **disparador automático** al mismo tiempo. Las habilidades aprendidas están escritas de manera uniforme en ``can_use_skill`` de la unidad.

+----+----+
| Propiedades | Descripción |
+
====+
====+
| `manual_use 1` | Aparece en el menú de comandos, los jugadores pueden presionar la tecla para soltar (predeterminado `1`) |
+----+----+
| `auto_trigger 1` | Se activa automáticamente cuando se cumplen las condiciones durante la batalla (predeterminado `0`) |
+----+----+
| `trigger_timing` | Momento de la activación automática (ver más abajo) |
+----+----+

Los dos pueden coexistir: por ejemplo, ``manual_use 1`` + ``auto_trigger 1`` significa que se puede liberar de forma manual o automática con probabilidad durante la batalla.

Los campos antiguos ``active_trigger_skills``, ``attack_trigger_skills``, ``attack_replace_skills``, ``passive_trigger_skills`` siguen siendo compatibles; Se recomienda que el nuevo mod solo use ``can_use_skill`` + ``auto_trigger`` / ``trigger_timing`` en habilidades.

Método de activación de habilidades
-----------------------------------

Cuatro tiempos de disparo automático (trigger_timing)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

``auto_trigger 1`` y ``trigger_timing`` deben configurarse al mismo tiempo. El valor predeterminado es ``on_hit``.

+------------------+------+----------+
| `trigger_timing` | Tiempo de activación | Lista de unidades antiguas (aún compatibles) |
+
===================+
======+
============+
| `on_hit` | Atacante **Después de golpear al enemigo** (predeterminado) | `active_trigger_skills` |
+------------------+------+----------+
| `on_attack` | **Liberación adicional al lanzar un ataque, **el ataque básico continúa como de costumbre** | `attack_trigger_skills` |
+------------------+------+----------+
| `on_attack_replace` | **Liberado al lanzar un ataque**, **reemplazando este ataque normal** (el ataque básico se omitirá si la habilidad se activa con éxito) | `attack_replace_skills` |
+------------------+------+----------+
| `on_damaged` | **Cuando es golpeado por el enemigo** (Pasivo) | `passive_trigger_skills` |
+------------------+------+----------+

Cuando se activa automáticamente, se verificará el maná (``mana_cost``) y el tiempo de reutilización (``cooldown``), se consumirá el maná y se ingresará el tiempo de reutilización (igual que la liberación manual). Si la habilidad está escrita como ``ready``, el disparador automático también entrará en movimiento hacia adelante antes de surtir efecto.

**Nota**: ``on_hit`` solo se activa después de que el atacante causa daño al **enemigo**; ``on_damaged`` lo activa la parte atacada cuando **es golpeado por un ataque enemigo**.

Ejemplo 1: daño adicional después del golpe (on_hit)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Cuando se activa contra **golpear al enemigo**, `⟦Y0⟧⟦Y1⟧⟦Y2⟧` (el valor predeterminado es uno mismo). Método práctico de escritura:

.. code-block:: text

   def skill_poison_strike
   class skill
   auto_trigger 1
   manual_use 0
   trigger_timing on_hit
   active_trigger_rate 30
   effect debuffs b_poison
   effect_target ask

Cuando se activa automáticamente `⟦Y0⟧⟦Y1⟧⟦Y2⟧⟦Y3⟧⟦Y4⟧`.

Ejemplo 2: agregar beneficio al disparo (on_attack)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: text

   def skill_battle_cry
   class skill
   auto_trigger 1
   manual_use 0
   trigger_timing on_attack
   active_trigger_rate 50
   effect buffs b_battle_cry
   effect_target self

Al lanzar un ataque, hay un 50% de probabilidad de mejorarse y **este ataque básico continuará**.

Ejemplo 3: Reemplazar ataque básico (on_attack_replace)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: text

   def skill_flame_strike
   class skill
   auto_trigger 1
   manual_use 1
   trigger_timing on_attack_replace
   active_trigger_rate 100
   effect harm_target mdg
   effect_target ask
   effect_range 1
   mdg 15
   cooldown 3
   mana_cost 10

Intente liberarse cuando comience el ataque; si tiene éxito, **esta vez no se realizará ningún ataque normal**. ``manual_use 1`` se puede conservar para que los jugadores también puedan lanzarlo manualmente desde el menú.

Ejemplo 4: Contraataque (on_damaged)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: text

   def skill_thorns
   class skill
   auto_trigger 1
   manual_use 0
   trigger_timing on_damaged
   passive_trigger_rate 30
   effect harm_target 10
   effect_target ask

Cuando es golpeado por un enemigo, hay un 30 % de posibilidades de causar 10 puntos de daño fijo al **atacante** (```effect_target ask``` se resuelve en el atacante cuando se activa pasivamente).

Ejemplo 5: Convivencia manual + automática
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: text

   def skill_heal_proc
   class skill
   auto_trigger 1
   manual_use 1
   trigger_timing on_hit
   active_trigger_rate 15
   effect buffs b_small_heal
   effect_target self
   mana_cost 20
   cooldown 8

Los jugadores pueden presionar el botón de habilidad para curarse manualmente; Hay un 15% de posibilidades de que se active automáticamente al golpear a un enemigo durante el combate (aún se consume maná y se respeta el tiempo de reutilización).

Probabilidad de activación
~~~~~~~~~~~~~~~~~~~~~~~~~~

+----+------+----+
| Propiedades | Hora aplicable | Descripción |
+
====+
======+
====+
| `active_trigger_rate` | `on_hit`, `on_attack`, `on_attack_replace` | Probabilidad de activación 1–100 (predeterminado 100) |
+----+------+----+
| `passive_trigger_rate` | `on_damaged` | Probabilidad de activación 1–100 (predeterminado 100) |
+----+------+----+
| `mdg_trigger_rate` | El tiempo de tipo activo anterior | Si > 0, **los ataques cuerpo a cuerpo se usan primero**, cubriendo `active_trigger_rate` |
+----+------+----+
| `rdg_trigger_rate` | La sincronización de tipo activo antes mencionada | Si > 0, **se utilizan primero los ataques remotos**, cubriendo `active_trigger_rate` |
+----+------+----+

Ejemplo: cuerpo a cuerpo 80%, disparo a distancia 40%:

.. code-block:: text

   active_trigger_rate 100
   mdg_trigger_rate 80
   rdg_trigger_rate 40
   trigger_timing on_hit

Condición de activación
~~~~~~~~~~~~~~~~~~~~~~~

+----+----+
| Propiedades | Descripción |
+
====+
====+
| `trigger_condition` |
+----+----+
| `hp_threshold` | Abreviatura: Se activa cuando el porcentaje de salud ≤ umbral (un número entero, como `30` significa menos del 30%) |
+----+----+

``trigger_condition`` La sintaxis es la misma que la de buff. ``hp``, ``mana`` Comparar por **Porcentaje** en condiciones:

.. code-block:: text

   trigger_condition hp < 30

Equivalente a la abreviatura ``hp_threshold 30`` (solo se puede activar cuando la salud ≤ 30%).

**Limitaciones**: ``trigger_condition`` / ``hp_threshold`` actualmente se verifican mediante las rutas ``on_hit`` y ``on_damaged``; ``on_attack`` / ``on_attack_replace`` **no** marca estas dos condiciones.

listo
~~~~~

.. code-block:: text

   ready 2

Es un gran lugar para comenzar, es un manual de liberación, es un manual de liberación, es una gran oferta, es una gran oferta.

Diferencias con el disparador de ataque de mejora
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

+----+------+------+
| Mecanismo | Ubicación de configuración | Uso típico |
+
====+
======+
======+
| Habilidad `auto_trigger` | `class skill` + `can_use_skill` | Libera el efecto completo de la habilidad (dañar, mejorar, desplegar, etc.) |
+----+------+------+
| El ataque viene con beneficio | Unidad `attack_trigger_buffs` / `attack_replace_buffs` etc. | Sólo se aplican ventajas/desventajas, no hay definición de habilidades independientes |
+----+------+------+
| pulir `is_active` / `is_passive` | `class buff` | acumulaciones de beneficios al atacar/recibir ataques |
+----+------+------+

La misma unidad puede utilizar la activación automática de habilidades y ventajas asociadas a los ataques al mismo tiempo; ambos determinan la probabilidad y el tiempo de reutilización de forma independiente.

Objetivos y alcance
~~~~~~~~~~~~~~~~~~~

+----+----+
| Propiedades | Descripción |
+
====+
====+
| `effect_target` | `self` (auto), `ask` (el jugador elige el objetivo), `random` (cuadrícula aleatoria) |
+----+----+
| `effect_range` | Distancia de lanzamiento (cuadrícula); `inf` es infinito |
+----+----+
| `effect_radius` | Radio del centro del efecto (utilizado por algunos efectos heredados) |
+----+----+

Consumo y refrigeración
~~~~~~~~~~~~~~~~~~~~~~~

``mana_cost``, ``cost`` (recursos), ``time_cost`` (segundos de canto), ``cooldown`` (segundos de enfriamiento), ``ready`` (segundos de avance; se puede definir en la habilidad ``style.txt`` para reproducir efectos de sonido).

Efectos generales de habilidad (efecto)
---------------------------------------

Gramática:``effect <tipo> [parámetros…]``

Por lo general, solo se escribe una línea para cada habilidad ``effect``. El motor admite los siguientes tipos de ejecutables (efectos heredados y genéricos 1.4.4.6):

harm_target — daño a un solo objetivo
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**DAÑO VERDADERO FIJADO** (Evita la armadura):

.. code-block:: text

   effect harm_target 60

**Daño en la tubería de combate** (proceso completo de armadura, golpe crítico, salpicadura, etc.; los atributos de combate distintos de cero en las habilidades cubren al lanzador):

.. code-block:: text

   effect harm_target mdg
   effect harm_target rdg

Ejemplos de wuxia: ``skill_lipi`` (fijo 60), ``skill_lipi_mdg`` (objetivo de combate).

harm_area — daño del área
~~~~~~~~~~~~~~~~~~~~~~~~~

**Daño verdadero arreglado**:

.. code-block:: text

efecto harm_area <daño> <radio>

Ejemplo (wuxia ``skill_heng_sao``): ``effect harm_area 50 3`` (se corrigió 50 de daño verdadero, radio 3).

**Daño al alcance del oleoducto de combate**:

.. code-block:: text

efecto harm_area mdg <radio>
efecto harm_area rdg <radio>

El radio se puede omitir, en cuyo caso se usa el ``effect_radius`` (predeterminado 6) de la habilidad. Las habilidades pueden sobrescribir los atributos de combate:

.. code-block:: text

   def skill_heng_sao_mdg
   class skill
   effect harm_area mdg 3
   mdg 12
   mdg_splash 6
   mdg_radius 1.5
   mdg_splash_decay_min 0.5
   effect_target ask
   effect_range 8

estallar - estallar (habilidad)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: text

efecto ráfaga mdg <número de veces> (intervalo <segundos>) (ventana <segundos>)
efecto de ráfaga rdg <número de veces> (intervalo <segundos>) (ventana <segundos>)

O utilice el retraso disparo a disparo:

.. code-block:: text

   effect burst mdg 3 (delays 0 0.2 0.5)

- `interval`: Intervalo entre dos clics adyacentes (segundos)
- `window`: Ventana de tiempo total combinada (segundos)
- `delays`: Lista de retraso absoluto para cada golpe, la duración debe ser igual al número de veces

El daño se obtiene de la habilidad o del lanzador ``mdg`` / ``rdg`` y de los atributos de combate completos. Ejemplos de wuxia: ``skill_jifengci``, ``skill_jifengci_rdg``.

.. epígrafe:: **Nota: Habilidad `effect burst` ≠ Unidad `damage_seq` Ataque continuo. ** Consulte la sección "Avanzado" de este artículo y `player/burst-attacks.htm` para obtener más detalles.

empujar - empujar hacia atrás
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: text

efecto empuje <distancia>

Empuja al objetivo enemigo lejos del lanzador y automáticamente encuentra un espacio para pararte. Ejemplo de wuxia: ``skill_moli_dan`` (``effect push 5``).

Mejoras/desventajas: aplica ventajas o desventajas.
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: text

Mejoras de efecto <nombre de mejora> [<nombre de mejora 2>…]
desventajas del efecto <nombre de la desventaja>

- `effect_target self`: Lanzado sobre uno mismo
- `effect_target ask` + `effect_range`: Lanzar sobre el objetivo seleccionado

``debuffs`` Solo es efectivo contra enemigos. Ejemplo de wuxia: ``skill_douzhuan`` → ``effect buffs b_douzhuan``.

**Rebote de daño**: No independiente ``effect reflect``. ``reflect_percent`` (porcentaje) debe usarse en la definición de mejora, que luego se aplica mediante la habilidad ``effect buffs``. Ejemplo de wuxia: ``b_douzhuan`` de ``reflect_percent 100``.

desplegar: desplegar efectos en el campo de batalla
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: text

implementación del efecto <segundos en vivo> [<número>] <nombre del tipo de efecto de clase>

Coloca entidades ``class effect`` (muros cortafuegos, áreas de curación, etc.) en la casilla objetivo. Consulta la Sección 3 "Efectos del campo de batalla" para obtener más detalles.

convocar — Invocar una unidad
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: text

efecto de invocación <número de segundos vivos> [<número>] <tipo de unidad> …

Opcional: ``summon_requires_build_field``, ``summon_requires_marked_field``.

Efectos heredados (aún disponibles)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

+--------+----+
| efecto | descripción |
+
========+
====+
| `teleportation` | Teletransporta unidades amigas a la red objetivo |
+--------+----+
| `recall` | Recuperar unidades amigas en la cuadrícula objetivo al lanzador |
+--------+----+
| `conversion` | Transformar unidades enemigas |
+--------+----+
| `raise_dead <segundos> <unidad…>` | Resurrección del cadáver |
+--------+----+
| `resurrection <límite>` | Resurrección de cadáveres amigos |
+--------+----+
| `harm <nivel>`|
+--------+----+

No ejecutable (solo visualización de UI)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

``effect heal``, ``effect damage`` solo están formateados y mostrados en la interfaz de atributos, y no realizarán tratamiento ni dañarán cuando se publiquen. Para curar, utilice unidades con atributos de curación mejorados ``heal_*``, ``class effect`` o ``effect buffs``.

Filtrado de tipo de objetivo (harm_target_type)
-----------------------------------------------

Efectivo para ``burst``, ``harm_target``, ``harm_area``, ``push``. Cuando no está configurado, **Solo tiene efecto en los enemigos de forma predeterminada** (desde 1.4.4.6).

.. code-block:: text

   harm_target_type enemy ground unit -building

- Agregue `-` antes de la etiqueta para indicar exclusión, como `-building`, `-undead`, `-enemy`
- `harm_target_type` y buff `target_type`: la etiqueta directa es **Y** (se deben cumplir todos)
- `heal_target_type` y `mdg_targets` / `rdg_targets`: la etiqueta de reenvío es **O**

Ejemplo:

.. code-block:: text

   harm_target_type enemy unit -building
   heal_target_type unit -undead
   mdg_targets ground air -building

Mod de referencia: comparación habilidad por habilidad de wuxia
---------------------------------------------------------------

Mod de demostración oficial: ``mods/wuxia/rules.txt``. Mapa de prueba: ``mods/wuxia/multi/skills_test.txt``.

+----+-----------+----+
| Habilidad | Tipo de efecto | Puntos clave |
+
====+
===========+
====+
| `skill_jifengci` | `burst mdg` | 5 combos, intervalo 0,2 s, ventana 1 s, alcance cuerpo a cuerpo 2 |
+----+-----------+----+
| `skill_jifengci_rdg` | `burst rdg` | Igual que arriba, rango 6 |
+----+-----------+----+
| `skill_heng_sao` | `harm_area 50 3` | Se corrigió 50 daños verdaderos, radio 3 |
+----+-----------+----+
| `skill_heng_sao_mdg` | `harm_area mdg 3` | Tubería de combate + Anulación de habilidades mdg/splash |
+----+-----------+----+
| `skill_lipi` | `harm_target 60` | Se corrigieron 60 daños verdaderos |
+----+-----------+----+
| `skill_lipi_mdg` | `harm_target mdg` | Combatir el daño a un solo objetivo del oleoducto |
+----+-----------+----+
| `skill_douzhuan` | `buffs b_douzhuan` | Beneficio personal; para rebote, consulte buff `reflect_percent` |
+----+-----------+----+
| `skill_moli_dan` | `push 5` | Retroceso 5 bloques |
+----+-----------+----+

Unidad de transporte ``wuxia_hero`` Aprende las 8 habilidades a través de ``can_use_skill``.

Avanzado

La diferencia entre explosión de habilidad y daño unitario_seq
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

+----+-------------------+------------------+
| Proyecto | Habilidad `effect burst` | Unidad `damage_seq` |
+
====+
===================+
==================+
| ubicación de configuración | `effect` fila en `class skill` | `damage_seq` en definición de unidad |
+----+-------------------+------------------+
| Método de activación | Liberación manual o automática de habilidades | Ataque normal/ataque de largo alcance |
+----+-------------------+------------------+
| Fuente del daño | Habilidad o lanzador `mdg`/`rdg` + atributo de combate | Unidad `mdg`/`rdg` Dividida en varias piezas |
+----+-------------------+------------------+
| Sintaxis de segmento | `burst mdg N (interval X)` | `damage_seq mdg N [(damage …)]` |
+----+-------------------+------------------+
| Documentación | Este artículo + `modding.htm` | `player/burst-attacks.htm` |
+----+-------------------+------------------+

Ambos usan el canal de combate, pero la entrada de configuración y el tiempo de activación son completamente diferentes. Por favor, no mezcle la sintaxis.

Libros de habilidades y mejoras para desbloquear.
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

- `level_skills <nivel> <habilidad> …`: Actualizar aprendizaje automático
- Artículo `skills` + `learn_level`: Aprendizaje del libro de habilidades de uso de mochila
- Consulte `modding.htm` y `relnotes.htm` §1.4.4.6 para obtener más detalles.

Efectos de sonido
~~

Habilidades ``style.txt``: ``alert`` (seleccionada), ``ready`` (adelante), ``triggered`` (efectiva). Mejora del disparador de ataque, consulte las mejoras ``triggered`` / ``noise loop``.

Documentos relacionados
-----------------------

- Tratamiento/daños propios de la unidad: `skills-and-effects.htm` (Sección 2 de este artículo)
- Campo de batalla `class effect` y despliegue: `skills-and-effects.htm` (Sección 3 de este artículo)
- Lista de palabras clave: `modding.htm`
- Resumen de notas de la versión: `relnotes.htm` §1.4.4.6

Para **Autores de mods**: configure unidades con auras curativas integradas, auras de daño y ritmos de regeneración de vida/maná en ``rules.txt``, no se requiere código fuente Python. Úselo junto con habilidades activas (``class skill``) y áreas del campo de batalla (``class effect``).

Descripción general

A partir de 1.4.1.7, el daño y la curación de la unidad se dividen en parámetros detallados que se pueden escribir en **definición de unidad** o **``class effect``**. Los parámetros de la unidad indican que la unidad produce de forma continua o periódica efectos de curación/daño en el entorno (o en sí misma).

Parámetros de daño (harm_*)
---------------------------

+----+----+
| Propiedades | Descripción |
+
====+
====+
| `harm_level` | Cantidad de daño cada vez (valor intuitivo, 1 = 1 punto) |
+----+----+
| `harm_cd` | Intervalo de daño (segundos); almacenado internamente en milisegundos, como 7,5 segundos para escribir `7.5` |
+----+----+
| `harm_ready` | Retraso antes del primer daño (segundos) |
+----+----+
| `harm_range` | Alcance (de la unidad al objetivo) |
+----+----+
| `harm_radius` | Radio de acción centrado en el objetivo |
+----+----+
| `harm_target_type` | Etiqueta de filtro de destino |
+----+----+

Ejemplo (la unidad viene con su propia nube venenosa):

.. code-block:: text

   def poison_aura_unit
   class soldier
   harm_level 2
   harm_cd 3
   harm_radius 4
   harm_target_type enemy unit -building

descripción del comportamiento harm_target_type
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

- **1.4.4.6 en adelante**: la habilidad `harm_target_type` por defecto **solo tiene efecto en los enemigos** cuando no está configurada.
- Puede escribir `enemy`, `allied`, `ground`, `air`, `unit`, `building`, etc.; El prefijo `-` excluye, como `-building`, `-undead`.
- La etiqueta de reenvío es **Y** (se deben cumplir todas).
- Si no se escriben etiquetas diplomáticas como `enemy` / `allied`, es posible que el aura de daño de la versión antigua de la unidad no distinga entre amigos y enemigos; el nuevo mod recomienda escribir explícitamente `harm_target_type enemy …`.

Parámetros de tratamiento (heal_*)
----------------------------------

+----+----+
| Propiedades | Descripción |
+
====+
====+
| `heal_level` | Cantidad de cada tratamiento |
+----+----+
| `heal_cd` | Intervalo de tratamiento (segundos) |
+----+----+
| `heal_ready` | Retraso antes del primer tratamiento |
+----+----+
| `heal_range` | Distancia de acción |
+----+----+
| `heal_radius` | Radio de acción |
+----+----+
| `heal_target_type` | Filtro de destino; la etiqueta directa es **O** |
+----+----+

Ejemplo (aura curativa estilo sacerdote):

.. code-block:: text

   def priest
   class soldier
   heal_level 3
   heal_cd 2
   heal_radius 5
   heal_target_type allied unit -undead

Regeneración de vida y maná (regen)
-----------------------------------

+----+----+
| Propiedades | Descripción |
+
====+
====+
| `hp_regen` | Regeneración de vida por segundo |
+----+----+
| `hp_regen_cd` | Intervalo de tic de respuesta |
+----+----+
| `hp_regen_ready` | Primera respuesta retrasada |
+----+----+
| `mana_regen` | Regeneración de maná por segundo |
+----+----+
| `mana_regen_cd` | Intervalo de recuperación de maná |
+----+----+
| `mana_regen_ready` | Primer retraso en la regeneración de maná |
+----+----+

Aumenta la curación/daño con mejoras.
-------------------------------------

``heal_level``, ``heal_cd``, ``heal_radius`` o ``harm_level``, etc. se pueden modificar en buff (buff de múltiples atributos). Ejemplo:

.. code-block:: text

   def HealEnhancementBuff
   class buff
   stat heal_level heal_cd heal_radius
   v 1 1500 6
   duration 300
   temporary 1

- `heal_level` de `v 1` = verdadero +1 punto de curación
- `heal_cd` de `v 1500` = 1,5 segundos de enfriamiento (milisegundos)
- `heal_radius` de `v 6` = +6 rango

Aplicación de habilidades: ``effect buffs HealEnhancementBuff``.

Relación con el efecto de clase
-------------------------------

Es un gran lugar para quedarse. Es un buen lugar para quedarse. Es un buen lugar para quedarse. Es un buen lugar para estar.

La diferencia con el efecto de habilidad.
-----------------------------------------

+----+----+
| Método | Propósito |
+
====+
====+
| Unidad `harm_*` / `heal_*` | Unidad de aura permanente o periódica |
+----+----+
| `class effect` + `deploy` | Área temporal del campo de batalla (muro cortafuegos, luz sagrada, etc.) |
+----+----+
| `effect harm_target` / `harm_area` | Habilidad activa daño único/combinado |
+----+----+
| `effect buffs` | Cambiar indirectamente los atributos de curación/daño mediante mejora |
+----+----+

**No existe** El efecto de habilidad ejecutable de ``effect heal``; utilice uno de los tres métodos anteriores para el tratamiento.

Actualiza y crece
-----------------

Las unidades se pueden configurar con ``heal_cd_per_level``, ``harm_radius_per_level`` y otros atributos ``*_per_level``, que se acumulan al actualizar. Consulte ``relnotes.htm`` §1.4.4.6 para obtener más detalles.

Comprobación rápida de comparación de parámetros
------------------------------------------------

+----+----+----+
| Lesión | Tratamiento | Significado |
+
====+
====+
====+
| `harm_level` | `heal_level` | Cada valor |
+----+----+----+
| `harm_cd` | `heal_cd` | Intervalo |
+----+----+----+
| `harm_ready` | `heal_ready` | Primer retraso |
+----+----+----+
| `harm_range` | `heal_range` | Distancia |
+----+----+----+
| `harm_radius` | `heal_radius` | Radio |
+----+----+----+
| `harm_target_type` | `heal_target_type` | Filtrado de objetivos |
+----+----+----+

Para **Autores de mods**: en ``rules.txt`` usa ``class effect`` para configurar los efectos del área del campo de batalla y ``class buff`` / ``class debuff`` para configurar ventajas y desventajas; aplicar a través de las habilidades ``effect deploy`` o ``effect buffs`` / ``debuffs``. No se requiere código fuente Python.

efecto del campo de batalla (efecto de clase)
---------------------------------------------

A partir de 1.4.1.7, las entidades ``class effect`` pueden causar daño de área, curar o llevar desventajas a lo largo del tiempo en el mapa.

Ejemplo de área de daño
~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: text

   def exorcism
   class effect
   harm_level 2
   harm_cd 7.5
   harm_radius 6
   harm_target_type undead
   debuffs b_slow

Ejemplos de áreas de tratamiento
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: text

   def holy_ground
   class effect
   heal_level 5
   heal_cd 3
   heal_radius 4
   heal_target_type allied unit

Descripción del parámetro
~~~~~~~~~~~~~~~~~~~~~~~~~

Los parámetros de daño y curación son los mismos que ``harm_*`` / ``heal_*`` en la unidad (consulte la Sección 2 "Curación/Daño de la unidad"). ``class effect`` también se puede escribir como ``decay`` (segundos de supervivencia, que también se pueden especificar mediante habilidades al desplegar).

a través del despliegue de habilidades
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: text

   def skill_blizzard
   class skill
   effect deploy 8 blizzard_fx
   effect_target ask
   effect_range 10

Gramática: ``effect deploy <segundos> [<cantidad>] <nombre_tipo_effect>``

A diferencia de ``effect summon``: el despliegue solo genera ``class effect``, no unidades. Opcional ``summon_requires_build_field`` / ``summon_requires_marked_field`` (como tumores de fluencia).

Consulte ``res/rules.txt`` para ver ejemplos integrados (Sacerdote ``effect deploy`` + Exorcismo ``class effect``).

Mejora y desventaja (mejora de clase / desventaja de clase)
-----------------------------------------------------------

gramática básica
~~~~~~~~~~~~~~~~

.. code-block:: text

   def b_slow
   class debuff
   stat speed
   v -2
   duration 10
   temporary 1
   stack 1

+----+----+
| Propiedades | Descripción |
+
====+
====+
| `stat` | Atributos afectados (pueden ser múltiples) |
+----+----+
| `v` | Bonificación fija |
+----+----+
| `dv` | Cambio por segundo (con `dt`) |
+----+----+
| `percentage` | Bonificación porcentual |
+----+----+
| `duration` | Duración (segundos) |
+----+----+
| `temporary` | `1` = Eliminado en caso de muerte |
+----+----+
| `stack` | Número de superposiciones |
+----+----+
| `target_type` | Condiciones que se pueden utilizar como objetivos de mejora (lógica Y) |
+----+----+
| `buff_radius` | Radio de halo (mejora tipo halo) |
+----+----+

La habilidad aplica buff
~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: text

   def skill_douzhuan
   class skill
   effect buffs b_douzhuan
   effect_target self

.. code-block:: text

   def skill_curse
   class skill
   effect debuffs b_slow
   effect_target ask
   effect_range 8

Los ataques también pueden venir con: ``buffs`` / ``debuffs`` escrito en la definición de la unidad, o activado por ``attack_trigger_buffs``, etc.

Reflexión de daños (reflect_percent)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Ninguno** ``effect reflect`` Palabras clave. El rebote debe configurarse en buff:

.. code-block:: text

   def b_douzhuan
   class buff
   duration 8
   temporary 1
   reflect_percent 100

Luego se aplica mediante la habilidad ``effect buffs b_douzhuan``. Este es el modo "estrella cambiante" del mod wuxia.

``reflect_percent`` es un porcentaje entero (100 = rebote completo).

Mejora de múltiples atributos
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Un beneficio puede afectar varios atributos al mismo tiempo:

.. code-block:: text

   def HealEnhancementBuff
   class buff
   stat heal_level heal_cd heal_radius
   v 1 1500 6
   duration 300
   temporary 1

Reglas de coincidencia de valores:

- Número de atributos = número de valores: correspondencia uno a uno
- Valores insuficientes: completar con el último valor
- Valor único: se aplica a todas las propiedades.

Atributos numéricos intuitivos (``v 1`` = 1 punto): ``hp``, ``mdg``, ``rdg``, ``heal_level``, ``harm_level``, ``heal_radius``, ``harm_radius``, ``speed`` y más de 20 artículos.

Clase de tiempo (milisegundos): ``heal_cd``, ``harm_cd``, ``mdg_cd``, ``rdg_cd``, etc.

Mejora activada
~~~~~~~~~~~~~~~

.. code-block:: text

   def CombatStanceBuff
   class buff
   stat mdg rdg
   v 30 25
   duration 100
   temporary 1
   is_active 1
   mdg_trigger_rate 80

+----+----+
| Esquema | Propiedades |
+
====+
====+
| Después del ataque | Predeterminado |
+----+----+
| Al lanzar un ataque | `is_active 1` |
+----+----+
| Cuando estás bajo ataque | `is_passive 1` + `trigger_condition` + `passive_trigger_rate` |
+----+----+

Efecto de sonido mejorado (style.txt)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: text

   def b_douzhuan
   triggered douzhuan_proc
   noise loop douzhuan_hum

- `triggered`: Aplicar reproducción instantánea
- `noise loop`: Bucle durante la duración
- `noise repeat <intervalo> <sonido…>`: Repetir por intervalo

Filtrado de tipo de destino (target_type)
-----------------------------------------

La sintaxis de ``target_type`` para mejora/desventaja es consistente con ``harm_target_type``, multicondición **Y**. Soporte ``-tag`` Excluir:

.. code-block:: text

   target_type unit -undead -building

Relación con el sistema de habilidades
--------------------------------------

+-----------+----+
| efecto de habilidad | efecto |
+
===========+
====+
| `effect deploy` | Lugar `class effect` |
+-----------+----+
| `effect buffs` / `debuffs` | Aplica mejora al objetivo |
+-----------+----+
| `effect harm_target` / `harm_area` | Daño directo (sin pasar por la entidad efectora) |
+-----------+----+

Consulte ``GENERIC_SKILL_SYSTEM.md`` (Sección 1) para conocer las palabras clave de habilidades completas.

referencia rápida
-----------------

mejora de curación
~~~~~~~~~~~~~~~~~~

.. code-block:: text

   def heal_aura_buff
   class buff
   stack 1
   stat heal_level heal_cd heal_radius
   v 1 1500 6
   temporary 1
   duration 10
   target_type self

Mejora de daño
~~~~~~~~~~~~~~

.. code-block:: text

   def harm_aura_buff
   class buff
   stack 1
   stat harm_level harm_cd harm_radius
   v 2 -1000 4
   temporary 1
   duration 15
   target_type self

Es el lugar perfecto para quedarte en tu casa. Es el lugar perfecto para estar. ``effect buffs``; no independiente ``effect reflect``. Consulte ``b_douzhuan`` para ver un ejemplo de wuxia.
