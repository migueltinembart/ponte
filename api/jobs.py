from typing import Literal, Optional, Any
from pydantic import BaseModel
from pydantic.types import UUID4

class Job(BaseModel):
    id: UUID4
    status: Literal["registered", "started", "failed", "done"]
    service: Optional[Any]

    
