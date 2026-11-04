import json
import os
import tempfile
import unittest
from unittest.mock import Mock
import requests

class ImportTests(unittest.TestCase):
    def test_critical_imports(self):
        import cognitive_core.cognitive_loop
        import cognitive_core.reasoning_engine
        import framework.resource_manager
        import framework.model_selector
        import projects.MCP.mpc_core
        import runtime.master_loop

class Provider:
    def __init__(self, value=None, error=None): self.value, self.error = value, error
    def collect(self):
        if self.error: raise self.error
        return self.value

class ResourceTests(unittest.TestCase):
    def test_provider_failure_isolated(self):
        from framework.resource_manager import ResourceManager
        result = ResourceManager({"ok": Provider({"usage": 10}), "bad": Provider(error=RuntimeError("boom"))}).collect()
        self.assertEqual(result["ok"]["usage"], 10)
        self.assertEqual(result["bad"]["status"], "error")

    def test_node_connection_success_and_timeout(self):
        from framework.providers.node_provider import NodeProvider
        session = Mock(); response = Mock(); response.ok = True; response.json.return_value = {"status": "ok"}
        session.get.return_value = response
        self.assertEqual(NodeProvider("http://node56", session=session).collect()["status"], "online")
        session.get.side_effect = requests.Timeout("timeout")
        self.assertEqual(NodeProvider("http://node56", session=session).collect()["status"], "offline")

class CognitiveTests(unittest.TestCase):
    def test_model_selector_missing_and_pressure(self):
        from framework.model_selector import ModelSelector
        selector = ModelSelector()
        self.assertIsNone(selector.select({}))
        self.assertEqual(selector.select({"cpu":{"usage":95},"ollama":{"models":["phi3:latest","llama3.1:latest"]}}), "phi3:latest")

    def test_goal_generator_allowlist_dedupe_and_priority(self):
        from cognitive_core.goal_generator import GoalGenerator
        data = {"goals":[{"goal":"Monitor Node56","priority":99},{"goal":"Monitor Node56"},{"goal":"arbitrary command","priority":10}]}
        goals = GoalGenerator().parse(json.dumps(data))
        self.assertEqual(len(goals), 1); self.assertEqual(goals[0]["priority"], 10)

    def test_reasoning_fallback_no_model(self):
        from cognitive_core.reasoning_engine import reason
        result = json.loads(reason({"problems":["Node56 offline"]}, resources={"ollama":{"models":[]}}))
        self.assertEqual(result["goals"][0]["goal"], "Monitor Node56")

class MPCTests(unittest.TestCase):
    def test_planner_and_decision_engine_mapping(self):
        from projects.MCP.planner import Planner
        from projects.MCP.decision_engine import DecisionEngine
        planner, engine = Planner(), DecisionEngine()
        tasks = {task for goal in planner.TEMPLATES for task in planner.build(goal)}
        self.assertFalse(tasks - set(engine.MAP))
        self.assertEqual(planner.build("unknown goal"), [])

    def test_executor_unknown_task_does_not_fake_success(self):
        from projects.MCP import executor as executor_module
        from projects.MCP.task_queue import TaskQueue
        queue = TaskQueue(); queue.enqueue("unknown_task")
        old = executor_module.task_queue
        try:
            executor_module.task_queue = queue
            result = executor_module.Executor(session=Mock()).execute()
            self.assertEqual(result["status"], "unknown_task")
        finally: executor_module.task_queue = old

    def test_remote_retry_is_bounded_and_queue_drains(self):
        from projects.MCP import executor as executor_module
        from projects.MCP.task_queue import TaskQueue
        queue = TaskQueue(); queue.enqueue("node_sync")
        session = Mock(); session.post.side_effect = requests.Timeout("timeout")
        old = executor_module.task_queue
        try:
            executor_module.task_queue = queue
            result = executor_module.Executor(worker_url="http://127.0.0.1:8000/worker/execute", max_attempts=2, session=session).execute()
            self.assertEqual(result["status"], "failed"); self.assertEqual(result["attempts"], 2)
            self.assertEqual(queue.size(), 0); self.assertEqual(session.post.call_count, 2)
        finally: executor_module.task_queue = old

