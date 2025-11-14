#!/bin/bash

# Get port from environment or use default
PORT=${PORT:-5000}

echo "Starting application on port $PORT"
echo "Data directory: $DATA_DIR"

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
