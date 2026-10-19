# -*- coding: utf-8 -*-
import sys
from typing import List, Dict, TYPE_CHECKING, Optional, Any
from instance_factory import InstanceFactory
import ui
from convert_data_structure import ConvertDataStructure
from get_idx import ogaColumnIndexError, GetIdx
from filter_data import FilterData
from IUpdate_master import IUpdateMaster
from hinban_master import HinbanMaster
from label_identification import LabelIdentification
from label_db_for_export import LabelDbForExport
from nhm import Nhm


# 実行時にはインポートせず、型チェックの為だけに書く
if TYPE_CHECKING:
    from fetch_data_for_list import IFetchDataForList, FetchCans


class Flow:

    _hinban_col: List[str] = []
    _hinban_data: List[List[str]] = []
    _mukesaki_col: List[str] = []
    _mukesaki_data: List[List[str]] = []
    _nonyusaki_col: List[str] = []
    _nonyusaki_data: List[List[str]] = []
    _label_col: List[str] = []
    _label_data: List[List[str]] = []
    _tokui_dict: Dict[str, List[str]] = {}
    _coaformat_col: List[str] = []   # 向先_ｼｰﾄ表のデータ
    _coaformat_data: List[List[str]] = [] # 向先_ｼｰﾄ表のデータ
    _cans_fire_fish: Dict[str, Any] = {}

    @classmethod
    def ui_run(cls):
        fetchHinban:IFetchDataForList = InstanceFactory.get_fetchHinban()
        fetchMukesaki:IFetchDataForList = InstanceFactory.get_fetchMukesaki()
        fetchNonyusaki:IFetchDataForList = InstanceFactory.get_fetchNonyusaki()
        fetchSeihinLabel:IFetchDataForList = InstanceFactory.get_fetchSeihinLabel()
        fetchTokui:IFetchDataForList = InstanceFactory.get_fetchTokui()
        fetchCoaFormat:IFetchDataForList = InstanceFactory.get_fetchCoaMukesaki()
        fetchCans:FetchCans = InstanceFactory.get_fetchCans()

        try:
            cls._hinban_col, cls._hinban_data = fetchHinban.fetch_data()
            hinbans:List[str] = \
               ConvertDataStructure.convert_2d_list_to_1d_list(
                                    cls._hinban_col, cls._hinban_data, 'hinban')
            cls._mukesaki_col, cls._mukesaki_data = fetchMukesaki.fetch_data()
            mukesakis:List[str] = \
               ConvertDataStructure.convert_2d_list_to_1d_list(
                             cls._mukesaki_col, cls._mukesaki_data, 'mukesaki_nam')
            cls._nonyusaki_col, cls._nonyusaki_data = fetchNonyusaki.fetch_data()
            nonyusakis:List[str] = \
                ConvertDataStructure.convert_2d_list_to_1d_list(
                           cls._nonyusaki_col, cls._nonyusaki_data, 'nonyusaki_nam')
            cls._label_col, cls._label_data = fetchSeihinLabel.fetch_data()
            seihinLabels:List[str] = \
                ConvertDataStructure.convert_2d_list_to_1d_list(
                                  cls._label_col, cls._label_data, 'seihinLabel_nam')
            _tokuiCD_col, _tokuiCD_data = fetchTokui.fetch_data()
            tokuis_dict:Dict[str, List[str]] = \
                ConvertDataStructure.convert_2d_list_to_3args_dict(
                                        _tokuiCD_col, _tokuiCD_data, 'tokuiCD',
                                                        'nonyuCD', 'tokuiRyaku')
            # 向先_ｼｰﾄ表のデータを取得
            cls._coaformat_col, cls._coaformat_data = fetchCoaFormat.fetch_data()
            coaFormats: List[str] = \
                ConvertDataStructure.convert_2d_list_to_1d_list(
                                 cls._coaformat_col, cls._coaformat_data, '向先')
            coaFormats = list(set(coaFormats)) # 重複を消す
            coaFormats.append('ﾒﾀﾙ') # メタルを追加

            # output_notification.ymlのデータを取得
            cls._cans_fire_fish:Dict[str, Any] = fetchCans.fetch_data()
            cans: List[str] = \
                ConvertDataStructure.convert_dict_dict_dict_to_list(
                                            cls._cans_fire_fish, 'cans_for_export')
        except ogaColumnIndexError as e:
            InstanceFactory.delete_cnxn()
            print(e)
            InstanceFactory.delete_cnxn()
            sys.exit(1)

        #輸出用の向先のため、本社、大阪、製造は削除しておく
        mukesakis_export = []
        for mukesaki in mukesakis:
            if mukesaki not in ['本社', '大阪', '製造']:
                mukesakis_export.append(mukesaki)

        ui.run(hinbans, mukesakis_export, nonyusakis, 
                        seihinLabels, tokuis_dict, coaFormats, cans)


    @classmethod
    def start(cls, ui_infos: Dict[str, str]) ->None:
        """
        ui.py def press_start()から呼び出されるメイン処理
        """
        print(ui_infos)



        # ['S6-SV3800L-U', 'ＳＶ－３８００Ｌ\u3000アンダー (15KG)', 'Decimal('15000')', '2']
        hinban_data: List[str] = FilterData.filter_data_from_2d_list(
                cls._hinban_data, cls._hinban_col, 'hinban', ui_infos['hinban']
                )
        if hinban_data == []:
            # ユーザーが入力したhinbanがない場合は、エラーメッセージを表示して終了
            print("品番マスタに入力した品番がありません。処理を中止します。")
            InstanceFactory.delete_cnxn()
            sys.exit(1)

        hinban_idx:int = GetIdx.get_idx(cls._hinban_col, 'hinban')
        hin_name_idx:int = GetIdx.get_idx(cls._hinban_col, 'hin_name')
        order_or_stocked_idx:int = GetIdx.get_idx(cls._hinban_col, 'order_or_stock')
        hinban: str = hinban_data[hinban_idx]
        hin_name: str = hinban_data[hin_name_idx]
        order_or_stocked: str = hinban_data[order_or_stocked_idx]


        # HinbanMaster:IUpdateMasterのインスタンスを作成
        hinban_master:IUpdateMaster = InstanceFactory.get_HinbanMaster(
                hinban, hin_name, order_or_stocked)
        hinban_master.update_master(ui_infos)


        # LabelIdentification:LabelIdentificationのインスタンスを作成
        label_identification: Optional[LabelIdentification] = None
        try:
            if ui_infos['is_export']:
                label_identification = \
                    InstanceFactory.get_LabelIdentification(ui_infos, 
                                        cls._mukesaki_col, cls._mukesaki_data,
                                        cls._nonyusaki_col, cls._nonyusaki_data)
                if label_identification is None:
                    print("\nラベル識別コードのインスタンス生成できないため、N&H&Mのアップデートができませんでした。")
        # ラベル識別コードのdataがない場合は、エラーメッセージを表示して終了
        except Exception as e: # InstanceFactory.get_LabelIdentificationでThrow
            print(f'{e} プログラムを終了します。')
            InstanceFactory.delete_cnxn()
            sys.exit(1)

        # N&H&Mのインスタンスを作成
        nhm: Optional[Nhm] = None
        if ui_infos['is_export'] and label_identification is not None:
            nhm = InstanceFactory.get_Nhm(label_identification, hinban, hin_name)
            nhm.update_master(ui_infos)

        # fish_kbn, fire_kbn, unsou_kbnのインスタンスを作成
        fetch_fish_kbn: IFetchDataForList = InstanceFactory.get_fetchFishKubun()
        fetch_fire_kbn: IFetchDataForList = InstanceFactory.get_fetchFireKubun()
        fetch_unsou_kbn: IFetchDataForList = InstanceFactory.get_fetchUnsouKubun()
        fish_kbn_col, fish_kbn_data = fetch_fish_kbn.fetch_data()
        fire_kbn_col, fire_kbn_data = fetch_fire_kbn.fetch_data()
        unsou_kbn_col, unsou_kbn_data = fetch_unsou_kbn.fetch_data()

        # cls._mukesaki, cls._nonyusaki, cls._label, fish_kbn, fire_kbn, unsou_kbnをdictにする
        # dic_kbs {'mukesaki': {'本社': '01',...}, 'nonyusaki':{'ﾀｲｽﾀﾝﾚｰ':'09',...}...} を作る
        try:
            dic_mukesakis: Dict[str,str] = \
                    ConvertDataStructure.convert_2d_list_to_1d_dict(
                        cls._mukesaki_col, cls._mukesaki_data,
                        'mukesaki_nam', 'mukesaki_kbn'
                    )    # key, valueの順になるようにする
            dic_nonyusakis: Dict[str,str] = \
                    ConvertDataStructure.convert_2d_list_to_1d_dict(
                        cls._nonyusaki_col, cls._nonyusaki_data, 
                        'nonyusaki_nam', 'nonyusaki_kbn'
                    )
            dic_labels: Dict[str,str] = \
                    ConvertDataStructure.convert_2d_list_to_1d_dict(
                        cls._label_col, cls._label_data,
                        'seihinLabel_nam', 'seihinLabel_kbn'
                    )
            dic_fishes: Dict[str,str] = \
                    ConvertDataStructure.convert_2d_list_to_1d_dict(
                        fish_kbn_col, fish_kbn_data,
                        'fish_display', 'fish_kbn'
                    )
            dic_fires: Dict[str,str] = \
                    ConvertDataStructure.convert_2d_list_to_1d_dict(
                        fire_kbn_col, fire_kbn_data,
                        'fire_display', 'fire_kbn'
                    )
            dic_unsous: Dict[str,str] = \
                    ConvertDataStructure.convert_2d_list_to_1d_dict(
                        unsou_kbn_col, unsou_kbn_data,
                        'unsou_display', 'unsou_kbn'
                    )

        except ogaColumnIndexError as e:
            InstanceFactory.delete_cnxn()
            print(f'{e} プログラムを終了します。')
            sys.exit(1)

        dic_kbns: Dict[str,Dict[str, str]] = {}
        dic_kbns['mukesaki'] = dic_mukesakis
        dic_kbns['nonyusaki'] = dic_nonyusakis
        dic_kbns['label'] = dic_labels
        dic_kbns['fish'] = dic_fishes
        dic_kbns['fire'] = dic_fires
        dic_kbns['unsou'] = dic_unsous

        # LabelDbForExportのインスタンスを作成
        if ui_infos['is_export']:
            can:str = ui_infos['can']
            is_exist_fire_print: bool = \
                cls._cans_fire_fish['cans_for_export'][can]['fire_print']
            is_exist_fish_print: bool = \
                cls._cans_fire_fish['cans_for_export'][can]['fish_print']


            try:
                label_db_for_export: IUpdateMaster = \
                    InstanceFactory.get_LabelDbForExport(
                        hinban, can, is_exist_fire_print, is_exist_fish_print,
                        dic_kbns
                    )
            except Exception as e:
                print(f'{e} label_dbにデータを追加できませんでした。')




        InstanceFactory.delete_cnxn()
