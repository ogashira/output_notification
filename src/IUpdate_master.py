from abc import ABC, abstractmethod
from typing import Dict, Any

class IUpdateMaster(ABC):

    @abstractmethod
    def update_master(self, ui_infos: Dict[str, Any])-> None:
        pass
