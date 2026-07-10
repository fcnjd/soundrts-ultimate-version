Guía de creación de mapas (introducción y avanzado)
===================================================

Crea primero un mapa jugable. Sintaxis completa: `Manual de creación de mapas <mapmaking.htm>`_.
.. contents::

----

Primeros pasos
--------------

.. list-table::
   :header-rows: 1

   * - Ubicación
     - Notas
   * - ``user/multi/``
     - Mapas privados
   * - ``user/single/…/N.txt``
     - Capítulos de campaña — `Guía de campañas <campaign-guide.htm>`_

Prueba en un jugador contra el ordenador. Errores: ``user/tmp/client.log``.

----

Mapa mínimo
-----------

.. code-block:: text

   title 4018 5000
   objective 145 88
   nb_players_min 2
   nb_players_max 2
   squares 3 3
   goldmines 1 1 5000
   woods 2 2 5000
   players 1 1 1

----

Avanzado
--------

Disparadores y sintaxis completa → `Manual de creación de mapas <mapmaking.htm>`_  
Acciones de campaña → `Guía de campañas <campaign-guide.htm>`_  
RMG → `Mapas aleatorios <randommap.htm>`_ · Interfaz del jugador → `Mapas aleatorios (jugador) <../player/random-map-play.htm>`_
