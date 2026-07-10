# Victoria por encontrar objeto (disparador ``has_item``)

Diseña objetivos en los que recoger un objeto completa la meta.

Condición central: :strong:```has_item`` — ¿tiene el jugador el objeto en el inventario de alguna unidad viva?

----

1. Resumen
----------

.. list-table::
   :header-rows: 1

   * - Parte
     - Nombre
     - Función
   * - Campo de unidad
     - ``class item``
     - objeto recogible
   * - Orden por defecto
     - ``pickup``
     - clic derecho sobre objeto en el suelo
   * - Condición
     - ``has_item``
     - el jugador tiene el tipo de objeto

Flujo: colocar objeto → recoger → ``(has_item …)`` → `` (objective_complete N)`` → victoria cuando todos los objetivos estén hechos.

No establezcas ``consume_on_pickup 1`` (por defecto 0). Si se consume al recoger, ``has_item`` nunca se vuelve verdadero.

----

2. ``has_item``
---------------

.. code-block:: text

   (has_item <item_type> [count])

Cuenta objetos en los inventarios de todas las unidades vivas del jugador.

.. code-block:: text

   (has_item lost_amulet)
   (has_item lost_amulet 2)

.. list-table::
   :header-rows: 1

   * - Condición
     - Comprueba
   * - ``has``
     - cantidad de unidades poseídas
   * - ``has_item``
     - objetos en el inventario
   * - ``has_brought_item``
     - llevado a una casilla
   * - ``npc_has_item``
     - el PNJ recibió el objeto
   * - ``find``
     - objeto en el suelo en una casilla

----

3. Definir objeto de misión
---------------------------

.. code-block:: text

   def lost_amulet
   class item

El recolector necesita ``inventory_capacity \> 0`` (peasant, footman, …).

----

4. Colocar en el mapa
---------------------

.. code-block:: text

   lost_amulet c3
   lost_amulet 2 c3

----

5. Ejemplo (cap. 17)
--------------------

Consulta `17.txt <../../../res/single/The Legend of Raynor/17.txt>`_:

.. code-block:: text

   trigger player1 (timer 0) (add_objective 1 "find the lost amulet")
   trigger player1 (has_item lost_amulet) (objective_complete 1)

----

6. Compuesto: cap. 20 (llevar + usar en inventario)
---------------------------------------------------

`mystery_treasure <../../../res/single/The Legend of Raynor/20.txt>`_: recoger → ``has_brought_item b2`` → usar en el santuario (``use_square b2``) → recompensa de oro.

----

7. Compuesto: cap. 22 (soltar + recolectar monedas)
---------------------------------------------------

`sealed_treasure <../../../res/single/The Legend of Raynor/22.txt>`_: soltar en b2 → ``find`` + ``remove_ground_item`` → generar ``gold_coin`` → recoger todas.

----

8. Compuesto: cap. 23 (soltar = entregar)
-----------------------------------------

`war_supplies <../../../res/single/The Legend of Raynor/23.txt>`_: ``has_item`` y luego ``find c3 war_supplies`` tras soltar.

.. list-table::
   :header-rows: 1

   * - Capítulo
     - Objeto
     - Entrega
   * - 20
     - ``mystery_treasure``
     - llevar + uso en inventario
   * - 22
     - ``sealed_treasure``
     - soltar, abrir, recolectar monedas
   * - 23
     - ``war_supplies``
     - soltar en la estación

----

9. Caps. 24–27
--------------

Recoge ``secret_letter`` en ``b1`` (mismo flujo que ``has_item``), luego dásela al líder (``npc_has_item``). Consulta `campaign-northern-arc.htm <campaign-secret-letter-alliance.htm>`_.

----

10. Implementación
------------------

- ``lang_has_item`` en ``soundrts/worldplayerbase/triggers.py``
- Ejemplo: `res/single/The Legend of Raynor/17.txt`, ``rules.txt`` (``lost_amulet``)
