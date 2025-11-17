# Sistema di Gestione Aziendale Agricola

Un'applicazione web completa per la gestione di aziende agricole, sviluppata con Flask e SQLite. Il sistema permette di gestire tutti gli aspetti dell'attività agricola: terreni, macchinari, animali, colture, personale, magazzino, manutenzioni e finanze.

## Caratteristiche Principali

- **Gestione Terreni**: Traccia appezzamenti con dati catastali e visualizzazione su mappa interattiva
- **Gestione Macchinari**: Monitora trattori e attrezzature agricole
- **Gestione Animali**: Registro completo del bestiame con genealogia
- **Gestione Colture**: Pianifica e traccia le coltivazioni per terreno
- **Gestione Personale**: Anagrafica dipendenti con contratti e ruoli
- **Magazzino**: Inventario di sementi, fertilizzanti e altri prodotti
- **Manutenzioni**: Calendario delle manutenzioni preventive e correttive
- **Finanze**: Traccia spese e ricavi con statistiche

## Tecnologie Utilizzate

- **Backend**: Flask (Python)
- **Database**: SQLite
- **Frontend**: HTML5, CSS3, JavaScript Vanilla
- **Mappe**: Leaflet.js con OpenStreetMap
- **Deployment**: Docker, Docker Compose
- **CI/CD**: GitHub Actions con security scanning

## Installazione

### Requisiti
- Python 3.9 o superiore
- pip (gestore pacchetti Python)

### Setup Locale

1. **Clone il repository**
   ```bash
   git clone <url-repository>
   cd farm-management-app
   ```

2. **Installa le dipendenze**
   ```bash
   pip install -r requirements.txt
   ```

3. **Avvia l'applicazione**
   ```bash
   python app.py
   ```

4. **Apri il browser**
   ```
   http://localhost:5000
   ```

### Setup con Docker

```bash
# Avvia con Docker Compose
docker-compose up -d

# Visualizza i log
docker-compose logs -f

# Ferma l'applicazione
docker-compose down
```

L'applicazione sarà disponibile su `http://localhost:5000`

## Manuale Utente

### Menu Principale

Dopo aver avviato l'applicazione, verrai accolto dal menu principale che mostra tutte le sezioni disponibili:

- Terreni
- Trattori
- Attrezzi
- Animali
- Colture
- Personale
- Magazzino
- Manutenzioni
- Finanze

### 1. Gestione Terreni

**Funzionalità**: Gestisci gli appezzamenti di terreno della tua azienda agricola.

**Come usare:**
1. Dalla dashboard farm, clicca su "Terreni"
2. Clicca "Nuovo Terreno" per aggiungere un appezzamento
3. Compila i campi:
   - **Nome**: Nome identificativo del terreno (es. "Campo Nord")
   - **Superficie (ettari)**: Dimensione in ettari
   - **Tipo di terreno**: Argilloso, sabbioso, limoso, ecc.
   - **Ubicazione**: Indirizzo o località
   - **Foglio**: Numero di foglio catastale
   - **Particella**: Numero di particella
   - **Subalterno**: Numero subalterno (opzionale)
   - **Note**: Annotazioni aggiuntive

**Mappa Interattiva:**
- Visualizza e disegna i confini dei terreni su mappa
- Salva le coordinate GeoJSON per riferimento futuro
- Naviga tra i diversi appezzamenti

### 2. Gestione Trattori e Mezzi

**Funzionalità**: Monitora i macchinari agricoli e il loro stato di manutenzione.

**Come usare:**
1. Clicca su "Trattori" dal menu
2. Clicca "Nuovo Trattore" per registrare un mezzo
3. Inserisci i dati:
   - **Marca e Modello**: Es. "John Deere 6110M"
   - **Anno**: Anno di produzione
   - **Targa**: Numero di targa
   - **Numero telaio**: VIN del veicolo
   - **Potenza (CV)**: Cavalli vapore
   - **Ore lavoro**: Contaore attuale
   - **Data acquisto**: Quando è stato acquistato
   - **Costo acquisto**: Prezzo pagato
   - **Stato**: Operativo, In manutenzione, Fuori servizio

**Suggerimenti:**
- Aggiorna regolarmente le ore di lavoro
- Collega le manutenzioni tramite il modulo apposito
- Monitora il valore residuo dei mezzi

### 3. Gestione Attrezzi

**Funzionalità**: Inventario completo di attrezzature e attrezzi agricoli.

