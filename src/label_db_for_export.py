import datetime
from IUpdate_master import IUpdateMaster
from typing import Dict, Any
from calc_fire_and_fish_kubun import CalcFireAndFishKubun


class LabelDbForExport(IUpdateMaster):
    def __init__(self, hinban: str,
                 dic_kbns: Dict[str,Dict[str,str]],
                 calc_fire_and_fish_kubun: CalcFireAndFishKubun,
                 cnxn
                 ) -> None:

        self._hinban = hinban
        self._dic_kbns = dic_kbns
        self._calc_fire_and_fish_kubun = calc_fire_and_fish_kubun

        self._fire_nam: str = calc_fire_and_fish_kubun.calc_fire_nam()
        self._fish_nam: str = calc_fire_and_fish_kubun.calc_fish_nam()

        self.cnxn = cnxn


    def update_master(self, ui_infos: Dict[str, Any]) -> None:

        if self._fire_nam == 'hoge':
            raise Exception(f"\nfire_namが不正です。")
        if self._fish_nam == 'hoge':
            raise Exception(f"\nfish_namが不正です。")
        
        mukesaki_kbn: str = self._dic_kbns['mukesaki'][ui_infos['mukesaki']]
        nonyusaki_kbn: str = self._dic_kbns['nonyusaki'][ui_infos['nonyusaki']]
        hinban: str = self._hinban
        label_kbn: str = self._dic_kbns['label'][ui_infos['label']]
        # ｸﾗｽ3の場合も''になる。
        fire_kbn: str = self._dic_kbns['fire'].get(self._fire_nam, '')
        fish_kbn: str = self._dic_kbns['fish'].get(self._fish_nam, '')

        update_datas: Dict[str, str] = {
            'mukesaki_kbn': mukesaki_kbn,
            'nonyusaki_kbn': nonyusaki_kbn,
            'hinban': hinban,
            'label_kbn': label_kbn,
            'fire_kbn': fire_kbn,
            'fish_kbn': fish_kbn
        }

        # label_dbにデータがあるかを調べる。
        is_exist_data_ship = self._check_is_exist_data(update_datas, 'ship')
        is_exist_data_air = self._check_is_exist_data(update_datas, 'air')
        if  is_exist_data_ship:
            print("""\nlabel_dbに既に「船」のデータがあります。
                  内容を上書きします。""")
            self._update_master(update_datas, 'ship')
        else:
            self._insert_data(update_datas, 'ship')

        if  is_exist_data_air:
            print("""\nlabel_dbに既に「エア」のデータがあります。
                  内容を上書きします。""")
            self._update_master(update_datas, 'air')
        else:
            self._insert_data(update_datas, 'air')


    def _insert_data(self, update_datas: Dict, 
                                ship_or_air: str)-> None:
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
                (LBL_DB_ID, MKSK_KBN, NNSK_KBN, UNSOU_KBN, ITEM_ID, 
                ITEM_LBL_KBN, FIRE_CHK_KBN, SAKANA_CHK_KBN, DANBORU_FLG, 
                DEL_FLG, INS_USER, INS_DTTM, INS_ID, UPD_USER, UPD_DTTM, 
                UPD_ID) 
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """

            # 挿入する値の準備
            # shipの場合
            ship_or_air_kbn = '01'
            fish_kbn = update_datas.get('fish_kbn') or None

            if ship_or_air == 'air':
                ship_or_air_kbn = '02'
                fish_kbn = None # airの場合は''になる

            # datetimeオブジェクトをそのまま渡せば、pyodbcドライバが自動的に
            # データベースが理解できるDATETIME型に変換してくれる(推奨)
            dttm_str = datetime.datetime.now().strftime('%Y/%m/%d %H%M%S')
            dttm_now = datetime.datetime.strptime(dttm_str, '%Y/%m/%d %H%M%S')

            params = (next_sequence_str,
                      update_datas['mukesaki_kbn'],
                      update_datas.get('nonyusaki_kbn') or None,
                      ship_or_air_kbn,
                      update_datas['hinban'],
                      update_datas['label_kbn'],
                      update_datas.get('fire_kbn') or None,
                      fish_kbn,
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
            print(f"label_dbに {ship_or_air} のデータを挿入しました。")

        except Exception as e:
            print(f"予期せぬエラーが発生しました: {e}")
            if self.cnxn:
                self.cnxn.rollback()
                print("トランザクションはロールバックされました。")
        finally:
            if cursor:
                cursor.close()


    def _check_is_exist_data(self, update_datas: Dict,
                             ship_or_air: str) -> bool:

        check_sql = """
        SELECT TOP 1 1 FROM TM_LBL_DB WHERE MKSK_KBN = ? 
        AND ISNULL(NNSK_KBN, '') = ? 
        AND UNSOU_KBN = ? AND ITEM_ID = ? AND DEL_FLG <> ?;
        """
        # SELECT TOP 1 1 whereが該当したら一回だけデータを取得し、1を返す
        # MySQLのLIMIIT 1 と同じ。

        # shipの場合
        ship_or_air_kbn = '01'

        if ship_or_air == 'air':
            ship_or_air_kbn = '02'

        params = (update_datas['mukesaki_kbn'],
                  update_datas['nonyusaki_kbn'],
                  ship_or_air_kbn,
                  update_datas['hinban'],
                  '1'
        )
        # get('fire_kbn') or '' とすることで、get('fire_kbn')が''が
        # 返っても、Noneが返っても偽になるのでorの右辺の''が返る

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
                       ship_or_air: str) -> None:

        update_sql = """
        UPDATE TM_LBL_DB 
        SET   ITEM_LBL_KBN = ?, FIRE_CHK_KBN = ?, SAKANA_CHK_KBN = ?,
              UPD_USER = ?, UPD_DTTM = ?, UPD_ID = ? 
        WHERE MKSK_KBN = ? AND ISNULL(NNSK_KBN, '') = ? AND UNSOU_KBN = ?
              AND ITEM_ID = ? AND DEL_FLG <> ?
        """
        # 挿入する値の準備
        # shipの場合
        ship_or_air_kbn = '01'
        fish_kbn = update_datas.get('fish_kbn') or None

        if ship_or_air == 'air':
            ship_or_air_kbn = '02'
            fish_kbn = None # airの場合は''になる

        # datetimeオブジェクトをそのまま渡せば、pyodbcドライバが自動的に
        # データベースが理解できるDATETIME型に変換してくれる(推奨)
        dttm_str = datetime.datetime.now().strftime('%Y/%m/%d %H%M%S')
        dttm_now = datetime.datetime.strptime(dttm_str, '%Y/%m/%d %H%M%S')

        params = (update_datas['label_kbn'],
                  update_datas.get('fire_kbn') or None,
                  fish_kbn,
                  'e05',
                  dttm_now,
                  'InsLblDbCh',
                  update_datas['mukesaki_kbn'],
                  update_datas.get('nonyusaki_kbn') or '',
                  ship_or_air_kbn,
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
            print(f"label_dbの {ship_or_air} のデータを更新しました。")

        except Exception as e:
            print(f"予期せぬエラーが発生しました: {e}")
            if self.cnxn:
                self.cnxn.rollback()
                print("トランザクションはロールバックされました。")
        finally:
            if cursor:
                cursor.close()


