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
