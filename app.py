from fastapi import FastAPI

app = FastAPI(
    title="Female Chat API",
    version="1.0.0"
)


@app.get("/")
async def home():
    return {
        "success": True,
        "message": "Female Chat API is running 🚀"
    }


@app.get("/health")
async def health():
    return {
        "status": "ok"
    }