from flask import Flask, render_template, request, jsonify
import sqlite3
from datetime import datetime
import os

app = Flask(__name__)

# Database path - use /data in production for volume persistence
DATA_DIR = os.getenv('DATA_DIR', '.')
DATABASE = os.path.join(DATA_DIR, 'farm_management.db')

def get_db_connection():
    """Create a database connection"""
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """Initialize the database with all necessary tables"""
    conn = get_db_connection()

    # Numbers table (original app)
    conn.execute('''
        CREATE TABLE IF NOT EXISTS numbers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            value REAL NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    # Farm management tables

    # Terreni/Appezzamenti
    conn.execute('''
        CREATE TABLE IF NOT EXISTS terreni (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome VARCHAR(100) NOT NULL,
            superficie_ettari REAL NOT NULL,
            tipo_terreno VARCHAR(50),
            ubicazione VARCHAR(200),
            foglio VARCHAR(20),
            particella VARCHAR(20),
            subalterno VARCHAR(20),
            note TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    # Trattori e Mezzi
    conn.execute('''
        CREATE TABLE IF NOT EXISTS trattori (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            marca VARCHAR(50) NOT NULL,
            modello VARCHAR(50) NOT NULL,
            anno INTEGER,
            targa VARCHAR(20),
            numero_telaio VARCHAR(50),
            potenza_cv INTEGER,
            ore_lavoro INTEGER DEFAULT 0,
            data_acquisto DATE,
            costo_acquisto REAL,
            stato VARCHAR(20) DEFAULT 'Operativo',
            note TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    # Attrezzi e Attrezzature
    conn.execute('''
        CREATE TABLE IF NOT EXISTS attrezzi (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome VARCHAR(100) NOT NULL,
            tipo VARCHAR(50),
            marca VARCHAR(50),
            modello VARCHAR(50),
            anno_acquisto INTEGER,
            costo_acquisto REAL,
            stato VARCHAR(20) DEFAULT 'Buono',
            ultima_manutenzione DATE,
            note TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    # Animali e Bestiame
    conn.execute('''
        CREATE TABLE IF NOT EXISTS animali (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            specie VARCHAR(50) NOT NULL,
            razza VARCHAR(50),
            identificativo VARCHAR(50),
            data_nascita DATE,
            sesso VARCHAR(10),
            peso_kg REAL,
            stato_salute VARCHAR(50) DEFAULT 'Sano',
            padre_id INTEGER,
            madre_id INTEGER,
            note TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (padre_id) REFERENCES animali(id),
            FOREIGN KEY (madre_id) REFERENCES animali(id)
        )
    ''')

    # Colture
    conn.execute('''
        CREATE TABLE IF NOT EXISTS colture (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            terreno_id INTEGER NOT NULL,
            tipo_coltura VARCHAR(100) NOT NULL,
            varieta VARCHAR(100),
            data_semina DATE,
            data_raccolta_prevista DATE,
            data_raccolta_effettiva DATE,
            quantita_raccolta_kg REAL,
            stato VARCHAR(50) DEFAULT 'In corso',
            note TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (terreno_id) REFERENCES terreni(id)
        )
    ''')

    # Personale/Dipendenti
    conn.execute('''
        CREATE TABLE IF NOT EXISTS personale (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome VARCHAR(50) NOT NULL,
            cognome VARCHAR(50) NOT NULL,
            ruolo VARCHAR(50),
            telefono VARCHAR(20),
            email VARCHAR(100),
            data_assunzione DATE,
            tipo_contratto VARCHAR(50),
            retribuzione_mensile REAL,
            note TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    # Magazzino (sementi, fertilizzanti, fitofarmaci)
    conn.execute('''
        CREATE TABLE IF NOT EXISTS magazzino (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            categoria VARCHAR(50) NOT NULL,
            nome_prodotto VARCHAR(100) NOT NULL,
            marca VARCHAR(50),
            quantita REAL NOT NULL,
            unita_misura VARCHAR(20),
            data_acquisto DATE,
            costo_unitario REAL,
            scadenza DATE,
            fornitore VARCHAR(100),
            note TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    # Manutenzioni
    conn.execute('''
        CREATE TABLE IF NOT EXISTS manutenzioni (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            tipo_oggetto VARCHAR(50) NOT NULL,
            oggetto_id INTEGER NOT NULL,
            data_manutenzione DATE NOT NULL,
            tipo_manutenzione VARCHAR(50),
            descrizione TEXT,
            costo REAL,
            eseguita_da VARCHAR(100),
            prossima_manutenzione DATE,
            note TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    # Finanze (Spese e Ricavi)
    conn.execute('''
        CREATE TABLE IF NOT EXISTS finanze (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            tipo VARCHAR(20) NOT NULL,
            categoria VARCHAR(50) NOT NULL,
            descrizione TEXT NOT NULL,
            importo REAL NOT NULL,
            data_operazione DATE NOT NULL,
            metodo_pagamento VARCHAR(50),
            riferimento VARCHAR(100),
            note TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    conn.commit()
    conn.close()

# ============= ROUTES MENU =============

@app.route('/')
def menu():
    """Render the main menu page"""
    return render_template('menu.html')

@app.route('/health')
def health():
    """Health check endpoint for monitoring"""
    try:
        # Test database connectivity
        conn = get_db_connection()
        conn.execute('SELECT 1').fetchone()
        conn.close()
        return jsonify({'status': 'healthy', 'database': 'connected'}), 200
    except Exception as e:
        return jsonify({'status': 'unhealthy', 'error': str(e)}), 500

# ============= ROUTES NUMBER APP =============

@app.route('/numbers')
def numbers_index():
    """Render the numbers storage page"""
    conn = get_db_connection()
    numbers = conn.execute('SELECT * FROM numbers ORDER BY created_at DESC').fetchall()
    conn.close()
    return render_template('index.html', numbers=numbers)

@app.route('/add', methods=['POST'])
def add_number():
    """Add a number to the database"""
    data = request.get_json()
    number = data.get('number')

    if number is None or number == '':
        return jsonify({'error': 'Number is required'}), 400

    try:
        number = float(number)
    except ValueError:
        return jsonify({'error': 'Invalid number format'}), 400

    conn = get_db_connection()
    conn.execute('INSERT INTO numbers (value) VALUES (?)', (number,))
    conn.commit()
    conn.close()

    return jsonify({'success': True, 'message': 'Number stored successfully'})

@app.route('/delete/<int:id>', methods=['DELETE'])
def delete_number(id):
    """Delete a number from the database"""
    conn = get_db_connection()
    conn.execute('DELETE FROM numbers WHERE id = ?', (id,))
    conn.commit()
    conn.close()

    return jsonify({'success': True, 'message': 'Number deleted successfully'})

# ============= ROUTES FARM MANAGEMENT =============

@app.route('/farm')
def farm_index():
    """Render the farm management main page"""
    return render_template('farm.html')

# ===== TERRENI ROUTES =====

@app.route('/api/terreni', methods=['GET'])
def get_terreni():
    conn = get_db_connection()
    terreni = conn.execute('SELECT * FROM terreni ORDER BY created_at DESC').fetchall()
    conn.close()
    return jsonify([dict(t) for t in terreni])

@app.route('/api/terreni', methods=['POST'])
def add_terreno():
    data = request.get_json()
    conn = get_db_connection()
    conn.execute('''INSERT INTO terreni
        (nome, superficie_ettari, tipo_terreno, ubicazione, foglio, particella, subalterno, note)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)''',
        (data['nome'], data['superficie_ettari'], data.get('tipo_terreno'),
         data.get('ubicazione'), data.get('foglio'), data.get('particella'),
         data.get('subalterno'), data.get('note')))
    conn.commit()
    conn.close()
    return jsonify({'success': True, 'message': 'Terreno aggiunto con successo'})

@app.route('/api/terreni/<int:id>', methods=['DELETE'])
def delete_terreno(id):
    conn = get_db_connection()
    conn.execute('DELETE FROM terreni WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    return jsonify({'success': True, 'message': 'Terreno eliminato con successo'})

# ===== TRATTORI ROUTES =====

@app.route('/api/trattori', methods=['GET'])
def get_trattori():
    conn = get_db_connection()
    trattori = conn.execute('SELECT * FROM trattori ORDER BY created_at DESC').fetchall()
    conn.close()
    return jsonify([dict(t) for t in trattori])

@app.route('/api/trattori', methods=['POST'])
def add_trattore():
    data = request.get_json()
    conn = get_db_connection()
    conn.execute('''INSERT INTO trattori
        (marca, modello, anno, targa, numero_telaio, potenza_cv, ore_lavoro,
         data_acquisto, costo_acquisto, stato, note)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
        (data['marca'], data['modello'], data.get('anno'), data.get('targa'),
         data.get('numero_telaio'), data.get('potenza_cv'), data.get('ore_lavoro', 0),
         data.get('data_acquisto'), data.get('costo_acquisto'),
         data.get('stato', 'Operativo'), data.get('note')))
    conn.commit()
    conn.close()
    return jsonify({'success': True, 'message': 'Trattore aggiunto con successo'})

@app.route('/api/trattori/<int:id>', methods=['DELETE'])
def delete_trattore(id):
    conn = get_db_connection()
    conn.execute('DELETE FROM trattori WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    return jsonify({'success': True, 'message': 'Trattore eliminato con successo'})

# ===== ATTREZZI ROUTES =====

@app.route('/api/attrezzi', methods=['GET'])
def get_attrezzi():
    conn = get_db_connection()
    attrezzi = conn.execute('SELECT * FROM attrezzi ORDER BY created_at DESC').fetchall()
    conn.close()
    return jsonify([dict(a) for a in attrezzi])

@app.route('/api/attrezzi', methods=['POST'])
def add_attrezzo():
    data = request.get_json()
    conn = get_db_connection()
    conn.execute('''INSERT INTO attrezzi
        (nome, tipo, marca, modello, anno_acquisto, costo_acquisto, stato, ultima_manutenzione, note)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)''',
        (data['nome'], data.get('tipo'), data.get('marca'), data.get('modello'),
         data.get('anno_acquisto'), data.get('costo_acquisto'),
         data.get('stato', 'Buono'), data.get('ultima_manutenzione'), data.get('note')))
    conn.commit()
    conn.close()
    return jsonify({'success': True, 'message': 'Attrezzo aggiunto con successo'})

@app.route('/api/attrezzi/<int:id>', methods=['DELETE'])
def delete_attrezzo(id):
    conn = get_db_connection()
    conn.execute('DELETE FROM attrezzi WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    return jsonify({'success': True, 'message': 'Attrezzo eliminato con successo'})

# ===== ANIMALI ROUTES =====

@app.route('/api/animali', methods=['GET'])
def get_animali():
    conn = get_db_connection()
    animali = conn.execute('SELECT * FROM animali ORDER BY created_at DESC').fetchall()
    conn.close()
    return jsonify([dict(a) for a in animali])

@app.route('/api/animali', methods=['POST'])
def add_animale():
    data = request.get_json()
    conn = get_db_connection()
    conn.execute('''INSERT INTO animali
        (specie, razza, identificativo, data_nascita, sesso, peso_kg,
         stato_salute, padre_id, madre_id, note)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
        (data['specie'], data.get('razza'), data.get('identificativo'),
         data.get('data_nascita'), data.get('sesso'), data.get('peso_kg'),
         data.get('stato_salute', 'Sano'), data.get('padre_id'),
         data.get('madre_id'), data.get('note')))
    conn.commit()
    conn.close()
    return jsonify({'success': True, 'message': 'Animale aggiunto con successo'})

@app.route('/api/animali/<int:id>', methods=['DELETE'])
def delete_animale(id):
    conn = get_db_connection()
    conn.execute('DELETE FROM animali WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    return jsonify({'success': True, 'message': 'Animale eliminato con successo'})

# ===== COLTURE ROUTES =====

@app.route('/api/colture', methods=['GET'])
def get_colture():
    conn = get_db_connection()
    colture = conn.execute('''
        SELECT c.*, t.nome as nome_terreno
        FROM colture c
        LEFT JOIN terreni t ON c.terreno_id = t.id
        ORDER BY c.created_at DESC
    ''').fetchall()
    conn.close()
    return jsonify([dict(c) for c in colture])

@app.route('/api/colture', methods=['POST'])
def add_coltura():
    data = request.get_json()
    conn = get_db_connection()
    conn.execute('''INSERT INTO colture
        (terreno_id, tipo_coltura, varieta, data_semina, data_raccolta_prevista,
         data_raccolta_effettiva, quantita_raccolta_kg, stato, note)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)''',
        (data['terreno_id'], data['tipo_coltura'], data.get('varieta'),
         data.get('data_semina'), data.get('data_raccolta_prevista'),
         data.get('data_raccolta_effettiva'), data.get('quantita_raccolta_kg'),
         data.get('stato', 'In corso'), data.get('note')))
    conn.commit()
    conn.close()
    return jsonify({'success': True, 'message': 'Coltura aggiunta con successo'})

@app.route('/api/colture/<int:id>', methods=['DELETE'])
def delete_coltura(id):
    conn = get_db_connection()
    conn.execute('DELETE FROM colture WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    return jsonify({'success': True, 'message': 'Coltura eliminata con successo'})

# ===== PERSONALE ROUTES =====

@app.route('/api/personale', methods=['GET'])
def get_personale():
    conn = get_db_connection()
    personale = conn.execute('SELECT * FROM personale ORDER BY cognome, nome').fetchall()
    conn.close()
    return jsonify([dict(p) for p in personale])

@app.route('/api/personale', methods=['POST'])
def add_personale():
    data = request.get_json()
    conn = get_db_connection()
    conn.execute('''INSERT INTO personale
        (nome, cognome, ruolo, telefono, email, data_assunzione,
         tipo_contratto, retribuzione_mensile, note)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)''',
        (data['nome'], data['cognome'], data.get('ruolo'), data.get('telefono'),
         data.get('email'), data.get('data_assunzione'), data.get('tipo_contratto'),
         data.get('retribuzione_mensile'), data.get('note')))
    conn.commit()
    conn.close()
    return jsonify({'success': True, 'message': 'Dipendente aggiunto con successo'})

@app.route('/api/personale/<int:id>', methods=['DELETE'])
def delete_personale(id):
    conn = get_db_connection()
    conn.execute('DELETE FROM personale WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    return jsonify({'success': True, 'message': 'Dipendente eliminato con successo'})

# ===== MAGAZZINO ROUTES =====

@app.route('/api/magazzino', methods=['GET'])
def get_magazzino():
    conn = get_db_connection()
    magazzino = conn.execute('SELECT * FROM magazzino ORDER BY categoria, nome_prodotto').fetchall()
    conn.close()
    return jsonify([dict(m) for m in magazzino])

@app.route('/api/magazzino', methods=['POST'])
def add_magazzino():
    data = request.get_json()
    conn = get_db_connection()
    conn.execute('''INSERT INTO magazzino
        (categoria, nome_prodotto, marca, quantita, unita_misura, data_acquisto,
         costo_unitario, scadenza, fornitore, note)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
        (data['categoria'], data['nome_prodotto'], data.get('marca'), data['quantita'],
         data.get('unita_misura'), data.get('data_acquisto'), data.get('costo_unitario'),
         data.get('scadenza'), data.get('fornitore'), data.get('note')))
    conn.commit()
    conn.close()
    return jsonify({'success': True, 'message': 'Prodotto aggiunto con successo'})

@app.route('/api/magazzino/<int:id>', methods=['DELETE'])
def delete_magazzino(id):
    conn = get_db_connection()
    conn.execute('DELETE FROM magazzino WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    return jsonify({'success': True, 'message': 'Prodotto eliminato con successo'})

# ===== MANUTENZIONI ROUTES =====

@app.route('/api/manutenzioni', methods=['GET'])
def get_manutenzioni():
    conn = get_db_connection()
    manutenzioni = conn.execute('SELECT * FROM manutenzioni ORDER BY data_manutenzione DESC').fetchall()
    conn.close()
    return jsonify([dict(m) for m in manutenzioni])

@app.route('/api/manutenzioni', methods=['POST'])
def add_manutenzione():
    data = request.get_json()
    conn = get_db_connection()
    conn.execute('''INSERT INTO manutenzioni
        (tipo_oggetto, oggetto_id, data_manutenzione, tipo_manutenzione,
         descrizione, costo, eseguita_da, prossima_manutenzione, note)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)''',
        (data['tipo_oggetto'], data['oggetto_id'], data['data_manutenzione'],
         data.get('tipo_manutenzione'), data.get('descrizione'), data.get('costo'),
         data.get('eseguita_da'), data.get('prossima_manutenzione'), data.get('note')))
    conn.commit()
    conn.close()
    return jsonify({'success': True, 'message': 'Manutenzione registrata con successo'})

@app.route('/api/manutenzioni/<int:id>', methods=['DELETE'])
def delete_manutenzione(id):
    conn = get_db_connection()
    conn.execute('DELETE FROM manutenzioni WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    return jsonify({'success': True, 'message': 'Manutenzione eliminata con successo'})

# ===== FINANZE ROUTES =====

@app.route('/api/finanze', methods=['GET'])
def get_finanze():
    conn = get_db_connection()
    finanze = conn.execute('SELECT * FROM finanze ORDER BY data_operazione DESC').fetchall()
    conn.close()
    return jsonify([dict(f) for f in finanze])

@app.route('/api/finanze', methods=['POST'])
def add_finanza():
    data = request.get_json()
    conn = get_db_connection()
    conn.execute('''INSERT INTO finanze
        (tipo, categoria, descrizione, importo, data_operazione,
         metodo_pagamento, riferimento, note)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)''',
        (data['tipo'], data['categoria'], data['descrizione'], data['importo'],
         data['data_operazione'], data.get('metodo_pagamento'),
         data.get('riferimento'), data.get('note')))
    conn.commit()
    conn.close()
    return jsonify({'success': True, 'message': 'Operazione registrata con successo'})

@app.route('/api/finanze/<int:id>', methods=['DELETE'])
def delete_finanza(id):
    conn = get_db_connection()
    conn.execute('DELETE FROM finanze WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    return jsonify({'success': True, 'message': 'Operazione eliminata con successo'})

# ===== STATISTICS ROUTES =====

@app.route('/api/stats', methods=['GET'])
def get_stats():
    conn = get_db_connection()

    stats = {
        'terreni_count': conn.execute('SELECT COUNT(*) as count FROM terreni').fetchone()['count'],
        'terreni_superficie': conn.execute('SELECT COALESCE(SUM(superficie_ettari), 0) as sum FROM terreni').fetchone()['sum'],
        'trattori_count': conn.execute('SELECT COUNT(*) as count FROM trattori').fetchone()['count'],
        'attrezzi_count': conn.execute('SELECT COUNT(*) as count FROM attrezzi').fetchone()['count'],
        'animali_count': conn.execute('SELECT COUNT(*) as count FROM animali').fetchone()['count'],
        'colture_attive': conn.execute("SELECT COUNT(*) as count FROM colture WHERE stato = 'In corso'").fetchone()['count'],
        'personale_count': conn.execute('SELECT COUNT(*) as count FROM personale').fetchone()['count'],
        'spese_totali': conn.execute("SELECT COALESCE(SUM(importo), 0) as sum FROM finanze WHERE tipo = 'Spesa'").fetchone()['sum'],
        'ricavi_totali': conn.execute("SELECT COALESCE(SUM(importo), 0) as sum FROM finanze WHERE tipo = 'Ricavo'").fetchone()['sum']
    }

    conn.close()
    return jsonify(stats)

if __name__ == '__main__':
    init_db()
    app.run(debug=True, host='0.0.0.0', port=5000)
