Sistema di abilità, cura, danno ed effetti
==========================================


.. epigraph:: Per **autori di mod**: configura abilità attive, aure di cura/danno integrate nelle unità ed effetti di area sul campo di battaglia (``class effect``) in ``rules.txt``. Dal base all’avanzato — leggi i capitoli in ordine.


----


Ordine di lettura
-----------------


1. **Abilità attive** (``class skill``) — mosse attivate dal giocatore o da trigger automatico
2. **Cura/danno di unità** (``heal_*`` / ``harm_*``) — chierici, nubi velenose, ritmo di rigenerazione vita/mana
3. **Effetti di battaglia** (``class effect``) — muri di fuoco, aure, attacchi ad area con debuff
4. **Avanzato** — raffiche burst, trigger automatico, tabella di riferimento dei parametri di area

L’elenco completo delle parole chiave ufficiali è in ``modding.htm``.


Per **autori di mod**: definisci abilità attive con ``class skill`` in ``rules.txt``, senza codice Python. Esempio completo nella mod ufficiale **``mods/wuxia/rules.txt``** (dimostrazione di abilità wuxia).

Concetti di base
----------------


Usa ``class skill`` per definire le abilità, al posto del vecchio ``class ability``:

.. code-block:: text

   def fireball
   class skill
   mana_cost 50
   cost 10 0
   time_cost 30
   effect harm_target 60
   effect_target ask
   effect_range 12
   cooldown 10


Le unità imparano le abilità tramite ``can_use_skill``; gli upgrade continuano a usare ``can_use_tech``.

Sistema unificato di abilità (da 1.4.4.6)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


La stessa ``class skill`` può configurare insieme **lancio manuale** e **trigger automatico**. Le abilità apprese stanno tutte in ``can_use_skill`` dell’unità.


+----+----+
| Attributo | Descrizione |
+====+====+
| `manual_use 1` | Compare nel menu comandi; il giocatore può lanciare con tasto (predefinito `1`) |
+----+----+
| `auto_trigger 1` | Si attiva automaticamente in combattimento quando le condizioni sono soddisfatte (predefinito `0`) |
+----+----+
| `trigger_timing` | Momento del trigger automatico (vedi sotto) |
+----+----+


Entrambi possono coesistere: ad esempio ``manual_use 1`` + ``auto_trigger 1`` significa che il giocatore può lanciare manualmente e l’abilità può anche attivarsi automaticamente in combattimento con una certa probabilità.

I campi legacy ``active_trigger_skills``, ``attack_trigger_skills``, ``attack_replace_skills``, ``passive_trigger_skills`` restano compatibili; le mod nuove dovrebbero usare solo ``can_use_skill`` + ``auto_trigger`` / ``trigger_timing`` sull’abilità.

Modalità di trigger delle abilità
---------------------------------


Quattro momenti di trigger automatico (trigger_timing)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


È necessario impostare ``auto_trigger 1`` e ``trigger_timing``. Il valore predefinito è ``on_hit``.


+------------------+------+------------+
| `trigger_timing` | Momento | Elenco legacy sull’unità (ancora compatibile) |
+==================+======+============+
| `on_hit` | **Dopo che l’attaccante colpisce un nemico** (predefinito) | `active_trigger_skills` |
+------------------+------+------------+
| `on_attack` | Lancio aggiuntivo **all’inizio dell’attacco**; **l’attacco normale continua** | `attack_trigger_skills` |
+------------------+------+------------+
| `on_attack_replace` | Lancio **all’inizio dell’attacco**, **sostituendo l’attacco normale** (se l’abilità si attiva, l’attacco normale viene saltato) | `attack_replace_skills` |
+------------------+------+------------+
| `on_damaged` | **Quando si viene colpiti da un nemico** (passivo) | `passive_trigger_skills` |
+------------------+------+------------+


Nel trigger automatico il gioco verifica mana (``mana_cost``), cooldown (``cooldown``), consuma mana ed entra in cooldown (come nel lancio manuale). Se l’abilità ha ``ready``, anche il trigger automatico attende la preparazione prima di applicare l’effetto.

**Attenzione**: ``on_hit`` si attiva solo dopo che l’attaccante infligge danno a un **nemico**; ``on_damaged`` è attivato dall’unità colpita quando **viene colpita da un nemico**.

