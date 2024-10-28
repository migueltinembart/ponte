from typing import Literal
from uuid import UUID, uuid4
from pydantic import BaseModel, Field


class DemoModel(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    plugin: Literal["demo"]
