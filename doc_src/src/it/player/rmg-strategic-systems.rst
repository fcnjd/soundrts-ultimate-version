Sistemi strategici RMG: eroe e civiltà
======================================

Questo strato aggiunge la progressione dell'eroe in stile Heroes of Might and
Magic e la gestione urbana in stile Civilization alle mappe casuali (Random Map
Generator, RMG). Resta strategia in tempo reale: i rendimenti si liquidano col
tempo di gioco, senza turni.


----


1. Come attivarlo
-----------------

Menu principale → **Avvia partita → Mappa casuale**. Ogni nuova mappa RMG
scrive ``rmg_strategic_systems 1`` e attiva eroe, rendimenti urbani, cultura,
punti diplomatici, tecnologie e politiche.

Mappe manuali e partite non RMG non attivano queste regole di default. Se il
mod non definisce ``rmg_hero``, il generatore salta l'eroe senza errori di
caricamento.


----


2. Progressione dell'eroe
-------------------------

Ogni giocatore inizia con un ``rmg_hero``:

- Livello 1 iniziale, massimo 8.
- Guadagna esperienza in combattimento e sale di livello automaticamente.
- Ogni livello aumenta punti ferita, danno corpo a corpo e mana massimo.
- Mana dedicato; le abilità consumano mana e si rigenera.
- Al massimo un eroe RMG per giocatore.
- In **RMG locale in solitaria**, livello ed esperienza massimi si salvano per
  mod e fazione e si ripristinano nella partita successiva. Multigiocatore e
  replay non leggono il file locale (evita desync).

Profilo eroe tra le partite
~~~~~~~~~~~~~~~~~~~~~~~~~~~

- Percorso: nella directory di configurazione utente, accanto a ``achievements``:
  ``rmg_heroes/<chiave_mod>/<fazione>.json`` (es. ``human.json``).
- A fine partita si salvano livello e XP massimi; all'avvio successivo si
  applicano a ``rmg_hero``, incluse le abilità per livello.
- Solo **mappe casuali locali in solitaria** (``TrainingGame``). Campagna,
  multigiocatore, replay e spettatore non usano questo file.
- Separato da ``campaign_carryover``: ``rmg_hero`` mantiene
  ``campaign_carryover 0``; la persistenza RMG usa JSON dedicato, non
  ``campaigns.ini``.

Albero delle abilità
~~~~~~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1

   * - Livello
     - Abilità
     - Costo mana
     - Effetto
   * - 2
     - Dardo arcano
     - 20
     - Danno magico a un bersaglio
   * - 4
     - Turbine
     - 35
     - Danno nel raggio corpo a corpo
   * - 6
     - Pioggia di meteoriti
     - 60
     - Danno ad area a lunga distanza

Le abilità si sbloccano al livello indicato. Seleziona l'eroe e usa il menu
abilità; mana insufficiente blocca il lancio.


----


3. Espansione urbana e rendimenti delle caselle
-----------------------------------------------

Municipio, roccaforte e castello contano come città. Nei mod compatibili, basi
con **sopravvivenza** e **deposito risorse** anche.

Ogni città possiede la casella principale. Seleziona la città, **Acquista
casella**, poi una casella principale adiacente al territorio attuale. Nessuna
doppia occupazione. Prima acquisto: 20 oro; ogni casella in più +10 oro. Una
nuova città reclama la casella alla costruzione.

Ogni 60 s, ogni città viva e ogni casella lavorata pagano una volta.

Rendimento base per città
~~~~~~~~~~~~~~~~~~~~~~~~~

Per tick:

- 6 oro, 4 legna, 4 cibo, 4 cultura, 1 punto diplomatico.

Bonus terreno urbano
~~~~~~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1

   * - Terreno
     - Extra
   * - Collina, altopiano, roccia alta, passo di montagna
     - +3 oro
   * - Foresta, foresta fitta, palude
     - +3 legna
   * - Pianura, villaggio, prato
     - +3 cibo
   * - Lago, fiume, ruscello, guado
     - +1 oro, +2 cibo

