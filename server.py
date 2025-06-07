import eventlet
eventlet.monkey_patch()
import os
import logging
from flask import Flask, request, jsonify, render_template
from flask_socketio import SocketIO
import redis

app = Flask(__name__)
socketio = SocketIO(app, message_queue='redis://localhost:6379/1')

r = redis.Redis()

os.makedirs('logs', exist_ok=True)

logger = logging.getLogger('flask_app')
logger.setLevel(logging.INFO)
file_handler = logging.FileHandler('logs/chaos_tasks_server.log')
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

@app.route('/')
def index():
    return render_template('index.html')

@app.route("/run")
def run_batch():
    chance = float(request.args.get("chance", 0.5))
    count = int(request.args.get("count", 10))
    logger.info(f"Received run request: count={count}, chance={chance}")
    from chaos_tasks import chaos_task  # import here to avoid circular import
    for i in range(count):
        chaos_task.delay(f"job_{i}", chance)
    logger.info(f"Started {count} chaos tasks")
    return {"message": f"{count} jobs started"}

@app.route("/stats")
def stats():
    stats = {
        "success": int(r.get("success") or 0),
        "retry": int(r.get("retry") or 0),
        "failed": int(r.get("failed") or 0),
    }
    logger.info(f"Stats requested: {stats}")
    return stats

@app.route("/reset")
def reset():
    r.set("success", 0)
    r.set("retry", 0)
    r.set("failed", 0)
    logger.info("Stats reset")
    return {"message": "Reset stats"}

@socketio.on('connect')
def handle_connect():
    logger.info(f'Client connected: {request.sid}')

@socketio.on('disconnect')
def handle_disconnect():
    logger.info(f'Client disconnected: {request.sid}')

if __name__ == '__main__':
    socketio.run(app, debug=True, host='0.0.0.0')
