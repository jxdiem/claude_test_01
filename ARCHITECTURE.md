# Architettura del Sistema
## Sistema di Gestione Aziendale Agricola

**Versione**: 1.0
**Data**: Gennaio 2025
**Stato**: Produzione

---

## 1. PANORAMICA DELL'ARCHITETTURA

### 1.1 Descrizione Generale
Il sistema è un'applicazione web monolitica basata su architettura a tre livelli (3-tier) per la gestione completa di aziende agricole. L'applicazione è progettata per essere deployata in container Docker e supporta deployment sia on-premise che cloud.

### 1.2 Principi Architetturali
- **Semplicità**: Architettura monolitica per facilità di deployment e manutenzione
- **Portabilità**: Containerizzazione con Docker per deployment multi-piattaforma
- **Persistenza**: Database SQLite con volume persistente
- **Scalabilità verticale**: Ottimizzata per singola istanza con possibilità di scaling verticale
- **Sicurezza by design**: Implementazione di best practices di sicurezza a ogni livello

---

## 2. ARCHITETTURA A LIVELLI

### 2.1 Presentation Layer (Frontend)

**Tecnologie**:
- HTML5
- CSS3 (Custom styling con gradient e animazioni)
- JavaScript Vanilla (ES6+)
- Leaflet.js (Mappe interattive)

**Caratteristiche**:
- Single Page Application (SPA) pattern per alcune sezioni
- Comunicazione asincrona tramite Fetch API
- Responsive design per supporto mobile
- Interfaccia utente con tema gradient purple personalizzato

**Componenti principali**:
```
templates/
├── menu.html           # Menu principale
├── index.html          # Modulo numeri (legacy)
├── farm.html           # Dashboard gestione agricola
└── terreni_map.html    # Mappa interattiva terreni
```

### 2.2 Application Layer (Backend)

**Tecnologie**:
- Python 3.9+
- Flask Framework 2.x
- SQLite3 (Python standard library)

**Architettura del Backend**:
```
app.py (Main Application)
│
├── Route Handlers
│   ├── Menu Routes (/, /health)
│   ├── Numbers Routes (/numbers, /add, /delete)
│   ├── Farm Routes (/farm, /terreni)
│   └── API Routes (/api/*)
│
├── Database Layer
│   ├── get_db_connection()
│   └── init_db()
│
└── Business Logic
    └── CRUD Operations per ogni modulo
```

**API Endpoints**:

| Endpoint | Metodo | Descrizione |
|----------|--------|-------------|
| `/` | GET | Menu principale |
| `/health` | GET | Health check endpoint |
| `/numbers` | GET | Pagina gestione numeri |
| `/farm` | GET | Dashboard farm management |
| `/terreni` | GET | Mappa interattiva terreni |
| `/api/terreni` | GET, POST | Gestione terreni |
| `/api/terreni/<id>` | DELETE | Eliminazione terreno |
| `/api/trattori` | GET, POST | Gestione trattori |
| `/api/trattori/<id>` | DELETE | Eliminazione trattore |
| `/api/attrezzi` | GET, POST | Gestione attrezzi |
| `/api/attrezzi/<id>` | DELETE | Eliminazione attrezzo |
| `/api/animali` | GET, POST | Gestione animali |
| `/api/animali/<id>` | DELETE | Eliminazione animale |
| `/api/colture` | GET, POST | Gestione colture |
| `/api/colture/<id>` | DELETE | Eliminazione coltura |
| `/api/personale` | GET, POST | Gestione personale |
| `/api/personale/<id>` | DELETE | Eliminazione personale |
| `/api/magazzino` | GET, POST | Gestione magazzino |
| `/api/magazzino/<id>` | DELETE | Eliminazione prodotto |
| `/api/manutenzioni` | GET, POST | Gestione manutenzioni |
| `/api/manutenzioni/<id>` | DELETE | Eliminazione manutenzione |
| `/api/finanze` | GET, POST | Gestione finanze |
| `/api/finanze/<id>` | DELETE | Eliminazione operazione |
| `/api/stats` | GET | Statistiche aggregate |

### 2.3 Data Layer (Database)

**Tecnologia**: SQLite 3

