# Arco settentrionale della campagna (The Legend of Raynor cap. 24–27)



I capitoli 24–27 formano una trama continua di alleanza settentrionale: recluta Garrek con la lettera del Re → consegna il gettone di Garrek al conte Roland e duella → presenta lo stendardo di guerra al generale Vera → sconfiggi Marco Ironhand. Ogni capitolo richiede anche di eliminare gli assassini ``traitor_guard``. I progressi persistono tramite ``campaign_flag``.



Mappe:



| Cap. | File | Tema |

| --- | --- | --- |

| 24 | [24.txt](../../../res/single/The Legend of Raynor/24.txt) | Lettera segreta; gettone di Garrek dopo la morte dei traditori |

| 25 | [25.txt](../../../res/single/The Legend of Raynor/25.txt) | Gettone a Roland; duello con resa; alleanza opzionale |

| 26 | [26.txt](../../../res/single/The Legend of Raynor/26.txt) | Stendardo di guerra a Vera; ``transfer_units`` |

| 27 | [27.txt](../../../res/single/The Legend of Raynor/27.txt) | Duello con Marco; controllo selettivo dei cavalieri di scorta |



Definizioni: `rules.txt <../../../res/single/The Legend of Raynor/rules.txt>`_. TTS: ``ui/tts.txt``, ``ui-zh/tts.txt`` (7575–7718, 7720–7730, 7740–7745).




----




1. Flag di campagna
-------------------




| Flag | Impostato in | Effetto |

| --- | --- | --- |

| ``ch24_garrek`` | 24 | Garrek reclutato; poi ``allied_control computer3`` |

| ``ch24_garrek_token`` | 24 | Gettone ottenuto; il cap. 25 inizia con esso nell’inventario di Raynor |

| ``ch25_duel_started`` | 25 | Gettone consegnato; duello iniziato; uccidere Roland/guardie prima di questo → sconfitta |

| ``ch25_roland_allied`` | 25 | Alleanza accettata; poi ``allied_assist computer4`` |

| ``ch25_roland_knights`` | 25 | Alleanza rifiutata; cavalieri di compensazione nei capitoli successivi |

| ``ch26_vera`` | 26 | Vera si unisce; rinforzi di Vera nel cap. 27 |

| ``ch27_duel_started`` | 27 | ``map_flag`` in mappa (non salvato tra capitoli): Raynor ha raggiunto l’accampamento di Marco; cutscene 7718 riprodotta; uccidere Marco prima di questo → sconfitta |

| ``ch27_marco`` | 27 | Marco reclutato |




----




2. Trigger (nuovi e comuni)
---------------------------




| Nome | Tipo | Riepilogo |

| --- | --- | --- |

| ``add_inventory_item`` | azione | Metti oggetto nell’inventario dell’unità: `(add_inventory_item <item> [<count>] [<unit_type>])` |

| ``set_ai_mode`` | azione | Imposta la modalità IA sulle unità del proprietario del trigger |

| ``set_yield_on_defeat`` | azione | Attiva/disattiva resa per unità: `(set_yield_on_defeat <0\|1> [unit selector…])` |

| ``units_yielded`` | condizione | Conteggio rese nemiche (``yield_on_defeat``) |

| ``units_yielded_by`` | condizione | Resa da un attaccante specifico: `(units_yielded_by <attacker> <count> <victim> [enemy\|ally])`; supporta ``is_a`` |

| ``has_entered`` | condizione | Le unità del proprietario del trigger sono entrate in una casella (griglia o alias nome luogo) |

| ``stop_all_units`` | azione | Arresta il combattimento; opzionale ``computer1`` ecc. |

| ``release_yielded_units`` | azione | Termina l’invulnerabilità da resa |

| ``npc_has_item`` | condizione | L’NPC ha ricevuto l’oggetto |

| ``alliance`` | azione | Imposta alleanza; multi-bersaglio: `(alliance 1 player1 computer1)` |

| ``alliance_request`` / ``alliance_with`` | azione/cond. | Alleanza dinamica (Ctrl+F4 / Shift+F4 in campagna) |

