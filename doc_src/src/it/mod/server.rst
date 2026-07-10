Guida al server autonomo
========================

.. contents::

Introduzione
------------

Questa guida spiega come installare un server autonomo pubblico. Un server pubblico consente a qualsiasi giocatore di creare partite.


Installazione dal codice sorgente
---------------------------------

- Metodo archivio:
    - Scarica l’archivio sorgente dell’ultima release da https://github.com/soundmud/soundrts/releases/latest
    - Estrai l’archivio nella cartella che preferisci.
- Metodo Git:
    - per installare v1.3.2:
        - git clone https://github.com/soundmud/soundrts.git
        - git checkout v1.3.2
    - in seguito, per aggiornare a v1.3.3:
        - git fetch
        - git checkout v1.3.3
- Crea una cartella vuota chiamata "user" nella cartella principale.
- Installa Python 3.7 o successivo.
- Avvia il server: python server.py
- Verrà generato "user/SoundRTS.ini".
- Premi Control+C per chiudere il server.
- Modifica il file appena creato "user/SoundRTS.ini":
    - Imposta "login" sul nome del server.
    - Imposta "require_humans" a 1 se vuoi solo partite con almeno 2 giocatori umani.
- Avvia il server: python server.py
- Assicurati che il server sia raggiungibile dall’esterno.


Come rendere il server raggiungibile dall’esterno
-------------------------------------------------

Nella maggior parte dei casi dovrai configurare il router per inoltrare le connessioni TCP in ingresso sulla porta 2500 all’indirizzo IP locale del server.

Potresti anche dover configurare il DHCP del router affinché il server abbia sempre lo stesso indirizzo IP locale.

Se sei dietro un firewall, assicurati che le connessioni TCP in ingresso sulla porta 2500 siano consentite.


Come verificare se il server è raggiungibile dall’esterno
---------------------------------------------------------

Per verificare se il server è raggiungibile dall’esterno della rete locale, attendi che un giocatore si colleghi oppure, idealmente, chiedi a un amico di collegarsi dall’esterno.

Come ultima risorsa puoi usare un sito di test del port forwarding (cerca ad esempio "port forwarding tester"). Attenzione: non posso garantire che questo tipo di sito non sia malevolo! Il sito non dovrebbe chiederti di installare uno strumento, per esempio.


L’elenco dei server
-------------------

L’elenco dei server è ospitato dal metaserver.

Non appena il server è avviato, dovrebbe essere incluso automaticamente nell’elenco. Ciò non significa che sia raggiungibile dall’esterno.

Dopo l’arresto, il server scompare automaticamente dall’elenco. Potrebbe però richiedere un po’ di tempo.


Il parametro require_humans in SoundRTS.ini
-------------------------------------------

Valore predefinito: 0

Se require_humans è impostato a 1, il server non consente al creatore della partita di invitare computer finché non sono registrati almeno due giocatori umani.

Solo i server pubblici sono influenzati da questo parametro.
