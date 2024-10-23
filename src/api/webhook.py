from typing import Any, Dict
from fastapi import FastAPI
import logging

from pydantic import BaseModel
app = FastAPI()

class Test(BaseModel):
    test: str

@app.post("/events/{provider}")
def react_to_webhook(provider: str, payload: Dict[Any, Any]):
    if provider == "github":
        return {'provider': "Github"}

    logging.info(payload)
    return {'event': "done"}

