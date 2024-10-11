from enum import Enum
from pydantic import BaseModel
from abc import ABC, abstractmethod

class ByteUnit(Enum):
    MB = 1
    GB = 2
    TB = 3

class VMProvider[T](BaseModel):
    client: None | str
    Config: T | str

class Repository[T: VMProvider](ABC):
    @abstractmethod
    def get_VM(self):
        raise NotImplementedError
    
    @abstractmethod
    def deleteVM(self):
        raise NotImplementedError
    
    @abstractmethod
    def createVM(self):
        raise NotImplementedError
    
    @abstractmethod
    def updateVM(self):
        raise NotImplementedError
