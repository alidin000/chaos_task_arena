# 🏗️ Chaos Task Arena - App Architecture Overview

This app simulates an unreliable distributed task system using Flask, Celery, Redis, and a real-time dashboard.

---

## 📦 Tech Stack

* **Flask** – REST API + WebSocket server
* **Celery** – Distributed task queue
* **Redis** – Message broker and in-memory task store
* **PostgreSQL** – Persistent logging (optional)
* **Flask-SocketIO** – Real-time push updates
* **Frontend** – Charts and task metrics visualization

---

## ⭮️ Architecture Flow

```
[User Clicks "Send 100 Tasks"]
           ↓
[Flask API triggers tasks via Celery]
           ↓
[Celery sends tasks to Redis Broker]
           ↓
[Worker executes tasks with random success/failure]
           ↓
[On retry/fail/success, log status to Redis or DB]
           ↓
[Flask-SocketIO sends real-time updates to frontend]
           ↓
[Frontend visualizes stats with charts]
```

---

## ✅ Task Status Lifecycle

Tasks follow this flow:

```
QUEUED → STARTED → SUCCESS / FAILURE
                 ↸ (if failed) RETRY → STARTED → ...
```

* Failures are retried based on Celery retry settings (like max retries, delay, etc.).
* All transitions are logged to Redis and optionally PostgreSQL.

---

## 📊 Real-time Dashboard

Frontend displays live metrics:

* Total tasks sent
* In progress
* Succeeded
* Failed
* Retry counts

Updates are pushed via WebSocket using Flask-SocketIO.

---

## ⚙️ Optional Integrations

* 🔔 **Slack / Email notifications** for task summaries or alerts
* 🐳 **Docker / Kubernetes** support for containerized deployment
* 🧚 **Testing & Monitoring** via pytest, Prometheus, etc. (optional)
