import subprocess
import requests

class NetworkAgent:

    def ping(self, host):

        result = subprocess.run(
            ["ping", "-n", "1", host],
            capture_output=True,
            text=True
        )

        return result.returncode == 0

    def status(self):

        return {
            "node_41": self.ping("192.168.1.41"),
            "node_56": self.ping("192.168.1.56")
        }

 