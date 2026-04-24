# 🐾 Wildlife Monitoring System

A full-stack wildlife detection and monitoring system that uses **YOLOv8** on edge devices (Raspberry Pi, laptop webcam, etc.) to detect animals in real time, stores detections locally when offline, syncs them to a **FastAPI** cloud backend, and displays everything on a **Next.js** dashboard.

Built this as a way to explore how AI-based conservation tools could work in the real world — where internet is spotty, cameras run 24/7, and you need alerts the moment a leopard shows up near a village.

---

## How It Works

```
Camera Feed → Motion Detection → YOLOv8 Inference → Local DB → Cloud Sync → Dashboard
```

1. The edge device captures video frames and runs background subtraction to detect motion.
2. When motion crosses a threshold, YOLOv8 runs on the frame to identify species.
3. Detections (species, confidence, image, timestamp) are saved to a local SQLite database.
4. A separate sync service runs **every 5 seconds** and pushes unsynced detections to the cloud backend.
5. The cloud backend processes the payload, securely uploads the full-resolution image to a **Supabase Storage Bucket**, and saves the public URL into its own database.
6. The Next.js frontend polls the backend and renders a live dashboard with species counts, alerts, and the latest detection image.

---

## Project Structure

```
Wildlife-monitoring/
├── start_all.bat          # 1-Click Windows execution script for all services
├── train_custom_model.py  # Automation script to trace/train custom YOLOv8 datasets
├── edge_device/           # Runs on the device with the camera
│   ├── config.py          # API URL, model path, species list, thresholds
│   ├── detect.py          # Main detection loop (motion + YOLOv8)
│   ├── offline_storage.py # Local SQLite storage for detections
│   ├── sync_cloud.py      # Periodic sync to cloud backend
│   └── requirements.txt
│
├── cloud_backend/         # FastAPI server 
│   ├── main.py            # API endpoints with direct Supabase bucket integration
│   ├── models.py          # SQLAlchemy + Pydantic models
│   ├── database.py        # DB engine setup
│   ├── email_utils.py     # Email alerts (placeholder, needs SMTP config)
│   └── requirements.txt
│
├── frontend/              # Next.js dashboard with Clerk auth
│   ├── app/
│   │   ├── page.js        # Landing page
│   │   ├── dashboard/     # Main monitoring dashboard
│   │   ├── (auth)/        # Clerk sign-in / sign-up pages
│   │   └── globals.css    # All the styling
│   ├── middleware.js       # Clerk auth middleware (protects /dashboard)
│   └── .env.local         # NEXT_PUBLIC_API_URL
│
├── models/
│   └── yolov8n.pt         # Pre-trained YOLOv8 nano model
│
└── datasets/
    └── african-wildlife/  # Training data (if you want to fine-tune)
```

---

## Setup

### Prerequisites

- Python 3.9+
- Node.js 18+
- A [Supabase](https://supabase.com) account (Requires a public bucket named `wildlife-images` for cloud image storage)
- A webcam or video file for the edge device
- (Optional) A [Clerk](https://clerk.com) account for auth on the frontend

### 🚀 Zero-Config Windows Start
If you are on Windows, you can simply double-click the **`start_all.bat`** file in the root directory. It will instantly boot up the Cloud Backend, the Next.js Dashboard, the Camera Detection, and the Edge Sync service in 4 separate, concurrent terminal windows!

If you prefer to start them manually or deploy to the cloud, follow the steps below:

### 1. Cloud Backend

```bash
cd cloud_backend
pip install -r requirements.txt
```

You must create a `.env` file inside `cloud_backend/` containing your Supabase super-admin keys:
```
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_KEY=your-service-role-secret-key
```

Then run the server:
```bash
uvicorn main:app --reload --port 8000
```
The API will be live at `http://localhost:8000`.

If you're deploying to Render, the API URL is already configured in `edge_device/config.py` and `frontend/.env.local` — just update it if your URL is different.

### 2. Edge Device

```bash
cd edge_device
pip install -r requirements.txt
```

Before running, update `config.py`:
- Set `API_URL` to your backend URL (localhost or deployed)
- Set `MODEL_PATH` to your model file (defaults to `models/yolov8n.pt`)
- If you trained a custom model, update `SPECIES_LIST` to match your classes

Then run the detection loop:
```bash
python detect.py
```

And in a separate terminal, to start the cloud sync:
```bash
cd edge_device
python sync_cloud.py
```

### 🧠 Training a Custom African Wildlife Model
The default model is YOLOv8 Nano pre-trained on generic objects. Because actual wildlife monitoring requires specialized species identification (e.g. Zebras, Elephants, Leopards), this repository includes an automation script to train your own custom AI model using the provided dataset.

Run this command from the root project folder:
```bash
python train_custom_model.py
```
This script will download the base YOLOv8 weights and automatically fine-tune them across 50 epochs using the dataset located in `datasets/african-wildlife/`. Once finished, point the `MODEL_PATH` in `edge_device/config.py` to the newly generated `best.pt` file to instantly deploy your custom wildlife intelligence!

### 3. Frontend

```bash
cd frontend
npm install
```

Create a `.env.local` file (one should already exist) with:
```
NEXT_PUBLIC_API_URL=http://localhost:8000
NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY=pk_test_your_key_here
CLERK_SECRET_KEY=sk_test_your_secret_here
```

Then start the dev server:
```bash
npm run dev
```

Open `http://localhost:3000` — you'll see the landing page. Click "Start Monitoring" to go to the dashboard.

---

## API Endpoints

All endpoints (except `/live-frame`) require the `X-API-KEY` header.

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/upload_detection/` | Upload a detection with image, species, confidence, etc. |
| `GET` | `/detections/` | Get all detections (newest first) |
| `GET` | `/live-frame` | Returns the most recently uploaded image |
| `POST` | `/set-alert-recipient` | Set email for critical species alerts |

---

## Email Alerts

The system can send email alerts when specific species are detected (currently leopard and elephant). Right now `email_utils.py` just prints to the console — to actually send emails, you'd need to:

1. Set up an SMTP account (Gmail app password works fine)
2. Add `EMAIL_SENDER_ADDRESS`, `EMAIL_SENDER_PASSWORD` to your `.env`
3. Uncomment the `smtplib` code in `email_utils.py`

---

## Tech Stack

| Component | Tech |
|-----------|------|
| Object Detection | YOLOv8 (Ultralytics) |
| Image Storage | **Supabase Buckets** |
| Edge Storage | SQLite |
| Cloud Backend | FastAPI + SQLAlchemy + SQLite |
| Frontend | Next.js 15 + React 19 |
| Analytics & Visualization | **Recharts** |
| Auth | Clerk |
| Styling | Vanilla CSS (dark theme, glassmorphism) |

---



## License

Do whatever you want with it. If you use it for actual conservation work, I'd love to hear about it.
