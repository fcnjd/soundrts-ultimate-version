Editor di mappatura tasti
=========================



Guida giocatore (schemi a livelli/classico): `../player/layered-hotkeys.md <../player/layered-hotkeys.htm>`_

In gioco: Opzioni → Mappatura tasti — rimappatura guidata dalla voce per il gioco accessibile. Le fasi 1–5 sono complete. Questo documento è per i manutentori: architettura e formati dati.

Sorgente: ``soundrts/hotkey_editor.py``, ``soundrts/hotkey_catalogs.py``, ``soundrts/hotkey_remapping_menu.py``, ``soundrts/clientgame/interface_modes.py``.


----


1. Stato
--------



.. list-table::
   :header-rows: 1

   * - Fase
     - Stato
     - Ambito
   * - Fase 1
     - Completata
     - Parser, archiviazione JSON, merge al caricamento, UI livello globale
   * - Fase 2
     - Completata
     - Cataloghi unit/building/command/skill/rpg/help/map/diplomacy, sottomenu per livello
   * - Fase 3
     - Completata
     - Schema classico (livello ``classic`` / ``legacy_bindings.txt``); ~179 binding primari
   * - Fase 4
     - Completata
     - Ricerca, sottomenu varianti avanzate, import/export dagli appunti
   * - Fase 5
     - Completata
     - Rimappatura indipendente dei tasti alias (LCTRL/RCTRL, RETURN/KP_ENTER, ecc.)



Flusso giocatore (riepilogo)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~


- Opzioni → Mappatura tasti (accanto a Schema tasti rapidi)
- Schema a livelli: scegli un livello (global / unit / building / command / skill / first person / help / map / diplomacy)
- Schema classico: Mappatura tasti apre direttamente l’elenco completo dei binding classici (senza un livello extra “Tasti classici”); First person resta un sottomenu al suo interno
- Ogni livello: Ricerca, Varianti avanzate (se presenti), Tasti alias (se presenti), poi voci del catalogo primario
- Livello superiore: Esporta / Importa JSON tasti tramite appunti (merge o sostituzione)
- Archiviazione per mod: `user/hotkey_overrides/{mod_key}.json`; ha effetto al successivo avvio partita


----


2. Perché non solo append su ``bindings.txt``
---------------------------------------------


Legacy: ``cfg/bindings.txt`` è un append chiave → comando; rimappare con append lascia funzionanti i tasti vecchi.

Nuovo modello: memorizza binding_id → tasto in JSON; al caricamento rimuove le righe predefinite sostituite e ne aggiunge di nuove. Un ``cfg/bindings.txt`` scritto a mano funziona ancora (aggiunto per ultimo).


----


3. File
-------



.. list-table::
   :header-rows: 1

   * - Percorso
     - Ruolo
   * - ``soundrts/hotkey_catalogs.py``
     - Cataloghi per livello, etichette varianti, catalogo alias
   * - ``soundrts/hotkey_editor.py``
     - Parse, binding_id, JSON, ``apply_overrides_to_bindings_text``, cattura
   * - ``soundrts/hotkey_remapping_menu.py``
     - UI del menu
   * - ``soundrts/clientgame/interface_modes.py``
     - Applica gli override prima del merge
   * - ``soundrts/msgparts.py``
     - ID TTS 5280–5399, 5500–5684
   * - ``user/hotkey_overrides/{mod_key}.json``
     - Override per mod + ``layered_hotkeys``
   * - ``user/hotkey_overrides.json``
     - File singolo legacy (migrato a ``\_base.json``)



Test: ``test_hotkey_editor.py`` fino a ``test_hotkey_editor_phase5.py``, ``test_hotkey_catalog_tts.py``


----


4. Modello dati
---------------


binding_id
~~~~~~~~~~


``{layer}.{command}.{arg1}.{arg2}...``

Gli override alias usano ``@`` + tasto predefinito codificato: ``global.examine@RCTRL``, ``global.validate.imperative@CTRL+KP_ENTER`` (spazi → `` +``).

Esempio JSON
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


5. Pipeline di caricamento
--------------------------


.. code-block:: text

   global_bindings.txt → apply_overrides(global)
     → + mode layer → + mod → + cfg/bindings.txt → Bindings.load()


Classico: ``\_legacy_bindings_with_overrides()`` applica gli override del livello ``classic``.


----


6. Funzionalità (fasi 4–5)
--------------------------


- Ricerca: filtra per etichetta o binding_id (EN/ZH)
- Varianti avanzate: binding in `*_bindings.txt` non presenti nel catalogo primario (es. Shift+Enter coda di convalida)
- Tasti alias: rimappa tasti secondari per lo stesso binding_id (es. KP_ENTER vs RETURN)
- Import/export: JSON negli appunti per la mod corrente


----


7. Test
-------


.. code-block:: bash

   pytest soundrts/tests/test_hotkey_editor.py -q
   pytest soundrts/tests/test_hotkey_editor_phase2.py -q
   pytest soundrts/tests/test_hotkey_editor_phase3.py -q
   pytest soundrts/tests/test_hotkey_editor_phase4.py -q
   pytest soundrts/tests/test_hotkey_editor_phase5.py -q
   pytest soundrts/tests/test_hotkey_catalog_tts.py -q
   pytest soundrts/tests/test_layered_bindings.py -q


L’editor non modifica mai i ``res/ui/*_bindings.txt`` distribuiti; solo il JSON utente.
