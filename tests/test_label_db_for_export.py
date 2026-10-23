import pytest
from typing import Dict, Any
from src.label_db_for_export import LabelDbForExport
from src.calc_fire_and_fish_kubun import CalcFireAndFishKubun
from src.instance_factory import InstanceFactory
from src.get_idx import GetIdx


ghs_col = ['ghs_class', 'ghs_fire', 'ghs_fish']
ghs_data = ['ｸﾗｽ3', '○', '×']
can_hinban = 'G-UN-18L-FRYL'
is_exist_fire_print = True
is_exist_fish_print = True

hinban = 'S6-UV542BBA-U-R-EX'
dic_kbns: Dict[str,Dict[str,str]] = {}
dic_kbns['mukesaki'] = {'本社': '01', '大阪': '02', '製造': '03', 
                        '豊通': '04', '長瀬': '05'}
dic_kbns['nonyusaki'] = {'ﾀｲｽﾀﾝﾚｰ': '09', 'ﾀｲ美光': '11'}
dic_kbns['label'] = {'日本': '01', '日大中小': '02', '中国': '03', '英語': '04', '台湾': '05'}
dic_kbns['unsou'] = {'船': '01', 'エア': '02' }

update_datas: Dict[str, Any] = {
    'mukesaki_kbn': '04',
    'nonyusaki_kbn': '11',
    'unsou_kbn': '01',
    'hinban': 'S6-UV542BBA-U-R-EX',
    'label_kbn': '04',
    'fire_kbn': '',
    'fish_kbn': '02'
}


@pytest.fixture
def get_label_db_for_export():

    label_db_for_export = InstanceFactory.get_LabelDbForExport(hinban, can_hinban, 
                                           is_exist_fire_print,
                                           is_exist_fish_print, 
                                           dic_kbns
                                           )

    return label_db_for_export


def test_check_is_exist_data_ship(get_label_db_for_export):
    result = get_label_db_for_export._check_is_exist_data(update_datas,
                                                               'ship')
    assert result == True


def test_check_is_exist_data_air(get_label_db_for_export):
    result = get_label_db_for_export._check_is_exist_data(update_datas,
                                                               'air')
    assert result == True

