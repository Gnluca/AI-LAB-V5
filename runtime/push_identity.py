# push_identity.py

import requests

identity = {
    "node": "NODE41",
    "role": "PRIMARY",
    "framework": "AI-LAB V6.3",
    "runtime": "ONLINE",
    "ip": "192.168.1.41"
}

response = requests.post(
    "http://192.168.1.56:8000/sync/identity",
    json=identity,
    timeout=10
)

print(response.json())