**Come usare:**
1. Accedi alla sezione "Attrezzi"
2. Aggiungi nuove attrezzature con:
   - **Nome**: Es. "Aratro reversibile"
   - **Tipo**: Categoria dell'attrezzo
   - **Marca e Modello**: Produttore e modello
   - **Anno acquisto**: Anno di acquisto
   - **Costo**: Prezzo di acquisto
   - **Stato**: Buono, Usurato, Da riparare
   - **Ultima manutenzione**: Data dell'ultimo controllo

### 4. Gestione Animali

**Funzionalità**: Registro completo del bestiame con tracciamento genealogico.

**Come usare:**
1. Vai su "Animali"
2. Registra nuovi animali:
   - **Specie**: Bovino, Ovino, Suino, ecc.
   - **Razza**: Razza specifica dell'animale
   - **Identificativo**: Codice univoco (es. marchio auricolare)
   - **Data di nascita**: Per calcolare l'età
   - **Sesso**: Maschio/Femmina
   - **Peso (kg)**: Peso attuale
   - **Stato salute**: Sano, Malato, In trattamento
   - **Padre/Madre ID**: Riferimento ai genitori per genealogia

**Funzionalità avanzate:**
- Traccia la genealogia collegando padri e madri
- Monitora lo stato di salute
- Registra variazioni di peso nel tempo

### 5. Gestione Colture

**Funzionalità**: Pianifica e traccia le coltivazioni su ciascun terreno.

**Come usare:**
1. Accedi a "Colture"
2. Crea una nuova coltura:
   - **Terreno**: Seleziona l'appezzamento (dai terreni registrati)
   - **Tipo coltura**: Grano, Mais, Orzo, Girasole, ecc.
   - **Varietà**: Varietà specifica della coltura
   - **Data semina**: Quando è stata seminata
   - **Data raccolta prevista**: Stima del raccolto
   - **Data raccolta effettiva**: Quando avviene realmente
   - **Quantità raccolta (kg)**: Produzione effettiva
   - **Stato**: In corso, Raccolta completata, Abbandonata

**Suggerimenti:**
- Pianifica le rotazioni delle colture
- Confronta rese previste vs effettive
- Analizza la produttività per terreno

### 6. Gestione Personale

**Funzionalità**: Anagrafica completa dei dipendenti e collaboratori.

**Come usare:**
1. Vai su "Personale"
2. Aggiungi dipendenti:
   - **Nome e Cognome**: Dati anagrafici
   - **Ruolo**: Trattorista, Operaio, Veterinario, ecc.
   - **Telefono**: Numero di contatto
   - **Email**: Indirizzo email
   - **Data assunzione**: Inizio del rapporto di lavoro
   - **Tipo contratto**: Tempo indeterminato, Determinato, Stagionale
   - **Retribuzione mensile**: Stipendio mensile
   - **Note**: Competenze specifiche, certificazioni

**Privacy:**
- I dati del personale sono sensibili: gestisci con attenzione
- Usa per pianificare turni e responsabilità

### 7. Gestione Magazzino

**Funzionalità**: Inventario di sementi, fertilizzanti, fitofarmaci e altri prodotti.

**Come usare:**
1. Clicca su "Magazzino"
2. Registra prodotti:
   - **Categoria**: Sementi, Fertilizzanti, Fitofarmaci, Carburanti, ecc.
   - **Nome prodotto**: Descrizione del prodotto
   - **Marca**: Produttore
   - **Quantità**: Quantità disponibile
   - **Unità di misura**: kg, litri, sacchi, ecc.
   - **Data acquisto**: Quando è stato acquistato
   - **Costo unitario**: Prezzo per unità
   - **Scadenza**: Data di scadenza (importante per fitofarmaci)
   - **Fornitore**: Chi ha fornito il prodotto

**Funzioni utili:**
- Monitora le scorte
- Ricevi alert per prodotti in scadenza
- Ottimizza gli ordini

### 8. Gestione Manutenzioni

**Funzionalità**: Calendario delle manutenzioni per macchinari e attrezzature.

**Come usare:**
1. Vai su "Manutenzioni"
2. Registra interventi:
   - **Tipo oggetto**: Trattore, Attrezzo, Edificio, ecc.
   - **ID oggetto**: Riferimento all'oggetto specifico
   - **Data manutenzione**: Quando è stata eseguita
   - **Tipo**: Ordinaria, Straordinaria, Riparazione
   - **Descrizione**: Cosa è stato fatto
   - **Costo**: Spesa sostenuta
   - **Eseguita da**: Meccanico interno o officina esterna
   - **Prossima manutenzione**: Pianifica il prossimo intervento

**Suggerimenti:**
- Imposta promemoria per manutenzioni programmate
- Mantieni storico completo per ogni mezzo
- Analizza i costi di manutenzione nel tempo

