import datetime
from IUpdate_master import IUpdateMaster
from typing import Dict, Any


class LabelDbForDomestic(IUpdateMaster):
    def __init__(self, hinban: str,
                 dic_kbns: Dict[str,Dict[str,str]],
                 cnxn
                 ) -> None:

        self._hinban = hinban
        self._dic_kbns = dic_kbns

        self.cnxn = cnxn


    def update_master(self, ui_infos: Dict[str, Any]) -> None:

        hinban: str = self._hinban
        label_kbn: str = self._dic_kbns['label'][ui_infos['label']]

        update_datas: Dict[str, str] = {
            'hinban': hinban,
            'label_kbn': label_kbn,
        }

        # label_dbにデータがあるかを調べる。
        is_exist_data_honsya = self._check_is_exist_data(update_datas, 'honsya')
        is_exist_data_osaka = self._check_is_exist_data(update_datas, 'osaka')

        if  is_exist_data_honsya:
            print("""\nlabel_dbに既に「本社」のデータがあります。
                  内容は変わりません。""")
        else:
            self._insert_data(update_datas, 'honsya')

        if  is_exist_data_osaka:
            print("""\nlabel_dbに既に「大阪」のデータがあります。
                  内容は変わりません。""")
        else:
            self._insert_data(update_datas, 'osaka')


    def _insert_data(self, update_datas: Dict, 
                                honsya_or_osaka: str)-> None:
        cursor = None
        try:
            self.cnxn.autocommit = False  # トランザクション管理を明示的に
            cursor = self.cnxn.cursor()

            table_name = 'TM_LBL_DB'
            sequence_column_name = 'LBL_DB_ID'

            # 1. 次の連番を取得して整形 NULLなら0になる
            select_max_sql = f"""
                SELECT ISNULL(MAX(CAST({sequence_column_name} AS INT)), 0)
                FROM {table_name}
            """
            cursor.execute(select_max_sql)
            current_max_int = cursor.fetchone()[0] # 結果の最初の列を取得
            next_sequence_int = current_max_int + 1
            next_sequence_str = f"{next_sequence_int:010}" # 10桁のゼロパディング

            print(f"\n現在の最大連番: {current_max_int}, 次の連番: {next_sequence_str}")

            # 2. 5つのカラムにデータを挿入するSQL
            # カラム名と ? の数を実際のテーブル構成に合わせてください
            insert_sql = f"""
                INSERT INTO {table_name} 
                (LBL_DB_ID, MKSK_KBN, ITEM_ID, ITEM_LBL_KBN, DANBORU_FLG, 
                DEL_FLG, INS_USER, INS_DTTM, INS_ID, UPD_USER, UPD_DTTM, 
                UPD_ID) 
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """

            # 挿入する値の準備
            # shipの場合
            honsya_or_osaka_kbn = '01'
            if honsya_or_osaka == 'osaka':
                honsya_or_osaka_kbn = '02'

            # datetimeオブジェクトをそのまま渡せば、pyodbcドライバが自動的に
            # データベースが理解できるDATETIME型に変換してくれる(推奨)
            dttm_now = datetime.datetime.now()

            params = (next_sequence_str,
                      honsya_or_osaka_kbn,
                      update_datas['hinban'],
                      update_datas['label_kbn'],
                      '0',
                      '0',
                      'e05',
                      dttm_now,
                      'InsLblDb',
                      'e05',
                      dttm_now,
                      'InsLblDbCh',
            )

            # executeにすべての値を渡す
            cursor.execute(insert_sql, params)

            self.cnxn.commit()
            print(f"label_dbに {honsya_or_osaka} のデータを挿入しました。")

        except Exception as e:
            print(f"予期せぬエラーが発生しました: {e}")
            if self.cnxn:
                self.cnxn.rollback()
                print("トランザクションはロールバックされました。")
        finally:
            if cursor:
                cursor.close()


    def _check_is_exist_data(self, update_datas: Dict,
                             honsya_or_osaka: str) -> bool:

        check_sql = """
        SELECT TOP 1 1 FROM TM_LBL_DB WHERE MKSK_KBN = ? AND ITEM_ID = ? 
        AND DEL_FLG <> ?;
        """
        # SELECT TOP 1 1 whereが該当したら一回だけデータを取得し、1を返す
        # MySQLのLIMIIT 1 と同じ。

        # shipの場合
        honsya_or_osaka_kbn = '01'

        if honsya_or_osaka == 'air':
            honsya_or_osaka_kbn = '02'

        params = (honsya_or_osaka_kbn,
                  update_datas['hinban'],
                  '1'
        )

        result = None

        with self.cnxn.cursor() as cursor:
            cursor.execute(check_sql, params)
            result = cursor.fetchone()
        '''
        データベースは [1] という結果（1行1列のデータ）を返します。
        Python側（cursor.fetchone()）は (1,) というタプルを受け取るため、
        if result: が True（存在する） と判定されます。
        もしテーブル内に、カラムAが 'aaa' のレコードが存在しない場合：
        データベースは何も返しません（0行）。
        Python側（cursor.fetchone()）は None を受け取るため、
        if result: が False（存在しない） と判定されます。
        '''

        if result:
            return True
        return False


    def _update_master(self, update_datas: Dict[str, str],
                       honsya_or_osaka: str) -> None:
        '''
        今は使っていない。既にデータベースにデータがある場合は、
        アップデートしても同じなので。ラベルは絶対に日本語であり、
        変わらない。
        '''

        update_sql = """
        UPDATE TM_LBL_DB 
        SET   ITEM_LBL_KBN = ?,
              UPD_USER = ?, UPD_DTTM = ?, UPD_ID = ? 
        WHERE MKSK_KBN = ? AND ISNULL(NNSK_KBN, '') = ? 
              AND ITEM_ID = ? AND DEL_FLG <> ?
        """
        # 挿入する値の準備
        # shipの場合
        honsya_or_osaka_kbn = '01'

        if honsya_or_osaka == 'osaka':
            honsya_or_osaka_kbn = '02'

        # datetimeオブジェクトをそのまま渡せば、pyodbcドライバが自動的に
        # データベースが理解できるDATETIME型に変換してくれる(推奨)
        dttm_str = datetime.datetime.now().strftime('%Y/%m/%d %H%M%S')
        dttm_now = datetime.datetime.strptime(dttm_str, '%Y/%m/%d %H%M%S')

        params = (update_datas['label_kbn'],
                  'e05',
                  dttm_now,
                  'InsLblDbCh',
                  honsya_or_osaka_kbn,
                  update_datas.get('nonyusaki_kbn') or '',
                  update_datas['hinban'],
                  '1'
            )

        self.cnxn.autocommit = False  # トランザクション管理を明示的に
        cursor = None
        try:
            cursor = self.cnxn.cursor()

            # executeにすべての値を渡す
            cursor.execute(update_sql, params)

            self.cnxn.commit()
            print(f"label_dbの {honsya_or_osaka} のデータを更新しました。")

        except Exception as e:
            print(f"予期せぬエラーが発生しました: {e}")
            if self.cnxn:
                self.cnxn.rollback()
                print("トランザクションはロールバックされました。")
        finally:
            if cursor:
                cursor.close()