Esempio 1: danno aggiuntivo dopo il colpo (on_hit)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^


Quando si attiva sul **nemico colpito**, non usare `self` in ``effect_target`` (il predefinito è l’unità stessa). Configurazione pratica:

.. code-block:: text

   def skill_poison_strike
   class skill
   auto_trigger 1
   manual_use 0
   trigger_timing on_hit
   active_trigger_rate 30
   effect debuffs b_poison
   effect_target ask


Nel trigger automatico, ``ask`` si risolve nel nemico attualmente colpito. Test in ``test_wuxia_skills.py``, caso ``skill_proc``.

Esempio 2: buff aggiuntivo all’attacco (on_attack)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^


.. code-block:: text

   def skill_battle_cry
   class skill
   auto_trigger 1
   manual_use 0
   trigger_timing on_attack
   active_trigger_rate 50
   effect buffs b_battle_cry
   effect_target self


All’inizio dell’attacco, 50% di probabilità di applicare un buff su di sé; **l’attacco normale di questa volta continua**.

Esempio 3: sostituire l’attacco normale (on_attack_replace)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^


.. code-block:: text

   def skill_flame_strike
   class skill
   auto_trigger 1
   manual_use 1
   trigger_timing on_attack_replace
   active_trigger_rate 100
   effect harm_target mdg
   effect_target ask
   effect_range 1
   mdg 15
   cooldown 3
   mana_cost 10


All’inizio dell’attacco tenta di lanciare; se riesce, **non esegue l’attacco normale di questa volta**. Puoi mantenere ``manual_use 1`` perché il giocatore possa lanciare anche dal menu.

Esempio 4: contrattacco quando si viene colpiti (on_damaged)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^


.. code-block:: text

   def skill_thorns
   class skill
   auto_trigger 1
   manual_use 0
   trigger_timing on_damaged
   passive_trigger_rate 30
   effect harm_target 10
   effect_target ask


Quando si viene colpiti da un nemico, 30% di probabilità di infliggere 10 di danno fisso all’**attaccante** (``effect_target ask`` nel trigger passivo si risolve nell’attaccante).

Esempio 5: manuale e automatico insieme
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^


.. code-block:: text

   def skill_heal_proc
   class skill
   auto_trigger 1
   manual_use 1
   trigger_timing on_hit
   active_trigger_rate 15
   effect buffs b_small_heal
   effect_target self
   mana_cost 20
   cooldown 8


Il giocatore può curare manualmente con il tasto dell’abilità; in combattimento, colpendo un nemico, c’è il 15% di probabilità di attivazione automatica (consuma ancora mana e rispetta il cooldown).

Probabilità di trigger
~~~~~~~~~~~~~~~~~~~~~~



+----+------+----+
| Attributo | Momento applicabile | Descrizione |
+====+======+====+
| `active_trigger_rate` | `on_hit`, `on_attack`, `on_attack_replace` | Probabilità 1–100 (predefinito 100) |
+----+------+----+
| `passive_trigger_rate` | `on_damaged` | Probabilità 1–100 (predefinito 100) |
+----+------+----+
| `mdg_trigger_rate` | Momenti attivi sopra | Se > 0, **ha priorità in mischia**, sostituendo `active_trigger_rate` |
+----+------+----+
| `rdg_trigger_rate` | Momenti attivi sopra | Se > 0, **ha priorità a distanza**, sostituendo `active_trigger_rate` |
+----+------+----+


Esempio: trigger al colpo con 80% in mischia e 40% a distanza:

.. code-block:: text

   active_trigger_rate 100
   mdg_trigger_rate 80
   rdg_trigger_rate 40
   trigger_timing on_hit


Condizioni di trigger
~~~~~~~~~~~~~~~~~~~~~



+----+----+
| Attributo | Descrizione |
+====+====+
| `trigger_condition` | Espressione condizionale nel formato `attributo operatore valore` (tre parole, separate da spazio) |
+----+----+
| `hp_threshold` | Scorciatoia: si attiva solo quando la percentuale di vita ≤ soglia (intero, es. `30` = 30% o meno) |
+----+----+


La sintassi di ``trigger_condition`` è la stessa dei buff. ``hp`` e ``mana`` nelle condizioni sono confrontati in **percentuale**:

.. code-block:: text

   trigger_condition hp < 30


