# Mod StarCraft: addon Terran e ricombinazione

Mod: attiva ``mods = starcraft`` in ``SoundRTS.ini``.

Questa guida tratta gli addon Tech Lab / Reactor: costruzione, distacco al decollo, ricombinazione in volo e la differenza tra **terreno edificabile** (permesso di costruzione) e allineamento dello slot (riattacco).

Le mappe StarCraft usano **siti di costruzione** (``build_site``, terreno di casella ``build_sites``) invece dei classici **prati**. Di seguito, «terreno edificabile» indica qualsiasi oggetto ``class building_land``; in questo mod di solito è ``build_site``.


----


1. Concetti
------------



.. list-table::
   :header-rows: 1

   * - Termine
     - Significato
   * - Host
     - Barracks, Factory o Starport (``can_have_addon``)
   * - Addon
     - Tech Lab o Reactor (``is_addon 1``), costruito sullo slot laterale dell'host
   * - Slot
     - Circa 3,5 caselle a est dell'host (``addon_offset_x``, predefinito 3500 unità interne)
   * - Terreno edificabile
     - Un oggetto ``class building_land`` sulla casella (``build_site`` in questo mod); gli edifici Terran a terra devono consumarne uno per atterrare
   * - Ricombinazione
     - Dopo il decollo l'addon resta a terra; un altro host atterra con lo slot allineato e riattacca automaticamente l'addon orfano



Il Tech Lab concede per host, es.:

- Barracks + Tech Lab → Marauder
- Factory + Tech Lab → Siege Tank
- Starport + Tech Lab → Medivac

Il Reactor usa ``addon_train_multiplier 2``.


----


2. Costruire un addon
----------------------


1. Seleziona un host esistente (es. Barracks), non il terreno nudo.
2. Costruisci Tech Lab o Reactor dal menu.
3. L'addon si auto-costruisce sul lato dell'host (``self_constructs 1``); non usa un proprio slot di terreno edificabile.

Mappa di test: ``terran_addon_test``.


----


3. Decollo
-----------


Barracks / Factory / Starport possono passare alla forma volante (``can_change_to flying_*``):

1. Seleziona l'edificio a terra → change_to → variante volante.
2. L'host lascia il suolo; l'addon resta e viene distaccato.
3. Il terreno edificabile viene ripristinato dove stava l'host: **lo stesso tipo che l'edificio aveva consumato alla costruzione** (``build_site`` in questo mod). Se la mappa genera solo siti di costruzione (``nb_build_site_by_square``, ``building_land build_site``, ecc.), il decollo lascia un build site — **non** serve ``default_building_land build_site`` nelle regole del mod per questo.

Una casella può avere più pezzi (es. Barracks e Factory decollo ciascuno una volta → due build site). Sui punti di partenza con un solo pezzo di mappa, la Factory può partire senza terreno edificabile; i pezzi compaiono a ogni posizione di decollo dell'edificio.


----


4. Atterraggio normale vs atterraggio di ricombinazione
---------------------------------------------------------


4.1 Due controlli separati
~~~~~~~~~~~~~~~~~~~~~~~~~~~



.. list-table::
   :header-rows: 1

   * - Passo
     - Decide
     - Non decide
   * - Atterraggio
     - Quale oggetto di terreno edificabile viene consumato; host (x, y)
     - Riattacco
   * - Riattacco
     - Il Tech Lab orfano si attacca all'host
     - Quale pezzo è stato usato



Terreno edificabile = permesso di atterrare (qualsiasi ``class building_land`` sulla casella; nomi API come ``find_meadow_near_xy`` sono storici).  
Slot = geometria: addon a ``(host.x + 3500, host.y)``; il riattacco richiede allineamento dello slot entro ~2,5 caselle di distanza Manhattan.

Puoi vedere la Factory su un «pezzo centrale» mentre l'addestramento dei Tank funziona: lo slot è allineato, non perché l'edificio stia sull'erba sotto il lab.

