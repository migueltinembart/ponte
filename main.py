from loguru import logger
import redis
from config import NoCredentialsError, generate_Credentials
from fastapi import FastAPI
from api import events

logger.info("Loading Routes")

try:
    credentials = generate_Credentials()
except NoCredentialsError as e:
    logger.error("Missing required environment variables, shutting down ponte", e)
    exit(1)



events.initialize_threads(azure_credentials=credentials["azure"], redis=credentials['redis'])

app = FastAPI()

# app.include_router(deployments.router)
app.include_router(events.router)

@app.get("/")
async def root():
    return {"message": "Nothing to see here"}