Equivalente alla scorciatoia ``hp_threshold 30`` (si attiva solo con vita ≤ 30%).

**Limitazione**: ``trigger_condition`` / ``hp_threshold`` sono verificati attualmente nei percorsi ``on_hit`` e ``on_damaged``; ``on_attack`` / ``on_attack_replace`` **non** verificano queste condizioni.

Preparazione (ready)
~~~~~~~~~~~~~~~~~~~~


.. code-block:: text

   ready 2


Trigger automatico e lancio manuale attendono ``ready`` secondi prima di eseguire l’``effect``; nello ``style.txt`` dell’abilità, ``ready <ID_suono>`` riproduce il suono all’inizio della preparazione.

Differenza tra trigger automatico di abilità e buff in attacco
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~



+----+------+------+
| Meccanismo | Dove configurare | Uso tipico |
+====+======+======+
| `auto_trigger` dell’abilità | `class skill` + `can_use_skill` | Lancia l’effetto completo dell’abilità (harm, buff, deploy ecc.) |
+----+------+------+
| Buff in attacco | `attack_trigger_buffs` / `attack_replace_buffs` ecc. sull’unità | Applica solo buff/debuff, senza def di abilità indipendente |
+----+------+------+
| `is_active` / `is_passive` del buff | `class buff` | Il buff stesso si accumula attaccando/venendo colpiti |
+----+------+------+


La stessa unità può usare insieme trigger automatico di abilità e buff in attacco; probabilità e cooldown sono valutati in modo indipendente.

Bersaglio e portata
~~~~~~~~~~~~~~~~~~~



+----+----+
| Attributo | Descrizione |
+====+====+
| `effect_target` | `self` (unità stessa), `ask` (il giocatore sceglie il bersaglio), `random` (casella casuale) |
+----+----+
| `effect_range` | Portata di lancio (caselle); `inf` = infinito |
+----+----+
| `effect_radius` | Raggio dal centro dell’effetto (alcuni effetti legacy) |
+----+----+


Costo e cooldown
~~~~~~~~~~~~~~~~


``mana_cost``, ``cost`` (risorse), ``time_cost`` (secondi di lancio), ``cooldown`` (secondi di ricarica), ``ready`` (secondi di preparazione; nello ``style.txt`` dell’abilità, ``ready <suono>`` riproduce l’effetto sonoro).

Effetti generali di abilità (effect)
------------------------------------


Sintassi: ``effect <tipo> [parametri…]``

Ogni abilità ha di solito una riga ``effect``. Il motore supporta i tipi eseguibili sotto (effetti legacy e generali da 1.4.4.6):

harm_target — danno su bersaglio singolo
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


**Danno vero fisso** (ignora l’armatura):

.. code-block:: text

   effect harm_target 60


**Danno tramite pipeline di combattimento** (armatura, critico, splash ecc.; gli attributi di combattimento non nulli sull’abilità sovrascrivono il lanciatore):

.. code-block:: text

   effect harm_target mdg
   effect harm_target rdg


Esempi wuxia: ``skill_lipi`` (60 fisso), ``skill_lipi_mdg`` (mdg di combattimento).

harm_area — danno ad area
~~~~~~~~~~~~~~~~~~~~~~~~~


**Danno vero fisso**:

.. code-block:: text

   effect harm_area <danno> <raggio>


Esempio (wuxia ``skill_heng_sao``): ``effect harm_area 50 3`` (50 di danno vero fisso, raggio 3).

**Danno ad area tramite pipeline di combattimento**:

.. code-block:: text

   effect harm_area mdg <raggio>
   effect harm_area rdg <raggio>


Il raggio può essere omesso; in tal caso usa ``effect_radius`` dell’abilità (predefinito 6). L’abilità può sovrascrivere attributi di combattimento:

.. code-block:: text

   def skill_heng_sao_mdg
   class skill
   effect harm_area mdg 3
   mdg 12
   mdg_splash 6
   mdg_radius 1.5
   mdg_splash_decay_min 0.5
   effect_target ask
   effect_range 8


burst — raffica (abilità)
~~~~~~~~~~~~~~~~~~~~~~~~~


.. code-block:: text

   effect burst mdg <volte> (interval <sec>) (window <sec>)
   effect burst rdg <volte> (interval <sec>) (window <sec>)


