# 🏗️ Chaos Task Arena - App Architecture Overview

This app simulates an unreliable distributed task system using Flask, Celery, Redis, and a real-time dashboard.

---

### 📦 Tech Stack
- **Flask** – REST API and WebSocket server
- **Celery** – Task queue system
- **Redis** – Broker and temporary store for task status
- **PostgreSQL** – Optional persistent DB for logging
- **Flask-SocketIO** – Real-time updates
- **Frontend** – Chart-based visualization (any JS framework)

---

### 🔁 Architecture Flow

```text
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
