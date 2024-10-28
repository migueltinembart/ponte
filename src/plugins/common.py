from typing import Union
from pydantic import BaseModel, Field
from uuid import UUID, uuid4
import json
from demo.model import DemoModel
from vsphere.model import VsphereVMConfig


class Deployment(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    job: Union[VsphereVMConfig, DemoModel] = Field(..., discriminator="plugin")

schema = Deployment.model_json_schema()

print(json.dumps(schema))
