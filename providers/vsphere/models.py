from typing import List
from pydantic import BaseModel
from providers.base import ByteUnit

class VSphereNetworkConfig(BaseModel):
    adapterType: str
    vlan_name: str

class Disk(BaseModel):
    size: int
    unit: ByteUnit

class VSphereGuestConfig(BaseModel):
    userdata: str
    metadata: str
    vendordata: str

class vSphereProviderConfig(BaseModel):
    cpu_cores: int
    memory: int
    disk: List[Disk]
    network: List[VSphereNetworkConfig]
    guestconfig: VSphereGuestConfig

class VSphereMachine(BaseModel):
    hostname: str
    providerConfig: vSphereProviderConfig
