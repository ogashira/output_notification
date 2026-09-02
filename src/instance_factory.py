from typing import Dict, TYPE_CHECKING, Any, List
import platform
import sys

# 実行時にはインポートせず、型チェックの為だけに書く
if TYPE_CHECKING:
    from fetch_data import IFetchData
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
            from sql_server import SqlServer as SqlServerEffit
            cls._sqlServerEffit = SqlServerEffit()
            cls._cnxn_effit = cls._sqlServerEffit.get_cnxn()

    @classmethod
    def delete_cnxn(cls) -> None:
        if cls._sqlServerTss:
            cls._sqlServerTss.close()
        if cls._sqlServerEffit:
            cls._sqlServerEffit.close()


    @classmethod
    def get_fetchHinban(cls) -> 'IFetchData':
        from fetch_data_for_list import FetchHinban
        ins_name: str = 'fetchHinban'
        if ins_name not in cls._instances:
            cls.get_sql_server_effit()
            cls._instances[ins_name] = FetchHinban(cls._cnxn_effit)
        return cls._instances[ins_name]


    @classmethod
    def get_fetchMukesaki(cls) -> 'IFetchData':
        from fetch_data_for_list import FetchMukesaki
        ins_name: str = 'fetchMukesaki'
        if ins_name not in cls._instances:
            cls.get_sql_server_tss()
            cls._instances[ins_name] = FetchMukesaki(cls._cnxn_tss)
        return cls._instances[ins_name]


    @classmethod
    def get_fetchNonyusaki(cls) -> 'IFetchData':
        from fetch_data_for_list import FetchNonyusaki
        ins_name: str = 'fetchNonyusaki'
        if ins_name not in cls._instances:
            cls.get_sql_server_tss()
            cls._instances[ins_name] = FetchNonyusaki(cls._cnxn_tss)
        return cls._instances[ins_name]


    @classmethod
    def get_fetchSeihinLabel(cls) -> 'IFetchData':
        from fetch_data_for_list import FetchSeihinLabel
        ins_name: str = 'fetchSeihinLabel'
        if ins_name not in cls._instances:
            cls.get_sql_server_tss()
            cls._instances[ins_name] = FetchSeihinLabel(cls._cnxn_tss)
        return cls._instances[ins_name]


    @classmethod
    def get_fetchTokui(cls) -> 'IFetchData':
        from fetch_data_for_list import FetchTokui
        ins_name: str = 'fetchTokui'
        if ins_name not in cls._instances:
            cls.get_sql_server_effit()
            cls._instances[ins_name] = FetchTokui(cls._cnxn_effit)
        return cls._instances[ins_name]


    @classmethod
    def get_fetchCoaMukesaki(cls) -> 'IFetchData':
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
    def get_UiInfo(cls, ui_infos: Dict[str, str]) -> 'UiInfo':
        from ui_info import UiInfo
        return UiInfo(ui_infos)


