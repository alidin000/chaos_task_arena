from flask import Flask, request, jsonify
from chaos_tasks import chaos_task
import redis

app = Flask(__name__)
r = redis.Redis()

@app.route("/run")
def run_batch():
    chance = float(request.args.get("chance", 0.5))
    count = int(request.args.get("count", 10))
    for i in range(count):
        chaos_task.delay(f"job_{i}", chance)
    return {"message": f"{count} jobs started"}

@app.route("/stats")
def stats():
    return {
        "success": int(r.get("success") or 0),
        "retry": int(r.get("retry") or 0),
        "failed": int(r.get("failed") or 0),
    }

@app.route("/reset")
def reset():
    r.set("success", 0)
    r.set("retry", 0)
    r.set("failed", 0)
    return {"message": "Reset stats"}