Le risorse contano per **raccolta totale** e vittoria economica RMG.

Cittadini e miglioramenti
~~~~~~~~~~~~~~~~~~~~~~~~~

Comandi **Assegna cittadino a oro / legna / cibo / cultura** su caselle
possedute. Se non ci sono slot, si libera il cittadino più vecchio:

- 1 slot base; pianificazione urbana e amministrazione civica +1 ciascuna;
  roccaforte o castello +1.

Miglioramenti: **miniera** (+3 oro), **segheria** (+3 legna), **fattoria** (+3
cibo). Costi: miniera 15 oro + 10 legna; segheria 10 oro + 15 legna; fattoria
10 oro + 5 legna + 10 cibo.

Rendimento base casella lavorata (ogni 60 s): 1 oro, 1 legna, 1 cibo; stessi
bonus terreno; specializzazione +2 oro/legna/cibo o +3 cultura.

Acquisto: prima espansione 20 oro, poi +10 oro per casella (casella città
gratis).


3.1 Comandi strategici di città
-------------------------------

Con municipio, roccaforte o castello in partita RMG (scegli casella e
conferma):

.. list-table::
   :header-rows: 1

   * - Comando (voce)
     - Parola chiave
     - Effetto
   * - Acquista casella (5718)
     - ``rmg_buy_tile``
     - Compra casella adiacente libera
   * - Assegna cittadino a oro (5719)
     - ``rmg_assign_gold``
     - Lavora casella posseduta
   * - Assegna cittadino a legna (5720)
     - ``rmg_assign_wood``
     - Specializzazione legna
   * - Assegna cittadino a cibo (5721)
     - ``rmg_assign_food``
     - Specializzazione cibo
   * - Assegna cittadino a cultura (5722)
     - ``rmg_assign_culture``
     - +3 cultura/min su quella casella
   * - Costruisci miniera (5723)
     - ``rmg_build_mine``
     - +3 oro/tick
   * - Costruisci segheria (5724)
     - ``rmg_build_lumber_mill``
     - +3 legna/tick
   * - Costruisci fattoria (5725)
     - ``rmg_build_farm``
     - +3 cibo/tick
   * - Attiva politica tradizione (5726)
     - ``rmg_switch_tradition``
     - Cambia tra politiche sbloccate senza costo cultura
   * - Attiva politica commercio (5727)
     - ``rmg_switch_commerce``
     - Idem
   * - Attiva politica diplomazia (5728)
     - ``rmg_switch_diplomacy``
     - Idem


----


4. Albero tecnologico
---------------------

.. list-table::
   :header-rows: 1

   * - Tecnologia
     - Richiede
     - Effetto
   * - Pianificazione urbana
     - —
     - +2 oro, legna e cibo per città/tick
   * - Amministrazione civica
     - Pianificazione urbana
     - +2 cultura per città/tick
   * - Servizio estero
     - Amministrazione civica
     - +1 punto diplomatico per città/tick


----


5. Cultura e carte politiche
----------------------------

La cultura è una statistica strategica di partita; le politiche la consumano
all'adozione.

.. list-table::
   :header-rows: 1

   * - Politica
     - Cultura
     - Richiede
     - Effetto
   * - Tradizione
     - 40
     - Pianificazione urbana
     - +50% cultura
   * - Commercio
     - 80
     - Amministrazione civica
     - +25% oro, legna e cibo urbani
   * - Diplomazia
     - 120
     - Servizio estero
     - Doppio punti diplomatici

Massimo **due** politiche attive. La terza sostituisce la più vecchia. Poi
**Attiva tradizione / commercio / diplomazia** cambia gratis tra quelle
sbloccate.

L'IA sceglie coppie fisse: aggressiva → commercio + tradizione; ≥2 nemici →
diplomazia + commercio; altro → tradizione + commercio.