Oppure usa ritardi per colpo:

.. code-block:: text

   effect burst mdg 3 (delays 0 0.2 0.5)


- `interval`: intervallo tra colpi adiacenti (secondi)
- `window`: finestra totale della raffica (secondi)
- `delays`: elenco di ritardi assoluti per colpo; la lunghezza deve essere uguale al numero di colpi

Il danno proviene da ``mdg`` / ``rdg`` dell’abilità o del lanciatore, con attributi di combattimento completi. Esempi wuxia: ``skill_jifengci``, ``skill_jifengci_rdg``.

.. epigraph:: **Attenzione: `effect burst` di abilità ≠ raffica di attacco `damage_seq` dell’unità.** Vedi la sezione «Avanzato» in questo documento e `player/burst-attacks.htm`.


push — spinta
~~~~~~~~~~~~~


.. code-block:: text

   effect push <distanza>


Spinge il bersaglio nemico lontano dal lanciatore, cercando automaticamente una casella dove possa stare. Esempio wuxia: ``skill_moli_dan`` (``effect push 5``).

buffs / debuffs — applicare buff o debuff
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


.. code-block:: text

   effect buffs <nome_buff> [<nome_buff2> …]
   effect debuffs <nome_debuff>


- `effect_target self`: applica su di sé
- `effect_target ask` + `effect_range`: applica sul bersaglio selezionato

``debuffs`` colpisce solo i nemici. Esempio wuxia: ``skill_douzhuan`` → ``effect buffs b_douzhuan``.

**Riflessione del danno**: non esiste ``effect reflect`` indipendente. Configura ``reflect_percent`` (percentuale) nella definizione del buff e applica con ``effect buffs`` dell’abilità. Esempio wuxia: ``reflect_percent 100`` in ``b_douzhuan``.

deploy — piazzare effetto di battaglia
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


.. code-block:: text

   effect deploy <secondi_vita> [<quantità>] <nome_tipo class effect>


Piazza un’entità ``class effect`` sulla casella bersaglio (muro di fuoco, zona di cura ecc.). Dettagli nella sezione 3 «Effetti di battaglia».

summon — evocazione di unità
~~~~~~~~~~~~~~~~~~~~~~~~~~~~


.. code-block:: text

   effect summon <secondi_vita> [<quantità>] <tipo_unità> …


Opzionale: ``summon_requires_build_field``, ``summon_requires_marked_field``.

Effetti legacy (ancora utilizzabili)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~



+--------+----+
| effect | Descrizione |
+========+====+
| `teleportation` | Teletrasporta un’unità alleata sulla casella bersaglio |
+--------+----+
| `recall` | Richiama un’unità alleata dalla casella bersaglio fino al lanciatore |
+--------+----+
| `conversion` | Converte un’unità nemica |
+--------+----+
| `raise_dead <sec> <unità…>` | Resuscita a partire da un cadavere |
+--------+----+
| `resurrection <limite>` | Resuscita cadaveri alleati |
+--------+----+
| `harm <livello>` | Legacy: genera un effetto harm temporaneo sulla casella bersaglio (preferisci `harm_target` / `harm_area`) |
+--------+----+


Non eseguibili (solo visualizzazione nella UI)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


``effect heal`` e ``effect damage`` formattano solo la visualizzazione nella schermata attributi; **non** curano né infliggono danno al lancio. Per la cura usa ``heal_*`` sull’unità, ``class effect`` o ``effect buffs`` che migliorano attributi di cura.

Filtro del tipo di bersaglio (harm_target_type)
-----------------------------------------------


Valido per ``burst``, ``harm_target``, ``harm_area``, ``push``. Se non configurato, **colpisce solo i nemici** per impostazione predefinita (da 1.4.4.6).

.. code-block:: text

   harm_target_type enemy ground unit -building


- Prefisso `-` su un tag esclude, es.: `-building`, `-undead`, `-enemy`
- `harm_target_type` e `target_type` del buff: i tag positivi sono **AND** (tutti devono essere soddisfatti)
- `heal_target_type` e `mdg_targets` / `rdg_targets`: i tag positivi sono **OR**

Esempi:

.. code-block:: text

   harm_target_type enemy unit -building
   heal_target_type unit -undead
   mdg_targets ground air -building


