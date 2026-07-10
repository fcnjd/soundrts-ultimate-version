# Arco da campanha do norte (The Legend of Raynor caps. 24–27)



Os capítulos 24–27 formam uma linha contínua da aliança do norte: recrutar Garrek com a carta do Rei → entregar o token de Garrek ao Conde Roland e duelar → apresentar o estandarte de guerra à General Vera → derrotar Marco Ironhand. Cada capítulo também exige eliminar assassinos ``traitor_guard``. O progresso persiste via ``campaign_flag``.



Mapas:



| Cap. | Arquivo | Tema |

| --- | --- | --- |

| 24 | [24.txt](../../../res/single/The Legend of Raynor/24.txt) | Carta secreta; token de Garrek após morte dos traidores |

| 25 | [25.txt](../../../res/single/The Legend of Raynor/25.txt) | Token para Roland; duelo com rendição; aliança opcional |

| 26 | [26.txt](../../../res/single/The Legend of Raynor/26.txt) | Estandarte de guerra para Vera; ``transfer_units`` |

| 27 | [27.txt](../../../res/single/The Legend of Raynor/27.txt) | Duelo com Marco; controle seletivo de cavaleiros de escolta |



Definições: `rules.txt <../../../res/single/The Legend of Raynor/rules.txt>`_. TTS: ``ui/tts.txt``, ``ui-zh/tts.txt`` (7575–7718, 7720–7730, 7740–7745).




----




1. Flags de campanha
-------------------




| Flag | Definida em | Efeito |

| --- | --- | --- |

| ``ch24_garrek`` | 24 | Garrek recrutado; depois ``allied_control computer3`` |

| ``ch24_garrek_token`` | 24 | Token obtido; cap. 25 começa com ele no inventário de Raynor |

| ``ch25_duel_started`` | 25 | Token entregue; duelo iniciado; matar Roland/guardas antes disso → derrota |

| ``ch25_roland_allied`` | 25 | Aliança aceita; depois ``allied_assist computer4`` |

| ``ch25_roland_knights`` | 25 | Aliança recusada; cavaleiros de compensação em capítulos posteriores |

| ``ch26_vera`` | 26 | Vera se junta; reforços de Vera no cap. 27 |

| ``ch27_duel_started`` | 27 | ``map_flag`` no mapa (não salva entre capítulos): Raynor chegou ao acampamento de Marco; cutscene 7718 reproduzida; matar Marco antes disso → derrota |

| ``ch27_marco`` | 27 | Marco recrutado |




----




2. Gatilhos (novos e comuns)
----------------------------




| Nome | Tipo | Resumo |

| --- | --- | --- |

| ``add_inventory_item`` | action | Colocar item no inventário da unidade: `(add_inventory_item <item> [<count>] [<unit_type>])` |

| ``set_ai_mode`` | action | Definir modo de IA nas unidades do dono do gatilho |

| ``set_yield_on_defeat`` | action | Alternar rendição por unidade: `(set_yield_on_defeat <0\|1> [unit selector…])` |

| ``units_yielded`` | condition | Contagem de rendição inimiga (``yield_on_defeat``) |

| ``units_yielded_by`` | condition | Rendição por atacante específico: `(units_yielded_by <attacker> <count> <victim> [enemy\|ally])`; suporta ``is_a`` |

| ``has_entered`` | condition | Unidades do dono do gatilho entraram em um quadrado (grade ou alias de nome de lugar) |

| ``stop_all_units`` | action | Parar combate; ``computer1`` etc. opcional |

| ``release_yielded_units`` | action | Encerrar invulnerabilidade de rendição |

| ``npc_has_item`` | condition | NPC recebeu item |

| ``alliance`` | action | Definir aliança; multi-alvo: `(alliance 1 player1 computer1)` |

| ``alliance_request`` / ``alliance_with`` | action/cond. | Aliança dinâmica (Ctrl+F4 / Shift+F4 na campanha) |

