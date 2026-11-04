"""Optional Node56 HTTP worker service.

Run with: uvicorn framework.node56_worker:app --host 0.0.0.0 --port 8000
Register real task adapters with register_handler(); unconfigured tasks are
reported as unavailable and are never marked as successfully executed.
"""
from __future__ import annotations

from threading import RLock
from typing import Any, Callable

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

app = FastAPI(title="AI-LAB Node56 Worker", version="7.0")
_handlers: dict[str, Callable[[dict[str, Any]], Any]] = {}
_lock = RLock()


class ExecuteRequest(BaseModel):
    task: str = Field(min_length=1, max_length=100)
    agent: str = Field(default="", max_length=100)
    payload: dict[str, Any] = Field(default_factory=dict)


def register_handler(task: str, handler: Callable[[dict[str, Any]], Any]) -> None:
    """Register a real implementation for a task name."""
    name = str(task).strip()
    if not name or not callable(handler):
        raise ValueError("task must be non-empty and handler must be callable")
    with _lock:
        _handlers[name] = handler


def unregister_handler(task: str) -> None:
    with _lock:
        _handlers.pop(str(task), None)


def health() -> dict[str, Any]:
    with _lock:
        available = sorted(_handlers)
    return {"status": "ok", "service": "node56-worker", "version": "7.0",
            "available_tasks": available}


def execute_task(request: ExecuteRequest) -> dict[str, Any]:
    with _lock:
        handler = _handlers.get(request.task)
    if handler is None:
        return {"status": "unavailable", "task": request.task,
                "detail": "No task adapter is registered on Node56"}
    try:
        result = handler({"task": request.task, "agent": request.agent,
                          "payload": request.payload})
        return {"status": "completed", "task": request.task, "result": result}
    except Exception as exc:
        return {"status": "failed", "task": request.task,
                "error": f"{type(exc).__name__}: {exc}"}


@app.get("/worker/health")
def worker_health():
    return health()


@app.post("/worker/execute")
def worker_execute(request: ExecuteRequest):
    return execute_task(request)