**Motivazione della scelta**:
- Zero configurazione
- File-based (facile backup)
- ACID compliant
- Adeguato per applicazioni single-tenant
- Supporto transazioni
- Basso overhead

**Schema del Database**:

#### Tabella: numbers
```sql
id                  INTEGER PRIMARY KEY AUTOINCREMENT
value               REAL NOT NULL
created_at          TIMESTAMP DEFAULT CURRENT_TIMESTAMP
```

#### Tabella: terreni
```sql
id                  INTEGER PRIMARY KEY AUTOINCREMENT
nome                VARCHAR(100) NOT NULL
superficie_ettari   REAL
tipo_terreno        VARCHAR(50)
ubicazione          VARCHAR(200)
foglio              VARCHAR(20)
particella          VARCHAR(20)
subalterno          VARCHAR(20)
geometria           TEXT (JSON GeoJSON)
note                TEXT
created_at          TIMESTAMP DEFAULT CURRENT_TIMESTAMP
```

#### Tabella: trattori
```sql
id                  INTEGER PRIMARY KEY AUTOINCREMENT
marca               VARCHAR(50) NOT NULL
modello             VARCHAR(50) NOT NULL
anno                INTEGER
targa               VARCHAR(20)
numero_telaio       VARCHAR(50)
potenza_cv          INTEGER
ore_lavoro          INTEGER DEFAULT 0
data_acquisto       DATE
costo_acquisto      REAL
stato               VARCHAR(20) DEFAULT 'Operativo'
note                TEXT
created_at          TIMESTAMP DEFAULT CURRENT_TIMESTAMP
```

#### Tabella: attrezzi
```sql
id                  INTEGER PRIMARY KEY AUTOINCREMENT
nome                VARCHAR(100) NOT NULL
tipo                VARCHAR(50)
marca               VARCHAR(50)
modello             VARCHAR(50)
anno_acquisto       INTEGER
costo_acquisto      REAL
stato               VARCHAR(20) DEFAULT 'Buono'
ultima_manutenzione DATE
note                TEXT
created_at          TIMESTAMP DEFAULT CURRENT_TIMESTAMP
```

#### Tabella: animali
```sql
id                  INTEGER PRIMARY KEY AUTOINCREMENT
specie              VARCHAR(50) NOT NULL
razza               VARCHAR(50)
identificativo      VARCHAR(50)
data_nascita        DATE
sesso               VARCHAR(10)
peso_kg             REAL
stato_salute        VARCHAR(50) DEFAULT 'Sano'
padre_id            INTEGER (FK -> animali.id)
madre_id            INTEGER (FK -> animali.id)
note                TEXT
created_at          TIMESTAMP DEFAULT CURRENT_TIMESTAMP
```

#### Tabella: colture
```sql
id                      INTEGER PRIMARY KEY AUTOINCREMENT
terreno_id              INTEGER NOT NULL (FK -> terreni.id)
tipo_coltura            VARCHAR(100) NOT NULL
varieta                 VARCHAR(100)
data_semina             DATE
data_raccolta_prevista  DATE
data_raccolta_effettiva DATE
quantita_raccolta_kg    REAL
stato                   VARCHAR(50) DEFAULT 'In corso'
note                    TEXT
created_at              TIMESTAMP DEFAULT CURRENT_TIMESTAMP
```

#### Tabella: personale
```sql
id                      INTEGER PRIMARY KEY AUTOINCREMENT
nome                    VARCHAR(50) NOT NULL
cognome                 VARCHAR(50) NOT NULL
ruolo                   VARCHAR(50)
telefono                VARCHAR(20)
email                   VARCHAR(100)
data_assunzione         DATE
tipo_contratto          VARCHAR(50)
retribuzione_mensile    REAL
note                    TEXT
created_at              TIMESTAMP DEFAULT CURRENT_TIMESTAMP
```

#### Tabella: magazzino
```sql
id                  INTEGER PRIMARY KEY AUTOINCREMENT
categoria           VARCHAR(50) NOT NULL
nome_prodotto       VARCHAR(100) NOT NULL
marca               VARCHAR(50)
quantita            REAL NOT NULL
unita_misura        VARCHAR(20)
data_acquisto       DATE
costo_unitario      REAL
scadenza            DATE
fornitore           VARCHAR(100)
note                TEXT
created_at          TIMESTAMP DEFAULT CURRENT_TIMESTAMP
```

