from typing import Literal, Union, Any
from uuid import UUID, uuid4
from fastapi import APIRouter
from pydantic import BaseModel, Field

from modules.azure.vm import AzureVM

VM = Union[AzureVM, Any]

class Deployment(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    type: Literal["vm"]
    config: VM = Field(..., discriminator='type')

router = APIRouter(
    prefix="/deployment",
    tags=["deployment"],
    responses={404: {'description': "Not found"}}
)

@router.get("/")
async def read_deployments():
    return "Nothing to see here for now"

@router.get("/{deployment_id}")
async def read_deployment(deployment_id: int):
    return deployment_id

