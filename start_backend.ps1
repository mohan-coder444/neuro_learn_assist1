# NeuroLearn Backend Starter
# Run this script to start the FastAPI backend on port 8000
# Usage: powershell -ExecutionPolicy Bypass -File start_backend.ps1

Write-Host "Starting NeuroLearn Backend..." -ForegroundColor Cyan
Write-Host "Using system Python 3.10 (compatible with faiss-cpu)" -ForegroundColor Yellow

Set-Location "d:\my projects\neurolearn v2\backend"
python -m uvicorn main:app --host 0.0.0.0 --port 8000 --reload
