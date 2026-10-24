# test_node56.py

import requests

r = requests.get(
    "http://192.168.1.56:8000/status",
    timeout=5
)

print(r.json())