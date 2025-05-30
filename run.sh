#!/bin/bash

# Start Redis if it's not already running
echo "🔁 Starting Redis..."
sudo redis-server

# Activate virtualenv
echo "🐍 Activating virtual environment..."
source env/bin/activate

# Start Celery worker in a new terminal
echo "⚙️ Launching Celery worker..."
gnome-terminal -- bash -c "cd $(pwd); source venv/bin/activate; celery -A chaos_tasks worker --loglevel=info; exec bash"

# Wait 2 seconds for Celery to boot
sleep 2

# Start Flask
echo "🌐 Starting Flask server at http://localhost:5000..."
export FLASK_APP=dashboard.py
export FLASK_ENV=development
flask run
