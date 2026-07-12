Sistemas estratégicos RMG: héroe y civilización
===============================================

Esta capa integra el progreso de héroe al estilo Heroes of Might and Magic y
la gestión urbana al estilo Civilization en mapas aleatorios (Random Map
Generator, RMG). Sigue siendo estrategia en tiempo real: los rendimientos se
liquidán con el tiempo de juego, sin turnos.


----


1. Cómo activarlo
-----------------

Menú principal → **Iniciar juego → Mapa aleatorio**. Todo mapa RMG nuevo
escribe ``rmg_strategic_systems 1`` y activa héroe, rendimientos urbanos,
cultura, puntos diplomáticos, tecnologías y políticas.

Mapas hechos a mano y partidas no RMG no activan estas reglas por defecto. Si
el mod no define ``rmg_hero``, el generador omite al héroe sin fallar la carga.


----


2. Progreso del héroe
---------------------

Cada jugador empieza con un ``rmg_hero``:

- Nivel 1 inicial, máximo 8.
- Gana experiencia en combate y sube de nivel automáticamente.
- Cada nivel aumenta vida, daño cuerpo a cuerpo y maná máximo.
- Maná propio; las habilidades consumen maná y se regenera.
- Como máximo un héroe RMG por jugador.
- En **RMG local en solitario**, se guardan el nivel y la experiencia máximos
  por mod y facción y se restauran en la siguiente partida. Multijugador y
  repeticiones no leen el archivo local (evita desincronización).

Perfil de héroe entre partidas
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

- Ruta: en el directorio de configuración del usuario, junto a ``achievements``:
  ``rmg_heroes/<clave_mod>/<facción>.json`` (p. ej. ``human.json``).
- Al terminar la partida se guarda nivel y XP máximos; al iniciar la siguiente
  se aplican a ``rmg_hero``, incluidas habilidades por nivel.
- Solo **mapas aleatorios locales en solitario** (``TrainingGame``). Campaña,
  multijugador, repetición y espectador no usan este archivo.
- Independiente de ``campaign_carryover`` de campaña: ``rmg_hero`` mantiene
  ``campaign_carryover 0``; la persistencia RMG usa JSON dedicado, no
  ``campaigns.ini``.

Árbol de habilidades
~~~~~~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1

   * - Nivel
     - Habilidad
     - Coste de maná
     - Efecto
   * - 2
     - Flecha arcano
     - 20
     - Daño mágico a un objetivo
   * - 4
     - Tornado
     - 35
     - Daño en alcance cuerpo a cuerpo
   * - 6
     - Lluvia de meteoros
     - 60
     - Daño en área a larga distancia

Las habilidades se desbloquean solas al alcanzar el nivel. Selecciona al héroe
y usa el menú de habilidades; sin maná suficiente no se puede lanzar.


----


3. Expansión urbana y rendimiento de casillas
---------------------------------------------

Ayuntamiento, fortaleza y castillo cuentan como ciudades. En mods compatibles,
bases con **supervivencia** y **almacenamiento de recursos** también.

Cada ciudad posee su casilla principal. Selecciona la ciudad, **Comprar
casilla**, luego una casilla principal adyacente al territorio actual. No hay
doble ocupación. Primera compra: 20 oro; cada casilla extra +10 oro. Una ciudad
nueva reclama su casilla al construirse.

Cada 60 s, cada ciudad viva y cada casilla con ciudadano pagan una vez.

Rendimiento base por ciudad
~~~~~~~~~~~~~~~~~~~~~~~~~~~

Por tick:

- 6 oro, 4 madera, 4 comida, 4 cultura, 1 punto diplomático.

Bonificación de terreno urbano
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1

   * - Terreno
     - Extra
   * - Colina, meseta, roca alta, paso de montaña
     - +3 oro
   * - Bosque, bosque denso, pantano
     - +3 madera
   * - Llanura, pueblo, pradera
     - +3 comida
   * - Lago, río, arroyo, vado
     - +1 oro, +2 comida

Los recursos cuentan para **recolección acumulada** y victoria económica RMG.

Ciudadanos y mejoras de casilla
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Comandos **Asignar ciudadano a oro / madera / comida / cultura** sobre
casillas propias. Si no hay huecos, se libera el ciudadano más antiguo:

- 1 hueco base; planificación urbana y administración cívica +1 cada una;
  fortaleza o castillo +1.

