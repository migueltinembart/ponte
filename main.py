from config import loadEnv
from fastapi import FastAPI
from api import deployments, events

# loadEnv()

app = FastAPI()

app.include_router(deployments.router)
app.include_router(events.router)

@app.get("/")
async def root():
    return {"message": "Nothing to see here"}
