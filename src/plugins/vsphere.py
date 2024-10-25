from typing import Dict, Optional, Union
from enum import Enum
import requests
import urllib3
from pydantic import Base64Str, BaseModel, HttpUrl, ValidationInfo, field_validator, TypeAdapter
from vmware.vapi.vsphere.client import create_vsphere_client 
import re
import json

def vSphereClientFactory(server: str, username: str, password: str):
    session = requests.session()

    session.verify = False

    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

    return create_vsphere_client(server=server, username=username, password=password, session=session)

class NICType(str, Enum):
    vmxnet3 = "vmxnet3"
    e1000 = "E1000"

class DiskType(str, Enum):
    thin = "thin"
    thick = "thick"

class Disk(BaseModel):
    type: DiskType

class NIC(BaseModel):
    vnet: str
    type: NICType

class ISOSource(BaseModel):
    url: HttpUrl

class TemplateSource(BaseModel):
    path: str

class VMDKSource(BaseModel):
    url: HttpUrl

class Customization(BaseModel):
    metadata: Optional[Base64Str]
    vendordata: Optional[Base64Str]
    userdata: Optional[Base64Str]

class VM(BaseModel):
    name: str
    cpu: int
    mem: int
    nic: Dict[str, NIC]
    disk: Dict[str, Disk]
    source: ISOSource | TemplateSource | VMDKSource
    customization: Union[Customization, None] = None

    @field_validator("source")
    def check_Template_path(cls, v: TemplateSource, info: ValidationInfo) -> TemplateSource:
        if isinstance(v, TemplateSource):
            pattern = '^(\\/)?(?:[a-zA-Z0-9._-]+\\/?)+$'
            is_path = re.search(pattern, v.path)
            assert is_path,  f"{info.field_name} must be a path"
        return v

vm = VM(name="sl911245", cpu=2, mem=2048, nic={'nic1': NIC(vnet="2", type=NICType.vmxnet3) }, disk={"disk1": Disk(type=DiskType.thin)}, source=TemplateSource(path="/whatever"), customization=None)

customvm = {'name': "sl911245", 'cpu': 2, 'mem': 2048, 'nic': { 'nic1': { 'vnet': "2", 'type': "vmxnet3"}}, 'disk': {'disk1': {'type': "thin"}}, 'source': {'url': "https://test.com"}}

test = vm.model_dump()


ta = TypeAdapter(VM)
ob = ta.validate_python(customvm)

print(json.dumps(vm.model_json_schema()))