Mejoras: **mina** (+3 oro), **aserradero** (+3 madera), **granja** (+3 comida).
Costes: mina 15 oro + 10 madera; aserradero 10 oro + 15 madera; granja 10 oro
+ 5 madera + 10 comida.

Rendimiento base de casilla trabajada (cada 60 s): 1 oro, 1 madera, 1 comida;
mismos bonos de terreno; especialización +2 oro/madera/comida o +3 cultura.

Compra: primera expansión 20 oro, luego +10 oro por casilla (la casilla de la
ciudad es gratis).


3.1 Comandos estratégicos de ciudad
-----------------------------------

Con ayuntamiento, fortaleza o castillo en partida RMG (elegir casilla objetivo
y confirmar):

.. list-table::
   :header-rows: 1

   * - Comando (voz)
     - Palabra clave
     - Efecto
   * - Comprar casilla (5718)
     - ``rmg_buy_tile``
     - Comprar casilla adyacente libre
   * - Asignar ciudadano a oro (5719)
     - ``rmg_assign_gold``
     - Trabajar casilla propia
   * - Asignar ciudadano a madera (5720)
     - ``rmg_assign_wood``
     - Especialización madera
   * - Asignar ciudadano a comida (5721)
     - ``rmg_assign_food``
     - Especialización comida
   * - Asignar ciudadano a cultura (5722)
     - ``rmg_assign_culture``
     - +3 cultura/min en esa casilla
   * - Construir mina (5723)
     - ``rmg_build_mine``
     - +3 oro/tick
   * - Construir aserradero (5724)
     - ``rmg_build_lumber_mill``
     - +3 madera/tick
   * - Construir granja (5725)
     - ``rmg_build_farm``
     - +3 comida/tick
   * - Activar política tradición (5726)
     - ``rmg_switch_tradition``
     - Cambiar entre políticas desbloqueadas sin coste de cultura
   * - Activar política comercio (5727)
     - ``rmg_switch_commerce``
     - Igual
   * - Activar política diplomacia (5728)
     - ``rmg_switch_diplomacy``
     - Igual


----


4. Árbol tecnológico
--------------------

.. list-table::
   :header-rows: 1

   * - Tecnología
     - Requisito
     - Efecto
   * - Planificación urbana
     - —
     - +2 oro, madera y comida por ciudad/tick
   * - Administración cívica
     - Planificación urbana
     - +2 cultura por ciudad/tick
   * - Servicio exterior
     - Administración cívica
     - +1 punto diplomático por ciudad/tick


----


5. Cultura y cartas de política
-------------------------------

Cultura es un recurso estratégico de partida; las políticas la consumen al
investigarse.

.. list-table::
   :header-rows: 1

   * - Política
     - Cultura
     - Requisito
     - Efecto
   * - Tradición
     - 40
     - Planificación urbana
     - +50% cultura
   * - Comercio
     - 80
     - Administración cívica
     - +25% oro, madera y comida urbanos
   * - Diplomacia
     - 120
     - Servicio exterior
     - Doble puntos diplomáticos

Máximo **dos** políticas activas. La tercera reemplaza la más antigua. Luego
**Activar tradición / comercio / diplomacia** cambia gratis entre desbloqueadas.

La IA elige pares fijos: agresiva → comercio + tradición; ≥2 enemigos →
diplomacia + comercio; resto → tradición + comercio.


----


6. Puntos diplomáticos
----------------------

Las ciudades generan puntos cada minuto. **Enviar solicitud de alianza** cuesta
20 puntos en RMG estratégico (aceptar/rechazar/salir gratis; cooldown 60 s).


6.1 Consultar cultura y diplomacia
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Cultura y diplomacia **no** usan la barra de recursos (Z / X / Mayús+Z). En
partidas RMG con ``rmg_strategic_systems``:

.. list-table::
   :header-rows: 1

   * - Método
     - Acción
   * - Atajos globales
     - **B** cultura actual; **Mayús+B** puntos diplomáticos
   * - Atributos de ciudad
     - Ciudad propia seleccionada, atributos (Alt+V): **U** cultura, **Y** diplomacia
   * - Voz periódica
     - Cada 60 s ``rmg_strategic_tick`` anuncia ciudades, cultura y diplomacia
   * - Alertas de cambio
     - Con alertas de recursos activas, también se anuncian cambios

Fuera de RMG, **B** / **Mayús+B** solo suenan aviso.


----


