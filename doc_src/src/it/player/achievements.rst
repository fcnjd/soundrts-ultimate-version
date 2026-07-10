Traguardi, gradi e arsenale (giocatori)
=======================================


Come usare l'hub Traguardi del menu principale — senza sintassi di ``achievements.txt``.

Autori di mod: `../mod/achievement-system <../mod/achievement-system.htm>`_.


----


Dove trovarlo
--------------


Menu principale → Traguardi:

1. Elenco traguardi — bloccati / sbloccati; le voci bloccate leggono un riassunto dei requisiti
2. Arsenale — grado attuale, titoli d'onore, totale medaglie, cariche delle carte

I mod multifazione (es. CrazyMod) chiedono prima di scegliere una fazione; Indietro da un sottomenu torna alla selezione della fazione.

Progresso interfazione (solo mod multifazione): meta-traguardi, riepilogo dei rami, onori meta.


----


Cosa conta?
------------



.. list-table::
   :header-rows: 1

   * - Tipo di partita
     - Traguardi / medaglie / gradi
     - Voce del punteggio
   * - Mappa personalizzata o casuale contro il computer
     - ✅
     - ✅
   * - Campagna, campagna cooperativa
     - ❌
     - ❌
   * - Multigiocatore
     - ❌
     - ✅



----


Dopo una partita (non campagna)
--------------------------------


Contro il computer (skirmish), la voce di solito annuncia:

1. Dettaglio del punteggio e voto letterale (S–E) — `score-and-grades.md <score-and-grades.htm>`_
2. Nuovi traguardi, medaglie, cariche delle carte, titoli d'onore
3. Promozione di grado, slot di carico extra se applicabile

Il multigiocatore annuncia solo il punto 1 — niente traguardi, medaglie, gradi o progresso delle carte.

I completamenti ripetuti possono concedere solo medaglie (senza ripetere la voce di carte/onori/sblocchi).


----


Progresso per fazione (CrazyMod, ecc.)
---------------------------------------


- Ogni fazione ha le proprie medaglie, gradi ed elenco di traguardi.
- I salvataggi sono in `user/achievements/<mod>/<faction>.json` (di norma automatici).
- Fazione casuale: all'avvio può chiederti di selezionare la fazione per questa partita.
- Scegli una fazione concreta nella configurazione skirmish per saltare quel passaggio.


----


Meta interfazione
------------------


Il progresso tra i rami sblocca meta-traguardi e titoli d'onore meta (es. tre regni / maestria decupla). Li trovi sotto Progresso interfazione. Le medaglie meta non contano per il grado di una singola fazione.


----


Carte pre-missione
-------------------


Vedi `loadout-cards <loadout-cards.htm>`_.


----


Vedi anche
-----------


- `Note di rilascio <../../relnotes.htm>`_
- `../mod/achievement-system.md <../mod/achievement-system.htm>`_
