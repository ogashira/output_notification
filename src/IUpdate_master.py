from abc import ABC, abstractmethod

class IUpdateMaster(ABC):

    @abstractmethod
    def update_master(self)-> None:
        pass
