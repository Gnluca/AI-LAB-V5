from network_agent import NetworkAgent

agent = NetworkAgent()

print(agent.status())

import uvicorn

uvicorn.run(
    "server:app",
    host="127.0.0.1",
    port=8000,
    reload=False
)