| ``allied_assist`` / ``allied_control`` | action | Aliados lutam sozinhos / jogador comanda aliados |

| ``transfer_units`` | action | Mudar propriedade (cap. 26) |

| ``has_killed`` | condition | Contagem de mortes da equipe |

| ``key_unit_killed`` | condition | Unidade-chave realmente morreu (não rendeu) |

| ``campaign_flag`` / ``set_campaign_flag`` | cond./action | Progresso entre capítulos |




``cut_scene`` deve rodar em gatilhos ``player1`` para o cliente humano receber voz. Alternâncias de modo de IA / rendição podem rodar em ``computer1`` (dono da unidade).




Sintaxe de gatilho é `trigger <owner> <condition> <action>` (três partes). Use `(and …) (defeat)`, não `(if (and …) (defeat))`.




Diplomacia F12 está desabilitada na campanha. Use Ctrl+F4 para aceitar, Shift+F4 para recusar.




----




3. Capítulo 24 — Garrek
------------------------




1. Pegue ``secret_letter``, entregue a Garrek no acampamento de Garrek (``c2``) → aliança, ``allied_control``, ``ch24_garrek``.

2. Mate 3 ``traitor_guard`` → ``add_inventory_item garrek_token``, ``ch24_garrek_token``.




----
 




4. Capítulo 25 — Roland
------------------------




Carryover: Garrek em A2 se ``ch24_garrek``; token no inventário se ``ch24_garrek_token``.



Objetivos: (1) entregar token a Roland, (2) derrotar Roland + 2 cavaleiros guarda (rendição), (3) matar traidores; aliança opcional.



Fluxo:



1. Roland e ``npc_roland_guard`` começam em ``guard``, sem ``yield_on_defeat`` (mortíveis antes da entrega; erro → derrota).

2. player1 em ``npc_has_item``: ``cut_scene 7701``, objetivo 1, ``ch25_duel_started``.

3. computer1 na mesma condição: ``set_ai_mode offensive`` + ``set_yield_on_defeat 1``.

4. Após rendição: cessar-fogo, ``alliance_request``; ramo Ctrl+F4 ou Shift+F4.



Registre três objetivos primários + um opcional no início (numeração independente).




----




5. Capítulo 26 — Vera
----------------------




Entregue ``war_banner`` a Vera → ``transfer_units computer1 player1``, ``ch26_vera``. Matar Vera falha a missão.




----
 




6. Capítulo 27 — Marco
-----------------------




Mapa: ``c2`` (acampamento de Marco); Marco + escoltas (cavaleiros/guerreiros/arqueiros); assassinos em ``b3``/``c3``. Marco e todas as escoltas começam em ``ai_mode guard`` (``rules.txt``).



Carryover: caps. 24–26 recompensam unidades por flag. Jogador começa como ``raynor7`` com séquito (2 footmen, 2 archers, 2 knights).



Fluxo:



1. Raynor ``enters ``c2`` (acampamento de Marco / 3,2)`` → player1: ``cut_scene 7718``, ``set_map_flag ch27_duel_started`` (``raynor7`` deve entrar; escoltas sozinhas não disparam).

2. computer1 (flag definida): apenas Marco `(set_ai_mode offensive c2 1 npc_marco_ironhand)`; escoltas `(order … ((go c1)))` para c1 para limpar a arena.

3. Raynor deve derrotar Marco pessoalmente: `(units_yielded_by raynor7 1 npc_marco_ironhand enemy)` completa o objetivo primário. Se escoltas ou outras unidades forçarem rendição de Marco → ``defeat``.

4. Após rendição: ``cut_scene 7710`` → `(alliance 1 player1 computer1)`, ``stop_all_units``, ``release_yielded_units``.

5. `(allied_control computer1 c2 4 npc_knight_escort)` — quatro cavaleiros de escolta sob comando do jogador; escoltas em c1 recebem ordem `(go c2)` para se reagrupar no acampamento de Marco.

