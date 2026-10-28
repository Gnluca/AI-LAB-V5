"""Stable, minimal AI-LAB API entry point."""
from __future__ import annotations

import os
import platform
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

try:
    import psutil
except ImportError:
    psutil = None

try:
    from .bridge import server_status
except ImportError:
    from bridge import server_status

VERSION = os.getenv("AI_LAB_VERSION", "6.3")
app = FastAPI(title="AI LAB", version=VERSION)

# Keep the default permissive for local-network deployments; production can restrict it.
origins = [item.strip() for item in os.getenv("AI_LAB_CORS_ORIGINS", "*").split(",") if item.strip()]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=origins != ["*"],
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["*"],
)


@app.get("/")
def home() -> dict:
    return {"name": "AI LAB", "version": VERSION, "status": "online"}


@app.get("/status")
def status() -> dict:
    ollama = server_status()
    return {"service": "AI-LAB", "version": VERSION, "runtime": "online", **ollama}


@app.get("/health")
def health() -> dict:
    # The API process is healthy even when the optional model service is offline.
    return {"healthy": True, "dependencies": {"ollama": server_status()["ollama"]}}


@app.get("/hardware")
def hardware() -> dict:
    if psutil is None:
        return {"hostname": platform.node(), "status": "degraded", "metrics_available": False}
    return {
        "hostname": platform.node(),
        "status": "online",
        "metrics_available": True,
        "cpu": round(psutil.cpu_percent(interval=0.1), 1),
        "ram": round(psutil.virtual_memory().percent, 1),
        "disk": round(psutil.disk_usage(os.path.abspath(os.sep)).percent, 1),
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("server.app:app", host=os.getenv("AI_LAB_HOST", "0.0.0.0"), port=int(os.getenv("AI_LAB_PORT", "8000")))