#### Tabella: manutenzioni
```sql
id                      INTEGER PRIMARY KEY AUTOINCREMENT
tipo_oggetto            VARCHAR(50) NOT NULL
oggetto_id              INTEGER NOT NULL
data_manutenzione       DATE NOT NULL
tipo_manutenzione       VARCHAR(50)
descrizione             TEXT
costo                   REAL
eseguita_da             VARCHAR(100)
prossima_manutenzione   DATE
note                    TEXT
created_at              TIMESTAMP DEFAULT CURRENT_TIMESTAMP
```

#### Tabella: finanze
```sql
id                  INTEGER PRIMARY KEY AUTOINCREMENT
tipo                VARCHAR(20) NOT NULL (Spesa/Ricavo)
categoria           VARCHAR(50) NOT NULL
descrizione         TEXT NOT NULL
importo             REAL NOT NULL
data_operazione     DATE NOT NULL
metodo_pagamento    VARCHAR(50)
riferimento         VARCHAR(100)
note                TEXT
created_at          TIMESTAMP DEFAULT CURRENT_TIMESTAMP
```

**Relazioni tra tabelle**:
- `colture.terreno_id` → `terreni.id` (Many-to-One)
- `animali.padre_id` → `animali.id` (Self-referencing)
- `animali.madre_id` → `animali.id` (Self-referencing)

---

## 3. DEPLOYMENT ARCHITECTURE

### 3.1 Containerizzazione

**Docker Multi-Stage Build**:

```dockerfile
# Stage 1: Builder (non utilizzato in questo caso, ma struttura pronta)
FROM python:3.9-slim

# Stage 2: Runtime
- Base image: python:3.9-slim
- Working directory: /app
- Non-root user: appuser (UID 1000)
- Exposed port: 5000
- Volume mount: /data (per persistenza database)
```

**Vantaggi**:
- Immagine ottimizzata (~150MB)
- Sicurezza: esecuzione come utente non-root
- Portabilità: funziona su qualsiasi piattaforma con Docker
- Isolamento: ambiente controllato e riproducibile

### 3.2 Docker Compose

**Configurazione per sviluppo locale**:
```yaml
services:
  web:
    build: .
    ports: 5000:5000
    volumes:
      - farm_data:/data
    environment:
      - DATA_DIR=/data
      - FLASK_ENV=development
```

**Volume persistente**: `farm_data` per database SQLite

### 3.3 Deployment su Render.com

**Configurazione (render.yaml)**:
- Tipo: Web Service
- Build: Docker
- Health check: `/health` endpoint
- Disco persistente: 1GB montato su `/data`
- Auto-deploy: Trigger su push a branch `main`

**Architettura Cloud**:
```
GitHub Repository
        ↓
   Git Push (main)
        ↓
Render.com Build Service
        ↓
   Docker Build
        ↓
Container Registry
        ↓
Production Instance
        ↓
Persistent Disk (1GB)
```

---

## 4. FLUSSI DI DATI

### 4.1 Flusso di Lettura (GET)

```
Browser → HTTP GET /api/terreni
              ↓
        Flask Route Handler
              ↓
        get_db_connection()
              ↓
        SQLite Query (SELECT)
              ↓
        Row Factory (dict conversion)
              ↓
        JSON Response
              ↓
        Browser (JavaScript Fetch)
              ↓
        DOM Update
```

### 4.2 Flusso di Scrittura (POST)

```
Browser → Form Submit
              ↓
    JavaScript Fetch (POST)
              ↓
    JSON Payload
              ↓
    Flask Route Handler
              ↓
    Input Validation
              ↓
    get_db_connection()
              ↓
    SQLite INSERT/UPDATE
              ↓
    Commit Transaction
              ↓
    JSON Response (success/error)
              ↓
    Browser Feedback
```

### 4.3 Flusso di Eliminazione (DELETE)

```
Browser → Delete Button Click
              ↓
    Confirmation Dialog
              ↓
    Fetch DELETE /api/resource/<id>
              ↓
    Flask Route Handler
              ↓
    SQLite DELETE WHERE id = ?
              ↓
    Commit Transaction
              ↓
    JSON Response
              ↓
    DOM Update (remove element)
```