6. Mate 3 ``traitor_guard`` (objetivo secundário) → ``cut_scene 7719`` (fala final de Marco — não diálogo de token de Garrek do cap. 24 `7580`).



Falha: matar Marco antes do duelo começar (``key_unit_killed``); Marco rendido por unidade que não seja Raynor; Raynor morre; wipe.




----
 




7. Unidades e itens
------------------




| Tipo | Função |

| --- | --- |

| ``garrek_token`` | Signet de Garrek (caps. 24–25) |

| ``npc_count_roland`` | Conde Roland; aceita ``garrek_token`` |

| ``npc_roland_guard`` | Cavaleiros guarda (Roland os chama de "brothers" no diálogo) |

| ``npc_marco_ironhand`` | Marco; ``yield_on_defeat`` |

| ``traitor_guard`` | Assassinos; ``guard``, não perseguem entre quadrados |




----
 




8. ``yield_on_defeat``
--------------------------




- Com 0 HP, unidade rende em vez de morrer; invulnerabilidade breve.

- ``release_yielded_units`` após escolha de aliança.

- Cap. 25: desabilitado até entrega do token (via gatilho ``set_yield_on_defeat 1``).




----
 




9. Comparação (caps. 24–27)
---------------------------




| Aspecto | 24 Garrek | 25 Roland | 26 Vera | 27 Marco |

| --- | --- | --- | --- | --- |

| Duelo com rendição | — | Após token | — | Desde o início; Raynor deve dar o golpe final |

| Início do duelo | Na entrega | Após token | Na transferência do estandarte | Ao entrar no acampamento de Marco |

| Matar NPC-chave cedo | Garrek morre → falha | Antes do token → falha | Vera morre → falha | Antes do duelo no acampamento → falha |




----




10. Documentação relacionada
------------------




| Tópico | Doc |

| --- | --- |

| Dar a NPC | [give-to-npc.md](give-to-npc.htm) |

| Modos de IA | [unit-default-behavior.md](unit-default-behavior.htm) |

| Seletores de índice | [map-unit-index-selectors.md](map-unit-index-selectors.htm) |

| Sintaxe oficial | ``mod/mapmaking.rst`` |




----
 




11. Testes
-----------




.. code-block:: text

   
   python -m pytest soundrts/tests/test_campaign_alliance_transfer_triggers.py -q
   
   python -m pytest soundrts/tests/test_yield_on_defeat_and_campaign_flags.py -q
   
   python -m pytest soundrts/tests/test_give_item_to_npc.py -q
   





----

 


12. Campanha inteira (crescimento de Raynor, séquito, nomes de lugares)
---------------------------------------------------------




Estágios de Raynor (``rules.txt`` / ``starting_units`` por mapa):



| Capítulos | Tipo de unidade | Séquito inicial (além de Raynor) |

| --- | --- | --- |

| 1–12 | ``raynor`` | padrões por capítulo |

| 13–15 | ``raynor2`` | 1 footman |

| 16–18 | ``raynor3`` | 2 footmen |

| 19–21 | ``raynor4`` | 2 footmen, 1 archer |

| 22–24 | ``raynor5`` | 2 footmen, 1 archer, 1 knight |

| 25–26 | ``raynor6`` | 2 footmen, 2 archers, 2 knights |

| 27–28 | ``raynor7`` | 2 footmen, 2 archers, 2 knights |



Cutscenes de estágio: fim do cap. 12 (``7730``); aberturas dos caps. 13/16/19/22/25/27 (``7720``–``7729``, ``7737``–``7738``). Intros da tela de atributos: ``ui/style.txt`` ``intro 7740``–``7746``.



Nomes de lugares: mapas dos caps. 1–28 usam ``square_name`` (província/condado/local). TTS em ``ui-zh/tts.txt`` seção Place names. Scripts ainda podem usar coordenadas de grade (``c2``) ou aliases de nome de lugar.
