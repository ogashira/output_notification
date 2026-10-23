from typing import List
from get_idx import GetIdx

class CalcFireAndFishKubun:
    def __init__(self, ghs_col: List[str], 
                 ghs_data:List[str],
                 can_hinban: str,
                 is_exist_fire_print:bool, 
                 is_exist_fish_print:bool) -> None:

        self.is_exist_fire_print = is_exist_fire_print
        self.is_exist_fish_print = is_exist_fish_print

        self.is_need_fire = False
        self.is_need_fish = False

        class_idx: int = GetIdx.get_idx(ghs_col, 'ghs_class')
        fire_idx: int = GetIdx.get_idx(ghs_col, 'ghs_fire')
        fish_idx: int = GetIdx.get_idx(ghs_col, 'ghs_fish')

        if ghs_data[fire_idx] == '○':
            self.is_need_fire = True
        if ghs_data[fish_idx] == '○':
            self.is_need_fish = True

        self.class_rank = ghs_data[class_idx] # 'ｸﾗｽ3'


    def calc_fire_nam(self) -> str:
        if not self.is_need_fire: # ファイヤーマークが不要の場合
            if self.class_rank == 'ｸﾗｽ3':
                return ''
        if not self.is_need_fire:  
            if self.class_rank != 'ｸﾗｽ3':
                return self.class_rank
        if self.is_need_fire: # ファイヤーマークが必要な場合
            if self.is_exist_fire_print: # プリントしてある場合
                if self.class_rank == 'ｸﾗｽ3':
                    return ''
                if self.class_rank != 'ｸﾗｽ3':
                    return self.class_rank
            if not self.is_exist_fire_print: # プリントしていない場合
                return '○'
        return 'hoge' # どこにも引っ掛からない場合


    def calc_fish_nam(self) -> str:
        if not self.is_need_fish: # 魚マークが不要の場合
            return ''
        if self.is_need_fish: # 魚マークが必要な場合
            if self.is_exist_fish_print: # 魚印刷してある場合
                return 'F'
            if not self.is_exist_fish_print: # 魚印刷していない場合
                return '○'
            # さらに、この後LabelDbForExportで、airだったら、''になる。
        return 'hoge' # どこにも引っ掛からない場合
