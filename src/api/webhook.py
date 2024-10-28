from typing import Any, Dict
from fastapi import FastAPI

app = FastAPI()

@app.post("/events/{provider}")
def react_to_webhook(provider: str, payload: Dict[Any, Any]):
    return {'event': "done"}



