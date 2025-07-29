from fastapi import FastAPI
from src.routes import upload
from src.utils.logging_config import setup_logging
from src.utils.exceptions import CustomException

setup_logging()
app = FastAPI()

@app.get("/health")
def health():
    return {"status": "ok"}

app.include_router(upload.router, prefix="/api")


