import csv
import yaml
import platform
import warnings
import openpyxl
from typing import List, Any, Tuple, Dict
from abc import ABC, abstractmethod

warnings.filterwarnings('ignore', category=UserWarning)

class IFetchDataForList(ABC):

    @abstractmethod
    def fetch_data(self)-> Tuple[List[str],List[List[Any]]]:
        pass


class FetchHinban(IFetchDataForList):

    def __init__(self, cnxn) -> None:
        self.cnxn = cnxn
        

    def fetch_data(self) -> Tuple[List[str],List[List[Any]]]:

        cursor = self.cnxn.cursor()

        sqlQuery = ("SELECT HinHinCD AS 'hinban',"
                    " HinNam AS 'hin_name',"
                    " HinTju AS 'tju',"
                    " HinFree18 AS 'order_or_stock'"
                    " From dbo.MHINCD"
                    " WHERE HinSeiKBN = '7'"
                    " ORDER BY HinHinCD"
                    )


        data_list: List[List[Any]] = []
        cursor.execute(sqlQuery)

        # 1. カラム名を取得（リスト内包表記）
        # cursor.description は (名前, 型, 表示サイズ, ...) というタプルのリスト
        columns = [column[0] for column in cursor.description]

        # 4. 2次元リストへ変換
        # fetchall() はタプルのリストを返すため、リスト内包表記で各行をリスト化します
        try:
            data_list = [list(row) for row in cursor.fetchall()]
        except Exception:
            print(f'データベースfetch中に予期せぬエラーです fetch_hinban')
        finally:
            cursor.close()
            # cnxnは呼び出しもとでクローズ

        return columns, data_list

        

class FetchMukesaki(IFetchDataForList):

    def __init__(self, cnxn) -> None:
        self.cnxn = cnxn
        

    def fetch_data(self) -> Tuple[List[str],List[List[Any]]]:

        cursor = self.cnxn.cursor()

        sqlQuery = ("SELECT DTL_NM AS 'mukesaki', DTL_CD AS 'mukesakiCD'"
                    " From dbo.TM_UNITY"
                    " WHERE MST_CD = 'MKSK_KBN' AND DEL_FLG <> '1'"
                    " ORDER BY DTL_CD"
                    )


        data_list: List[List[Any]] = []
        cursor.execute(sqlQuery)

        # 1. カラム名を取得（リスト内包表記）
        # cursor.description は (名前, 型, 表示サイズ, ...) というタプルのリスト
        columns = [column[0] for column in cursor.description]

        # 4. 2次元リストへ変換
        # fetchall() はタプルのリストを返すため、リスト内包表記で各行をリスト化します
        try:
            data_list = [list(row) for row in cursor.fetchall()]
        except Exception:
            print(f'データベースfetch中に予期せぬエラーです fetch_mukesaki')
        finally:
            cursor.close()
            # cnxnは呼び出しもとでクローズ

        return columns, data_list


class FetchNonyusaki(IFetchDataForList):

    def __init__(self, cnxn) -> None:
        self.cnxn = cnxn
        

    def fetch_data(self) -> Tuple[List[str],List[List[Any]]]:

        cursor = self.cnxn.cursor()

        sqlQuery = ("SELECT DTL_NM AS 'nonyusaki', DTL_CD AS 'nonyusakiCD'"
                    " From dbo.TM_UNITY"
                    " WHERE MST_CD = 'NNSK_KBN' AND DEL_FLG <> '1'"
                    " ORDER BY DTL_CD"
                    )


        data_list: List[List[Any]] = []
        cursor.execute(sqlQuery)

        # 1. カラム名を取得（リスト内包表記）
        # cursor.description は (名前, 型, 表示サイズ, ...) というタプルのリスト
        columns = [column[0] for column in cursor.description]

        # 4. 2次元リストへ変換
        # fetchall() はタプルのリストを返すため、リスト内包表記で各行をリスト化します
        try:
            data_list = [list(row) for row in cursor.fetchall()]
        except Exception:
            print(f'データベースfetch中に予期せぬエラーです fetch_nonyusaki')
        finally:
            cursor.close()
            # cnxnは呼び出しもとでクローズ

        return columns, data_list


