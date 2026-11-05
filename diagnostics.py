#!/usr/bin/env python3
"""Production health check for AI-LAB.

Prints one line per subsystem:

    [OK]      component is healthy
    [WARNING] component is degraded or idle
    [ERROR]   component is unavailable or invalid

Writes ``data/diagnostics_report.json`` and prints a score from 0 to 100.
Exit code is 0 when every check is OK or WARNING, and 1 when any check is ERROR.
"""

from __future__ import annotations

import argparse
import importlib.metadata as importlib_metadata
import json
import os
import re
import socket
import sqlite3
import subprocess
import sys
import urllib.error
import urllib.request
from datetime import datetime
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parent
DATA_DIR = ROOT / "data"
REPORT_PATH = DATA_DIR / "diagnostics_report.json"
COGNITIVE_REPORT = DATA_DIR / "cognitive_report.json"
MASTER_LOOP_STATE = DATA_DIR / "master_loop_state.json"
LOOP_STATUS = DATA_DIR / "loop_status.json"

LOCAL_BASE = os.environ.get("AI_LAB_BASE_URL", "http://127.0.0.1:8000").rstrip("/")
OLLAMA_BASE = os.environ.get("OLLAMA_URL", "http://127.0.0.1:11434").rstrip("/")
NODE41_URL = os.environ.get("AI_LAB_NODE41_URL", "http://192.168.1.41:8000/status")
NODE56_URL = os.environ.get("AI_LAB_NODE56_URL", "http://192.168.1.56:8000/status")
ACTIVE_MODEL = os.environ.get("OLLAMA_MODEL", "llama3.1")
TIMEOUT = float(os.environ.get("AI_LAB_NODE_TIMEOUT", "3"))

MIN_PYTHON = (3, 11)
LOOP_INTERVAL_SECONDS = 300
FRESH_LOOP_SECONDS = LOOP_INTERVAL_SECONDS * 2 + 60
FRESH_REPORT_SECONDS = 20 * 60

# Weights sum to 100. WARNING keeps half of the weight, ERROR keeps none.
WEIGHTS = {
    "python": 6,
    "dependencies": 10,
    "runtime": 10,
    "master_loop": 8,
    "cognitive_core": 8,
    "mpc": 8,
    "fastapi": 10,
    "dashboard": 6,
    "ollama": 8,
    "model": 8,
    "node41": 6,
    "node56": 4,
    "json_report": 4,
    "database": 4,
}

REQUIREMENTS_FILE = ROOT / "requirements.txt"
PYPROJECT_FILE = ROOT / "pyproject.toml"
RUNTIME_PACKAGES = ("fastapi", "uvicorn", "requests", "psutil", "pydantic")

COGNITIVE_MODULES = (
    "cognitive_core/cognitive_loop.py",
    "cognitive_core/context_builder.py",
    "cognitive_core/observation.py",
    "cognitive_core/reasoning_engine.py",
    "cognitive_core/goal_generator.py",
    "cognitive_core/state_manager.py",
)

DB_CANDIDATES = (
    Path(os.environ["AI_LAB_HOME"]) / "database" / "chat.db"
    if os.environ.get("AI_LAB_HOME")
    else None,
    Path(r"D:\AI-Server\database\chat.db"),
    Path(r"E:\AI-Server\database\chat.db"),
    ROOT / "database" / "chat.db",
)


def check(check_id: str, name: str, level: str, message: str, **details: Any) -> dict[str, Any]:
    if level not in {"OK", "WARNING", "ERROR"}:
        raise ValueError(f"invalid level: {level}")
    item = {
        "id": check_id,
        "name": name,
        "level": level,
        "message": message,
        "weight": WEIGHTS[check_id],
    }
    if details:
        item["details"] = details
    return item


def parse_timestamp(value: str) -> datetime | None:
    try:
        parsed = datetime.fromisoformat(value)
    except (TypeError, ValueError):
        return None
    if parsed.tzinfo is not None:
        parsed = parsed.astimezone().replace(tzinfo=None)
    return parsed


def age_seconds(value: str) -> float | None:
    parsed = parse_timestamp(value)
    if parsed is None:
        return None
    return (datetime.now() - parsed).total_seconds()


def read_json(path: Path) -> tuple[Any | None, str | None]:
    try:
        return json.loads(path.read_text(encoding="utf-8")), None
    except FileNotFoundError:
        return None, "file not found"
    except json.JSONDecodeError as exc:
        return None, f"invalid JSON: {exc}"
    except OSError as exc:
        return None, str(exc)


