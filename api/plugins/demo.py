from typing import Literal
from pydantic import BaseModel

class DemoVMConfig(BaseModel):
    name: str
    cpu: int
    mem: int

class DemoVM(BaseModel):
    type: Literal["demo"]
    config: DemoVMConfig
