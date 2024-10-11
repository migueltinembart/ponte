from fastapi import APIRouter, Request

router = APIRouter()

@router.post("/event/{git_provder}")
async def receive_Webhook(git_provder, item: Request):
    print(git_provder)
    body = await item.json()
    return body
