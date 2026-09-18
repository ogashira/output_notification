from abc import ABC, abstractmethod

class IInsertMaster(ABC):

    @abstractmethod
    def insert_master(self)-> None:
        pass
