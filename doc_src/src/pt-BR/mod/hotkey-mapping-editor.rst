Editor de mapeamento de teclas de atalho
========================================



Guia do jogador (esquemas em camadas/clássico): `../player/layered-hotkeys.md <../player/layered-hotkeys.htm>`_

Versão em chinês: `../../zh/mod/hotkey-mapping-editor.md <../../zh/mod/hotkey-mapping-editor.htm>`_

No jogo Opções → Mapeamento de teclas — remapeamento guiado por voz para
jogabilidade acessível a cegos. Fases 1–5 concluídas. Este doc é para
mantenedores: arquitetura e formatos de dados.

Fonte: ``soundrts/hotkey_editor.py``, ``soundrts/hotkey_catalogs.py``,
``soundrts/hotkey_remapping_menu.py``,
``soundrts/clientgame/interface_modes.py``.


----


1. Status
---------



.. list-table::
   :header-rows: 1

   * - Fase
     - Status
     - Escopo
   * - Fase 1
     - Concluída
     - Parser, armazenamento JSON, merge no carregamento, UI de camada global
   * - Fase 2
     - Concluída
     - Catálogos unit/building/command/skill/rpg/help/map/diplomacy, submenus
       de camada
   * - Fase 3
     - Concluída
     - Esquema clássico (camada ``classic`` / ``legacy_bindings.txt``); ~179
       bindings primários
   * - Fase 4
     - Concluída
     - Busca, submenu de variantes avançadas, importar/exportar clipboard
   * - Fase 5
     - Concluída
     - Remapeamento independente de teclas alias (LCTRL/RCTRL, RETURN/KP_ENTER
       etc.)



Fluxo do jogador (resumo)
~~~~~~~~~~~~~~~~~~~~~~~~~


- Opções → Mapeamento de teclas (irmão de Esquema de atalhos)
- Esquema em camadas: escolha uma camada (global / unit / building / command /
  skill / first person / help / map / diplomacy)
- Esquema clássico: Mapeamento de teclas abre a lista completa de bindings
  clássicos diretamente (sem camada extra "Classic hotkeys"); First person
  permanece submenu dentro dela
- Cada camada: Busca, Variantes avançadas (se houver), Teclas alias (se
  houver), depois itens primários do catálogo
- Nível superior: Exportar / Importar JSON de atalhos via clipboard (mesclar
  ou substituir)
- Armazenamento por mod: `user/hotkey_overrides/{mod_key}.json`; entra em vigor
  no próximo início de partida


----


2. Por que não ``bindings.txt`` apenas append
---------------------------------------------


Legado: ``cfg/bindings.txt`` é append tecla → comando; remapear via append
deixa teclas antigas funcionando.

Novo modelo: armazena binding_id → tecla em JSON; no carregamento remove
linhas padrão substituídas e adiciona novas. ``cfg/bindings.txt`` escrito à mão
ainda funciona (append por último).


----


3. Arquivos
-----------



.. list-table::
   :header-rows: 1

   * - Caminho
     - Função
   * - ``soundrts/hotkey_catalogs.py``
     - Catálogos por camada, rótulos de variantes, catálogo alias
   * - ``soundrts/hotkey_editor.py``
     - Parse, binding_id, JSON, ``apply_overrides_to_bindings_text``, captura
   * - ``soundrts/hotkey_remapping_menu.py``
     - UI do menu
   * - ``soundrts/clientgame/interface_modes.py``
     - Aplica overrides antes do merge
   * - ``soundrts/msgparts.py``
     - IDs TTS 5280–5399, 5500–5684
   * - ``user/hotkey_overrides/{mod_key}.json``
     - Overrides por mod + ``layered_hotkeys``
   * - ``user/hotkey_overrides.json``
     - Arquivo único legado (migrado para ``\_base.json``)



Testes: ``test_hotkey_editor.py`` até ``test_hotkey_editor_phase5.py``,
``test_hotkey_catalog_tts.py``


----


4. Modelo de dados
------------------


binding_id
~~~~~~~~~~


``{layer}.{command}.{arg1}.{arg2}...``

Overrides alias usam ``@`` + tecla padrão codificada: ``global.examine@RCTRL``,
``global.validate.imperative@CTRL+KP_ENTER`` (espaços → `` +``).

Exemplo JSON
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


5. Pipeline de carregamento
---------------------------


.. code-block:: text

   global_bindings.txt → apply_overrides(global)
     → + mode layer → + mod → + cfg/bindings.txt → Bindings.load()


Clássico: ``\_legacy_bindings_with_overrides()`` aplica overrides da camada
``classic``.


----


6. Recursos (Fases 4–5)
-----------------------


- Busca: filtrar por rótulo ou binding_id (EN/ZH)
- Variantes avançadas: bindings em `*_bindings.txt` fora do catálogo primário
  (por exemplo Shift+Enter validar fila)
- Teclas alias: remapear teclas secundárias para o mesmo binding_id (por
  exemplo KP_ENTER vs RETURN)
- Importar/exportar: JSON clipboard para o mod atual


----


7. Testes
---------


.. code-block:: bash

   pytest soundrts/tests/test_hotkey_editor.py -q
   pytest soundrts/tests/test_hotkey_editor_phase2.py -q
   pytest soundrts/tests/test_hotkey_editor_phase3.py -q
   pytest soundrts/tests/test_hotkey_editor_phase4.py -q
   pytest soundrts/tests/test_hotkey_editor_phase5.py -q
   pytest soundrts/tests/test_hotkey_catalog_tts.py -q
   pytest soundrts/tests/test_layered_bindings.py -q


O editor nunca edita ``res/ui/*_bindings.txt`` enviados; apenas JSON do
usuário.

Para detalhes completos veja o `doc de desenvolvedor em chinês
<../../zh/mod/hotkey-mapping-editor.htm>`_.