class FetchSeihinLabel(IFetchDataForList):

    def __init__(self, cnxn) -> None:
        self.cnxn = cnxn
        

    def fetch_data(self) -> Tuple[List[str],List[List[Any]]]:

        cursor = self.cnxn.cursor()

        sqlQuery = ("SELECT DTL_NM AS 'seihinLabel', DTL_CD AS 'seihinLabelCD'"
                    " From dbo.TM_UNITY"
                    " WHERE MST_CD = 'ITEM_LBL_KBN' AND DEL_FLG <> '1'"
                    " ORDER BY DTL_CD"
                    )


        data_list: List[List[Any]] = []
        cursor.execute(sqlQuery)

        # 1. カラム名を取得（リスト内包表記）
        # cursor.description は (名前, 型, 表示サイズ, ...) というタプルのリスト
        columns = [column[0] for column in cursor.description]

        # 4. 2次元リストへ変換
        # fetchall() はタプルのリストを返すため、リスト内包表記で各行をリスト化します
        try:
            data_list = [list(row) for row in cursor.fetchall()]
        except Exception:
            print(f'データベースfetch中に予期せぬエラーです fetch_seihinLabel')
        finally:
            cursor.close()
            # cnxnは呼び出しもとでクローズ

        return columns, data_list


class FetchCoaMukesaki(IFetchDataForList):

    def fetch_data(self) -> Tuple[List[str],List[List[Any]]]:

        path: str = r'\\192.168.1.247\Guest\向先_ｼｰﾄ表.xlsx'
        if platform.system() == 'Linux':
            path = r'/mnt/guest/向先_ｼｰﾄ表.xlsx'

        # Excelブックを開く
        wb = openpyxl.load_workbook(path, data_only=True)
        sheet = wb['向先_ｼｰﾄ表']

        # 全ての行を取得
        rows = list(sheet.iter_rows(values_only=True))

        # 1行目をカラム名として取得
        columns = [str(col) for col in rows[0]]

        # 2行目以降をデータとして取得
        data_list = [list(row) for row in rows[1:]]

        return columns, data_list


class FetchTokui(IFetchDataForList):

    def __init__(self, cnxn) -> None:
        self.cnxn = cnxn
        

    def fetch_data(self) -> Tuple[List[str],List[List[Any]]]:

        cursor = self.cnxn.cursor()

        sqlQuery = ("SELECT TokTokCD AS 'tokuiCD'," 
                    " TokNonyuCD AS 'nonyuCD',"
                    " TokRyaku AS 'tokuiRyaku'"
                    " From dbo.MTOKUI"
                    " WHERE TokTokCD < 'T6000'"
                    " ORDER BY TokTokCD, TokNonyuCD"
                    )


        data_list: List[List[Any]] = []
        cursor.execute(sqlQuery)

        # 1. カラム名を取得（リスト内包表記）
        # cursor.description は (名前, 型, 表示サイズ, ...) というタプルのリスト
        columns = [column[0] for column in cursor.description]

        # 4. 2次元リストへ変換
        # fetchall() はタプルのリストを返すため、リスト内包表記で各行をリスト化します
        try:
            data_list = [list(row) for row in cursor.fetchall()]
        except Exception:
            print(f'データベースfetch中に予期せぬエラーです fetch_tokuiCD')
        finally:
            cursor.close()
            # cnxnは呼び出しもとでクローズ

        return columns, data_list


class FetchCans:

    def fetch_data(self) -> Dict[str, Dict[str, bool]]:

        path: str = r'\\192.168.1.247\共有\技術課ﾌｫﾙﾀﾞ\26. 製品DB\新ﾌｫｰﾏｯﾄ\営業部master\output_notification.yml'
        if platform.system() == 'Linux':
            path = r'/mnt/public/技術課ﾌｫﾙﾀﾞ/26. 製品DB/新ﾌｫｰﾏｯﾄ/営業部master/output_notification.yml'

        # YAMLファイルを開いて読み込む
        with open(path, "r", encoding="utf-8") as file:
            data = yaml.safe_load(file)

        return data


