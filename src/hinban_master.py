import pyodbc
from typing import Dict
from IUpdate_master import IUpdateMaster


class HinbanMaster(IUpdateMaster):
    def __init__(self,
                 hinban: str, hin_name: str, 
                 order_or_stocked: str,
                 cnxn)-> None:
        self.hinban = hinban
        self.hin_name = hin_name
        self.order_or_stocked = order_or_stocked # '1'なら受注品、'2'なら在庫品
        self.cnxn = cnxn

    def update_master(self, ui_infos: Dict[str, str])-> None:

        dic_order_stocked = {'受注製品': '1', '見込製品': '2'}

        ui_hinban: str = ui_infos['hinban']
        ui_order_or_stocked: str = dic_order_stocked[ui_infos['order_or_stocked']]
        is_exist_same_data:bool = self._is_same_for_ui(ui_hinban, 
                                                       ui_order_or_stocked)
        if is_exist_same_data:
            print("\n品番マスタの修正は不要です。")
            return 

        self._update_master(ui_order_or_stocked)


    def _is_same_for_ui(self, ui_hinban: str, ui_order_or_stocked: str) -> bool:
        return (self.hinban == ui_hinban and 
                self.order_or_stocked == ui_order_or_stocked)


    def _update_master(self, ui_order_or_stocked: str) -> None:
        # 2. 実行するSQL文（セキュリティのためプレースホルダ「?」を使用）
        sql = """
        UPDATE MHINCD
        SET HinFree18 = ?
        WHERE HinHinCD = ?
        """

        # パラメータの値をタプルで定義
        params = (ui_order_or_stocked, self.hinban )

        try:
            # 3. データベースへの接続と実行
            with self.cnxn.cursor() as cursor:
                # SQLの実行
                cursor.execute(sql, params)

                # 影響を受けた行数の確認
                print(f"\n品番マスター更新された行数: {cursor.rowcount}")

                # 変更を確定（コミット）
                self.cnxn.commit()
                print(f"{self.hinban} の品番マスターアップデートが正常に完了しました。")

        except Exception as e:
            print(f"\n品番マスターアップデートで予期せぬエラーが発生しました: {e}")
