from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def home():
    return {"message": "Hello from CI/CD", "version": "1.0"}

@app.get("/health")
def health():
    return {"status": "ok"}