Riferimento mod: wuxia abilità per abilità
------------------------------------------


Mod di dimostrazione ufficiale: ``mods/wuxia/rules.txt``. Mappa di test: ``mods/wuxia/multi/skills_test.txt``.


+----+-----------+----+
| Abilità | Tipo di effect | Punti chiave |
+====+===========+====+
| `skill_jifengci` | `burst mdg` | 5 colpi, intervallo 0,2 s, finestra 1 s, portata mischia 2 |
+----+-----------+----+
| `skill_jifengci_rdg` | `burst rdg` | Idem, portata a distanza 6 |
+----+-----------+----+
| `skill_heng_sao` | `harm_area 50 3` | 50 di danno vero fisso, raggio 3 |
+----+-----------+----+
| `skill_heng_sao_mdg` | `harm_area mdg 3` | Pipeline di combattimento + override mdg/splash sull’abilità |
+----+-----------+----+
| `skill_lipi` | `harm_target 60` | 60 di danno vero fisso |
+----+-----------+----+
| `skill_lipi_mdg` | `harm_target mdg` | Danno su bersaglio singolo tramite pipeline di combattimento |
+----+-----------+----+
| `skill_douzhuan` | `buffs b_douzhuan` | Buff su di sé; riflessione via `reflect_percent` del buff |
+----+-----------+----+
| `skill_moli_dan` | `push 5` | Spinta di 5 caselle |
+----+-----------+----+


L’unità portatrice ``wuxia_hero`` impara tutte le 8 abilità tramite ``can_use_skill``.

Avanzato
--------


Differenza tra burst di abilità e damage_seq dell’unità
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~



+----+-------------------+-----------------+
| Voce | `effect burst` dell’abilità | `damage_seq` dell’unità |
+====+===================+=================+
| Dove configurare | Riga `effect` in `class skill` | `damage_seq` nella def dell’unità |
+----+-------------------+-----------------+
| Come si attiva | Lancio manuale o automatico dell’abilità | Attacco normale / a distanza |
+----+-------------------+-----------------+
| Fonte del danno | `mdg`/`rdg` dell’abilità o del lanciatore + attributi di combattimento | `mdg`/`rdg` dell’unità suddivisi in più segmenti |
+----+-------------------+-----------------+
| Sintassi dei segmenti | `burst mdg N (interval X)` | `damage_seq mdg N [(damage …)]` |
+----+-------------------+-----------------+
| Documentazione | Questo doc + `modding.htm` | `player/burst-attacks.htm` |
+----+-------------------+-----------------+


Entrambi usano la pipeline di combattimento, ma il punto di configurazione e il momento di attivazione sono del tutto diversi — non mescolare la sintassi.

Libro di abilità e sblocco per upgrade
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


- `level_skills <livello> <abilità> …`: impara automaticamente salendo di livello
- Oggetto `skills` + `learn_level`: impara usando il libro di abilità dell’inventario
- Dettagli in `modding.htm` e `relnotes.htm` §1.4.4.6

Suoni
~~~~~


``style.txt`` dell’abilità: ``alert`` (selezionata), ``ready`` (preparazione), ``triggered`` (effetto applicato). Buff in attacco: vedi ``triggered`` / ``noise loop`` del buff.

Documentazione correlata
------------------------


- Cura/danno integrato nell’unità: `HEAL_HARM_自定义功能说明.md` (sezione 2 di questo documento)
- `class effect` di battaglia e deploy: `EFFECT_BUFF_SYSTEM_说明.md` (sezione 3 di questo documento)
- Elenco completo delle parole chiave: `modding.htm`
- Riepilogo delle note di versione: `relnotes.htm` §1.4.4.6

Per **autori di mod**: configura aure di cura, aure di danno e ritmo di rigenerazione vita/mana sulle unità in ``rules.txt``, senza codice Python. Usa insieme ad abilità attive (``class skill``) e aree di battaglia (``class effect``).

Panoramica
----------


Da 1.4.1.7, danno e cura delle unità sono stati suddivisi in parametri granulari, configurabili nella **def dell’unità** o in **``class effect``**. I parametri sull’unità indicano un effetto continuo o periodico di cura/danno intorno (o su se stessa).

Parametri di danno (harm_*)
---------------------------



