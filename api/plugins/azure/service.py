from typing import Any, Optional
from pydantic import BaseModel
from azure.identity import ClientSecretCredential
from api.deployments import Deployment
from api.plugins.azure.vm import AzureVM
from api.service import Service, Diff
from config import ServerConfig
from store.redis import RedisRepository, redisRepositoryFactory
from .uow import getAzureVM, createAzureVM, deleteAzureVM
from azure.mgmt.compute import ComputeManagementClient
import logging

class AzureRMresourceDefinition(BaseModel):
    name: str
    resourceGroupName: str 

def generate_client(client_secret_Credential: ClientSecretCredential, subscription_id: str | None):
    if isinstance(subscription_id, str):
        client = ComputeManagementClient(credential=client_secret_Credential, subscription_id=subscription_id, api_version=ComputeManagementClient.DEFAULT_API_VERSION)
        return client
    else:
        raise ValueError("No subscription id set for this operation")
        
class VMService(Service[AzureVM]):
    def __init__(self, vm: AzureVM, client_secret_Credential: ClientSecretCredential):
        self.vm = vm 
        self.computeClient = generate_client(client_secret_Credential=client_secret_Credential, subscription_id=ServerConfig.azure_subscription_id)
        self.repo: RedisRepository[AzureVM] = redisRepositoryFactory("azurevm")

    def check_state(self) -> Diff[AzureVM]:
        remoteState = getAzureVM(client=self.computeClient, env=self.vm.config.environment, name=self.vm.name)
        if remoteState is not None:
            if remoteState == self.vm:
                return Diff(expr=False, local=self.vm, remote=remoteState)
            else:
                return Diff(expr=True, local=self.vm, remote=remoteState)
        else:
            return Diff(expr=True, local=self.vm, remote=None)
    
    def commit(self):
        diff = self.check_state()

        if diff.expr is True:
            if diff.remote is None:
               createAzureVM(client=self.computeClient, vm=diff.local)
            else:
                try:
                    result = deleteAzureVM(client=self.computeClient, vm=diff.remote)
                    if result is False:
                        raise Exception("Could not delete vm")
                    createAzureVM(client=self.computeClient, vm=diff.local)
                except Exception as e:
                    logging.info(e)
        else:
            return None

