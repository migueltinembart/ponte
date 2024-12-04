from abc import abstractmethod, ABC
from pydantic import BaseModel
from typing import Optional

class Diff[T](BaseModel):
    expr: bool
    local: T = None
    remote: Optional[T] = None

class Service[T](ABC):
    
    @abstractmethod 
    def check_state(self) -> Diff[T]:
        pass

    @abstractmethod
    def commit(self):
        pass

