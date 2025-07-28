from fastapi import FastAPI
from src.utils.logging_config import setup_logging
from src.utils.exceptions import CustomException

setup_logging()
app = FastAPI()

@app.get("/health")
def health():
    return {"status": "ok"}


