# Mini Distributed System

A lightweight, fault-tolerant **Distributed Task Execution Platform** capable of orchestrating jobs across multiple autonomous worker nodes. Designed to simulate the core architecture of systems like **Jenkins**, **Celery**, or **GitHub Actions**.

![Project Status](https://img.shields.io/badge/status-active-success)
![License](https://img.shields.io/badge/license-MIT-blue)

## Architecture
The system follows a **Master-Slave** architecture with three distinct components:
1.  **The Orchestrator (Server):** A FastAPI backend that manages the job queue, handles client requests, and persists state via SQLite.
2.  **The Agents (Workers):** Autonomous Python processes that poll the server for work, execute arbitrary shell commands, and upload resulting artifacts (files).
3.  **The Dashboard (Frontend):** A real-time React UI for monitoring job status, viewing logs, and downloading build artifacts.

## Tech Stack
* **Backend:** Python 3.10+, FastAPI, SQLAlchemy
* **Frontend:** React, Vite, TailwindCSS, Lucide Icons
* **Database:** SQLite (Relational)
* **Communication:** REST API (HTTP Polling), Multipart File Uploads

## Key Features
* **Distributed Execution:** Spin up 1 or 100 workers; the load is distributed automatically.
* **Artifact Pipeline:** Workers automatically detect, compress, and upload build artifacts (e.g., `output.txt`, binaries) to the central server.
* **Fault Tolerance:** If a worker goes offline, the server tracks the heartbeat and status.
* **Real-time Monitoring:** Live status updates (Queued → Running → Success/Failed).

## How to Run

### 1. Start the Server (The Brain)
```bash
# Navigate to root
pip install -r requirements.txt
uvicorn server.main:app --reload


