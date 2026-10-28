import json
from pathlib import Path

from runtime.factory import Factory
from runtime.master_loop import MasterLoop


class Agent:
    name = "test"


def test_factory_register_and_get():
    factory = Factory()
    agent = Agent()
    factory.register(agent)
    assert factory.get("test") is agent
    assert factory.status() == {"registered": 1, "agents": ["test"]}


def test_master_loop_writes_atomic_status(tmp_path: Path):
    target = tmp_path / "status.json"
    loop = MasterLoop(status_file=target, log_file=tmp_path / "loop.log")
    result = loop.run_once()
    assert target.exists()
    assert json.loads(target.read_text(encoding="utf-8"))["cycle"] == 1
    assert result["status"] == "online"