+----+----+
| Attributo | Descrizione |
+====+====+
| `harm_level` | Quantità di danno per tick (valore diretto, 1 = 1 punto) |
+----+----+
| `harm_cd` | Intervallo tra i danni (secondi); memorizzato internamente in ms, es. 7,5 s come `7.5` |
+----+----+
| `harm_ready` | Ritardo prima del primo danno (secondi) |
+----+----+
| `harm_range` | Distanza di azione (dall’unità al bersaglio) |
+----+----+
| `harm_radius` | Raggio di azione centrato sul bersaglio |
+----+----+
| `harm_target_type` | Tag di filtro del bersaglio |
+----+----+


Esempio (nube velenosa sull’unità):

.. code-block:: text

   def poison_aura_unit
   class soldier
   harm_level 2
   harm_cd 3
   harm_radius 4
   harm_target_type enemy unit -building


Comportamento di harm_target_type
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


- **Da 1.4.4.6**: nelle abilità, se `harm_target_type` non è configurato, il predefinito è **solo nemici**.
- Puoi usare `enemy`, `allied`, `ground`, `air`, `unit`, `building` ecc.; il prefisso `-` esclude, es.: `-building`, `-undead`.
- I tag positivi sono **AND** (tutti devono essere soddisfatti).
- Senza tag diplomatici come `enemy` / `allied`, le aure harm legacy di unità possono non distinguere alleati e nemici; le mod nuove dovrebbero definire esplicitamente `harm_target_type enemy …`.

Parametri di cura (heal_*)
--------------------------



+----+----+
| Attributo | Descrizione |
+====+====+
| `heal_level` | Quantità di cura per tick |
+----+----+
| `heal_cd` | Intervallo tra le cure (secondi) |
+----+----+
| `heal_ready` | Ritardo prima della prima cura |
+----+----+
| `heal_range` | Distanza di azione |
+----+----+
| `heal_radius` | Raggio di azione |
+----+----+
| `heal_target_type` | Filtro del bersaglio; i tag positivi sono **OR** |
+----+----+


Esempio (aura di cura stile chierico):

.. code-block:: text

   def priest
   class soldier
   heal_level 3
   heal_cd 2
   heal_radius 5
   heal_target_type allied unit -undead


Rigenerazione di vita e mana (regen)
------------------------------------



+----+----+
| Attributo | Descrizione |
+====+====+
| `hp_regen` | Rigenerazione di vita al secondo |
+----+----+
| `hp_regen_cd` | Intervallo del tick di rigenerazione |
+----+----+
| `hp_regen_ready` | Ritardo prima della prima rigenerazione |
+----+----+
| `mana_regen` | Rigenerazione di mana al secondo |
+----+----+
| `mana_regen_cd` | Intervallo di rigenerazione del mana |
+----+----+
| `mana_regen_ready` | Ritardo prima della prima rigenerazione di mana |
+----+----+


Migliorare cura/danno tramite buff
----------------------------------


I buff possono modificare ``heal_level``, ``heal_cd``, ``heal_radius`` o ``harm_level`` ecc. (buff multi-attributo). Esempio:

.. code-block:: text

   def HealEnhancementBuff
   class buff
   stat heal_level heal_cd heal_radius
   v 1 1500 6
   duration 300
   temporary 1


- `v 1` su `heal_level` = +1 punto reale di cura
- `v 1500` su `heal_cd` = cooldown di 1,5 s (millisecondi)
- `v 6` su `heal_radius` = +6 di portata

Applicazione per abilità: ``effect buffs HealEnhancementBuff``.

Relazione con class effect
--------------------------


Le entità ``class effect`` usano gli stessi parametri ``harm_*`` / ``heal_*``, piazzate sul campo da ``effect deploy`` delle abilità. Dettagli in ``EFFECT_BUFF_SYSTEM_说明.md``.

Differenza dagli effect di abilità
----------------------------------



+----+----+
| Forma | Uso |
+====+====+
| `harm_*` / `heal_*` dell’unità | Aura permanente o periodica sull’unità |
+----+----+
| `class effect` + `deploy` | Area temporanea sul campo (muro di fuoco, luce sacra ecc.) |
+----+----+
| `effect harm_target` / `harm_area` | Danno puntuale/raffica di abilità attiva |
+----+----+
| `effect buffs` | Modifica indirettamente attributi heal/harm tramite buff |
+----+----+


