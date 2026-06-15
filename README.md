# Wildlife Monitoring System 🦁
### Edge AI Real-Time Wildlife Detection

> A production-grade edge AI system for real-time wildlife detection using YOLOv8 — achieving sub-200ms inference latency under concurrent load, with async FastAPI data ingestion and Supabase cloud sync.



---

## What This Does

Wildlife monitoring at scale is hard. Camera traps generate massive amounts of footage. Manual review is slow, expensive, and misses events. This system runs **YOLOv8 object detection at the edge** — on-device inference that identifies animals in real time, logs detections asynchronously, and syncs to the cloud even under intermittent connectivity.

Built for real deployment conditions: concurrent sensor streams, unreliable network, and accuracy that holds up under production load.

---

## Performance

| Metric | Result |
|---|---|
| Inference latency | **< 200ms** under concurrent load |
| Detection model | YOLOv8 (fine-tuned for wildlife) |
| Data persistence | Offline-first, edge-to-cloud sync |
| API throughput | Async FastAPI, tested under high concurrency |

---

## Architecture

```
edge_device/               ← YOLOv8 runs here, locally on device
     │
     │  (detections + sensor data)
     ▼
cloud_backend/             ← Async FastAPI server ingests data
     │
     ├── Online:  Push to Supabase cloud storage
     └── Offline: Buffer locally → sync on reconnect
     │
     ▼
Supabase Cloud             ← Reliable persistence + sync layer
     │
     ▼
frontend/                  ← Next.js dashboard, real-time feed
```

---

## Project Structure

```
Wildlife-Monitoring/
├── cloud_backend/      # FastAPI async REST API for sensor data ingestion
│                       # Supabase integration, offline-first sync logic
├── edge_device/        # YOLOv8 inference pipeline (runs on-device)
│                       # Real-time detection, local buffering
├── frontend/           # Next.js dashboard
│                       # Live detection feed + analytics UI
├── models/             # YOLOv8 weights, training scripts, F1 evaluation
├── .gitignore
└── README.md
```

---

## Tech Stack

| Layer | Technology |
|---|---|
| Computer Vision | YOLOv8 (Ultralytics) |
| Edge Inference | Python, runs locally on `edge_device` |
| Backend API | FastAPI (async REST) — `cloud_backend` |
| Frontend | Next.js — `frontend` |
| Cloud Storage | Supabase |
| Deployment | Vercel (frontend), Docker (backend) |

---

## Key Features

**Sub-200ms Edge Inference**
YOLOv8 runs inside `edge_device/` — no cloud round-trip for detection. Fast, local inference regardless of connectivity.

**Fine-Tuned for Wildlife**
End-to-end model training and fine-tuning in `models/`. F1-score evaluated against production-grade accuracy targets before deployment.

**Async Data Ingestion**
`cloud_backend/` FastAPI server handles sensor streams asynchronously — high throughput without blocking the detection pipeline.

**Offline-First Sync**
When the network drops, detections buffer on the edge device. Supabase sync in `cloud_backend/` resumes automatically on reconnect — zero data loss.

**Real-Time Dashboard**
`frontend/` Next.js app displays live detections, species logs, and system health. Fixed React Server Components CVE vulnerabilities for production security.

---

## Getting Started

```bash
# Clone the repo
git clone https://github.com/anshi78/Wildlife-Monitoring.git
cd Wildlife-Monitoring
```

**Run the backend (cloud_backend/):**
```bash
cd cloud_backend
pip install -r requirements.txt
cp .env.example .env   # Add your Supabase URL + API key
uvicorn main:app --reload
```

**Run edge detection (edge_device/):**
```bash
cd edge_device
pip install -r requirements.txt
python detect.py --source your_video.mp4
```

**Run the frontend (frontend/):**
```bash
cd frontend
npm install
npm run dev
```

**Train / evaluate the model (models/):**
```bash
cd models
python train.py --model yolov8n.pt --data wildlife.yaml --epochs 50
python evaluate.py --weights runs/train/weights/best.pt
```

---

## Why Edge AI?

Running detection in the cloud means every frame travels over a network before you get an answer. In wildlife monitoring — cameras in forests, reserves, and remote locations — that's not practical. Edge inference keeps detection fast and reliable regardless of connectivity, and only syncs what matters (detections, metadata) to the cloud via `cloud_backend/`.

---



---