---

## 5. GESTIONE DELLO STATO

### 5.1 Stato Applicazione
- **Stateless backend**: Ogni richiesta è indipendente
- **Stato nel database**: Persistenza completa in SQLite
- **No sessioni utente**: Attualmente single-user (no autenticazione)

### 5.2 Transazioni Database
- **ACID Compliance**: Garantito da SQLite
- **Connection pooling**: Una connessione per richiesta
- **Auto-commit**: Commit esplicito dopo ogni operazione di scrittura

---

## 6. CONSIDERAZIONI SULLE PERFORMANCE

### 6.1 Ottimizzazioni Attuali
- Query indicizzate su PRIMARY KEY
- Connessioni database chiuse dopo ogni operazione
- Asset statici serviti direttamente da Flask
- Minimal JavaScript framework (no overhead)

### 6.2 Limiti Identificati
- **Concorrenza**: SQLite ha limiti su scritture concorrenti
- **Scalabilità orizzontale**: Non supportata (monolitico)
- **Cache**: Nessuna cache implementata

### 6.3 Raccomandazioni per Scaling
Per carichi elevati (>1000 utenti concorrenti):
- Migrazione a PostgreSQL/MySQL
- Implementazione di Redis per caching
- Load balancing con multiple istanze
- Separazione frontend/backend (microservices)

---

## 7. MONITORING E LOGGING

### 7.1 Health Check
**Endpoint**: `/health`

**Funzionalità**:
- Verifica connettività database
- Test query SELECT
- Response JSON con status

**Utilizzo**:
- Render.com health checks
- Monitoring esterno (UptimeRobot, Pingdom)
- CI/CD pipeline verification

### 7.2 Logging
**Attuale**:
- Flask default logging (console output)
- Docker logs capture

**Raccomandazioni**:
- Implementare logging strutturato (JSON)
- Livelli: DEBUG, INFO, WARNING, ERROR, CRITICAL
- Rotazione log files
- Integrazione con servizi esterni (Sentry, LogRocket)

---

## 8. DISASTER RECOVERY E BACKUP

### 8.1 Strategia di Backup
**Database**:
- File singolo: `farm_management.db`
- Backup manuale: copia file
- Backup automatico: script cron/systemd timer

**Frequenza raccomandata**:
- Giornaliera: backup incrementale
- Settimanale: backup completo
- Mensile: backup archiviato long-term

### 8.2 Recovery Procedure
1. Stop applicazione
2. Replace database file
3. Verificare integrità (PRAGMA integrity_check)
4. Restart applicazione
5. Verificare funzionamento

**RTO (Recovery Time Objective)**: < 5 minuti
**RPO (Recovery Point Objective)**: 24 ore (con backup giornaliero)

---

## 9. DIPENDENZE E STACK TECNOLOGICO

### 9.1 Runtime Dependencies

```
Flask>=2.0.0          # Web framework
Werkzeug>=2.0.0       # WSGI utilities
Jinja2>=3.0.0         # Template engine
click>=8.0.0          # CLI utilities
itsdangerous>=2.0.0   # Security helpers
MarkupSafe>=2.0.0     # String handling
```

### 9.2 Development Dependencies
```
flake8                # Linting
bandit                # Security linting
safety                # Dependency vulnerability check
pytest                # Testing (da implementare)
```

### 9.3 Infrastructure
```
Docker>=20.10
Docker Compose>=1.29
Python 3.9+
SQLite 3.31+
```

---

## 10. EVOLUZIONE ARCHITETTURALE

### 10.1 Fase Attuale: Monolith v1.0
- Applicazione monolitica
- Single-user
- File-based database
- Deployment containerizzato

### 10.2 Fase Futura: Multi-tenant v2.0
**Modifiche previste**:
- Sistema di autenticazione (JWT/OAuth2)
- Multi-tenancy con isolamento dati
- Migrazione a PostgreSQL
- API REST completamente documentata (OpenAPI)
- Frontend SPA React/Vue.js separato
- Microservices per moduli critici

### 10.3 Fase Avanzata: Cloud-Native v3.0
**Architettura target**:
- Kubernetes deployment
- Service mesh (Istio)
- Message queue (RabbitMQ/Kafka)
- Cache distribuita (Redis Cluster)
- Object storage (S3) per file/immagini
- Serverless functions per task asincroni
- GraphQL API layer