7. Compatibilidad con mods
--------------------------

Arquitectura del juego RMG
~~~~~~~~~~~~~~~~~~~~~~~~~~

Las mapas aleatorios combinan un **marco del motor** (generador, cuatro modos de
victoria, API de triggers, sistemas estratégicos opcionales al estilo Civ) con
**datos de reglas y plantillas**. Los valores por defecto y si los sistemas
estratégicos están activos viven en ``def parameters`` de ``rules.txt``; las
plantillas ``cfg/randommap/*.txt`` los sobrescriben. Los mods extienden el RMG
editando reglas y plantillas, sin cambiar Python. Un ``map.txt`` manual permite
condiciones de victoria totalmente libres.

Valores estratégicos, mejoras de casilla, comercio diplomático y objetivos de
victoria son configurables en ``rules.txt``.

Parámetros globales (``def parameters``)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1

   * - Clave
     - Predeterminado
     - Significado
   * - ``rmg_diplomacy_request_cost``
     - 20
     - Diplomacia al enviar solicitud de alianza
   * - ``rmg_tile_purchase_base`` / ``_step``
     - 20 / 10
     - Coste en oro de comprar casillas
   * - ``rmg_policy_slot_limit``
     - 2
     - Cartas de política activas
   * - ``rmg_trade_cooldown``
     - 60
     - Enfriamiento comercial (segundos)
   * - ``rmg_economic_goal`` / ``_fast`` / ``_macro`` / ``_lanes``
     - 3000 / 2000 / 5000 / 2500
     - Victoria económica (``resource1`` acumulado)
   * - ``rmg_survival_seconds`` / ``_fast``
     - 900 / 600
     - Victoria supervivencia (segundos)
   * - ``rmg_exploration_ruin_pairs_*`` + ``_bonus``
     - ver reglas
     - Pares simétricos de ruinas antiguas
   * - ``rmg_strategic_systems``
     - 1
     - Activar sistemas estratégicos Civ en RMG

Mejoras de casilla (edificios ``rmg_tile_*``)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

- ``rmg_tile_improvement 1``, ``rmg_improvement_key``, ``rmg_tile_yield`` (oro / madera / comida / cultura / diplomacia por 60 s con trabajador presente)

Comercio diplomático (mejoras ``rmg_trade_*``)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Campos: ``rmg_trade_id``, ``rmg_trade_pay``, ``rmg_trade_gain``,
``rmg_trade_diplomacy_cost``, ``rmg_trade_alliance``, ``rmg_trade_cooldown``.

Victoria y desafíos personalizados (``cfg/randommap/*.txt``)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Campos de plantilla: ``default_victory_mode``, ``economic_goal``,
``survival_seconds``, ``exploration_ruin_pairs``, ``strategic_systems 0`` (RTS
puro). Cuartel general: ``provides_survival 1`` + ``storable_resource_types``.

**Quinto modo y más** — bloque ``victory_triggers`` con líneas ``trigger``;
ver ``res/randommap/example.txt``.

Otras notas
~~~~~~~~~~~

- ``rmg_hero`` necesario para héroe inicial.
- Bases con ``provides_survival`` y ``storable_resource_types`` = ciudad.
- Las ciudades reciben tecnología y políticas RMG dinámicamente; mapas no RMG filtran investigación ``rmg_``.
- ``can_research`` se guarda como ``_rules_can_research``; ``effective_can_research()`` inyecta ``rmg_*`` solo en RMG.

Atributos: ``culture_cost``, ``rmg_policy 1``. Triggers: ``rmg_strategic_tick``,
``rmg_has_culture``, ``rmg_has_diplomacy``, ``rmg_grant_culture``,
``rmg_grant_diplomacy``.


----


8. Implementación
-----------------

``soundrts/rmg_systems.py``, ``rmg_progress.py``, ``worldorders/strategic.py``,
``randommap.py``, ``worldplayercomputer.py``, ``game.py``,
``clientgame/game_resources.py``, ``attributes/basic_attributes.py``,
``res/rules.txt``, voz 5702–5728 y estados cultura/diplomacia 5716–5717,
pruebas ``test_rmg_systems.py``.


----


9. Límites actuales
-------------------

Sin turnos Civ5, crecimiento poblacional, mantenimiento de caminos ni UI
diplomática. Territorio por casilla RMG sin cambiar paso de unidades. Héroe
entre partidas solo en RMG local en solitario.
