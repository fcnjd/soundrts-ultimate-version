IU de inventario y equipo
=========================

Cómo las unidades usan el inventario (mochila), la pantalla de equipo y el modelo de objeto del mismo tipo en ``rules.txt`` (un tipo puede ser a la vez objeto recogible y arma/armadura equipable).

----

1. Resumen
----------

.. list-table::
   :header-rows: 1

   * - Pantalla
     - Tecla rápida
     - Muestra
   * - Atributos
     - `Alt+V`
     - todas las estadísticas
   * - Mochila
     - `Shift+V`
     - todos los objetos del inventario
   * - Equipo
     - `Ctrl+V`
     - armas y armadura (equipo de inventario + integrado)

Solo una pantalla a la vez. Selecciona exactamente una unidad amiga.

Mochila frente a equipo
~~~~~~~~~~~~~~~~~~~~~~~

- Mochila: equipar/usar/soltar cualquier objeto.
- Equipo: solo armas y armadura. El equipo integrado se etiqueta «arma integrada / armadura integrada» (solo lectura).

Equipo mixto integrado + objeto
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Cuando una unidad tiene tanto ``class weapon``/``class armor`` como equipo ``class item`` (p. ej. ``weapons bow sword``):

.. list-table::
   :header-rows: 1

   * - Regla
     - Significado
   * - Prioridad al aparecer
     - Lo integrado siempre se equipa primero; el equipo-objeto va a la mochila
   * - ``spawn_weapons_equipped 1`` (por defecto)
     - Las armas-objeto permanecen en la mochila y no se pueden equipar manualmente
   * - ``spawn_weapons_equipped 0``
     - Las armas-objeto en la mochila se pueden equipar
   * - Cambio
     - Solo integrado ↔ integrado; solo objeto ↔ objeto; sin cambio cruzado
   * - Armadura
     - Igual con ``spawn_armor_equipped``

Si la unidad solo tiene equipo-objeto, las banderas de aparición controlan el equipado silencioso al crear (activado por defecto).

----

2. Controles del jugador
------------------------

Abrir
~~~~~

- Exactamente 1 unidad amiga seleccionada.
- Mochila: inventario no vacío.
- Equipo: al menos un arma o armadura (integrada o de inventario).

En mochila / equipo
~~~~~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1

   * - Tecla
     - Acción
   * - Flechas
     - objeto anterior / siguiente
   * - ``g``
     - leer introducción del objeto (de ``style.txt``)
   * - ``Enter``
     - equipar arma / poner armadura / usar consumible
   * - ``Shift+Enter``
     - desequipar arma o armadura
   * - ``Delete``
     - soltar (confirmar, luego Intro)
   * - ``Shift+Delete``
     - soltar sin confirmar
   * - ``Esc``
     - cerrar / cancelar soltar

Mundo
~~~~~

- Recoger: ``pickup`` (clic derecho por defecto).
- Soltar: ``drop`` o Delete en la IU.
- Dar: ``give`` — consulta `give-to-npc.htm <../mod/campaign/give-to-npc.htm>`_.

----

3. Dos sistemas de equipo
-------------------------

3.1 Arma / armadura integrada (clásico)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: text

   def footman
   weapons sword          ; class weapon
   armor footman_armor    ; class armor

No está en la mochila. La pantalla de equipo lo muestra como integrado; no se puede desequipar ni soltar vía IU.

3.2 Equipo de objeto de mochila (modelo del mismo tipo)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: text

   def sword
   class item
   equippable_as_weapon 1
   mdg 3.5
   ...

Las estadísticas se aplican mientras está equipado; se quitan al desequipar. Consulta ``res/rules.txt`` para ejemplos de ``sword``, ``footman_armor``.

----

4. Generar equipo en la mochila
-------------------------------

Al aparecer:

- `weapons <name>`: si el tipo es ``class item`` + ``equippable_as_weapon 1`` → instancia en la mochila; equipado silencioso si no hay arma integrada y ``spawn_weapons_equipped 1``.
- `armor <name>`: igual para armadura.

Ejemplo footman con espada-objeto + armadura-objeto: ambas en la mochila, ambas equipadas por defecto, visibles en Shift+V y Ctrl+V.

.. code-block:: text

   spawn_weapons_equipped 0/1   ; default 1
   spawn_armor_equipped 0/1     ; default 1

Arquero mixto
~~~~~~~~~~~~~

.. code-block:: text

   def archer
   weapons bow sword

- ``bow`` = ``class weapon`` → integrado, siempre equipado.
- ``sword`` = ``class item`` → mochila; con la bandera de aparición por defecto, la espada no se puede equipar mientras el arco es integrado.

Establece ``spawn_weapons_equipped 0`` para permitir equipar la espada manualmente (sigue sin cambio directo arco↔espada).

Requisitos
~~~~~~~~~~

.. list-table::
   :header-rows: 1

   * - Campo
     - Nota
   * - ``inventory_capacity``
     - debe ser > 0
   * - ``transport_volume``
     - espacio por objeto (por defecto 1); la capacidad cuenta objetos, no volumen

----

5. Lista de comprobación del autor
----------------------------------

Solo integrado
~~~~~~~~~~~~~~

.. code-block:: text

   def my_unit
   weapons short_sword
   armor light_armor

Recogible, equipable, extraíble
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

1. Define el objeto con ``equippable_as_weapon 1`` o ``equippable_as_armor 1``.
2. Unidad: ``inventory_capacity`` + ``weapons my_sword``.
3. ``style.txt``: ``title``, ``intro``.

Consumibles
~~~~~~~~~~~

.. code-block:: text

   def health_potion
   class item
   buffs heal

Usar con Intro en la mochila (``use_item``), no en la pantalla de equipo.

----

6. Órdenes del servidor
-----------------------

.. list-table::
   :header-rows: 1

   * - Orden
     - Args
   * - ``equip_weapon``
     - id de objeto
   * - ``unequip_weapon``
     - id de objeto
   * - ``equip_armor``
     - id de objeto
   * - ``unequip_armor``
     - id de objeto
   * - ``use_item``
     - id de objeto
   * - ``drop``
     - id de objeto

Las transferencias de inventario en mejora/morph van vía ``transfer_inventory_to``.

----

7. Preguntas frecuentes
-----------------------

P: ¿Mochila vacía en footman?  
El ``class weapon`` integrado no entra en la mochila hasta que el tipo sea ``class item`` con lógica de aparición-a-inventario.

P: «Armadura integrada» y no se puede desequipar?  
Sigue siendo ``class armor``; añade ``class item`` + ``equippable_as_armor 1``.

P: ¿Mismo nombre para objeto y arma?  
Sí (modelo del mismo tipo): p. ej. ``sword`` como objeto para mochila/aparición; ``bow`` permanece ``class weapon`` puro.

----

8. Archivos relacionados
------------------------

.. list-table::
   :header-rows: 1

   * - Archivo
   * - ``res/ui/bindings.txt``
     - Shift+V, Ctrl+V
   * - ``soundrts/attributes/inventory_screen.py``
     - IU de mochila
   * - ``soundrts/attributes/equipment_screen.py``
     - IU de equipo
   * - ``soundrts/worldunit/worldbase.py``
     - lógica de aparición / equipo
   * - ``res/rules.txt``
     - ejemplos

Véase también `give-to-npc <../mod/campaign/give-to-npc.htm>`_, `find-item <../mod/campaign/find-item.htm>`_.