def http_get(url: str, timeout: float = TIMEOUT) -> dict[str, Any]:
    request = urllib.request.Request(url, headers={"Accept": "application/json, text/html"})
    started = datetime.now()
    try:
        with urllib.request.urlopen(request, timeout=timeout) as response:
            body = response.read(65536)
            elapsed = (datetime.now() - started).total_seconds() * 1000
            text = body.decode("utf-8", errors="replace")
            payload: Any = text[:500]
            try:
                payload = json.loads(text)
            except json.JSONDecodeError:
                pass
            return {
                "ok": 200 <= response.status < 300,
                "status_code": response.status,
                "latency_ms": round(elapsed, 1),
                "payload": payload,
            }
    except urllib.error.HTTPError as exc:
        return {
            "ok": False,
            "status_code": exc.code,
            "error": f"HTTP {exc.code}",
        }
    except Exception as exc:  # noqa: BLE001 - diagnostics must report every failure mode
        return {
            "ok": False,
            "status_code": None,
            "error": f"{type(exc).__name__}: {exc}",
        }


def port_open(host: str, port: int, timeout: float = 1.5) -> bool:
    try:
        with socket.create_connection((host, port), timeout=timeout):
            return True
    except OSError:
        return False


def local_ipv4() -> list[str]:
    addresses: set[str] = set()
    try:
        for info in socket.getaddrinfo(socket.gethostname(), None, socket.AF_INET):
            addresses.add(info[4][0])
    except OSError:
        pass
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as probe:
            probe.connect(("192.168.1.41", 80))
            addresses.add(probe.getsockname()[0])
    except OSError:
        pass
    return sorted(addresses)


def lab_processes() -> list[dict[str, Any]]:
    """Return Python / AI-LAB processes. Empty when the scan itself fails."""
    if os.name != "nt":
        return []
    script = (
        "Get-CimInstance Win32_Process | "
        "Where-Object { $_.Name -match 'python|AI-LAB|uvicorn' } | "
        "Select-Object ProcessId, Name, CommandLine | ConvertTo-Json -Compress"
    )
    try:
        completed = subprocess.run(
            ["powershell", "-NoProfile", "-Command", script],
            capture_output=True,
            text=True,
            timeout=15,
            check=False,
        )
    except (OSError, subprocess.TimeoutExpired):
        return []
    raw = completed.stdout.strip()
    if not raw:
        return []
    try:
        payload = json.loads(raw)
    except json.JSONDecodeError:
        return []
    rows = payload if isinstance(payload, list) else [payload]
    return [row for row in rows if isinstance(row, dict)]


