# Previsione Mutuo — Web App Flask con Machine Learning

Applicazione web sviluppata in Flask, che integra un modello di Machine Learning per prevedere l'esito di una richiesta di mutuo. Progetto realizzato durante i miei studi alla Steve Jobs Academy, sede di Catania, come esame in Python.

## Sul mio contributo al progetto

Flask e Jinja2 non sono stati scritti da me: sono strumenti già esistenti, rispettivamente un framework web e un motore di template, ampiamente usati nello sviluppo Python. Il punto di partenza dell'esercitazione era un progetto Flask vuoto, con la struttura di base già predisposta.

Il mio lavoro è consistito nello studiare il funzionamento di questi strumenti e nel costruirci sopra un'applicazione completa: definire le route, scrivere la logica di lettura e conversione dei dati del form, realizzare le pagine HTML e, soprattutto, integrare il modello di Machine Learning nel flusso dell'applicazione, gestendo la previsione e tutti i casi di errore che possono presentarsi lungo il percorso.

## Cosa fa

L'utente apre la pagina iniziale e compila un form con i propri dati anagrafici e finanziari: genere, stato civile, istruzione, persone a carico, redditi del richiedente e dell'eventuale co-richiedente, importo e durata del mutuo, storico creditizio e area geografica dell'immobile. Alla conferma l'applicazione raccoglie i dati, li organizza in una struttura tabellare e li sottopone al modello, che restituisce una previsione. In base all'esito l'utente viene reindirizzato a una pagina di approvazione o a una di rifiuto.

## Come funziona

Il progetto segue il pattern MVT (MODEL · VIEW · TEMPLATE), che distribuisce il lavoro su tre livelli distinti anziché concentrare tutto in un unico blocco di codice.


La prima parte (MODEL), si occupa esclusivamente del Machine Learning: converte i valori ricevuti dal form nei tipi attesi, costruisce un DataFrame con le colonne corrette e restituisce la previsione insieme alla probabilità associata. La seconda parte (VIEW), è costituita dalle route Flask, che ricevono le richieste, invocano il modello e decidono verso quale pagina indirizzare l'utente. La terza parte (TEMPLATE), raccoglie le tre pagine HTML costruite con Jinja2: `index.html` con il form di inserimento, `success.html` e `fail.html` per i due esiti possibili.

Il modello è stato addestrato separatamente su un dataset tabellare di richieste di mutuo ed esportato come pipeline unica, che racchiude sia il preprocessing sia il classificatore. Questo semplifica il lavoro dell'applicazione, che non deve applicare scaler o encoder in modo manuale: costruisce i dati, chiama il metodo di previsione e interpreta il risultato. Il caricamento del file avviene una sola volta all'avvio, non a ogni richiesta.

Particolare attenzione è stata dedicata alla gestione degli errori: l'applicazione non si interrompe in presenza di problemi prevedibili. 
Sono gestiti: il file del modello mancante o non caricabile, i campi del form lasciati vuoti, i valori inseriti in formato errato e gli errori che possono verificarsi durante la previsione. In tutti questi casi l'utente riceve un messaggio nella pagina iniziale, invece di trovarsi davanti a un'applicazione bloccata.

## Struttura

Il codice dell'applicazione risiede nella cartella `restful`. Il file `app.py` contiene la logica completa: caricamento del modello, lettura dei dati del form, previsione e definizione delle route. Accanto si trovano `modello_mutuo.joblib`, ovvero il modello addestrato, e `requirements.txt` con l'elenco delle dipendenze. La cartella `templates` raccoglie le pagine HTML, mentre `static/img` contiene le risorse grafiche utilizzate dall'interfaccia.

## Ambiente virtuale

Il progetto utilizza un ambiente virtuale Python, contenuto nella cartella `.venv`. Si tratta di un'installazione di Python isolata e dedicata unicamente a questo progetto: le librerie necessarie — Flask, scikit-learn, pandas, joblib, NumPy e le rispettive dipendenze — vengono installate al suo interno anziché nell'installazione di sistema.

Questa scelta evita due problemi ricorrenti. Il primo è l'interferenza tra progetti diversi: senza isolamento, aggiornare una libreria per un progetto rischierebbe di rompere il funzionamento di un altro che dipende da una versione precedente. Il secondo riguarda la riproducibilità: le versioni esatte utilizzate sono registrate in `requirements.txt`, così l'ambiente può essere ricostruito in modo identico su qualunque macchina.

L'ambiente virtuale non viene versionato: pesa centinaia di megabyte e sarebbe comunque legato al sistema operativo su cui è stato creato. Chi scarica il progetto se lo ricrea in locale a partire da `requirements.txt`, come indicato di seguito.

## Come eseguire il progetto

Dal terminale, dentro la cartella `restful`, si crea e si attiva l'ambiente virtuale:

```bash
python -m venv .venv (per windows) | python3 -m venv .venv (per Linux o macOS)
source .venv/Scripts/activate (per windows) | source .venv/bin/activate (per Linux o  macOS)
```

Poi si installano le dipendenze e si avvia l'applicazione:

```bash
pip install -r requirements.txt (sia per windows che linux/macOS
python app.py (se l'ambiente virtuale è attivo), (altrimenti se l'ambiente non è attivo, su macOS e Linux) python3 app.py 
```

L'applicazione si avvia in locale, di norma all'indirizzo `http://127.0.0.1:5000`. Il file `modello_mutuo.joblib` deve trovarsi nella cartella del progetto: in sua assenza l'applicazione parte comunque, ma segnala che il modello non è disponibile.
