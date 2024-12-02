from typing import List, Literal, Optional, Union
from pydantic import Base64Str, BaseModel

class AzureEnvironment(BaseModel):
    subscription: str
    resource_group: str

class AzureOSConfig(BaseModel):
    publisher: str
    offer: str
    sku: str
    version: str

class AzurePrivateIPConfig(BaseModel):
    primary: bool = False
    subscription: Optional[str] = None
    resource_group: str
    vnet_name: str
    subnet: str

class AzureCPUConfig(BaseModel):
    size: str

class AzureVMAccessConfig(BaseModel):
    username: str
    public_key_values: List[str]

class AzureCustomizationConfig(BaseModel):
    access: AzureVMAccessConfig
    userdata: Base64Str

class AzureStorageConfig(BaseModel):
    type: Literal["primary", "data"]
    size: int
    disk_type: Literal["Standard_LRS", "Premium_LRS", "StandardSSD_LRS", "UltraSSD_LRS", "Premium_ZRS", "StandardSSD_ZRS", "PremiumV2_LRS"]

class AzureVMAddons(BaseModel):
    defender: bool = False
    managed_identity: bool = False
    entra_id_login_enabled: bool = False

class AzureVMConfig(BaseModel):
    environment: AzureEnvironment
    availability_zones: Union[int, List[int]]
    cpu_config: AzureCPUConfig
    os_config: AzureOSConfig
    network_config: List[Union[AzurePrivateIPConfig, AzurePublicIPConfig]]
    customization: AzureCustomizationConfig
    storage_config: List[AzureStorageConfig]
    addons: Optional[AzureVMAddons]

class AzureVM(BaseModel):
    type: Literal["azure"]
    config: AzureVMConfig