def relevant_processes(processes: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """AI-LAB runtimes visible on this machine, marked when they belong to this tree."""
    needles = ("ai_lab_runtime", "master_loop", "uvicorn", "ai-lab-runtime")
    root_text = str(ROOT).lower()
    found: list[dict[str, Any]] = []
    for row in processes:
        command = " ".join(str(row.get("CommandLine") or "").split())
        if not any(needle in command.lower() for needle in needles):
            continue
        pid = row.get("ProcessId")
        if not isinstance(pid, int):
            continue
        found.append(
            {
                "pid": pid,
                "command": command,
                "this_tree": root_text in command.lower(),
            }
        )
    return found


def process_note(rows: list[dict[str, Any]]) -> str:
    if not rows:
        return "no AI-LAB runtime process"
    commands = []
    for row in rows:
        script = row["command"]
        for part in script.split():
            if part.lower().endswith(".py") or part.lower().endswith(".exe"):
                script = part.strip('"')
        if script not in commands:
            commands.append(script)
    pid_text = ", ".join(str(row["pid"]) for row in rows)
    return f"pid {pid_text} ({'; '.join(commands)})"


def version_tuple(value: str) -> tuple[int, ...]:
    parts: list[int] = []
    for chunk in re.split(r"[.+]", value.strip()):
        match = re.match(r"(\d+)", chunk)
        if not match:
            break
        parts.append(int(match.group(1)))
    return tuple(parts) or (0,)


def compare_versions(left: tuple[int, ...], right: tuple[int, ...]) -> int:
    width = max(len(left), len(right))
    padded_left = left + (0,) * (width - len(left))
    padded_right = right + (0,) * (width - len(right))
    if padded_left > padded_right:
        return 1
    if padded_left < padded_right:
        return -1
    return 0


def parse_requirement(line: str) -> tuple[str, list[tuple[str, str]]] | None:
    text = line.split("#", 1)[0].strip().strip('"').strip("'")
    if not text or text.startswith("["):
        return None
    match = re.match(
        r"^(?P<name>[A-Za-z0-9_.\-]+)(?:\[[^\]]+\])?\s*(?P<spec>.*)$",
        text,
    )
    if not match:
        return None
    spec = match.group("spec").strip()
    clauses: list[tuple[str, str]] = []
    if spec:
        for part in spec.split(","):
            clause = part.strip()
            operator_match = re.match(r"^(<=|>=|==|!=|~=|<|>)\s*(.+)$", clause)
            if not operator_match:
                return None
            clauses.append((operator_match.group(1), operator_match.group(2).strip()))
    return match.group("name"), clauses


def bounds_conflict(
    left: list[tuple[str, str]],
    right: list[tuple[str, str]],
) -> bool:
    """True when two version ranges cannot be true at the same time."""

    def bounds(clauses: list[tuple[str, str]]) -> tuple[tuple[int, ...], bool, tuple[int, ...] | None, bool]:
        lower = (0,)
        lower_inclusive = True
        upper: tuple[int, ...] | None = None
        upper_inclusive = False
        for operator, raw in clauses:
            current = version_tuple(raw)
            if operator in {">=", ">"}:
                order = compare_versions(current, lower)
                if order > 0 or (order == 0 and operator == ">" and lower_inclusive):
                    lower = current
                    lower_inclusive = operator == ">="
            elif operator in {"<=", "<"}:
                order = 1 if upper is None else compare_versions(current, upper)
                if upper is None or order < 0 or (order == 0 and operator == "<" and upper_inclusive):
                    upper = current
                    upper_inclusive = operator == "<="
            elif operator == "==":
                lower = current
                upper = current
                lower_inclusive = True
                upper_inclusive = True
        return lower, lower_inclusive, upper, upper_inclusive

    lower_a, lower_a_inclusive, upper_a, upper_a_inclusive = bounds(left)
    lower_b, lower_b_inclusive, upper_b, upper_b_inclusive = bounds(right)
    lower = lower_a if compare_versions(lower_a, lower_b) >= 0 else lower_b
    lower_inclusive = lower_a_inclusive if compare_versions(lower_a, lower_b) > 0 else lower_b_inclusive
    if compare_versions(lower_a, lower_b) == 0:
        lower_inclusive = lower_a_inclusive and lower_b_inclusive

    candidates = [(upper_a, upper_a_inclusive), (upper_b, upper_b_inclusive)]
    present = [(item, inclusive) for item, inclusive in candidates if item is not None]
    if not present:
        return False
    upper, upper_inclusive = min(present, key=lambda item: (item[0], not item[1]))
    order = compare_versions(lower, upper)
    if order > 0:
        return True
    if order == 0 and not (lower_inclusive and upper_inclusive):
        return True
    return False


def requirement_satisfied(version: str, clauses: list[tuple[str, str]]) -> bool:
    current = version_tuple(version)
    for operator, raw in clauses:
        target = version_tuple(raw)
        order = compare_versions(current, target)
        if operator == ">=" and order < 0:
            return False
        if operator == ">" and order <= 0:
            return False
        if operator == "<=" and order > 0:
            return False
        if operator == "<" and order >= 0:
            return False
        if operator == "==" and order != 0:
            return False
        if operator == "!=" and order == 0:
            return False
        if operator == "~=":
            return False
    return True


def load_requirement_lines(path: Path) -> list[tuple[str, list[tuple[str, str]]]]:
    if not path.exists():
        return []
    parsed: list[tuple[str, list[tuple[str, str]]]] = []
    if path.suffix == ".toml":
        in_dependencies = False
        for line in path.read_text(encoding="utf-8").splitlines():
            stripped = line.strip()
            if stripped.startswith("dependencies") and stripped.endswith("["):
                in_dependencies = True
                continue
            if in_dependencies and stripped.startswith("]"):
                break
            if in_dependencies:
                item = parse_requirement(stripped.strip(","))
                if item:
                    parsed.append(item)
        return parsed
    for line in path.read_text(encoding="utf-8").splitlines():
        item = parse_requirement(line)
        if item:
            parsed.append(item)
    return parsed


def installed_version(name: str) -> str | None:
    try:
        return importlib_metadata.version(name)
    except importlib_metadata.PackageNotFoundError:
        return None


def check_python() -> dict[str, Any]:
    version = sys.version_info
    version_text = f"{version.major}.{version.minor}.{version.micro}"
    in_venv = sys.prefix != sys.base_prefix
    details = {
        "executable": sys.executable,
        "version": version_text,
        "virtualenv": in_venv,
        "required": f">={MIN_PYTHON[0]}.{MIN_PYTHON[1]}",
    }
    if version < MIN_PYTHON:
        return check(
            "python",
            "Python environment",
            "ERROR",
            f"{version_text} is older than {MIN_PYTHON[0]}.{MIN_PYTHON[1]}",
            **details,
        )
    if not in_venv:
        return check(
            "python",
            "Python environment",
            "WARNING",
            f"{version_text} at {sys.executable}; no virtualenv is active",
            **details,
        )
    return check(
        "python",
        "Python environment",
        "OK",
        f"{version_text} at {sys.executable}",
        **details,
    )


def check_dependencies() -> dict[str, Any]:
    runtime_specs = {name: clauses for name, clauses in load_requirement_lines(REQUIREMENTS_FILE)}
    project_specs = {name: clauses for name, clauses in load_requirement_lines(PYPROJECT_FILE)}
    missing: list[str] = []
    unsatisfied: list[str] = []
    conflicts: list[str] = []
    installed: dict[str, str] = {}

    names = list(dict.fromkeys([*RUNTIME_PACKAGES, *runtime_specs, *project_specs]))
    for name in names:
        version = installed_version(name)
        if version is None:
            if name in RUNTIME_PACKAGES or name in runtime_specs:
                missing.append(name)
            continue
        installed[name] = version
        runtime_ok = requirement_satisfied(version, runtime_specs.get(name, []))
        project_ok = requirement_satisfied(version, project_specs.get(name, []))
        if name in runtime_specs and not runtime_ok:
            unsatisfied.append(f"{name} {version} does not satisfy requirements.txt")
        elif name in project_specs and not project_ok:
            unsatisfied.append(f"{name} {version} does not satisfy pyproject.toml")
        if (
            name in runtime_specs
            and name in project_specs
            and bounds_conflict(runtime_specs[name], project_specs[name])
        ):
            conflicts.append(name)

    details = {"installed": installed, "missing": missing, "conflicts": conflicts}
    if missing:
        return check(
            "dependencies",
            "Installed dependencies",
            "ERROR",
            "missing " + ", ".join(missing),
            **details,
        )
    if conflicts or unsatisfied:
        reason = []
        if conflicts:
            reason.append("manifest conflict for " + ", ".join(conflicts))
        reason.extend(unsatisfied)
        return check(
            "dependencies",
            "Installed dependencies",
            "WARNING",
            "; ".join(reason),
            **details,
        )
    listed = ", ".join(f"{name} {installed[name]}" for name in RUNTIME_PACKAGES if name in installed)
    return check(
        "dependencies",
        "Installed dependencies",
        "OK",
        listed or "runtime packages importable",
        **details,
    )


def check_runtime(processes: list[dict[str, Any]]) -> dict[str, Any]:
    listening = port_open("127.0.0.1", 8000)
    health = http_get(f"{LOCAL_BASE}/runtime/health") if listening else {"ok": False}
    rows = relevant_processes(processes)
    details = {"port_8000": listening, "health": health, "processes": rows}
    payload = health.get("payload") if isinstance(health.get("payload"), dict) else {}
    healthy = health.get("ok") and payload.get("status") == "healthy" and payload.get("runtime") == "online"
    if listening and healthy:
        return check("runtime", "Runtime status", "OK", "port 8000 serving /runtime/health", **details)
    if listening:
        return check(
            "runtime",
            "Runtime status",
            "WARNING",
            "port 8000 is open but /runtime/health is not healthy",
            **details,
        )
    if rows:
        return check(
            "runtime",
            "Runtime status",
            "WARNING",
            f"{process_note(rows)} is running, but port 8000 is closed",
            **details,
        )
    return check("runtime", "Runtime status", "ERROR", "AI-LAB runtime is not listening on port 8000", **details)


def check_master_loop(processes: list[dict[str, Any]]) -> dict[str, Any]:
    state, state_error = read_json(MASTER_LOOP_STATE)
    loop_file, loop_error = read_json(LOOP_STATUS)
    rows = relevant_processes(processes)
    own_rows = [row for row in rows if row["this_tree"]]
    details = {
        "state_file": str(MASTER_LOOP_STATE),
        "state": state,
        "loop_status": loop_file,
        "processes": rows,
    }
    if not isinstance(state, dict):
        return check(
            "master_loop",
            "Master Loop status",
            "ERROR",
            state_error or "master_loop_state.json is not an object",
            **details,
        )

    status = str(state.get("status") or "unknown")
    stamp = str(state.get("timestamp") or "")
    age = age_seconds(stamp)
    details["age_seconds"] = None if age is None else round(age, 1)
    fresh = age is not None and 0 <= age <= FRESH_LOOP_SECONDS
    cycle = state.get("cycle")
    if loop_error and LOOP_STATUS.exists():
        details["loop_status_error"] = loop_error

    published_age = None
    if isinstance(loop_file, dict) and loop_file.get("timestamp"):
        published_age = age_seconds(str(loop_file["timestamp"]))
        details["published_status_age_seconds"] = None if published_age is None else round(published_age, 1)

    if status == "error":
        return check(
            "master_loop",
            "Master Loop status",
            "ERROR",
            f"cycle {cycle} recorded status error: {state.get('message') or 'no message'}",
            **details,
        )
    if status == "stopped":
        return check(
            "master_loop",
            "Master Loop status",
            "ERROR",
            f"cycle {cycle} is stopped",
            **details,
        )

    published_stale = published_age is None or published_age > FRESH_LOOP_SECONDS
    if fresh and own_rows and status in {"running", "completed"} and not published_stale:
        return check(
            "master_loop",
            "Master Loop status",
            "OK",
            f"cycle {cycle} {status}, {process_note(own_rows)}",
            **details,
        )
    if own_rows or rows or fresh:
        reason = f"state file says cycle {cycle} {status}"
        if age is not None:
            reason += f" ({int(age)}s old)"
        if not own_rows and rows:
            reason += f"; live processes are outside this tree: {process_note(rows)}"
        elif not rows:
            reason += "; no master loop process is running"
        if published_stale:
            reason += "; data/loop_status.json is stale"
        return check("master_loop", "Master Loop status", "WARNING", reason, **details)

    shown_age = "unknown age" if age is None else f"{int(age)}s old"
    return check(
        "master_loop",
        "Master Loop status",
        "ERROR",
        f"master loop is not live ({status}, {shown_age})",
        **details,
    )


def check_cognitive_core() -> dict[str, Any]:
    compile_errors: list[str] = []
    for relative in COGNITIVE_MODULES:
        path = ROOT / relative
        if not path.exists():
            compile_errors.append(f"{relative} missing")
            continue
        try:
            compile(path.read_text(encoding="utf-8"), str(path), "exec")
        except (OSError, SyntaxError) as exc:
            compile_errors.append(f"{relative}: {exc}")

    report, report_error = read_json(COGNITIVE_REPORT)
    details: dict[str, Any] = {"compile_errors": compile_errors}
    if compile_errors:
        return check(
            "cognitive_core",
            "Cognitive Core status",
            "ERROR",
            "; ".join(compile_errors),
            **details,
        )
    if not isinstance(report, dict):
        return check(
            "cognitive_core",
            "Cognitive Core status",
            "ERROR",
            f"cognitive report unreadable: {report_error}",
            **details,
        )

    stamp = str(report.get("timestamp") or "")
    age = age_seconds(stamp)
    details["report_timestamp"] = stamp
    details["age_seconds"] = None if age is None else round(age, 1)
    required = ("timestamp", "observation", "context", "reasoning", "goals")
    missing_keys = [key for key in required if key not in report]
    if missing_keys:
        return check(
            "cognitive_core",
            "Cognitive Core status",
            "ERROR",
            "cognitive report missing " + ", ".join(missing_keys),
            **details,
        )
    if age is None or age > FRESH_REPORT_SECONDS:
        shown = "undated" if age is None else f"{int(age // 60)} min old"
        return check(
            "cognitive_core",
            "Cognitive Core status",
            "WARNING",
            f"modules compile; last cognitive report is {shown}",
            **details,
        )
    context = report.get("context") if isinstance(report.get("context"), dict) else {}
    if context.get("status") not in (None, "ok", "success", "healthy"):
        return check(
            "cognitive_core",
            "Cognitive Core status",
            "WARNING",
            f"last cycle context status is {context.get('status')}",
            **details,
        )
    return check(
        "cognitive_core",
        "Cognitive Core status",
        "OK",
        f"last cognitive report {stamp}",
        **details,
    )


def check_mpc() -> dict[str, Any]:
    if str(ROOT) not in sys.path:
        sys.path.insert(0, str(ROOT))
    import_error = None
    status: dict[str, Any] | None = None
    try:
        from projects.MCP.mpc_core import mpc

        raw = mpc.status()
        if isinstance(raw, dict):
            status = raw
        else:
            import_error = f"mpc.status() returned {type(raw).__name__}"
    except Exception as exc:  # noqa: BLE001 - import and status failures are diagnostic results
        import_error = f"{type(exc).__name__}: {exc}"

    endpoint = http_get(f"{LOCAL_BASE}/mpc/status")
    details = {"in_process": status, "endpoint": endpoint}
    endpoint_payload = endpoint.get("payload") if isinstance(endpoint.get("payload"), dict) else None
    endpoint_online = bool(endpoint.get("ok") and endpoint_payload and endpoint_payload.get("status") == "online")

    if import_error and not endpoint_online:
        return check("mpc", "MPC status", "ERROR", import_error, **details)
    if endpoint_online and status is not None:
        pending = endpoint_payload.get("pending_goals", status.get("pending_goals"))
        queued = endpoint_payload.get("queue_size", status.get("queue_size"))
        return check(
            "mpc",
            "MPC status",
            "OK",
            f"online, pending goals {pending}, queue {queued}",
            **details,
        )
    if status is not None:
        return check(
            "mpc",
            "MPC status",
            "WARNING",
            "MPC module loads, but /mpc/status is not reachable",
            **details,
        )
    return check("mpc", "MPC status", "ERROR", import_error or "MPC status unavailable", **details)


def check_fastapi() -> dict[str, Any]:
    health = http_get(f"{LOCAL_BASE}/health")
    status = http_get(f"{LOCAL_BASE}/status")
    details = {"health": health, "status": status}
    health_payload = health.get("payload") if isinstance(health.get("payload"), dict) else {}
    status_payload = status.get("payload") if isinstance(status.get("payload"), dict) else {}
    if health.get("ok") and health_payload.get("status") in {"ok", "online", "healthy"} and status.get("ok"):
        service = status_payload.get("service") or status_payload.get("status") or "online"
        return check("fastapi", "FastAPI status", "OK", f"/health ok, /status {service}", **details)
    if health.get("ok") or status.get("ok"):
        return check(
            "fastapi",
            "FastAPI status",
            "WARNING",
            "API answered but /health and /status do not both look healthy",
            **details,
        )
    error = health.get("error") or status.get("error") or "no response"
    return check("fastapi", "FastAPI status", "ERROR", f"API unreachable: {error}", **details)


def check_dashboard() -> dict[str, Any]:
    index = ROOT / "webui" / "index.html"
    assets = [index, ROOT / "webui" / "style.css", ROOT / "webui" / "app.js"]
    missing = [str(path.relative_to(ROOT)) for path in assets if not path.exists()]
    page = http_get(f"{LOCAL_BASE}/") if port_open("127.0.0.1", 8000) else {"ok": False, "error": "port 8000 closed"}
    body = page.get("payload") if isinstance(page.get("payload"), str) else ""
    served = page.get("ok") and ("AI-LAB" in body or "Command Center" in body)
    legacy = Path(r"E:\AI-Learning-Studio\app\dashboard.py")
    details = {
        "missing_assets": missing,
        "served": bool(served),
        "legacy_dashboard": str(legacy),
        "legacy_dashboard_exists": legacy.exists(),
    }
    if missing:
        return check(
            "dashboard",
            "Dashboard status",
            "ERROR",
            "missing " + ", ".join(missing),
            **details,
        )
    if served:
        note = "" if legacy.exists() else "; legacy Dashboard-Runtime target is absent"
        return check("dashboard", "Dashboard status", "OK", f"web UI is served at {LOCAL_BASE}/{note}", **details)
    return check(
        "dashboard",
        "Dashboard status",
        "WARNING",
        "web UI files exist, but the dashboard is not being served",
        **details,
    )


def ollama_models() -> tuple[list[str], dict[str, Any]]:
    result = http_get(f"{OLLAMA_BASE}/api/tags")
    payload = result.get("payload") if isinstance(result.get("payload"), dict) else {}
    models = []
    for item in payload.get("models", []) if isinstance(payload, dict) else []:
        if isinstance(item, dict) and item.get("name"):
            models.append(str(item["name"]))
    return models, result


def model_matches(name: str, expected: str) -> bool:
    target = expected.strip().lower()
    candidate = name.strip().lower()
    return candidate == target or candidate.startswith(target + ":") or candidate.split(":", 1)[0] == target


def check_ollama() -> tuple[dict[str, Any], list[str]]:
    models, result = ollama_models()
    details = {"endpoint": f"{OLLAMA_BASE}/api/tags", "result": result, "models": models}
    if result.get("ok"):
        return check(
            "ollama",
            "Ollama connectivity",
            "OK",
            f"{len(models)} model(s) visible at {OLLAMA_BASE}",
            **details,
        ), models
    return check(
        "ollama",
        "Ollama connectivity",
        "WARNING",
        f"Ollama unreachable at {OLLAMA_BASE}: {result.get('error', 'request failed')}",
        **details,
    ), models


def check_active_model(models: list[str], ollama_level: str) -> dict[str, Any]:
    registry, registry_error = read_json(ROOT / "registry" / "models_registry.json")
    matched = [name for name in models if model_matches(name, ACTIVE_MODEL)]
    details = {
        "expected": ACTIVE_MODEL,
        "matched": matched,
        "registry_error": registry_error,
        "registry_declares_expected": isinstance(registry, dict)
        and any(model_matches(name, ACTIVE_MODEL) for name in registry),
    }
    if matched:
        return check("model", "Active model availability", "OK", "available: " + ", ".join(matched), **details)
    if ollama_level != "OK":
        return check(
            "model",
            "Active model availability",
            "WARNING",
            f"cannot verify {ACTIVE_MODEL} because Ollama is offline",
            **details,
        )
    return check(
        "model",
        "Active model availability",
        "ERROR",
        f"{ACTIVE_MODEL} is not in the Ollama model list",
        **details,
    )


def check_node(check_id: str, name: str, url: str, *, offline_level: str) -> dict[str, Any]:
    result = http_get(url)
    payload = result.get("payload") if isinstance(result.get("payload"), dict) else {}
    details = {"url": url, "result": result, "local_ipv4": local_ipv4()}
    if result.get("ok"):
        status = payload.get("status", "online")
        return check(check_id, name, "OK", f"{url} responded ({status})", **details)
    return check(
        check_id,
        name,
        offline_level,
        f"unreachable: {result.get('error', 'request failed')}",
        **details,
    )


def sqlite_probe(path: Path) -> dict[str, Any]:
    uri = path.resolve().as_uri() + "?mode=ro"
    try:
        connection = sqlite3.connect(uri, uri=True, timeout=3)
    except sqlite3.Error as exc:
        return {"path": str(path), "ok": False, "error": str(exc)}
    try:
        tables = [
            row[0]
            for row in connection.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name")
        ]
        count = None
        if "memory" in tables:
            count = connection.execute("SELECT COUNT(*) FROM memory").fetchone()[0]
        return {"path": str(path), "ok": True, "tables": tables, "memory_rows": count}
    except sqlite3.Error as exc:
        return {"path": str(path), "ok": False, "error": str(exc)}
    finally:
        connection.close()


def check_database() -> dict[str, Any]:
    probes = []
    for candidate in DB_CANDIDATES:
        if candidate is not None and candidate.exists():
            probes.append(sqlite_probe(candidate))
    json_store = ROOT / "database" / "memory.json"
    json_ok = False
    json_error = None
    if json_store.exists():
        payload, json_error = read_json(json_store)
        json_ok = json_error is None and isinstance(payload, (dict, list))
    details = {"sqlite": probes, "json_store": str(json_store), "json_store_ok": json_ok}
    readable = [probe for probe in probes if probe.get("ok")]
    if readable:
        best = readable[0]
        rows = best.get("memory_rows")
        row_text = "memory table absent" if rows is None else f"{rows} memory rows"
        return check("database", "Database accessibility", "OK", f"{best['path']} ({row_text})", **details)
    if probes:
        return check(
            "database",
            "Database accessibility",
            "ERROR",
            "chat.db exists but cannot be read: " + probes[0].get("error", "unknown error"),
            **details,
        )
    if json_ok:
        return check(
            "database",
            "Database accessibility",
            "WARNING",
            "chat.db was not found; only database/memory.json is readable",
            **details,
        )
    return check(
        "database",
        "Database accessibility",
        "ERROR",
        "no readable chat.db at D:\\AI-Server, E:\\AI-Server, or the project database directory",
        **details,
    )


def cognitive_report_status() -> tuple[str, str, dict[str, Any]]:
    payload, error = read_json(COGNITIVE_REPORT)
    if not isinstance(payload, dict):
        return "ERROR", f"cognitive_report.json {error}", {"path": str(COGNITIVE_REPORT)}
    required = ("timestamp", "observation", "context", "reasoning", "goals")
    missing = [key for key in required if key not in payload]
    if missing:
        return "ERROR", "cognitive report missing " + ", ".join(missing), {"path": str(COGNITIVE_REPORT)}
    try:
        json.loads(json.dumps(payload))
    except (TypeError, ValueError) as exc:
        return "ERROR", f"cognitive report is not serializable: {exc}", {"path": str(COGNITIVE_REPORT)}
    age = age_seconds(str(payload.get("timestamp") or ""))
    details = {
        "path": str(COGNITIVE_REPORT),
        "timestamp": payload.get("timestamp"),
        "age_seconds": None if age is None else round(age, 1),
    }
    if age is None or age > FRESH_REPORT_SECONDS:
        shown = "undated" if age is None else f"{int(age // 60)} min old"
        return "WARNING", f"cognitive report is valid but {shown}", details
    return "OK", f"cognitive report generated at {payload.get('timestamp')}", details


def score_of(checks: list[dict[str, Any]]) -> int:
    total = 0
    for item in checks:
        weight = int(item["weight"])
        if item["level"] == "OK":
            total += weight
        elif item["level"] == "WARNING":
            total += weight // 2
    return max(0, min(100, total))


def summary_of(checks: list[dict[str, Any]]) -> dict[str, int]:
    return {
        "ok": sum(1 for item in checks if item["level"] == "OK"),
        "warning": sum(1 for item in checks if item["level"] == "WARNING"),
        "error": sum(1 for item in checks if item["level"] == "ERROR"),
    }


def build_report(checks: list[dict[str, Any]]) -> dict[str, Any]:
    return {
        "generated_at": datetime.now().isoformat(timespec="seconds"),
        "project_root": str(ROOT),
        "version": "7.1.0",
        "health_score": score_of(checks),
        "summary": summary_of(checks),
        "checks": checks,
    }


def write_report(report: dict[str, Any], path: Path) -> tuple[bool, str | None]:
    try:
        path.parent.mkdir(parents=True, exist_ok=True)
        text = json.dumps(report, indent=4, ensure_ascii=False)
        json.loads(text)
        path.write_text(text + "\n", encoding="utf-8")
        written, error = read_json(path)
        if error:
            return False, error
        if not isinstance(written, dict) or written.get("health_score") != report["health_score"]:
            return False, "written report did not round-trip"
        return True, None
    except (OSError, TypeError, ValueError) as exc:
        return False, str(exc)


def assemble(report_path: Path) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    processes = lab_processes()
    checks = [
        check_python(),
        check_dependencies(),
        check_runtime(processes),
        check_master_loop(processes),
        check_cognitive_core(),
        check_mpc(),
        check_fastapi(),
        check_dashboard(),
    ]
    ollama, models = check_ollama()
    checks.append(ollama)
    checks.append(check_active_model(models, ollama["level"]))
    checks.append(check_node("node41", "Node41 connectivity", NODE41_URL, offline_level="ERROR"))
    checks.append(check_node("node56", "Node56 connectivity", NODE56_URL, offline_level="WARNING"))

    report_level, report_message, report_details = cognitive_report_status()
    checks.append(
        check(
            "json_report",
            "JSON report generation",
            report_level,
            report_message,
            **report_details,
        )
    )
    checks.append(check_database())

    json_check = checks[-2]
    json_details = dict(json_check.get("details") or {})
    json_details["diagnostics_report"] = str(report_path)
    json_check["details"] = json_details

    report = build_report(checks)
    written, write_error = write_report(report, report_path)
    json_details["diagnostics_report_written"] = written
    if not written:
        json_check["level"] = "ERROR"
        json_check["message"] = f"failed to write diagnostics report: {write_error}"
        report = build_report(checks)
        write_report(report, report_path)
    elif json_check["level"] == "OK":
        json_check["message"] = f"{json_check['message']}; diagnostics report written to {report_path.name}"
        report = build_report(checks)
        write_report(report, report_path)
    return checks, report


def print_checks(checks: list[dict[str, Any]], health_score: int, report_path: Path) -> None:
    for item in checks:
        print(f"[{item['level']}] {item['name']} - {item['message']}")
    print(f"SYSTEM HEALTH SCORE: {health_score}/100")
    print(f"REPORT: {report_path}")


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="AI-LAB production diagnostics")
    parser.add_argument(
        "--output",
        type=Path,
        default=REPORT_PATH,
        help="path of the JSON report (default: data/diagnostics_report.json)",
    )
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(sys.argv[1:] if argv is None else argv)
    checks, report = assemble(args.output)
    print_checks(checks, report["health_score"], args.output)
    return 1 if any(item["level"] == "ERROR" for item in checks) else 0


if __name__ == "__main__":
    raise SystemExit(main())