| ``allied_assist`` / ``allied_control`` | azione | Gli alleati combattono da soli / il giocatore comanda gli alleati |

| ``transfer_units`` | azione | Cambia proprietà (cap. 26) |

| ``has_killed`` | condizione | Conteggio uccisioni di squadra |

| ``key_unit_killed`` | condizione | L’unità chiave è davvero morta (non resa) |

| ``campaign_flag`` / ``set_campaign_flag`` | cond./azione | Progressi tra capitoli |




``cut_scene`` deve essere eseguito sui trigger di ``player1`` così il client umano riceve la voce. I toggle di modalità IA / resa possono essere eseguiti su ``computer1`` (proprietario dell’unità).




La sintassi dei trigger è `trigger <owner> <condition> <action>` (tre parti). Usa `(and …) (defeat)`, non `(if (and …) (defeat))`.




La diplomazia F12 è disabilitata in campagna. Usa Ctrl+F4 per accettare, Shift+F4 per rifiutare.




----




3. Capitolo 24 — Garrek
-----------------------




1. Raccogli ``secret_letter``, consegnala a Garrek all’accampamento di Garrek (``c2``) → alleanza, ``allied_control``, ``ch24_garrek``.

2. Uccidi 3 ``traitor_guard`` → ``add_inventory_item garrek_token``, ``ch24_garrek_token``.




----




4. Capitolo 25 — Roland
-----------------------




Trasferimento: Garrek in A2 se ``ch24_garrek``; gettone in inventario se ``ch24_garrek_token``.



Obiettivi: (1) consegna il gettone a Roland, (2) sconfiggi Roland + 2 cavalieri di guardia (resa), (3) uccidi i traditori; alleanza opzionale.



Flusso:



1. Roland e ``npc_roland_guard`` partono in ``guard``, senza ``yield_on_defeat`` (uccidibili prima della consegna; errore → sconfitta).

2. player1 su ``npc_has_item``: ``cut_scene 7701``, obiettivo 1, ``ch25_duel_started``.

3. computer1 sulla stessa condizione: ``set_ai_mode offensive`` + ``set_yield_on_defeat 1``.

4. Dopo la resa: cessate il fuoco, ``alliance_request``; ramo Ctrl+F4 o Shift+F4.



Registra tre obiettivi primari + uno opzionale all’inizio (numerazione indipendente).




----




5. Capitolo 26 — Vera
---------------------




Consegna ``war_banner`` a Vera → ``transfer_units computer1 player1``, ``ch26_vera``. Uccidere Vera fa fallire la missione.




----




6. Capitolo 27 — Marco
----------------------




Mappa: ``c2`` (accampamento di Marco); Marco + scorte (cavalieri/guerrieri/arcieri); assassini in ``b3``/``c3``. Marco e tutte le scorte partono in ``ai_mode guard`` (``rules.txt``).



Trasferimento: unità premio dei cap. 24–26 per flag. Il giocatore parte come ``raynor7`` con seguito (2 fanti, 2 arcieri, 2 cavalieri).



Flusso:



