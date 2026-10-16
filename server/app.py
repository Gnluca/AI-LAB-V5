from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

app = FastAPI(
    title="AI LAB V6",
    version="6.0"
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def home():
    return {
        "name": "AI LAB V6",
        "status": "online"
    }

@app.get("/status")
def status():
    return {
        "status": "online",
        "ollama": "online",
        "model": "llama3.1"
    }

@app.get("/health")
def health():
    return {
        "healthy": True
    }

if __name__ == "__main__":
    uvicorn.run(
        "app:app",
        host="0.0.0.0",
        port=8000,
        reload=False
    )
