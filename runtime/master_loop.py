import json
import os
import traceback

from pathlib import Path
from datetime import datetime, timezone
from threading import Event

from cognitive_core.cognitive_loop import run_cycle

BASE_DIR = Path(__file__).resolve().parent.parent

STATE_FILE = Path(
    os.getenv(
        "AI_LAB_MASTER_STATE_FILE",
        str(BASE_DIR / "data" / "master_loop_state.json")
    )
)

CYCLE_INTERVAL = max(
    1,
    int(os.getenv("AI_LAB_CYCLE_INTERVAL", "300"))
)


class MasterLoop:

    def __init__(self, interval=None):
        self.cycle = 0
        self.status = "starting"
        self.interval = max(
            1,
            int(CYCLE_INTERVAL if interval is None else interval)
        )
        self.stop_event = Event()

    def stop(self):
        self.stop_event.set()

    def save_state(self, message=""):

        STATE_FILE.parent.mkdir(
            parents=True,
            exist_ok=True
        )

        data = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "cycle": self.cycle,
            "status": self.status,
            "message": message
        }

        tmp = STATE_FILE.with_suffix(".tmp")

        tmp.write_text(
            json.dumps(
                data,
                indent=2,
                ensure_ascii=False
            ),
            encoding="utf-8"
        )

        tmp.replace(STATE_FILE)

    def run(self, max_cycles=None):

        completed = 0

        while (
            not self.stop_event.is_set()
            and (
                max_cycles is None
                or completed < max_cycles
            )
        ):

            self.cycle += 1

            try:

                self.status = "running"
                self.save_state()

                result = run_cycle()

                status_file = (
                    BASE_DIR
                    / "data"
                    / "loop_status.json"
                )

                status_file.parent.mkdir(
                    parents=True,
                    exist_ok=True
                )

                loop_status = {
                    "status": "online",
                    "cycle": self.cycle,
                    "timestamp": datetime.now(
                        timezone.utc
                    ).isoformat(),
                    "result": result
                }

                with open(
                    status_file,
                    "w",
                    encoding="utf-8"
                ) as f:

                    json.dump(
                        loop_status,
                        f,
                        indent=2,
                        ensure_ascii=False
                    )

                self.status = "completed"

                self.save_state(
                    json.dumps(
                        result,
                        ensure_ascii=False
                    )
                )

            except KeyboardInterrupt:

                self.stop_event.set()

                self.status = "stopped"

                self.save_state(
                    "manual stop"
                )

                break

            except Exception as exc:

                self.status = "error"

                self.save_state(
                    f"{type(exc).__name__}: {exc}"
                )

                traceback.print_exc()

            completed += 1

            if (
                max_cycles is not None
                and completed >= max_cycles
            ):
                break

            self.stop_event.wait(
                self.interval
            )

        if (
            self.stop_event.is_set()
            and self.status != "error"
        ):
            self.status = "stopped"
            self.save_state(
                "stop requested"
            )


if __name__ == "__main__":
    MasterLoop().run()