from loguru import logger
from config import loadEnv
from fastapi import FastAPI
from api import events

logger.info("Loading Routes")
# loadEnv()

logger.info("Creating Job Queue")

events.initialize_threads()

app = FastAPI()

# app.include_router(deployments.router)
app.include_router(events.router)

@app.get("/")
async def root():
    return {"message": "Nothing to see here"}
