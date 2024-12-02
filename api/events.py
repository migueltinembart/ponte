from typing import Any, Dict, Literal
from fastapi import APIRouter
from .models.gh_pr import PullRequestEvent  

allowed_providers = Literal["github", "bitbucket"]

router = APIRouter(prefix="/events")

@router.post("/{provider}")
def react_to_webhook(provider: allowed_providers, payload: PullRequestEvent):
    if provider == "github":
        if payload is PullRequestEvent:

    return {'event': "done"}