### 9. Gestione Finanze

**Funzionalità**: Traccia tutte le spese e i ricavi dell'azienda agricola.

**Come usare:**
1. Accedi a "Finanze"
2. Registra operazioni:
   - **Tipo**: Spesa o Ricavo
   - **Categoria**:
     - *Spese*: Carburante, Sementi, Manodopera, Manutenzione, ecc.
     - *Ricavi*: Vendita prodotti, Contributi, Affitti
   - **Descrizione**: Dettaglio dell'operazione
   - **Importo**: Somma in euro
   - **Data operazione**: Quando è avvenuta
   - **Metodo pagamento**: Contanti, Bonifico, Carta, ecc.
   - **Riferimento**: Numero fattura o ricevuta
   - **Note**: Informazioni aggiuntive

**Dashboard Statistiche:**
- Visualizza totale spese vs ricavi
- Analizza il bilancio aziendale
- Monitora i flussi di cassa

### Dashboard Principale

La dashboard della farm mostra statistiche in tempo reale:
- Numero di terreni e superficie totale
- Conteggio macchinari e attrezzature
- Numero di animali
- Colture attive
- Numero dipendenti
- Bilancio (spese vs ricavi)

## Deployment su Render.com

### Deploy Rapido

1. **Carica il codice su GitHub**
   ```bash
   git add .
   git commit -m "Ready for deployment"
   git push origin main
   ```

2. **Configura Render.com**
   - Vai su [render.com](https://render.com)
   - Clicca "New +" → "Blueprint"
   - Connetti il repository GitHub
   - Render rileverà automaticamente `render.yaml`
   - Clicca "Apply" per deployare

3. **Accedi all'app**
   - L'app sarà disponibile su `https://your-app-name.onrender.com`
   - Il database SQLite è persistito su disco

### Note sul Free Tier
- L'app va in sleep dopo 15 minuti di inattività
- Primo accesso dopo sleep: ~30 secondi (cold start)
- Database persistito su disco da 1GB (incluso nel free tier)
- Auto-deploy automatico ad ogni push su `main`

## Sicurezza e Backup

### Security Features
- **Scanning automatico**: Ogni commit viene scansionato per vulnerabilità
- **Container security**: L'app Docker gira con utente non-root
- **Input validation**: Validazione dei dati in input

### Backup del Database

Il database è un singolo file `farm_management.db`. Per fare backup:

```bash
# Locale
cp farm_management.db farm_management_backup_$(date +%Y%m%d).db

# Docker
docker cp farm-app:/data/farm_management.db ./backup/
```

### Restore

```bash
# Locale
cp farm_management_backup_20250117.db farm_management.db

# Docker
docker cp ./backup/farm_management.db farm-app:/data/
```

## Troubleshooting

### L'app non si avvia

```bash
# Verifica che le dipendenze siano installate
pip install -r requirements.txt

# Controlla i log
python app.py
```

### Database bloccato

```bash
# Chiudi tutte le connessioni e riavvia
# Su Docker:
docker-compose restart
```

### Problemi con Docker

```bash
# Ricostruisci l'immagine
docker-compose down
docker-compose build --no-cache
docker-compose up -d
```

### Health Check

Verifica che l'app sia operativa:
```bash
curl http://localhost:5000/health
```

Risposta attesa:
```json
{
  "status": "healthy",
  "database": "connected"
}
```

## Contribuire

Questo progetto è in attivo sviluppo. Per contribuire:

1. Fai un fork del repository
2. Crea un branch per la tua feature (`git checkout -b feature/nuova-funzionalita`)
3. Committa le modifiche (`git commit -m 'Aggiunge nuova funzionalità'`)
4. Pusha il branch (`git push origin feature/nuova-funzionalita`)
5. Apri una Pull Request

## Licenza

Questo progetto è distribuito con licenza MIT. Vedi il file `LICENSE` per i dettagli.

## Supporto

Per domande, problemi o suggerimenti:
- Apri una Issue su GitHub
- Consulta la documentazione nel file `CLAUDE.md`

## Roadmap Future

- [ ] Export dati in Excel/PDF
- [ ] Dashboard con grafici interattivi
- [ ] App mobile (React Native)
- [ ] Sistema di notifiche (email/SMS)
- [ ] Integrazione con sensori IoT
- [ ] Previsioni meteo integrate
- [ ] Sistema di reportistica avanzata
- [ ] Multi-utente con autenticazione
- [ ] API REST documentata

---

**Sviluppato con Flask e Python**

Per maggiori informazioni tecniche, consulta `CLAUDE.md` nella root del progetto.
