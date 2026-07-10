# Llevar un objeto a una casilla y entrega narrativa (``has_brought_item`` + ``remove_item``)

Dos disparadores usados juntos:

- ``has_brought_item`` (condición): una unidad del jugador lleva un objeto a una casilla
- ``remove_item`` (acción): quitar y destruir el objeto del inventario (entrega narrativa)

Típico: llevar poción de maná al santuario → escena → la poción desaparece → objetivo completado.

Ejemplo: The Legend of Raynor cap. 18 (`18.txt <../../../res/single/The Legend of Raynor/18.txt>`_).

----

1. frente a otros disparadores de objetos
-----------------------------------------

.. list-table::
   :header-rows: 1

   * - Disparador
     - Detecta / efecto
     - Ubicación del objeto
     - Caso de uso
   * - ``has_item``
     - el jugador tiene el objeto
     - inventario de cualquier unidad
     - encontrado / recogido
   * - ``has_brought_item``
     - objeto llevado a la casilla
     - unidades en esa casilla
     - entregar al llegar (sin soltar)
   * - ``find``
     - objeto en el suelo
     - soltado en la casilla
     - colocar objeto; sintaxis: casilla primero ``(find c3 mana_potion)``
   * - ``npc_has_item``
     - el PNJ recibió el objeto
     - inventario del PNJ / ``received_items``
     - dar a un PNJ
   * - ``remove_item``
     - destruir del inventario
     - —
     - entrega narrativa automática

----

2. Condición: ``has_brought_item``
----------------------------------

.. code-block:: text

   (has_brought_item <square> <item_type> [count])

- Casilla: p. ej. ``c3``, `"3,3"`
- Tipo de objeto: p. ej. ``mana_potion``
- Cantidad: opcional, por defecto `1`

Verdadero cuando al menos una unidad viva del jugador en esa casilla tiene suficiente del objeto en el inventario.

- Manos vacías en la casilla → falso
- Objeto en otro sitio, unidad no en la casilla → falso
- Llevado a la casilla → verdadero (no hace falta soltarlo)

----

3. Acción: ``remove_item``
--------------------------

.. code-block:: text

   (remove_item <item_type> [square] [count])

- Sin casilla: quitar de todas las unidades vivas del jugador
- Con casilla: solo unidades en esa casilla
- Cantidad: opcional, por defecto `1`

El objeto se destruye (como al consumirlo). Combínalo con ``cut_scene`` para la narrativa.

----

4. Ejemplo completo (cap. 18)
-----------------------------

.. code-block:: text

   trigger player1 (has_brought_item c3 mana_potion)
       (do (cut_scene 7560) (remove_item mana_potion c3) (objective_complete 1))

Encadena varias acciones con ``do``. No uses ``if`` para tres acciones seguidas.

Flujo: recoger poción → caminar al santuario c3 → condición verdadera → escena → objeto eliminado → objetivo 1 hecho.

----

5. frente a dar a un PNJ
------------------------

.. list-table::
   :header-rows: 1

   * - Método
     - Cuándo
   * - ``npc_has_item`` + ``give`` del jugador
     - receptor PNJ físico
   * - ``has_brought_item`` + ``remove_item``
     - llegar y entregar, sin PNJ, historia automática

----

6. Archivos relacionados
------------------------

.. list-table::
   :header-rows: 1

   * - Contenido
     - Ruta
   * - Implementación
     - ``soundrts/worldplayerbase/triggers.py``
   * - Mapa de ejemplo
     - `res/single/The Legend of Raynor/18.txt`
   * - Encontrar objeto
     - [find-item-objective.md](find-item-objective.htm)
   * - Dar a un PNJ
     - [give-to-npc.md](give-to-npc.htm)
