from typing import Any, Optional
from pydantic import BaseModel
from azure.identity import ClientSecretCredential
from api.deployments import Deployment
from api.service import Service
from config import ServerConfig
from .uow import getAzureVMConfig
from azure.mgmt.compute import ComputeManagementClient

class AzureRMresourceDefinition(BaseModel):
    name: str
    resourceGroupName: str 

class Diff(BaseModel):
    expr: bool
    local: Optional[Any] = None
    remote: Optional[Any] = None

def generate_client(client_secret_Credential: ClientSecretCredential, subscription_id: str | None):
    if isinstance(subscription_id, str):
        client = ComputeManagementClient(credential=client_secret_Credential, subscription_id=subscription_id, api_version=ComputeManagementClient.DEFAULT_API_VERSION)
        return client
    else:
        raise ValueError("No subscription id set for this operation")
            

class VMService(Service):
    def __init__(self, deployment: Deployment, client_secret_Credential: ClientSecretCredential):
        self.deployment = deployment
        self.computeClient = generate_client(client_secret_Credential=client_secret_Credential, subscription_id=ServerConfig.azure_subscription_id)

    def check_state(self):
        remoteState = getAzureVMConfig(self.computeClient, resourceDefinition=AzureRMresourceDefinition(name="", resourceGroupName=""))
        if remoteState == self.deployment.config.config:
            return Diff(expr=False)
        else:
            return Diff(expr=True, local=self.deployment.config.config, remote=remoteState)
