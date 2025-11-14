#!/bin/bash

# Get port from environment or use default
PORT=${PORT:-5000}

echo "Starting application on port $PORT"
echo "Data directory: $DATA_DIR"

# Ensure data directory exists and has correct permissions
mkdir -p $DATA_DIR
touch $DATA_DIR/farm_management.db
chmod 777 $DATA_DIR
chmod 666 $DATA_DIR/farm_management.db 2>/dev/null || true

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
