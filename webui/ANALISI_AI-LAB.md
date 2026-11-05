# Analisi WebUI AI-LAB V7

## Preview

La preview renderizzata è disponibile in [preview.png](preview.png). A 1440 px la pagina appare come una dashboard dark “operations center”: sidebar fissa a sinistra, contenuto a griglia sulla destra, card con bordi blu scuro, accenti cyan/verde e due aloni ambientali. Nella preview senza backend i valori dinamici restano su `—`, `Unknown`, `Waiting` o messaggi di attesa.

## Layout completo

- **Sidebar**: brand AI-LAB, label Workspace, quattro ancore (`Overview`, `Infrastructure`, `Cognitive Core`, `Activity & feedback`), card di connessione al runtime locale e versione V7.
- **Topbar**: breadcrumb `SYSTEM OVERVIEW / NODE41`, titolo Command Center, sottotitolo, pill LIVE con ultimo aggiornamento e pulsante refresh.
- **Metrics grid**: quattro card: CPU gauge, Memory gauge, stato Node41 Primary e stato Node56 Worker.
- **Infrastructure**: Service topology con nodi Node41/Node56 e link LAN, strip di servizi Ollama/FastAPI/Registry, lista modelli disponibili.
- **Alerts**: contatore e lista alert.
- **Cognitive Core**: stato salute, contatori goals/pending/recommendations, coda goal e nota di contesto.
- **Runtime Monitor**: barre CPU, Memory, Node41, Node56 e timestamp del report.
- **Activity**: timeline Feedback con massimo 12 eventi renderizzati.
- **Footer**: nome command center e indicazione polling ogni 5 secondi.
- **Toast**: notifica temporanea in basso a destra per errore completo di connessione.

## ID e binding

Gli ID necessari risultano presenti nell’HTML: `refresh-btn`, tutti i gauge e valori CPU/RAM, orb e barre dei nodi, servizi, modello, alert, goal, report, feedback, toast e indicatori di connessione. Il controllo sintattico di `app.js` passa con `node --check`.

Non risultano ID JavaScript mancanti. Gli ID di sezione (`overview`, `infrastructure`, `cognition`, `activity`) sono usati dalla navigazione ma non devono essere aggiornati da JavaScript. La versione originale però usava accessi DOM non difensivi in più punti: se un elemento fosse rimosso, un singolo `null` avrebbe interrotto il polling. La versione corretta usa guardie sui nodi opzionali.

## Endpoint

L’archivio contiene esclusivamente HTML/CSS/JS: non contiene server, router, FastAPI, proxy o fixture JSON. Gli endpoint dichiarati sono:

- `GET /status`
- `GET /runtime/master-loop`
- `GET /mpc/tasks`

Nel test locale con `python -m http.server`, tutti e tre hanno risposto **404**; non esisteva inoltre alcun server applicativo in ascolto sulla porta 8000. Pertanto non è possibile affermare che esistano realmente lato backend: nel pacchetto non sono implementati. La dashboard può essere corretta solo dopo aver collegato un backend che esponga questi contratti oppure modificando `ENDPOINTS`.

La versione corretta supporta `window.AI_LAB_API_BASE`, per esempio:

```html
<script>window.AI_LAB_API_BASE = 'http://localhost:8000';</script>
<script src="app.js" defer></script>
```

## Perché compaiono i trattini `—`

1. Il frontend avvia subito tre `fetch`; senza backend ricevono 404 o connection failure.
2. `Promise.allSettled` ignora il risultato dei fetch falliti e non dispone di dati da renderizzare.
3. I valori numerici CPU/RAM vengono aggiornati solo se `Number(value)` è finito; altrimenti restano i placeholder iniziali.
4. Anche con HTTP 200, se il JSON non contiene i percorsi attesi (`cpu.usage`, `memory.percent`, `node41`, ecc.), alcuni elementi restano su `—`.
5. Il codice originale poteva trattare oggetti di stato come stringhe, producendo `[object Object]` o stato offline; la versione corretta normalizza `status/state/health/online`.
6. Gli endpoint devono restituire JSON; HTML di errore, redirect o risposta con content type errato non è un payload valido.

## Elementi mai o parzialmente aggiornati nella versione originale

- `app-version` è statico: resta sempre `V7`.
- Il testo `Polling interval: 5s` è statico, anche se `POLL_MS` è configurabile solo nel codice.
- La classe `active` della sidebar non cambia quando si selezionano le altre sezioni.
- CPU e RAM restano intenzionalmente su `—` se il dato manca; non compare la causa specifica per singolo campo.
- Il placeholder iniziale dei modelli viene sostituito solo dopo una risposta status con array modelli.
- `lastSuccess` e `feedback` nello state originale sono assegnati ma non usati per una logica ulteriore.

## Problemi e rischi individuati

- I percorsi assoluti `/style.css` e `/app.js` funzionano solo se la WebUI è pubblicata alla root del dominio; falliscono in una sottocartella. La versione corretta usa percorsi relativi.
- Gli endpoint sono hard-coded e same-origin; manca una configurazione per host/porta API separati.
- Non c’è un contratto/schema del JSON API, quindi i nomi dei campi sono ipotesi.
- `response.json()` nell’originale non verifica il content type e genera errori poco espliciti su pagine HTML di errore.
- Il DOM originale è trattato come sempre presente nelle funzioni `setBar`, `gauge`, `setOrb`, `setDot` e nei render principali.
- Il menu non sincronizza la voce attiva con lo scroll/hash.
- Il footer dichiara read-only, ma la UI non visualizza la versione API o il motivo dettagliato di un endpoint degradato.
- CSS: nessun errore sintattico evidente; il font `Manrope` e `DM Mono` non è importato, quindi il browser usa fallback. La responsività è presente a 1100 e 700 px. Su mobile la sidebar diventa un header compatto e il topology passa in verticale.

## Modifiche necessarie per una dashboard completamente funzionante

1. Implementare o collegare i tre endpoint e documentare il JSON restituito.
2. Stabilire uno schema minimo coerente, ad esempio CPU/RAM numerici 0–100, status testuali, modelli array, `observation`, `goals`, `context`, `alerts` e `feedback`.
3. Configurare l’API base in modo esplicito e abilitare CORS se frontend e backend sono su origini diverse.
4. Servire HTML, CSS e JS dalla stessa base path oppure mantenere i riferimenti relativi corretti.
5. Restituire sempre JSON anche in errore, con status HTTP appropriato.
6. Aggiungere timestamp e stato per singolo endpoint, così un 2/3 non appare come una dashboard quasi sana senza dettaglio.
7. Aggiungere un contratto/schema testato e fixture locali per sviluppo.
8. Decidere una policy per dati mancanti: placeholder, ultimo valore valido o “non disponibile”, senza lasciare ambiguità.
9. Sincronizzare la voce attiva della sidebar con hash e scroll.
10. Aggiungere test browser con risposte API simulate per CPU/RAM, report, alert, modelli, feedback e errori parziali.
11. Valutare import locali o fallback intenzionali per i font, se la resa tipografica deve essere identica in ambiente offline.

## File corretti

- `index.html`: percorsi relativi e script `defer`.
- `app.js`: base API configurabile, controlli DOM, verifica JSON, normalizzazione payload e gestione più robusta di dati parziali.
- `style.css`: invariato perché non presenta bug sintattici bloccanti; resta incluso nella cartella corretta.
