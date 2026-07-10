Primeros pasos para mods
========================

Tu primer parche y tu primera unidad funcional — aún no mapas ni campañas. Siguiente: `Guía avanzada de mods <advanced.htm>`_.
------------------------------------------------------------------------------------------------------------------------------

Qué modificas
-------------

Un mod es una carpeta de archivos de texto. Guarda, recarga el mapa o reinicia el juego.

.. list-table::
   :header-rows: 1

   * - Archivo
     - Función
   * - ``rules.txt``
     - Unidades, tecnología, habilidades (esta guía)
   * - ``style.txt`` + ``ui/tts.txt``
     - Nombres y líneas de voz
   * - ``ai.txt``
     - Estrategia del ordenador (más adelante)

Referencia de palabras clave: `Manual de modding <modding.htm>`_.

----

Paso 1: carpeta y activación
----------------------------

Pon tu mod en ``user/mods/mymod/``. Actívalo en ``user/SoundRTS.ini``:

.. code-block:: ini

   mods = mymod

Los mods posteriores en la lista anulan a los anteriores. Atajo de desarrollo: ``python soundrts.py --mods=mymod``

----

Paso 2: prueba de dos líneas
----------------------------

``user/mods/mymod/rules.txt``:

.. code-block:: text

   def peasant
   decay 20

Los campesinos desaparecen tras ~20 segundos — tu mod está cargado.

Mods solo de sonido: copia ``mods/soundpack/`` o usa Opciones → soundpack.

----

Paso 3: leer rules.txt
----------------------

.. code-block:: text

   def my_soldier
   class soldier
   is_a footman
   hp 120
   mdg 8

- ``def`` — iniciar una definición
- ``class`` — soldier, building, skill, …
- ``is_a`` — heredar, luego sobrescribir campos
- ``clear`` al inicio del archivo — reemplazar los valores por defecto en lugar de parchear

Facciones: ``def orc_faction`` + ``class faction``.

----

Paso 4: nombres que oyen los jugadores
--------------------------------------

.. code-block:: text

   ; ui/style.txt — title 7801
   ; ui/tts.txt — 7801 Heavy Infantry

Consulta `Internacionalización de mods <mod-i18n.htm>`_.

----

Paso 5: probar
--------------

Un jugador contra el ordenador; Ctrl+Shift+F2 revela el mapa (solo, único humano).  
Registros: ``user/tmp/client.log``

Significado de campos del lado del jugador: `Inventario <../player/inventory.htm>`_ · `Comportamientos por defecto <../player/unit-default-behavior.htm>`_

----

¿Qué sigue?
-----------

.. list-table::
   :header-rows: 1

   * - Objetivo
     - Leer
   * - Mod completo, habilidades, facciones
     - `Mod avanzado <advanced.htm>`_ · `Manual de modding <modding.htm>`_
   * - Primer mapa
     - `Guía de mapas <map-guide.htm>`_
   * - Campaña
     - `Guía de campañas <campaign-guide.htm>`_
   * - Notas de la versión
     - `Notas de la versión <../relnotes.htm>`_

Volver al `Índice de docs de mods <index.htm>`_
