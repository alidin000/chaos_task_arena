#!/bin/bash

# 💥 Chaos Arena Launcher

# Start Redis in background if not running
if ! pgrep -x "redis-server" > /dev/null; then
    echo "🔁 Starting Redis..."
    redis-server --daemonize yes
    if [ $? -ne 0 ]; then
        echo "❌ Failed to start Redis. Exiting."
        exit 1
    fi
else
    echo "✅ Redis is already running."
fi

# Activate virtualenv
echo "🐍 Activating virtual environment..."
source venv/bin/activate
if [ $? -ne 0 ]; then
    echo "❌ Failed to activate virtual environment. Exiting."
    exit 1
fi

# Start Celery worker in background
echo "⚙️ Launching Celery worker..."
celery -A chaos_tasks worker --loglevel=info &
CELERY_PID=$!
sleep 2

# Check if Celery is running
if ! ps -p $CELERY_PID > /dev/null; then
    echo "❌ Celery worker failed to start. Exiting."
    exit 1
fi

# Export Flask environment vars
export FLASK_APP=dashboard.py
export FLASK_ENV=development

# Start Flask server
echo "🌐 Starting Flask server at http://localhost:5000..."
flask run
if [ $? -ne 0 ]; then
    echo "❌ Failed to start Flask server. Exiting."
    exit 1
fi
