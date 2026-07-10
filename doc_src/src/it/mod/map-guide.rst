Guida alla creazione di mappe (introduzione e avanzata)
=======================================================


Prima costruisci una mappa giocabile. Sintassi completa: `Manuale di creazione mappe <mapmaking.htm>`_.
.. contents::

----

Primi passi
-----------

.. list-table::
   :header-rows: 1

   * - Posizione
     - Note
   * - ``user/multi/``
     - Mappe private
   * - ``user/single/…/N.txt``
     - Capitoli di campagna — `Guida alle campagne <campaign-guide.htm>`_

Prova dalla partita singola contro il computer. Errori: ``user/tmp/client.log``.

----

Mappa minima
------------

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

Avanzato
--------

Trigger e sintassi completa → `Manuale di creazione mappe <mapmaking.htm>`_  
Azioni di campagna → `Guida alle campagne <campaign-guide.htm>`_  
RMG → `Mappe casuali <randommap.htm>`_ · UI giocatore → `Mappe casuali (giocatore) <../player/random-map-play.htm>`_