1. Raynor ``enters ``c2`` (Marco's camp / 3,2)`` → player1: ``cut_scene 7718``, ``set_map_flag ch27_duel_started`` (deve entrare ``raynor7``; le sole scorte non attivano).

2. computer1 (flag impostato): solo Marco `(set_ai_mode offensive c2 1 npc_marco_ironhand)`; scorte `(order … ((go c1)))` verso c1 per liberare l’arena.

3. Raynor deve sconfiggere Marco di persona: `(units_yielded_by raynor7 1 npc_marco_ironhand enemy)` completa l’obiettivo primario. Se scorte o altre unità costringono Marco alla resa → ``defeat``.

4. Dopo la resa: ``cut_scene 7710`` → `(alliance 1 player1 computer1)`, ``stop_all_units``, ``release_yielded_units``.

5. `(allied_control computer1 c2 4 npc_knight_escort)` — quattro cavalieri di scorta sotto il comando del giocatore; le scorte in c1 ricevono ordine `(go c2)` per riformarsi all’accampamento di Marco.

6. Uccidi 3 ``traitor_guard`` (obiettivo secondario) → ``cut_scene 7719`` (battuta finale di Marco — non il dialogo del gettone di Garrek del cap. 24 `7580`).



Fallimento: uccidere Marco prima dell’inizio del duello (``key_unit_killed``); Marco reso da un’unità non-Raynor; Raynor muore; sterminio.




----




7. Unità e oggetti
------------------




| Tipo | Ruolo |

| --- | --- |

| ``garrek_token`` | Sigillo di Garrek (cap. 24–25) |

| ``npc_count_roland`` | Conte Roland; accetta ``garrek_token`` |

| ``npc_roland_guard`` | Cavalieri di guardia (Roland li chiama “fratelli” nel dialogo) |

| ``npc_marco_ironhand`` | Marco; ``yield_on_defeat`` |

| ``traitor_guard`` | Assassini; ``guard``, non inseguono tra caselle |




----




8. ``yield_on_defeat``
----------------------



- A zero PF, l’unità si arrende invece di morire; breve invulnerabilità.

- ``release_yielded_units`` dopo la scelta di alleanza.

- Cap. 25: disabilitato fino alla consegna del gettone (tramite trigger ``set_yield_on_defeat 1``).




----




9. Confronto (cap. 24–27)
-------------------------




| Aspetto | 24 Garrek | 25 Roland | 26 Vera | 27 Marco |

| --- | --- | --- | --- | --- |

| Duello con resa | — | Dopo il gettone | — | Dall’inizio; Raynor deve dare il colpo finale |

| Inizio duello | Alla consegna | Dopo il gettone | Al trasferimento dello stendardo | All’ingresso nell’accampamento di Marco |

| Uccidere NPC chiave troppo presto | Garrek muore → fallimento | Prima del gettone → fallimento | Vera muore → fallimento | Prima del duello all’accampamento → fallimento |




----




10. Documenti correlati
-----------------------




| Argomento | Doc |

| --- | --- |

| Dare a NPC | [give-to-npc.md](give-to-npc.htm) |

| Modalità IA | [unit-default-behavior.md](unit-default-behavior.htm) |

| Selettori indice | [map-unit-index-selectors.md](map-unit-index-selectors.htm) |

| Sintassi ufficiale | ``mod/mapmaking.rst`` |




----




11. Test
--------



.. code-block:: text

   
   python -m pytest soundrts/tests/test_campaign_alliance_transfer_triggers.py -q
   
   python -m pytest soundrts/tests/test_yield_on_defeat_and_campaign_flags.py -q
   
   python -m pytest soundrts/tests/test_give_item_to_npc.py -q
   





----




12. A livello di campagna (crescita di Raynor, seguito, nomi dei luoghi)
------------------------------------------------------------------------




Fasi di Raynor (``rules.txt`` / ``starting_units`` per mappa):



| Capitoli | Tipo unità | Seguito iniziale (oltre Raynor) |

| --- | --- | --- |

| 1–12 | ``raynor`` | predefiniti per capitolo |

| 13–15 | ``raynor2`` | 1 fante |

| 16–18 | ``raynor3`` | 2 fanti |

| 19–21 | ``raynor4`` | 2 fanti, 1 arciere |

| 22–24 | ``raynor5`` | 2 fanti, 1 arciere, 1 cavaliere |

| 25–26 | ``raynor6`` | 2 fanti, 2 arcieri, 2 cavalieri |

| 27–28 | ``raynor7`` | 2 fanti, 2 arcieri, 2 cavalieri |


Cutscene di fase: fine del cap. 12 (``7730``); aperture dei cap. 13/16/19/22/25/27 (``7720``–``7729``, ``7737``–``7738``). Intro schermata attributi: ``ui/style.txt`` ``intro 7740``–``7746``.



Nomi dei luoghi: le mappe dei cap. 1–28 usano ``square_name`` (provincia/contea/sito). TTS nella sezione Place names di ``ui-zh/tts.txt``. Gli script possono ancora usare coordinate di griglia (``c2``) o alias di nomi luogo.
