# 🐍 PyPulse Engine - Full-Stack Python Cloud Platform

> Modern Asynchronous REST API & Real-time Telemetry Dashboard built with **Python 3.10**, **FastAPI**, **Pydantic v2**, and **Uvicorn**.

---

## 🌟 Key Architecture & Highlights

- **Backend Framework**: Python FastAPI (Async ASGI) with auto-generated OpenAPI / Swagger specs (`/docs`).
- **Real-Time Telemetry**: Host hardware utilization monitoring (CPU, RAM, Disks, Uptime) via `psutil`.
- **Node Cluster Manager**: Dynamic cluster node registration, decommissioning, and role dispatching.
- **Frontend SPA**: Clean dark-mode single page dashboard served directly from `app/static/` with live charts and interactive API sandbox.
- **Deployment Ready**: Includes `Dockerfile`, `Procfile`, `runtime.txt`, and standard `requirements.txt`.
- **Zero Workflows**: Clean codebase without CI/CD pipeline locks.

---

## 🚀 Quick Start

### 1. Installation

```bash
cd py-pulse-engine
pip install -r requirements.txt
```

### 2. Run the Development Server

```bash
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Open [http://localhost:8000](http://localhost:8000) in your browser.

---

## 🐳 Docker Support

```bash
# Build Docker Image
docker build -t py-pulse-engine .

# Run Container
docker run -p 8000:8000 py-pulse-engine
```

---

## 📡 API Endpoints

| Method | Route | Description |
|---|---|---|
| `GET` | `/` | Live Telemetry & Cluster Manager Dashboard |
| `GET` | `/docs` | Interactive Swagger / OpenAPI Specification |
| `GET` | `/api/health` | Service health status and uptime metrics |
| `GET` | `/api/system` | Detailed host OS, CPU cores, RAM and storage telemetry |
| `GET` | `/api/analytics/summary`| Live RPS, throughput and latency analytics |
| `GET` | `/api/nodes` | List all active cluster nodes |
| `POST` | `/api/nodes` | Provision a new cluster node |
| `DELETE`| `/api/nodes/{id}` | Decommission a cluster node |

---

## 📄 License

MIT © [turguzdev](https://github.com/turguzdev)