**Non esiste** un effect eseguibile ``effect heal``; usa uno dei tre metodi sopra per la cura.

Crescita per upgrade
--------------------


Le unità possono avere ``heal_cd_per_level``, ``harm_radius_per_level`` e altri ``*_per_level`` che si accumulano salendo di livello. Dettagli in ``relnotes.htm`` §1.4.4.6.

Riferimento rapido dei parametri
--------------------------------



+----+----+----+
| Danno | Cura | Significato |
+====+====+====+
| `harm_level` | `heal_level` | Valore per tick |
+----+----+----+
| `harm_cd` | `heal_cd` | Intervallo |
+----+----+----+
| `harm_ready` | `heal_ready` | Ritardo iniziale |
+----+----+----+
| `harm_range` | `heal_range` | Distanza |
+----+----+----+
| `harm_radius` | `heal_radius` | Raggio |
+----+----+----+
| `harm_target_type` | `heal_target_type` | Filtro del bersaglio |
+----+----+----+


Per **autori di mod**: configura effetti di area sul campo con ``class effect``, buff e debuff con ``class buff`` / ``class debuff``; applica tramite ``effect deploy`` o ``effect buffs`` / ``debuffs`` nelle abilità. Senza codice Python.

Effetti di battaglia (class effect)
-----------------------------------


Da 1.4.1.7, le entità ``class effect`` possono infliggere danno ad area, cura o portare debuff in modo continuo sulla mappa.

Esempio di zona di danno
~~~~~~~~~~~~~~~~~~~~~~~~


.. code-block:: text

   def exorcism
   class effect
   harm_level 2
   harm_cd 7.5
   harm_radius 6
   harm_target_type undead
   debuffs b_slow


Esempio di zona di cura
~~~~~~~~~~~~~~~~~~~~~~~


.. code-block:: text

   def holy_ground
   class effect
   heal_level 5
   heal_cd 3
   heal_radius 4
   heal_target_type allied unit


Descrizione dei parametri
~~~~~~~~~~~~~~~~~~~~~~~~~


I parametri di danno e cura sono gli stessi di ``harm_*`` / ``heal_*`` sull’unità (sezione 2 «Cura/danno di unità»). ``class effect`` accetta anche ``decay`` (secondi di vita; il deploy può specificarli dall’abilità).

Piazzamento per abilità
~~~~~~~~~~~~~~~~~~~~~~~


.. code-block:: text

   def skill_blizzard
   class skill
   effect deploy 8 blizzard_fx
   effect_target ask
   effect_range 10


Sintassi: ``effect deploy <sec> [<quantità>] <nome_tipo_effect>``

Diverso da ``effect summon``: deploy genera solo ``class effect``, non unità. Opzionale: ``summon_requires_build_field`` / ``summon_requires_marked_field`` (es. tumore creep).

Esempi integrati in ``res/rules.txt`` (chierico con ``effect deploy`` + ``class effect`` di esorcismo).

Buff e Debuff (class buff / class debuff)
-----------------------------------------


Sintassi di base
~~~~~~~~~~~~~~~~


.. code-block:: text

   def b_slow
   class debuff
   stat speed
   v -2
   duration 10
   temporary 1
   stack 1



+----+----+
| Attributo | Descrizione |
+====+====+
| `stat` | Attributi influenzati (possono essere più di uno) |
+----+----+
| `v` | Bonus fisso |
+----+----+
| `dv` | Variazione al secondo (con `dt`) |
+----+----+
| `percentage` | Bonus percentuale |
+----+----+
| `duration` | Durata (secondi) |
+----+----+
| `temporary` | `1` = rimosso alla morte |
+----+----+
| `stack` | Livelli accumulabili |
+----+----+
| `target_type` | Condizioni per essere bersaglio del buff (logica AND) |
+----+----+
| `buff_radius` | Raggio dell’aura (buff tipo aura) |
+----+----+


Applicare buff per abilità
~~~~~~~~~~~~~~~~~~~~~~~~~~


.. code-block:: text

   def skill_douzhuan
   class skill
   effect buffs b_douzhuan
   effect_target self


.. code-block:: text

   def skill_curse
   class skill
   effect debuffs b_slow
   effect_target ask
   effect_range 8


