from IUpdate_master import IUpdateMaster
from typing import Dict, Any

class LabelDbForExport(IUpdateMaster):
    def __init__(self, hinban: str,
                 dic_kbns: Dict[str,Dict[str,str]],
                 ) -> None:
        self._hinban = hinban
        self._dic_kbns = dic_kbns

    def update_master(self, ui_infos: Dict[str, Any]) -> None:
        pass


