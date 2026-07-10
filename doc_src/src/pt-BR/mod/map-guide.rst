Guia de criação de mapas (introdução e avançado)
================================================


Monte primeiro um mapa jogável. Sintaxe completa: `Manual de criação de mapas <mapmaking.htm>`_.
.. contents::

----

Primeiros passos
----------------

.. list-table::
   :header-rows: 1

   * - Local
     - Notas
   * - ``user/multi/``
     - Mapas privados
   * - ``user/single/…/N.txt``
     - Capítulos de campanha — `Guia de campanhas <campaign-guide.htm>`_

Teste no modo um jogador contra o computador. Erros: ``user/tmp/client.log``.

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

Avançado
--------

Gatilhos e sintaxe completa → `Manual de criação de mapas <mapmaking.htm>`_  
Ações de campanha → `Guia de campanhas <campaign-guide.htm>`_  
RMG → `Mapas aleatórios <randommap.htm>`_ · Interface do jogador → `Mapas aleatórios (jogador) <../player/random-map-play.htm>`_