Anche gli attacchi possono portarli: ``buffs`` / ``debuffs`` nella def dell’unità, o tramite ``attack_trigger_buffs`` ecc.

Riflessione del danno (reflect_percent)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


**Non esiste** la parola chiave ``effect reflect``. Configura sul buff:

.. code-block:: text

   def b_douzhuan
   class buff
   duration 8
   temporary 1
   reflect_percent 100


Poi applica con ``effect buffs b_douzhuan``. La mod wuxia «Dou Zhuan Xing Yi» segue questo schema.

``reflect_percent`` è una percentuale intera (100 = riflessione totale).

Buff multi-attributo
~~~~~~~~~~~~~~~~~~~~


Un buff può influenzare più attributi contemporaneamente:

.. code-block:: text

   def HealEnhancementBuff
   class buff
   stat heal_level heal_cd heal_radius
   v 1 1500 6
   duration 300
   temporary 1


Regole di corrispondenza dei valori:

- Numero di attributi = numero di valori: corrispondenza uno a uno
- Valori insufficienti: ripete l’ultimo valore
- Un solo valore: applica a tutti gli attributi

Attributi a valore diretto (``v 1`` = 1 punto): ``hp``, ``mdg``, ``rdg``, ``heal_level``, ``harm_level``, ``heal_radius``, ``harm_radius``, ``speed`` e oltre 20 altri.

Attributi di tempo (millisecondi): ``heal_cd``, ``harm_cd``, ``mdg_cd``, ``rdg_cd`` ecc.

Buff con trigger
~~~~~~~~~~~~~~~~


.. code-block:: text

   def CombatStanceBuff
   class buff
   stat mdg rdg
   v 30 25
   duration 100
   temporary 1
   is_active 1
   mdg_trigger_rate 80



+----+----+
| Modalità | Attributo |
+====+====+
| Dopo aver colpito | Predefinito |
+----+----+
| All’inizio dell’attacco | `is_active 1` |
+----+----+
| Quando si subisce un attacco | `is_passive 1` + `trigger_condition` + `passive_trigger_rate` |
+----+----+


Suoni del buff (style.txt)
~~~~~~~~~~~~~~~~~~~~~~~~~~


.. code-block:: text

   def b_douzhuan
   triggered douzhuan_proc
   noise loop douzhuan_hum


- `triggered`: riproduce al momento dell’applicazione
- `noise loop`: in loop durante la durata
- `noise repeat <intervallo> <suono…>`: ripete all’intervallo

Filtro del tipo di bersaglio (target_type)
------------------------------------------


La sintassi di ``target_type`` in buff/debuff è uguale a ``harm_target_type``; più condizioni in **AND**. Supporta l’esclusione ``-tag``:

.. code-block:: text

   target_type unit -undead -building


Relazione con il sistema di abilità
-----------------------------------



+-----------+----+
| effect di abilità | Funzione |
+===========+====+
| `effect deploy` | Piazza `class effect` |
+-----------+----+
| `effect buffs` / `debuffs` | Applica buff sul bersaglio |
+-----------+----+
| `effect harm_target` / `harm_area` | Danno diretto (senza entità effect) |
+-----------+----+


Parole chiave complete delle abilità in ``GENERIC_SKILL_SYSTEM.md`` (sezione 1).

Riferimento rapido
------------------


Buff di miglioramento cura
~~~~~~~~~~~~~~~~~~~~~~~~~~


.. code-block:: text

   def heal_aura_buff
   class buff
   stack 1
   stat heal_level heal_cd heal_radius
   v 1 1500 6
   temporary 1
   duration 10
   target_type self


Buff di miglioramento danno
~~~~~~~~~~~~~~~~~~~~~~~~~~~


.. code-block:: text

   def harm_aura_buff
   class buff
   stack 1
   stat harm_level harm_cd harm_radius
   v 2 -1000 4
   temporary 1
   duration 15
   target_type self


Esempi più completi di buff multi-attributo in ``MULTI_ATTRIBUTE_BUFF_说明.md <MULTI_ATTRIBUTE_BUFF_说明.htm>``_. La riflessione del danno usa l’attributo ``reflect_percent`` del buff (percentuale intera, 100 = totale), applicato da ``effect buffs``; non esiste ``effect reflect`` indipendente. Esempio wuxia: ``b_douzhuan``.
