from abc import ABC, abstractmethod
from typing import Any

class Repository(ABC):

    @abstractmethod
    def list(self) -> Any:
        pass
    
    # @abstractmethod
    # def get(self, id):
    #     pass
    #
    # @abstractmethod
    # def create(self, entity):
    #     pass
    #
    # @abstractmethod
    # def update(self, id, entity):
    #     pass
    #
    # @abstractmethod
    # def delete(self, id):
    #     pass
    #

