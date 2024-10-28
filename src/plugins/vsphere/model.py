from typing import Literal, Optional, Union, List
from uuid import UUID, uuid4
import requests
import urllib3
from pydantic import Base64Str, BaseModel, Field
from vmware.vapi.vsphere.client import create_vsphere_client

def vSphereClientFactory(server: str, username: str, password: str):
    session = requests.session()

    session.verify = False

    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

    return create_vsphere_client(server=server, username=username, password=password, session=session)

class VsphereStorageConfig(BaseModel):
    type: Literal["thin", "thick"]
    size: int
    unit: Literal["TB", "GB", "MB"]

class VsphereNetworkConfig(BaseModel):
    type: Literal["vmxnet3", "e1000"]
    vnet: str

class VsphereIsoSource(BaseModel):
    type: Literal["iso"]
    url: str

class VsphereTemplateSource(BaseModel):
    type: Literal["template"]
    target: str

class VsphereCustomizationConfig(BaseModel):
    metadata: Optional[Base64Str]
    vendordata: Optional[Base64Str]
    userdata: Optional[Base64Str]

class VsphereVMConfig(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    plugin: Literal["vsphere"]
    name: str
    cpu: int
    mem: int
    target: str
    networkConf: VsphereNetworkConfig
    storageConf: List[VsphereStorageConfig]
    osConf: Union[VsphereIsoSource, VsphereTemplateSource] = Field(..., discriminator='type')

