# Campagne cooperative in stile Age of Empires


Guida completa (1.4.3.9): `../player/campaign-and-co-op-improvements.md <../player/campaign-and-co-op-improvements.htm>`_ — browser missioni, livelli di difficoltà, partner IA, determinismo, authoring mappe.

中文：`../../zh/player/战役与合作战役改进说明.md <../../zh/player/战役与合作战役改进说明.htm>`_

Questo motore gioca i capitoli di campagna in cooperativo come Age of Empires II/III
Definitive Edition: più giocatori entrano nella stessa missione narrativa, ciascuno
comanda il proprio slot (base/esercito) nella stessa squadra, condividono gli
obiettivi e le cutscene della missione, e affrontano nemici che scalano con la
difficoltà e il numero di giocatori. Gli slot vuoti sono presi da un partner IA
alleato, così una sola persona può anche giocare una missione coop da sola.

Come funziona la coop (vista giocatore)
----------------------------------------


1. Lobby server → `Co-op campaign` → scegli campagna → scegli capitolo →
   scegli difficoltà (Easy / Standard / Moderate / Hard / Extreme) → scegli velocità.
   (Nessun passo trattato: le campagne coop non offrono mai un trattato.)
2. Gli altri giocatori entrano in lobby; l'host avvia.
3. La cutscene introduttiva della missione viene riprodotta per tutti, poi la missione
   procede con i propri obiettivi che guidano vittoria/sconfitta condivise (non
   «distruggi tutti i nemici»). Cutscene e aggiornamenti obiettivi sono annunciati a voce a tutti.
4. Completare il capitolo sblocca il successivo (segnalibro campagna dell'host).

Come una campagna dichiara la coop (autore campagna)
-----------------------------------------------------


Come le tabelle campagna di Age of Empires, la coop si dichiara in :strong:```campaign.txt``
insieme a ``title`` / ``synopsis``. Non distribuire file paralleli ``N.coop.txt``;
single-player e coop caricano la stessa mappa missione ``N.txt``.

.. code-block:: text

   title 7747
   synopsis 7751
   coop_campaign 1
   coop_intro 0
   coop_missions 1-29



.. list-table::
   :header-rows: 1

   * - Campo
     - Significato
   * - ``coop_campaign``
     - ``1`` — la campagna compare nel menu Co-op campaign del server
   * - ``coop_intro``
     - Numeri capitolo cutscene mostrati nel flusso coop (es. prologo `0`)
   * - ``coop_missions``
     - Numeri capitolo missione giocabili in coop (`1-29`, `1 2 3`, ecc.)



Il motore li analizza in `soundrts/campaign.py <../../../soundrts/campaign.py>`_
(``supports_coop``, ``coop_menu_chapters``, ``coop_mission_chapters``). Le partite coop
caricano la mappa normale del capitolo via ``ensure_chapter_map``. Nessun nome campagna è
hard-coded — qualsiasi mod può aderire con il proprio ``campaign.txt``.

Come un capitolo dichiara gli slot coop (autore mappa)
-------------------------------------------------------


Un capitolo è semplicemente una mappa di campagna. Per renderlo capace di coop, scrivilo con
più di uno slot giocatore umano, tutti destinati alla stessa squadra:

.. code-block:: text

   nb_players_min 1            ; allow solo + AI partners
   nb_players_max 2            ; two co-op slots (Player A / Player B)
   ; one starting square per slot, in different places:
   player_start 1 a1 raynor footman footman
   player_start 2 h8 raynor2 footman archer
   ; enemies are computer_only as usual (they form their own "ai" team):
   computer_only e5 ...


Punti chiave:

- ``nb_players_max`` = numero di slot giocatore coop. Il motore assegna a ogni
  umano (e a ogni partner IA) una posizione di partenza distinta dagli start
  della mappa, così ciascuno ha la propria base/esercito.
- ``nb_players_min 1`` permette a un solo umano di avviare la missione; il motore riempie gli
  slot rimanenti con partner IA alleati
  (``Game._fill_coop_ai_partners`` in `soundrts/serverroom.py <../../../soundrts/serverroom.py>`_).
- Tutti gli slot umani + partner IA sono forzati su una sola squadra (alleanza 1) all'
  avvio. I nemici dichiarati con ``computer_only`` formano una squadra separata
  (``populate_map`` li mette sull'alleanza ``"ai"``), quindi restano ostili.
- I trigger di missione che indirizzano ``player1``, ``player2``, ... mappano ai giocatori
  umani in ordine. Gli slot solo-partner-IA non sono indirizzati da quei
  trigger narrativi (combattono semplicemente con le forze del loro slot).

Il ``MissionGame`` single-player registra ancora un solo umano e usa solo il primo spawn.

Strumento di manutenzione opzionale (solo Raynor)
--------------------------------------------------


`tools/generate_raynor_coop_maps.py <../../../tools/generate_raynor_coop_maps.py>`_ applica trasformazioni di layout coop (mappa più ampia, secondo giocatore specchiato, ecc.) in :strong:```N.txt`` solo per *The Legend of Raynor*. Le altre campagne devono scrivere ``campaign.txt`` + ``N.txt`` direttamente.

Cosa scala con difficoltà / numero di giocatori
-------------------------------------------------


HP e danno in uscita delle unità nemiche sono scalati in modo deterministico (aritmetica intera,
identica su ogni client) dalla difficoltà scelta, ulteriormente aumentati dal
numero di giocatori umani. Vedi
`soundrts/coop_difficulty.py <../../../soundrts/coop_difficulty.py>`_.

Note sul determinismo
----------------------


- I fattori di difficoltà sono calcolati una volta sul server e trasmessi, così tutti
  i client / spettatori / replay ricostruiscono un mondo identico.
- Il carry-over inter-capitolo ``campaign_flag`` è intenzionalmente un no-op in coop
  (il mondo non ha un oggetto campagna locale), evitando divergenze di salvataggio per client.
  ``set_map_flag`` / ``map_flag`` in missione usano lo stato mondo sincronizzato e funzionano
  normalmente.

Test
----


.. code-block:: bash

   python -m pytest soundrts/tests/test_coop_chapter_maps.py -q
   python -m pytest soundrts/tests/test_changelog_1429_coop_campaign_difficulty.py -q
   python -m pytest soundrts/tests/test_changelog_1429c_coop_story_mission.py -q
   python -m pytest soundrts/tests/test_changelog_1429d_coop_player_slots.py -q
