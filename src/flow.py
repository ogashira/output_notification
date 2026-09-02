# -*- coding: utf-8 -*-
import sys
from typing import List, Dict
from instance_factory import InstanceFactory
import ui


class ogaColumnIndexError(Exception):
    pass


def get_idx(cols:List[str], col_name:str)-> int:
    idx: int = -1
    for i in range(len(cols)):
        if cols[i] == col_name:
            idx = i
            break
    return idx

def get_hinbans(cols, data, col_name) -> List[str]:
    hinbans: List[str] = []
    idx = get_idx(cols, col_name)
    if idx == -1:
        raise ogaColumnIndexError('品番マスターのカラムが不正です。')

    for line in data:
        hinbans.append(line[idx])
    return hinbans

def get_list(cols, data, col_name) -> List[str]:
    resultList: List[str] = []
    idx = get_idx(cols, col_name)
    if idx == -1:
        raise ogaColumnIndexError(f'{col_name}のカラムが不正です。')

    for line in data:
        resultList.append(line[idx])
    return resultList


def create_list_from_dict(dict: Dict[str, Dict[str, bool]]) -> List[str]:
    list: List[str] = []
    for key in dict['cans_for_export']:
        list.append(key)
    return list


def get_nonyuList_dict(cols, data) -> Dict[str, List[str]]:
    resultDict: Dict[str, List[str]] = {}
    tokui_idx: int = get_idx(cols, 'tokuiCD')     
    nonyu_idx: int = get_idx(cols, 'nonyuCD')
    ryaku_idx: int = get_idx(cols, 'tokuiRyaku')
    if tokui_idx == -1 or nonyu_idx == -1 or ryaku_idx == -1:
        raise ogaColumnIndexError('得意先コードのカラムが不正です。')

    for line in data:
        nonyu_cd = line[nonyu_idx]
        if nonyu_cd ==  ' ':
            nonyu_cd = '     '
        strs = f'{nonyu_cd} -> {line[ryaku_idx]}'
        if not line[tokui_idx] in resultDict:
            resultDict[line[tokui_idx]] = [strs]
        else:
            resultDict[line[tokui_idx]].append(strs)

    return resultDict


def ui_run():
    fetchHinban = InstanceFactory.get_fetchHinban()
    fetchMukesaki = InstanceFactory.get_fetchMukesaki()
    fetchNonyusaki = InstanceFactory.get_fetchNonyusaki()
    fetchSeihinLabel = InstanceFactory.get_fetchSeihinLabel()
    fetchTokui = InstanceFactory.get_fetchTokui()
    fetchCoaFormat = InstanceFactory.get_fetchCoaMukesaki()
    fetchCans = InstanceFactory.get_fetchCans()
    try:
        cols, data = fetchHinban.fetch_data()
        hinbans:List[str] = get_hinbans(cols, data, 'hinban')
        cols, data = fetchMukesaki.fetch_data()
        mukesakis:List[str] = get_list(cols, data, 'mukesaki')
        cols, data = fetchNonyusaki.fetch_data()
        nonyusakis:List[str] = get_list(cols, data, 'nonyusaki')
        cols, data = fetchSeihinLabel.fetch_data()
        seihinLabels:List[str] = get_list(cols, data, 'seihinLabel')
        cols, data = fetchTokui.fetch_data()
        tokuis_dict:Dict[str, List[str]] = get_nonyuList_dict(cols, data)
        cols, data = fetchCoaFormat.fetch_data()
        coaFormats: List[str] = get_list(cols, data, '向先')
        coaFormats = list(set(coaFormats)) # 重複を消す
        coaFormats.append('ﾒﾀﾙ')
        cans_fire_fish:Dict[str, Dict[str, bool]] = fetchCans.fetch_data()
        cans: List[str] = create_list_from_dict(cans_fire_fish)
    except ogaColumnIndexError as e:
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




def start(ui_infos: Dict[str, str]) ->None:
    """
    ui.py def press_start()から呼び出されるメイン処理
    """

    print(ui_infos)

    # ここに実際の業務ロジックを記述します
