from enum import Enum
from typing import List
from pydantic import BaseModel

class ByteUnit(Enum):
    MB = 1
    GB = 2
    TB = 3

class NetworkConfig(BaseModel):
    pass

class VSphereNetworkConfig(NetworkConfig):
    adapterType: str
    vlan_name: str

class ProviderConfig(BaseModel):
    pass

class Disk(BaseModel):
    size: int
    unit: ByteUnit

class VSphereGuestConfig(BaseModel):
    userdata: str
    metadata: str
    vendordata: str

class vSphereProviderConfig(ProviderConfig):
    cpu_cores: int
    memory: int
    disk: List[Disk]
    network: List[NetworkConfig]
    guestconfig: VSphereGuestConfig

class Machine(BaseModel):
    hostname: str
    providerConfig: ProviderConfig
