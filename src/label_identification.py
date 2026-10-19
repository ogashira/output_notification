from typing import List, Dict
from get_idx import GetIdx

class LabelIdentification:
    def __init__(self, col: List[str], data: List[str],
                 tokuiCD: str, ui_nonyusaki: str) -> None:

        mukesaki_kbn_idx:int = GetIdx.get_idx(col, 'mukesaki_kbn')
        nonyusaki_kbn_idx:int = GetIdx.get_idx(col, 'nonyusaki_kbn')
        self.nonyuAlphabet_idx:int = GetIdx.get_idx(col, 'nonyuAlphabet')
        self.nonyuNoMin_idx:int = GetIdx.get_idx(col, 'nonyuNoMin')
        self.nonyuNoMax_idx:int = GetIdx.get_idx(col, 'nonyuNoMax')

        self.mukesaki_kbn: str = data[mukesaki_kbn_idx]
        self.nonyusaki_kbn:str = data[nonyusaki_kbn_idx]
        self.nonyuAlphabet:str = data[self.nonyuAlphabet_idx]
        self.nonyuNoMin:str = data[self.nonyuNoMin_idx]
        self.nonyuNoMax:str = data[self.nonyuNoMax_idx]

        self.tokuiCD: str = tokuiCD
        self.ui_nonyusaki: str = ui_nonyusaki


    def create_new_nhm_mukesaki(self) -> str:
        return f"{self.nonyuAlphabet}_{self.ui_nonyusaki}"


    def does_contain_alphabet(self, nonyuCD: str) -> bool:
        # THS01はTHSを含むか？
        return self.nonyuAlphabet in nonyuCD


    def create_tokuiCDs_dict(self) -> Dict:
        # tokuiCDs_dict = {'T0210':['THS01', 'THS02', 'THS03',...]} 
        tokuiCDs_dict: Dict[str, List[str]] = {}

        inner_list: List[str] = []
        for i in range(int(self.nonyuNoMin), int(self.nonyuNoMax)+1):
            no: str = str(i)
            if len(no) == 1:
                no = '0' + no
            inner_list.append(self.nonyuAlphabet + no)
                
        tokuiCDs_dict[self.tokuiCD] = inner_list

        return tokuiCDs_dict
