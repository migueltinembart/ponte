import logging
import re
from typing import List

from azure.mgmt.compute.v2024_07_01 import _compute_management_client
from azure.mgmt.compute.v2024_07_01.models import VirtualMachine
from pydantic import ValidationError
from .service import AzureRMresourceDefinition

from api.plugins.azure.vm import AzureCPUConfig, AzureCustomizationConfig, AzureEnvironment, AzureOSConfig, AzurePrivateIPConfig,AzureStorageConfig, AzureVMAccessConfig, AzureVMConfig, AzureVMInboundPortConfig 

def getAzureCPUConfig(vm: VirtualMachine)-> AzureCPUConfig:
    if (hardware_profile := vm.hardware_profile) and (vm_size := hardware_profile.vm_size):
        return AzureCPUConfig(size=vm_size)
    else:
        raise ValueError("No CPU Configuration found for virtual machine")

def getAzureVMStorageConfig(vm: VirtualMachine) -> List[AzureStorageConfig]:
    disks: List[AzureStorageConfig] = []
    secondary_disks: List[AzureStorageConfig] = []
    
    if (storage_profile := vm.storage_profile):
        if (os_disk := storage_profile.os_disk) and (disk_size_gb := os_disk.disk_size_gb) and ( managed_disk := os_disk.managed_disk ) and (storage_account_type := managed_disk.storage_account_type):
            if storage_account_type is str:
                primary_disk = AzureStorageConfig(
                    type="primary", 
                    size=disk_size_gb,
                    disk_type=storage_account_type
                )
                disks.append(primary_disk)
        else:
            raise ValidationError("No os Disk found for virtual machine")

        if (data_disks := storage_profile.data_disks):
            for disk in data_disks:
                if (disk_size_gb := disk.disk_size_gb) and (managed_disk := disk.managed_disk) and (storage_account_type := managed_disk.storage_account_type):
                    secondary_disks.append(AzureStorageConfig(type="data", size=disk_size_gb, disk_type=storage_account_type)) # type: ignore
    
        disks.extend(secondary_disks)
    else:
        raise ValueError("Storage profile could not be read from virtual machine")

    return disks

def getAzureVMNetworkConfig(vm: VirtualMachine) -> List[AzurePrivateIPConfig]:
    """ Raises Value Error if no Network configuration is found """
    ip_configurations_list: List[AzurePrivateIPConfig] = []

    if ( network_profile := vm.network_profile) and ( network_config := network_profile.network_interface_configurations ):
        for config in network_config:
            if config.ip_configurations:
                for ipconf in config.ip_configurations:
                    if (subnet := ipconf.subnet) and (subnet_id := subnet.id) and (primary := ipconf.primary):
                        chunked_id = re.findall(r'/[^/]+', subnet_id)
                        resource_group_name = chunked_id[3]
                        vnet_name = chunked_id[7]
                        subnet_name = chunked_id[9]
                        ip_configurations_list.append(
                            AzurePrivateIPConfig(
                                primary=primary, 
                                resource_group=resource_group_name, 
                                vnet_name=vnet_name, subnet=subnet_name)
                        )
    else:
        raise ValueError("No Network Configuration found for virtual machine")
    return ip_configurations_list

def getAzureVMOSConfig(vm: VirtualMachine) -> AzureOSConfig:
    os_config = {}

    if (storage_profile := vm.storage_profile) and (image_ref := storage_profile.image_reference):
        if (publisher := image_ref.publisher) and (offer := image_ref.offer) and (sku := image_ref.sku) and (version := image_ref.version):

            os_config = {
                'publisher': publisher,
                'offer': offer,
                'sku':sku,
                'version': version
            }
    else:
        raise ValueError("No os configuration found for virtual machine")
    
    return AzureOSConfig(
        publisher=os_config["publisher"],
        offer=os_config["offer"],
        sku=os_config["sku"],
        version=os_config["version"]
    )

def getAzureVMAccessConfig(vm: VirtualMachine) -> AzureVMAccessConfig:
    vm_access_config = {}

    if (os_profile := vm.os_profile) and (admin_username := os_profile.admin_username ) and (linux_conf := os_profile.linux_configuration) and (ssh := linux_conf.ssh) and (public_keys := ssh.public_keys):
        public_key_values = []
        for key in public_keys:
            assert key.key_data is str
            public_key_values.append(key.key_data)
        
        vm_access_config = {
            'admin_username': admin_username,
            'public_key_values': public_key_values
        }
    else:
        raise ValueError("No vm access configuration found for virtual machine")
    return AzureVMAccessConfig(username=vm_access_config["admin_username"], public_key_values=vm_access_config["public_key_values"])

def getAzureVMConfig(client: _compute_management_client.ComputeManagementClient, resourceDefinition: AzureRMresourceDefinition) -> AzureVMConfig | None:
    
    try:
        vm = client.virtual_machines.get(resourceDefinition.resourceGroupName, resourceDefinition.name)
        client_access_config = getAzureVMAccessConfig(vm)
        cpu_config = getAzureCPUConfig(vm)
        os_config = getAzureVMOSConfig(vm)
        storage_configs = getAzureVMStorageConfig(vm)
        network_config = getAzureVMNetworkConfig(vm)
        customization_config = AzureCustomizationConfig(access=client_access_config , userdata="")
        return AzureVMConfig(environment=AzureEnvironment(subscription="", resource_group=""), cpu_config=cpu_config, os_config=os_config, storage_config=storage_configs, network_config=network_config, customization=customization_config, addons=None, availability_zones=1)
    except ValidationError as validation_error:
        logging.info(validation_error)
    except ValueError as value_error:
        logging.info(value_error)
    
    return None