class LoopAndFeedbackTests(unittest.TestCase):
    def test_execute_tasks_has_budget(self):
        from cognitive_core import cognitive_loop
        from projects.MCP import task_queue as queue_module
        old_queue = queue_module.task_queue
        class FakeQueue:
            def size(self): return 3
        class FakeMPC:
            def __init__(self): self.n = 0
            def status(self): return {"queue_size": 3-self.n}
            def execute_next(self): self.n += 1; return {"status":"ok"}
        old_mpc = cognitive_loop.mpc
        try:
            fake = FakeMPC(); cognitive_loop.mpc = fake
            results = cognitive_loop.execute_tasks(max_tasks=2)
            self.assertEqual(len(results), 3)  # two results plus a deferred marker
            self.assertEqual(results[-1]["status"], "deferred")
        finally: cognitive_loop.mpc = old_mpc



    def test_master_loop_single_cycle_and_state_file(self):
        from runtime import master_loop
        from pathlib import Path
        from unittest.mock import patch
        with tempfile.TemporaryDirectory() as tmp:
            with patch.object(master_loop, "STATE_FILE", Path(tmp) / "state.json"), \
                 patch.object(master_loop, "run_cycle", return_value={"status":"success"}):
                loop = master_loop.MasterLoop(interval=1)
                loop.run(max_cycles=1)
                with open(Path(tmp) / "state.json", encoding="utf-8") as handle:
                    state = json.load(handle)
                self.assertEqual(state["cycle"], 1)
                self.assertEqual(state["status"], "completed")

    def test_full_cognitive_cycle_with_mocked_services(self):
        from cognitive_core import cognitive_loop
        from pathlib import Path
        from unittest.mock import patch
        old_data, old_report, old_feedback = cognitive_loop.DATA_DIR, cognitive_loop.REPORT_FILE, cognitive_loop.FEEDBACK_FILE
        try:
            with tempfile.TemporaryDirectory() as tmp:
                cognitive_loop.DATA_DIR = Path(tmp)
                cognitive_loop.REPORT_FILE = Path(tmp) / "report.json"
                cognitive_loop.FEEDBACK_FILE = Path(tmp) / "feedback.json"
                observation = {"node41":"online", "node56":"offline", "cpu":{"usage":10,"status":"healthy"},
                               "memory":{"usage":30}, "ollama":{"status":"offline","models":[]}, "alerts":["Node56 offline"]}
                with patch.object(cognitive_loop, "build_observation", return_value=observation), \
                     patch.object(cognitive_loop, "reason", return_value='{"goals":[{"goal":"Monitor Node56","priority":9}]}'), \
                     patch.object(cognitive_loop, "mpc") as fake_mpc:
                    fake_mpc.create_goal.return_value = {"id":1,"goal":"Monitor Node56","status":"pending"}
                    fake_mpc.status.return_value = {"queue_size":0,"status":"online"}
                    result = cognitive_loop.run_cycle()
                self.assertEqual(result["status"], "success")
                self.assertTrue(cognitive_loop.REPORT_FILE.exists())
                self.assertTrue(cognitive_loop.FEEDBACK_FILE.exists())
                with open(cognitive_loop.FEEDBACK_FILE, encoding="utf-8") as handle:
                    self.assertEqual(json.load(handle)[-1]["results"], [])
        finally:
            cognitive_loop.DATA_DIR, cognitive_loop.REPORT_FILE, cognitive_loop.FEEDBACK_FILE = old_data, old_report, old_feedback

    def test_feedback_is_valid_json_and_bounded(self):
        from cognitive_core import cognitive_loop
        old_data, old_file = cognitive_loop.DATA_DIR, cognitive_loop.FEEDBACK_FILE
        try:
            with tempfile.TemporaryDirectory() as tmp:
                cognitive_loop.DATA_DIR = tmp
                cognitive_loop.FEEDBACK_FILE = __import__("pathlib").Path(tmp) / "feedback.json"
                for i in range(205): cognitive_loop.save_feedback([{"i":i}])
                with open(cognitive_loop.FEEDBACK_FILE, encoding="utf-8") as handle:
                    history = json.load(handle)
                self.assertEqual(len(history), 200); self.assertEqual(history[-1]["results"][0]["i"], 204)
        finally:
            cognitive_loop.DATA_DIR, cognitive_loop.FEEDBACK_FILE = old_data, old_file

if __name__ == "__main__": unittest.main()

class Node56WorkerTests(unittest.TestCase):
    def test_worker_health_and_unconfigured_task(self):
        from framework.node56_worker import ExecuteRequest, health, execute_task
        self.assertEqual(health()["status"], "ok")
        result = execute_task(ExecuteRequest(task="node_sync"))
        self.assertEqual(result["status"], "unavailable")

    def test_worker_registered_handler_and_failure(self):
        from framework.node56_worker import ExecuteRequest, register_handler, unregister_handler, execute_task
        register_handler("test_task", lambda request: {"echo": request["payload"].get("value")})
        try:
            result = execute_task(ExecuteRequest(task="test_task", payload={"value": 42}))
            self.assertEqual(result["status"], "completed")
            self.assertEqual(result["result"]["echo"], 42)
        finally:
            unregister_handler("test_task")
        register_handler("broken_task", lambda request: 1 / 0)
        try:
            result = execute_task(ExecuteRequest(task="broken_task"))
            self.assertEqual(result["status"], "failed")
        finally:
            unregister_handler("broken_task")
