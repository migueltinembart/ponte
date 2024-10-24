from abc import abstractmethod
from typing import Any

from pydantic import BaseModel

class Repository(BaseModel):

    @abstractmethod
    def list(self) -> Any:
        pass
    
    # @abstractmethod 
    # def get(self, id) -> Any:
    #     pass
    #
    # @abstractmethod
    # def create(self, entity) -> Any:
    #     pass
    #
    # @abstractmethod
    # def update(self, id, entity) -> Any:
    #     pass
    #
    # @abstractmethod
    # def delete(self, id) -> Any:
    #     pass
    #

