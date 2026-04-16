from __future__ import annotations

import logging
import os
from contextlib import asynccontextmanager
from pathlib import Path

from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

logging.basicConfig(level=logging.INFO)

load_dotenv(Path(__file__).resolve().parent / ".env")


@asynccontextmanager
async def lifespan(app: FastAPI):
    logging.info("Starting NeuroLearn Assist API...")
    yield
    logging.info("Shutting down NeuroLearn Assist API...")


app = FastAPI(
    title="NEUROLEARN ASSIST API",
    version="1.0.0",
    description="AI tutor backend for accessible document learning.",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.middleware("http")
async def add_server_header(request, call_next):
    response = await call_next(request)
    response.headers["Server"] = "NeuroLearn/1.0"
    return response


from api.routes import router

app.include_router(router)


@app.get("/health")
async def health_check():
    return {"status": "ok", "service": "neurolearn-assist"}


@app.get("/")
async def root():
    return {"message": "NeuroLearn Assist API", "docs": "/docs", "health": "/health"}
