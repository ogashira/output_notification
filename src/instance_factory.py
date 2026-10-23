from typing import Dict, TYPE_CHECKING, Any, List, Tuple, Optional
import platform
import sys
from fetch_data_for_list import IFetchDataForList
from IUpdate_master import IUpdateMaster
from get_idx import GetIdx
from filter_data import FilterData
from label_identification import LabelIdentification
from nhm import Nhm
from calc_fire_and_fish_kubun import CalcFireAndFishKubun

# 実行時にはインポートせず、型チェックの為だけに書く
if TYPE_CHECKING:
    from fetch_data_for_list import FetchCans


class InstanceFactory:
    '''
    各モジュールのインポートは必要な時にメソッド内で行う。
    冒頭でまとめてやると実行速度が急激に遅くなったため
    '''

    _sqlServerTss: Any = None
    _sqlServerEffit: Any = None
    _cnxn_tss = None
    _cnxn_effit = None

    _instances: Dict[str, Any] = {}

    @classmethod
    def _setup_sql_path(cls) -> None:
        """SQLサーバー用モジュールのパスを通す (一度だけ実行)"""
        if 'sql_path_setup' in cls._instances:
            return
            
        shared_folder_path: str = r'./'
        if platform.system() == 'Linux':
            shared_folder_path = \
                r'/mnt/public/技術課ﾌｫﾙﾀﾞ/200. effit_data/ﾏｽﾀ/sql_python_module'
        elif platform.system() == 'Windows':
            shared_folder_path = \
                r'//192.168.1.247/共有/技術課ﾌｫﾙﾀﾞ/200. effit_data/ﾏｽﾀ/sql_python_module'
        
        if shared_folder_path not in sys.path:
            sys.path.append(shared_folder_path)
        cls._instances['sql_path_setup'] = True

    @classmethod
    def get_sql_server_tss(cls) -> None:
        if cls._sqlServerTss is None:
            cls._setup_sql_path()
            from sql_server_tss_addmin import SqlServer as SqlServerTss 
            cls._sqlServerTss = SqlServerTss()
            cls._cnxn_tss = cls._sqlServerTss.get_cnxn()

    @classmethod
    def get_sql_server_effit(cls) -> None:
        if cls._sqlServerEffit is None:
            cls._setup_sql_path()
            from sql_server_effit_addmin import SqlServer as SqlServerEffit
            cls._sqlServerEffit = SqlServerEffit()
            cls._cnxn_effit = cls._sqlServerEffit.get_cnxn()

    @classmethod
    def delete_cnxn(cls) -> None:
        if cls._sqlServerTss:
            cls._sqlServerTss.close()
        if cls._sqlServerEffit:
            cls._sqlServerEffit.close()


    @classmethod
    def get_fetchHinban(cls) -> IFetchDataForList:
        from fetch_data_for_list import FetchHinban
        ins_name: str = 'fetchHinban'
        if ins_name not in cls._instances:
            cls.get_sql_server_effit()
            cls._instances[ins_name] = FetchHinban(cls._cnxn_effit)
        return cls._instances[ins_name]


    @classmethod
    def get_fetchMukesaki(cls) -> IFetchDataForList:
        from fetch_data_for_list import FetchMukesaki
        ins_name: str = 'fetchMukesaki'
        if ins_name not in cls._instances:
            cls.get_sql_server_tss()
            cls._instances[ins_name] = FetchMukesaki(cls._cnxn_tss)
        return cls._instances[ins_name]


    @classmethod
    def get_fetchNonyusaki(cls) -> IFetchDataForList:
        from fetch_data_for_list import FetchNonyusaki
        ins_name: str = 'fetchNonyusaki'
        if ins_name not in cls._instances:
            cls.get_sql_server_tss()
            cls._instances[ins_name] = FetchNonyusaki(cls._cnxn_tss)
        return cls._instances[ins_name]


    @classmethod
    def get_fetchSeihinLabel(cls) -> IFetchDataForList:
        from fetch_data_for_list import FetchSeihinLabel
        ins_name: str = 'fetchSeihinLabel'
        if ins_name not in cls._instances:
            cls.get_sql_server_tss()
            cls._instances[ins_name] = FetchSeihinLabel(cls._cnxn_tss)
        return cls._instances[ins_name]


    @classmethod
    def get_fetchTokui(cls) -> IFetchDataForList:
        from fetch_data_for_list import FetchTokui
        ins_name: str = 'fetchTokui'
        if ins_name not in cls._instances:
            cls.get_sql_server_effit()
            cls._instances[ins_name] = FetchTokui(cls._cnxn_effit)
        return cls._instances[ins_name]


    @classmethod
    def get_fetchCoaMukesaki(cls) -> IFetchDataForList:
        from fetch_data_for_list import FetchCoaMukesaki
        ins_name: str = 'fetchCoaFormat'
        if ins_name not in cls._instances:
            cls._instances[ins_name] = FetchCoaMukesaki()
        return cls._instances[ins_name]


    @classmethod
    def get_fetchCans(cls) -> 'FetchCans':
        from fetch_data_for_list import FetchCans
        ins_name: str = 'fetchCans'
        if ins_name not in cls._instances:
            cls._instances[ins_name] = FetchCans()
        return cls._instances[ins_name]



    @classmethod
    def get_HinbanMaster(cls, hinban: str, hin_name: str, 
                         order_or_stocked: str) -> IUpdateMaster:
        from hinban_master import HinbanMaster
        hinban_master: IUpdateMaster = HinbanMaster(hinban, hin_name, 
                                                    order_or_stocked,
                                                    cls._cnxn_effit)
        return hinban_master




    @classmethod
    def get_fetchFishKubun(cls) -> IFetchDataForList:
        from fetch_data_for_list import FetchFishKubun
        cls.get_sql_server_tss()
        fetchFishKubun: IFetchDataForList = FetchFishKubun(cls._cnxn_tss)
        return fetchFishKubun

    @classmethod
    def get_fetchFireKubun(cls) -> IFetchDataForList:
        from fetch_data_for_list import FetchFireKubun
        cls.get_sql_server_tss()
        fetchFireKubun: IFetchDataForList = FetchFireKubun(cls._cnxn_tss)
        return fetchFireKubun

    @classmethod
    def get_fetchUnsouKubun(cls) -> IFetchDataForList:
        from fetch_data_for_list import FetchUnsouKubun
        cls.get_sql_server_tss()
        fetchUnsouKubun: IFetchDataForList = FetchUnsouKubun(cls._cnxn_tss)
        return fetchUnsouKubun

    '''
    LabalIdentificationのインスタンスを作成 >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
    '''
    @classmethod
    def get_fetchLabelIdentificatiion(cls, 
                        mukesaki_kbn, nonyusaki_kbn) -> IFetchDataForList:
        from fetch_data_for_list import FetchLabelIdentification


        cls.get_sql_server_tss()
        return FetchLabelIdentification(cls._cnxn_tss, 
                                        mukesaki_kbn, nonyusaki_kbn)

    @classmethod
    def get_LabelIdentificationData(cls, mukesaki_kbn: str,
                                    nonyusaki_kbn: str)-> Tuple:

        # FetchLabelIdentification:IFetchDataForListのインスタンスを作成
        fetch_label_identification:IFetchDataForList = \
            cls.get_fetchLabelIdentificatiion(
                mukesaki_kbn, nonyusaki_kbn)

        # fetch_label_identification.fetch_data()の戻り値を取得
        col, data = fetch_label_identification.fetch_data()

        # dataは２次元リストで要素数は１なので、それを取得
        # データがない場合は、一次元リスト[]が返る
        if len(data) == 0:
            return col, []
        return col, data[0]


    @classmethod
    def get_LabelIdentification(cls, ui_infos: Dict[str, Any],
                                mukesaki_col: List[str], 
                                mukesaki_data: List[List[str]],
                                nonyusaki_col: List[str],
                                nonyusaki_data: List[List[str]]
                                )-> Optional[LabelIdentification]:

        if mukesaki_data == []:
            return None
        if nonyusaki_data == []:
            return None

        ui_mukesaki: str = ui_infos['mukesaki']  # 豊通
        ui_nonyusaki: str = ui_infos['nonyusaki'] # タイスタンレー

        mukesaki_kbn:str = ""
        nonyusaki_kbn:str = ""
        tokuiCD:str = ""

        # mukesakis = ['豊通', '04', 'T1210']
        mukesakis: List[str] = FilterData.filter_data_from_2d_list(
                                            mukesaki_data, 
                                            mukesaki_col, 
                                            'mukesaki_nam',
                                            ui_mukesaki)
        mukesaki_kbn_idx:int = GetIdx.get_idx(mukesaki_col, 'mukesaki_kbn')
        mukesaki_kbn = mukesakis[mukesaki_kbn_idx]

        tokuiCD_idx:int = GetIdx.get_idx(mukesaki_col, 'tokuiCD')
        tokuiCD = mukesakis[tokuiCD_idx]

        # nonyusakis = [タイスタンレー', '09']
        nonyusakis: List[str] = FilterData.filter_data_from_2d_list(
                                            nonyusaki_data, 
                                            nonyusaki_col, 
                                            'nonyusaki_nam',
                                            ui_nonyusaki)
        nonyusaki_kbn_idx:int = GetIdx.get_idx(nonyusaki_col, 'nonyusaki_kbn')
        nonyusaki_kbn = nonyusakis[nonyusaki_kbn_idx]

        col, data = \
                cls.get_LabelIdentificationData(mukesaki_kbn, nonyusaki_kbn)
                
        if data == []:
            raise Exception(f"\nラベル識別コードに {ui_mukesaki}:{ui_nonyusaki} が存在しません。")

        label_identification:LabelIdentification = \
                LabelIdentification(col, data, tokuiCD, ui_nonyusaki)

        return label_identification
    '''
    label_identificationのインスタンスを作成 ~ここまで~ >>>>>>>>>>>>>>>>>>>>>>>>
    '''


    @classmethod
    def get_Nhm(cls, label_identification: LabelIdentification,
                hinban: str, hin_name: str) -> Nhm:
        nhm: Nhm = Nhm(label_identification, hinban, hin_name)
        return nhm


    '''
    LabelDbForExportのインスタンスを作成 >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
    '''
    @classmethod
    def get_fetchGhsDb(cls, hinban: str) -> IFetchDataForList:
        from fetch_data_for_list import FetchGhsDb
        cls.get_sql_server_tss()
        return FetchGhsDb(cls._cnxn_tss, hinban)

    @classmethod
    def get_CalcFireAndFishKubun(cls, ghs_col, ghs_data, 
                                 can_hinban, is_exist_fire_print, 
                                 is_exist_fish_print) -> CalcFireAndFishKubun:

        calc_fireAndFishKubun: CalcFireAndFishKubun = \
            CalcFireAndFishKubun(ghs_col, ghs_data, 
                                 can_hinban, is_exist_fire_print, 
                                 is_exist_fish_print
            )
        return calc_fireAndFishKubun


    @classmethod
    def get_LabelDbForExport(cls, hinban: str, can_hinban: str,
                             is_exist_fire_print: bool,
                             is_exist_fish_print: bool,
                             dic_kbns: Dict[str,Dict[str,str]],
                             ) -> IUpdateMaster:

        from label_db_for_export import LabelDbForExport

        fetch_ghs_db: IFetchDataForList = cls.get_fetchGhsDb(hinban)
        ghs_col, ghs_datas = fetch_ghs_db.fetch_data()
        if ghs_datas != []:
            ghs_data = ghs_datas[0]
        else:
            ghs_data = []

        if ghs_data == []:
            raise Exception(f"\nghs_dbに {hinban} が存在しません。")

        calc_fire_and_fish_kubun: CalcFireAndFishKubun = \
            cls.get_CalcFireAndFishKubun(ghs_col, ghs_data,
                                 can_hinban, is_exist_fire_print, 
                                 is_exist_fish_print)

        label_db_for_export: LabelDbForExport = LabelDbForExport(
            hinban, dic_kbns, calc_fire_and_fish_kubun, cls._cnxn_tss
        )
        return label_db_for_export

    '''
    LabelDbForExportのインスタンスを作成 ~ ここまで~ >>>>>>>>>>>>>>>>>>>>>
    '''

    '''
    LabelDbForDomesticのインスタンスを作成 >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
    '''
    @classmethod
    def get_LabelDbForDomestic(cls, hinban: str,
                             dic_kbns: Dict[str,Dict[str,str]],
                             ) -> IUpdateMaster:

        from label_db_for_domestic import LabelDbForDomestic

        label_db_for_domestic: LabelDbForDomestic = LabelDbForDomestic(
            hinban, dic_kbns, cls._cnxn_tss
        )
        return label_db_for_domestic

    '''
    LabelDbForDomesticのインスタンスを作成 ~ ここまで~ >>>>>>>>>>>>>>>>>>>>>
    '''
