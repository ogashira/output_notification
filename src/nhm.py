from typing import List, Dict, Any
import platform
import openpyxl
from IUpdate_master import IUpdateMaster
from label_identification import LabelIdentification
from get_idx import GetIdx

class Nhm(IUpdateMaster):

    def __init__(self, label_identification: LabelIdentification,
                 hinban: str, hin_name: str) -> None:

        self._label_identification = label_identification
        self._hinban = hinban
        self._hin_name = hin_name

        self._path: str = r'\\192.168.1.247\共有\受注check\master\n&h&m_modify.xlsx'
        if platform.system() == 'Linux':
            self._path = r'/mnt/public/受注check/master/n&h&m_modify.xlsx'

        # Excelブックを開く
        self._wb = openpyxl.load_workbook(self._path, data_only=True)
        self._ws = self._wb['n&h&m_modify']

        # 全ての行を取得
        rows = list(self._ws.iter_rows(values_only=True))

        # 1行目をカラム名として取得
        # 得意先コード,納入先コード,品番,品名,向け先
        self._nhm_col = [str(col) for col in rows[0]]

        # 2行目以降をデータとして取得
        self._nhm_data = [list(row) for row in rows[1:]]


        # {'T0210':['THS01', 'THS02', 'THS03',...]}
        self._nonyuCDs:Dict[str, List[str]] = \
                self._label_identification.create_tokuiCDs_dict()
        # 'T0210'
        self._need_tokuiCD: str = list(self._nonyuCDs.keys())[0]
        # 'THS01', 'THS02', 'THS03',...
        self._need_nonyuCDs: List[str] = self._nonyuCDs[self._need_tokuiCD]

        self._nonexistent_data:List[List[str]] = self._create_nonexistent_data()

        # nhmの向け先を求める
        self._nhm_mukesaki: str = self._get_nhm_mukesaki()


    def _get_nhm_mukesaki(self) -> str:

        def get_need_nhm_mukesaki(row: List[Any]) -> str:
            exist_tokuiCD_idx:int = GetIdx.get_idx(self._nhm_col, '得意先コード')
            exist_nonyuCD_idx:int = GetIdx.get_idx(self._nhm_col, '納入先コード')
            exist_nhm_mukesaki_idx: int = GetIdx.get_idx(self._nhm_col, '向け先')
            exist_tokuiCD:str = row[exist_tokuiCD_idx]
            exist_nonyuCD:str = row[exist_nonyuCD_idx]

            need_nhm_mukesaki = ''

            # 向け先がない、または空文字の場合は空文字を返す。
            if (row[exist_nhm_mukesaki_idx] is None or 
                row[exist_nhm_mukesaki_idx] == ''):
                return need_nhm_mukesaki

            # 得意先コードが一致していない、または納入先コードにlabel_identificationが持つ納入先のアルファベットが含まれていない場合は、空文字を返す
            if not (self._need_tokuiCD == exist_tokuiCD and 
                self._label_identification.does_contain_alphabet(exist_nonyuCD)):
                return need_nhm_mukesaki


            # 得意先コードが一致して、納入先コードにアルファベットが含まれていて、向け先に記載がある場合はその向け先を返す
            need_nhm_mukesaki = row[exist_nhm_mukesaki_idx]
            return need_nhm_mukesaki
                
        '''
        get_need_nhm_mukesaki()からは、空文字か、strが返ってくる。
        文字が返ってきたら終了。空文字だったら、新たに向け先を作る。 
        '''
        need_nhm_mukesaki: str = ''
        for row in self._nhm_data:
            need_nhm_mukesaki = get_need_nhm_mukesaki(row)
            if need_nhm_mukesaki != '':
                break  # 文字が返ってきたら終了
            
        # 最終的に空文字だったら
        if need_nhm_mukesaki == '':
            need_nhm_mukesaki = \
            self._label_identification.create_new_nhm_mukesaki()

        return need_nhm_mukesaki



    def _create_nonexistent_data(self) -> List[List[str]]:

        def is_existent_data(need_tokuiCD: str, need_nonyuCD: str,
                                    exist_tokuiCD: str, exist_nonyuCD: str,
                                    exist_hinban: str)-> bool:

            if (exist_tokuiCD == need_tokuiCD and 
                exist_nonyuCD == need_nonyuCD and 
                exist_hinban == self._hinban):
                return True

            return False


        def create_nonexistent_data(need_nonyuCD: str,
                                nonexistent_data: List[List[str]])-> None:

            is_existent:bool = False
            exist_tokuiCD: str = ''
            exist_nonyuCD: str = ''
            exist_hinban: str = ''
            for row in self._nhm_data:
                exist_tokuiCD_idx:int = \
                        GetIdx.get_idx(self._nhm_col, '得意先コード')
                exist_nonyuCD_idx:int = \
                        GetIdx.get_idx(self._nhm_col, '納入先コード')
                exist_hinban_idx:int = \
                        GetIdx.get_idx(self._nhm_col, '品番')

                exist_tokuiCD = str(row[exist_tokuiCD_idx])
                exist_nonyuCD = str(row[exist_nonyuCD_idx])
                exist_hinban = str(row[exist_hinban_idx])

                is_existent = is_existent_data(self._need_tokuiCD, need_nonyuCD,
                                        exist_tokuiCD, exist_nonyuCD,
                                        exist_hinban)

                if is_existent:
                    return  # すでにデータがあるので、スキップ

            nonexistent_data.append([self._need_tokuiCD, need_nonyuCD, 
                                         self._hinban])


        def break_down_nonyuCDs( nonexistent_data: List[List[str]])-> None:
            for need_nonyuCD in self._need_nonyuCDs:
                create_nonexistent_data(need_nonyuCD, nonexistent_data)


        nonexistent_data: List[List[str]] = []
        break_down_nonyuCDs(nonexistent_data)

        return nonexistent_data


    def update_master(self, ui_infos: Dict[str, Any])-> None:
        if not self._nonexistent_data:
            print()
            print("\n n&h&m_modifyへの追加データはありません。")
            return

        for row in self._nonexistent_data:
            row.append(self._hin_name)
            row.append(self._nhm_mukesaki)
            self._ws.append(row)

        self._wb.save(self._path)
        self._wb.close()

        print()
        print(f'\n n&h&m_modify.xlsxファイルに{len(self._nonexistent_data)}件データを追加しました。')
        for row in self._nonexistent_data:
            print(row)

