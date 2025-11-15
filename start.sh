#!/bin/bash

# Get port from environment or use default
PORT=${PORT:-5000}

echo "Starting application on port $PORT"
echo "Data directory: $DATA_DIR"

# Ensure data directory exists
mkdir -p $DATA_DIR

# Initialize database (create tables if they don't exist)
echo "Initializing database..."
python -c "from app import init_db; init_db()"
echo "Database initialized!"

# Run migrations (add missing columns)
echo "Running database migrations..."
python -c "
import sqlite3
import os

DATABASE = os.path.join(os.getenv('DATA_DIR', '.'), 'farm_management.db')
conn = sqlite3.connect(DATABASE)

# Check if geometria column exists, if not add it
try:
    cursor = conn.cursor()
    cursor.execute('PRAGMA table_info(terreni)')
    columns = [row[1] for row in cursor.fetchall()]

    if 'geometria' not in columns:
        print('Adding geometria column to terreni table...')
        cursor.execute('ALTER TABLE terreni ADD COLUMN geometria TEXT')
        conn.commit()
        print('✅ Column geometria added successfully')
    else:
        print('✅ Column geometria already exists')

except Exception as e:
    print(f'Migration error: {e}')
finally:
    conn.close()
"
echo "Migrations completed!"

# Start gunicorn
exec gunicorn \
    --bind 0.0.0.0:$PORT \
    --workers 2 \
    --threads 4 \
    --timeout 60 \
    --access-logfile - \
    --error-logfile - \
    --log-level info \
    app:app
