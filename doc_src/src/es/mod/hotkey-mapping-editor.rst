Editor de mapeo de teclas rápidas
=================================

Guía del jugador (esquemas por capas/clásico): `../player/layered-hotkeys.htm <../player/layered-hotkeys.htm>`_

En el juego: Opciones → Mapeo de teclas — reasignación guiada por voz para juego accesible. Las fases 1–5 están completas. Este documento es para mantenedores: arquitectura y formatos de datos.

Fuente: ``soundrts/hotkey_editor.py``, ``soundrts/hotkey_catalogs.py``, ``soundrts/hotkey_remapping_menu.py``, ``soundrts/clientgame/interface_modes.py``.

----

1. Estado
---------

.. list-table::
   :header-rows: 1

   * - Fase
     - Estado
     - Alcance
   * - Fase 1
     - Hecho
     - Analizador, almacenamiento JSON, fusión al cargar, IU de capa global
   * - Fase 2
     - Hecho
     - Catálogos unit/building/command/skill/rpg/help/map/diplomacy, submenús de capa
   * - Fase 3
     - Hecho
     - Esquema clásico (capa ``classic`` / ``legacy_bindings.txt``); ~179 enlaces primarios
   * - Fase 4
     - Hecho
     - Búsqueda, submenú de variantes avanzadas, importar/exportar portapapeles
   * - Fase 5
     - Hecho
     - Reasignación independiente de teclas alias (LCTRL/RCTRL, RETURN/KP_ENTER, etc.)

Flujo del jugador (resumen)
~~~~~~~~~~~~~~~~~~~~~~~~~~~

- Opciones → Mapeo de teclas (hermano de Esquema de teclas rápidas)
- Esquema por capas: elige una capa (global / unit / building / command / skill / first person / help / map / diplomacy)
- Esquema clásico: Mapeo de teclas abre directamente la lista completa de enlaces clásicos (sin capa extra «Teclas clásicas»); Primera persona sigue siendo un submenú dentro
- Cada capa: Buscar, Variantes avanzadas (si hay), Teclas alias (si hay), luego elementos del catálogo primario
- Nivel superior: Exportar / Importar JSON de teclas vía portapapeles (fusionar o reemplazar)
- Almacenamiento por mod: `user/hotkey_overrides/{mod_key}.json`; entra en vigor en el próximo inicio de partida

----

2. Por qué no solo añadir a ``bindings.txt``
--------------------------------------------

Heredado: ``cfg/bindings.txt`` es clave → comando por añadido; reasignar añadiendo deja las teclas antiguas funcionando.

Modelo nuevo: guardar binding_id → tecla en JSON; al cargar se eliminan las líneas por defecto reemplazadas y se añaden las nuevas. Un ``cfg/bindings.txt`` escrito a mano sigue funcionando (se añade al final).

----

3. Archivos
-----------

.. list-table::
   :header-rows: 1

   * - Ruta
     - Función
   * - ``soundrts/hotkey_catalogs.py``
     - Catálogos por capa, etiquetas de variantes, catálogo de alias
   * - ``soundrts/hotkey_editor.py``
     - Análisis, binding_id, JSON, ``apply_overrides_to_bindings_text``, captura
   * - ``soundrts/hotkey_remapping_menu.py``
     - IU del menú
   * - ``soundrts/clientgame/interface_modes.py``
     - Aplicar anulaciones antes de fusionar
   * - ``soundrts/msgparts.py``
     - IDs TTS 5280–5399, 5500–5684
   * - ``user/hotkey_overrides/{mod_key}.json``
     - Anulaciones por mod + ``layered_hotkeys``
   * - ``user/hotkey_overrides.json``
     - Archivo único heredado (migrado a ``\_base.json``)

Pruebas: ``test_hotkey_editor.py`` hasta ``test_hotkey_editor_phase5.py``, ``test_hotkey_catalog_tts.py``

----

4. Modelo de datos
------------------

binding_id
~~~~~~~~~~

``{layer}.{command}.{arg1}.{arg2}...``

Las anulaciones de alias usan ``@`` + tecla por defecto codificada: ``global.examine@RCTRL``, ``global.validate.imperative@CTRL+KP_ENTER`` (espacios → `` +``).

Ejemplo JSON
~~~~~~~~~~~~

.. code-block:: json

   {
     "version": 1,
     "layered_hotkeys": 1,
     "overrides": {
       "global": {
         "global.resource_status.resource1": "y",
         "global.examine@RCTRL": "F3"
       }
     }
   }

----

5. Canalización de carga
------------------------

.. code-block:: text

   global_bindings.txt → apply_overrides(global)
     → + mode layer → + mod → + cfg/bindings.txt → Bindings.load()

Clásico: ``\_legacy_bindings_with_overrides()`` aplica las anulaciones de la capa ``classic``.

----

6. Funciones (fases 4–5)
------------------------

- Buscar: filtrar por etiqueta o binding_id (EN/ZH)
- Variantes avanzadas: enlaces en `*_bindings.txt` que no están en el catálogo primario (p. ej. Shift+Intro validar cola)
- Teclas alias: reasignar teclas secundarias para el mismo binding_id (p. ej. KP_ENTER frente a RETURN)
- Importar/exportar: JSON del portapapeles para el mod actual

----

7. Pruebas
----------

.. code-block:: bash

   pytest soundrts/tests/test_hotkey_editor.py -q
   pytest soundrts/tests/test_hotkey_editor_phase2.py -q
   pytest soundrts/tests/test_hotkey_editor_phase3.py -q
   pytest soundrts/tests/test_hotkey_editor_phase4.py -q
   pytest soundrts/tests/test_hotkey_editor_phase5.py -q
   pytest soundrts/tests/test_hotkey_catalog_tts.py -q
   pytest soundrts/tests/test_layered_bindings.py -q

El editor nunca edita los ``res/ui/*_bindings.txt`` incluidos; solo el JSON del usuario.