----


6. Punti diplomatici
--------------------

Le città generano punti ogni minuto. **Inviare richiesta di alleanza** costa 20
punti in RMG strategico (accettare/rifiutare/uscire gratis; cooldown 60 s).


6.1 Consultare cultura e diplomazia
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Cultura e diplomazia **non** usano la barra risorse (Z / X / Maiusc+Z). Nelle
partite RMG con ``rmg_strategic_systems``:

.. list-table::
   :header-rows: 1

   * - Metodo
     - Azione
   * - Scorciatoie globali
     - **B** cultura attuale; **Maiusc+B** punti diplomazia
   * - Attributi città
     - Città propria, attributi (Alt+V): **U** cultura, **Y** diplomazia
   * - Voce periodica
     - Ogni 60 s ``rmg_strategic_tick`` annuncia città, cultura e diplomazia
   * - Avvisi di cambio
     - Con avvisi risorse attivi, anche cambi cultura/diplomazia

Fuori da RMG, **B** / **Maiusc+B** emettono solo segnale.


----


7. Compatibilità mod
--------------------

Architettura gameplay RMG
~~~~~~~~~~~~~~~~~~~~~~~~~

Le mappe casuali uniscono un **framework del motore** (generatore, quattro modi
vittoria, API trigger, sistemi strategici stile Civ opzionali) e **dati da
regole e template**. Valori predefiniti e attivazione sistemi strategici in
``def parameters`` di ``rules.txt``; i template ``cfg/randommap/*.txt`` li
sovrascrivono. Le mod estendono l’RMG via regole/template, senza Python. Un
``map.txt`` manuale consente vittorie totalmente personalizzate.

Parametri globali (``def parameters``)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Include ``rmg_diplomacy_request_cost``, ``rmg_tile_purchase_*``,
``rmg_policy_slot_limit``, ``rmg_trade_cooldown``, ``rmg_economic_goal*``,
``rmg_survival_seconds*``, ``rmg_exploration_ruin_pairs_*``,
``rmg_strategic_systems``.

Miglioramenti casella (``rmg_tile_*``), commercio (``rmg_trade_*``), vittoria
per template (``default_victory_mode``, ``survival_seconds``,
``exploration_ruin_pairs``, ``strategic_systems 0``) e blocco
``victory_triggers`` per modalità personalizzate — vedi
``res/randommap/example.txt`` e la documentazione cinese/inglese completa in
``player/rmg-strategic-systems.htm``.

Altre note
~~~~~~~~~~

- ``rmg_hero`` necessario per l'eroe iniziale.
- Basi con ``provides_survival`` e ``storable_resource_types`` = città.
- Le città ricevono tecnologia e politiche RMG dinamicamente; le mappe non RMG filtrano ricerche ``rmg_``.
- ``can_research`` è salvato come ``_rules_can_research``; ``effective_can_research()`` inietta ``rmg_*`` solo su mappe RMG.

Attributi: ``culture_cost``, ``rmg_policy 1``. Trigger: ``rmg_strategic_tick``,
``rmg_has_culture``, ``rmg_has_diplomacy``, ``rmg_grant_culture``,
``rmg_grant_diplomacy``.


----


8. Implementazione
------------------

``soundrts/rmg_systems.py``, ``rmg_progress.py``, ``worldorders/strategic.py``,
``randommap.py``, ``worldplayercomputer.py``, ``game.py``,
``clientgame/game_resources.py``, ``attributes/basic_attributes.py``,
``res/rules.txt``, voce 5702–5728 e stato cultura/diplomazia 5716–5717,
test ``test_rmg_systems.py``.


----


9. Limiti attuali
-----------------

Niente turni Civ5, crescita popolazione, manutenzione strade o UI diplomatica.
Territorio per casella RMG senza cambiare passaggio unità. Eroe tra partite
solo in RMG locale in solitaria.
