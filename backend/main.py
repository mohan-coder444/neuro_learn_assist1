from __future__ import annotations

import logging
from pathlib import Path

from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

logging.basicConfig(level=logging.INFO)

load_dotenv(Path(__file__).resolve().parent / ".env")

from api.routes import router

app = FastAPI(
    title="NEUROLEARN ASSIST API",
    version="1.0.0",
    description="AI tutor backend for accessible document learning.",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)


@app.get("/health")
def health_check():
    return {"status": "ok"}
