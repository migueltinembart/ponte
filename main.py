from fastapi import FastAPI
from routes import event
from providers.vsphere.repository import VSphereRepository

repo = VSphereRepository()
repo.updateVM()
