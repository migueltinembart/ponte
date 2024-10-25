from enum import Enum
from typing import Any, Dict, Optional
from fastapi import FastAPI
import logging

from pydantic import BaseModel
app = FastAPI()

@app.post("/events/{provider}")
def react_to_webhook(provider: str, payload: Dict[Any, Any]):
    
    logging.info(payload)
    return {'event': "done"}