---

## 11. CONFORMITÀ E STANDARD

### 11.1 Standard Seguiti
- **REST API**: Principi RESTful per endpoint API
- **HTTP Status Codes**: Utilizzo corretto di 200, 400, 500
- **JSON**: Formato standard per API responses
- **Semantic Versioning**: Per versioning applicazione
- **12-Factor App**: Parziale (config via env, stateless process)

### 11.2 Best Practices
- Separation of Concerns (MVC-like pattern)
- DRY (Don't Repeat Yourself)
- Single Responsibility Principle
- Database normalization (3NF)

---

## 12. DIAGRAMMI ARCHITETTURALI

### 12.1 Architettura Generale

```
┌─────────────────────────────────────────────┐
│           CLIENT LAYER                       │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  │
│  │ Browser  │  │  Mobile  │  │   API    │  │
│  │   Web    │  │  Device  │  │  Client  │  │
│  └──────────┘  └──────────┘  └──────────┘  │
└──────────────────┬──────────────────────────┘
                   │ HTTPS
┌──────────────────▼──────────────────────────┐
│        APPLICATION LAYER (Flask)             │
│  ┌────────────────────────────────────────┐ │
│  │         Route Handlers                 │ │
│  │  /api/terreni  /api/trattori  etc.    │ │
│  └────────────────┬───────────────────────┘ │
│  ┌────────────────▼───────────────────────┐ │
│  │       Business Logic Layer             │ │
│  │   CRUD Operations + Validations        │ │
│  └────────────────┬───────────────────────┘ │
└───────────────────┼─────────────────────────┘
┌───────────────────▼─────────────────────────┐
│         DATA LAYER (SQLite)                  │
│  ┌──────────────────────────────────────┐  │
│  │     farm_management.db               │  │
│  │  ┌────────┐ ┌────────┐ ┌─────────┐  │  │
│  │  │terreni │ │trattori│ │ animali │  │  │
│  │  └────────┘ └────────┘ └─────────┘  │  │
│  │  ┌────────┐ ┌────────┐ ┌─────────┐  │  │
│  │  │colture │ │finanze │ │  etc.   │  │  │
│  │  └────────┘ └────────┘ └─────────┘  │  │
│  └──────────────────────────────────────┘  │
└─────────────────────────────────────────────┘
```

### 12.2 Deployment Architecture

```
┌───────────────────────────────────────────┐
│         RENDER.COM CLOUD                  │
│  ┌─────────────────────────────────────┐ │
│  │    Docker Container                 │ │
│  │  ┌───────────────────────────────┐  │ │
│  │  │  Flask App (Port 5000)        │  │ │
│  │  │  User: appuser (non-root)     │  │ │
│  │  └───────────────────────────────┘  │ │
│  │  ┌───────────────────────────────┐  │ │
│  │  │  Persistent Volume (/data)    │  │ │
│  │  │  farm_management.db (1GB)     │  │ │
│  │  └───────────────────────────────┘  │ │
│  └─────────────────────────────────────┘ │
│                                           │
│  ┌─────────────────────────────────────┐ │
│  │     Load Balancer / HTTPS           │ │
│  │     SSL Certificate (Auto)          │ │
│  └─────────────────────────────────────┘ │
└───────────────────────────────────────────┘
                    ▲
                    │ HTTPS
┌───────────────────┴───────────────────────┐
│              INTERNET                      │
└───────────────────┬───────────────────────┘
                    ▼
            ┌───────────────┐
            │  End Users    │
            └───────────────┘
```

---

## APPENDICE A: GLOSSARIO

- **3-Tier Architecture**: Architettura a tre livelli (presentation, application, data)
- **ACID**: Atomicity, Consistency, Isolation, Durability
- **CRUD**: Create, Read, Update, Delete
- **ORM**: Object-Relational Mapping (non utilizzato in questo progetto)
- **REST**: Representational State Transfer
- **RTO**: Recovery Time Objective
- **RPO**: Recovery Point Objective
- **SPA**: Single Page Application

---

**Documento compilato da**: Sistema di documentazione automatica
**Ultima revisione**: Gennaio 2025
**Revisione**: 1.0
