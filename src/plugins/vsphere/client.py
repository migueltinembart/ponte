import requests
import urllib3
from vmware.vapi.vsphere.client import create_vsphere_client

def vSphereClientFactory(server: str, username: str, password: str):
    session = requests.session()

    session.verify = False

    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

    return create_vsphere_client(server=server, username=username, password=password, session=session)
