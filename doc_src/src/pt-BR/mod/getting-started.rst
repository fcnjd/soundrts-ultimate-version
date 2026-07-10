Mod — primeiros passos
======================


Seu primeiro patch e sua primeira unidade funcional — ainda sem mapas nem campanhas. Próximo: `Guia avançado de mod <advanced.htm>`_.
-------------------------------------------------------------------------------------------------------------------------------------

O que você altera
-----------------

Um mod é uma pasta de arquivos de texto. Salve, recarregue o mapa ou reinicie o jogo.

.. list-table::
   :header-rows: 1

   * - Arquivo
     - Função
   * - ``rules.txt``
     - Unidades, tecnologia, habilidades (este guia)
   * - ``style.txt`` + ``ui/tts.txt``
     - Nomes e falas
   * - ``ai.txt``
     - Estratégia do computador (depois)

Referência de palavras-chave: `Manual de modding <modding.htm>`_.

----

Passo 1: pasta e ativação
-------------------------

Coloque o mod em ``user/mods/mymod/``. Ative em ``user/SoundRTS.ini``:

.. code-block:: ini

   mods = mymod

Mods posteriores na lista sobrescrevem os anteriores. Atalho de desenvolvimento: ``python soundrts.py --mods=mymod``

----

Passo 2: prova em duas linhas
-----------------------------

``user/mods/mymod/rules.txt``:

.. code-block:: text

   def peasant
   decay 20

Camponeses desaparecem após ~20 segundos — seu mod está carregado.

Mods só de som: copie ``mods/soundpack/`` ou use Opções → soundpack.

----

Passo 3: ler o rules.txt
------------------------

.. code-block:: text

   def my_soldier
   class soldier
   is_a footman
   hp 120
   mdg 8

- ``def`` — inicia uma definição
- ``class`` — soldier, building, skill, …
- ``is_a`` — herda e depois sobrescreve campos
- ``clear`` no topo do arquivo — substitui os padrões em vez de apenas aplicar patches

Facções: ``def orc_faction`` + ``class faction``.

----

Passo 4: nomes que o jogador ouve
---------------------------------

.. code-block:: text

   ; ui/style.txt — title 7801
   ; ui/tts.txt — 7801 Heavy Infantry

Veja `Internacionalização de mods <mod-i18n.htm>`_.

----

Passo 5: testar
---------------

Um jogador contra o computador; Ctrl+Shift+F2 revela o mapa (solo, único humano).  
Logs: ``user/tmp/client.log``

Significado dos campos no lado do jogador: `Inventário <../player/inventory.htm>`_ · `Comportamentos padrão <../player/unit-default-behavior.htm>`_

----

E depois?
---------

.. list-table::
   :header-rows: 1

   * - Objetivo
     - Leia
   * - Mod completo, habilidades, facções
     - `Mod avançado <advanced.htm>`_ · `Manual de modding <modding.htm>`_
   * - Primeiro mapa
     - `Guia de mapas <map-guide.htm>`_
   * - Campanha
     - `Guia de campanhas <campaign-guide.htm>`_
   * - Notas de versão
     - `Notas de versão <../relnotes.htm>`_

Voltar ao `índice de docs de mod <index.htm>`_