4.2 Atterraggio normale (proprio pezzo di decollo)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


1. Tab sul terreno edificabile lasciato quando quell'edificio è decollato (build site in questo mod).
2. Backspace (``go`` predefinito), attendi l'arrivo.
3. change_to forma a terra.

L'edificio atterra lì e non prende un Tech Lab orfano. Se sulla casella resta un addon orfano compatibile, senti: *Vai prima al Tech Lab, poi atterra per riattaccare l'addon* (TTS 7350).

4.3 Atterraggio di ricombinazione (prendere il Tech Lab orfano)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


1. Costruisci Tech Lab sui Barracks, fai decollare i Barracks (il lab resta).
2. Fai decollare la Factory, vola su quella casella.
3. Tab sul Tech Lab (non su un pezzo di terreno edificabile).
4. Backspace go — il bersaglio diventa lo slot di atterraggio (~3,5 caselle a ovest del lab), non il centro del lab.
5. change_to Factory.

Risultato:

- La Factory compare alle coordinate dello slot;
- Viene consumato l'oggetto di terreno edificabile più vicino sulla casella (spesso un pezzo centrale);
- Lo slot si allinea al lab → riattacco automatico → Tank (ecc.) disponibili.

Mappa di test: ``terran_recombine_test``; campagna ``sc_build_tests`` capitolo 4.


----


5. Riferimento rapido
----------------------



.. list-table::
   :header-rows: 1

   * - Obiettivo
     - Tab
     - Dopo go
     - Risultato di change_to
   * - Atterrare sul punto di decollo
     - Build site del decollo
     - Backspace
     - Nessun riattacco, nessun Tank
   * - Prendere il Tech Lab orfano
     - Tech Lab
     - Backspace (vola allo slot)
     - Riattacco, Tank disponibili



Con più pezzi, la voce di Tab può dire «build site» per tutti — usa la direzione; per la ricombinazione, Tab sul lab.


----


6. FAQ
-------


Perché posso addestrare Tank quando il lab non ha pezzi vicini, solo pezzi centrali?

Andare al Tech Lab ti fa volare allo slot. L'atterraggio piazza la Factory allo slot (x,y) ma elimina l'oggetto di terreno edificabile più vicino (spesso uno centrale). Il riattacco controlla la distanza dal lab a ``factory.x + 3500``, non quale pezzo è stato usato.

Perché l'atterraggio al centro riattaccava prima?

La logica precedente agganciava l'atterraggio ovunque sulla casella entro ~5,5 m dal lab. Ora: vai al tuo pezzo di decollo → atterra sul posto; la ricombinazione richiede di andare al Tech Lab.

Slot allineato ma sembra lontano dal lab?

Il lab è sul lato dell'host (offset di ~3,5 caselle), non sotto il centro dell'host — layout in stile SC2.


----


7. Autori di mod (rules.txt)
-----------------------------



.. list-table::
   :header-rows: 1

   * - Parola chiave
     - Ruolo
   * - ``can_have_addon``
     - Tipi di addon consentiti sull'host
   * - ``is_addon 1``
     - Edificio addon
   * - ``addon_host_types``
     - Quali host accettano questo addon
   * - ``addon_grants_train_\<host\>``
     - Opzioni di addestramento extra quando attaccato
   * - ``addon_grants_research``
     - Ricerca extra quando attaccato
   * - ``addon_train_multiplier``
     - Moltiplicatore del Reactor
   * - ``can_change_to`` / ``ground_form``
     - Forme di decollo / atterraggio
   * - ``change_time``
     - Tempo di morfosi
   * - ``nb_build_site_by_square``
     - Riempie automaticamente ogni casella con ``build_site``; vedi ``mod/mapmaking.rst`` e ``mod/building-land-terrain.htm``



Vedi anche ``mods/starcraft/readme.txt``.  
Riferimento per autori: ``mod/modding.rst`` sezione *Build fields, addons & lift-off*.
