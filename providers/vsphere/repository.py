from providers.base import Repository, VMProvider
from providers.vsphere.models import vSphereProviderConfig

class VSphereRepository(Repository[VMProvider[vSphereProviderConfig]]):
    def __init__(self, config: vSphereProviderConfig) -> None:
        self.VMProvider = VMProvider(client="test", config=config)

    def get_VM(self):
        print(self.VMProvider.config)

    def deleteVM(self):
        print("deleted VM")

    def createVM(self): i
        print("created VM")

    def updateVM(self):
        print("updated VM")

if __name__ == "__main__":
    config = vSphereProviderConfig(
            cpu_cores=2
            memory=2048
            
            )
    repo = VSphereRepository()
    repo.updateVM()

 

