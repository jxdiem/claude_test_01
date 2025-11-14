from flask import Flask, render_template, request, jsonify
import sqlite3
from datetime import datetime
import os

app = Flask(__name__)
DATABASE = 'numbers.db'

def get_db_connection():
    """Create a database connection"""
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """Initialize the database with the numbers table"""
    conn = get_db_connection()
    conn.execute('''
        CREATE TABLE IF NOT EXISTS numbers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            value REAL NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

@app.route('/')
def index():
    """Render the main page"""
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

if __name__ == '__main__':
    init_db()
    app.run(debug=True, host='0.0.0.0', port=5000)
