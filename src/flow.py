# -*- coding: utf-8 -*-
import sys
from typing import List, Dict, TYPE_CHECKING
from instance_factory import InstanceFactory
import ui
from convert_data_structure import ConvertDataStructure
from get_idx import ogaColumnIndexError, GetIdx
from filter_data import FilterData


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
    _cans_fire_fish: Dict[str, Dict[str, bool]] = {}

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
                             cls._mukesaki_col, cls._mukesaki_data, 'mukesaki')
            cls._nonyusaki_col, cls._nonyusaki_data = fetchNonyusaki.fetch_data()
            nonyusakis:List[str] = \
                ConvertDataStructure.convert_2d_list_to_1d_list(
                           cls._nonyusaki_col, cls._nonyusaki_data, 'nonyusaki')
            cls._label_col, cls._label_data = fetchSeihinLabel.fetch_data()
            seihinLabels:List[str] = \
                ConvertDataStructure.convert_2d_list_to_1d_list(
                                  cls._label_col, cls._label_data, 'seihinLabel')
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
            cls._cans_fire_fish:Dict[str, Dict[str, bool]] = fetchCans.fetch_data()
            cans: List[str] = \
                ConvertDataStructure.convert_dict_dict_to_list(
                                            cls._cans_fire_fish, 'cans_for_export')
        except ogaColumnIndexError as e:
            InstanceFactory.delete_cnxn()
            print(e)
            sys.exit(1)

        #輸出用の向先のため、本社、大阪、製造は削除しておく
        mukesakis_export = []
        for mukesaki in mukesakis:
            if mukesaki not in ['本社', '大阪', '製造']:
                mukesakis_export.append(mukesaki)

        ui.run(hinbans, mukesakis_export, nonyusakis, 
                        seihinLabels, tokuis_dict, coaFormats, cans)

        InstanceFactory.delete_cnxn()


    @classmethod
    def start(cls, ui_infos: Dict[str, str]) ->None:
        """
        ui.py def press_start()から呼び出されるメイン処理
        """
        print(ui_infos)


        # ['S6-SV3800L-U', 'CN', 'Decimal('15000')', '2']
        hinban_data = FilterData.filter_data_from_2d_list(
                cls._hinban_data, cls._hinban_col, 'hinban', ui_infos['hinban']
                )
        hinban_idx:int = GetIdx.get_idx(cls._hinban_col, 'hinban')
        hin_name_idx:int = GetIdx.get_idx(cls._hinban_col, 'hin_name')
        order_or_stocked_idx:int = GetIdx.get_idx(cls._hinban_col, 'order_or_stock')
        hinban: str = hinban_data[hinban_idx]
        hin_name: str = hinban_data[hin_name_idx]
        order_or_stocked: str = hinban_data[order_or_stocked_idx]
    # ここに実際の業務ロジックを記述します
