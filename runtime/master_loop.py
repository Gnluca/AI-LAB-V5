import sys
import json
import time
import traceback

from pathlib import Path
from datetime import datetime

BASE_DIR = Path(__file__).resolve().parent.parent

if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

from cognitive_core.cognitive_loop import run_cycle

STATE_FILE = BASE_DIR / "data" / "master_loop_state.json"

CYCLE_INTERVAL = 300


class MasterLoop:

    def __init__(self):

        self.cycle = 0
        self.status = "starting"

        STATE_FILE.parent.mkdir(
            parents=True,
            exist_ok=True
        )

    def save_state(self, message=""):

        data = {
            "timestamp": datetime.now().isoformat(),
            "cycle": self.cycle,
            "status": self.status,
            "message": message
        }

        with open(
            STATE_FILE,
            "w",
            encoding="utf-8"
        ) as f:

            json.dump(
                data,
                f,
                indent=4,
                ensure_ascii=False
            )

    def banner(self):

        print()
        print("===================================")
        print("AI-LAB MASTER LOOP")
        print("===================================")
        print(
            f"Started: {datetime.now()}"
        )
        print()

    def run(self):

        self.banner()

        while True:

            self.cycle += 1

            try:

                self.status = "running"

                self.save_state()

                print()
                print(
                    f"[CYCLE {self.cycle}]"
                )

                result = run_cycle()

                print()
                print("[RESULT]")
                print(result)

                self.status = "completed"

                self.save_state()

            except KeyboardInterrupt:

                self.status = "stopped"

                self.save_state(
                    "manual stop"
                )

                print()
                print(
                    "[MASTER LOOP STOPPED]"
                )

                break

            except Exception as e:

                self.status = "error"

                self.save_state(
                    str(e)
                )

                print()
                print(
                    "[MASTER LOOP ERROR]"
                )

                print(str(e))

                traceback.print_exc()

            print()
            print(
                f"[WAIT] {CYCLE_INTERVAL} sec"
            )

            time.sleep(
                CYCLE_INTERVAL
            )


if __name__ == "__main__":

    loop = MasterLoop()

    loop.run()