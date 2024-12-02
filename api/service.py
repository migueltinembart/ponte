from abc import abstractmethod, ABC

from deployments import Deployment

class Service(ABC):
    @abstractmethod 
    def check_state(self):
        pass

    @abstractmethod 
    def diff(self):
        pass

    @abstractmethod 
    def decide(self):
        pass

    def commit(self):
        pass

