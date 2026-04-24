@echo off
title Wildlife Monitoring System
echo =========================================
echo Starting Wildlife Monitoring System...
echo =========================================

echo.
echo [1/4] Starting Cloud Backend (Port 8000)...
start "Backend API" cmd /k "cd cloud_backend && uvicorn main:app --reload --port 8000"

echo [2/4] Starting Next.js Frontend (Port 3000)...
start "Frontend Dashboard" cmd /k "cd frontend && npm run dev"

echo [3/4] Starting Edge Device Sync Service...
start "Edge Sync" cmd /k "cd edge_device && python sync_cloud.py"

echo [4/4] Starting Edge Device Detection (Webcam)...
start "Edge Detection" cmd /k "cd edge_device && python detect.py"

echo.
echo All 4 components are starting in separate windows!
echo Make sure you allow time for the Next.js server to build.
echo.
echo - Your API is running at: http://localhost:8000
echo - Your Dashboard is at:   http://localhost:3000
echo.
pause
