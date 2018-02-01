- [OK] login da configurazione
- [OK] parametri dichiarati da CLI
- [OK] follow/unfollow
- comment in base a ricerche e configurazione
- comment in base a top trending e recupero tramite api
- comment da un set di frasi/parole
- tenere traccia delle variazione del profilo: quanti follower all'inizio e quanti dopo... da fare??? boh
- set di tag da ricercare o da prediligere
- mettere like
- pubblicare foto sui gruppi (possibile?? verificare)
- abilitare proxy? (possibile ban, forse no se è della stessa nazione. nel caso riprenderli da free-proxies.info)


- login solo tramite user e psw


2018 - TODO step by step
- [OK] Inizializzare le code per ogni tipologia di azione: [follow, unfollow, like, unlike, search, comment]
- Tenere le statistiche in un file giornaliero [creare quindi uno storico a rotazione]
- Cercare tramite i criteria base o quelli definiti nel config
- Determinare quindi una serie di keyword o tags sui quali effettuare la ricerca
- Per ogni ricerca, salvare sul corrispettivo file, gli utenti da followare, le foto da like, le foto da unlike, le foto da comment e gli utenti da unfollow
- Inizializzare un array (default inglese) con i commenti base e generici per foto
- Inizializzare un array di keyword o tag da escludere nelle ricerche e/o dalle singole foto
- Dopo che si è fatto un follow, sarà necessario inserire l'utente followato all'interno di un file "tounfollow" con associato una data di "unfollow" [solo se il flag di unfollow è attivo]
- Inserire le funzioni all'interno di una classe Bot [ultima cosa]

[IMPORTANTE, leggi sotto]

Flusso:
- Recupero la configurazione e le credenziali di accesso
- Tento il login
- Se il login ha successo, controllo se ci sono dei parametri di ricerca
- Se ci sono dei parametri di ricerca, mi costruisco le varie possibilità di ricerca
- Costruiti i parametri di ricerca, effettuo le ricerche mettendo ogni ricerca in una coda
- Consumo la coda nei vari thread
- Ogni volta che recupero la pagina di ricerca, mi costruisco un array di informazioni
- Per ogni array (quindi per ogni ricerca), inserisco il risultato in tutte le code delle azioni possibili (comment, vote, unfollow etc) [perciò ogni thread inserisce nelle code]
- Per ogni coda, scorro l'array ritornato ed effettuo le operazioni che sono da effettuare
- Terminate tutte le code, ho due possibilità: termino il programma oppure effettuo ricerche su categorie predefinite
- Se effettuo, al termine, ricerche su categorie predefinite, il ciclo rinizia

come procedere:
- inizializzare le code all'inizio del flusso
- inizializzarei worker all'inizio del flusso con le code e i vari parametri per le funzioni
- iniziare ad effettuare le ricerche
- inserire il tutto in un do while
- Valutare quindi se è meglio definire delle classi o semplici funzioni in altri file