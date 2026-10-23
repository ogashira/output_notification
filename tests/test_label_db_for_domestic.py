import pytest
from typing import Dict, Any
from src.label_db_for_domestic import LabelDbForDomestic
from src.instance_factory import InstanceFactory


hinban = 'S6-SV3800L-U'
dic_kbns: Dict[str,Dict[str,str]] = {}
dic_kbns['mukesaki'] = {'本社': '01', '大阪': '02', '製造': '03', 
                        '豊通': '04', '長瀬': '05'}
dic_kbns['label'] = {'日本': '01', '日大中小': '02', '中国': '03', '英語': '04', '台湾': '05'}

update_datas: Dict[str, Any] = {
    'hinban': 'S6-SV3800L-U',
    'label_kbn': '01',
}


@pytest.fixture
def get_label_db_for_domestic():

    label_db_for_domestic = InstanceFactory.get_LabelDbForDomestic(hinban, 
                                           dic_kbns
                                           )

    return label_db_for_domestic


def test_check_is_exist_data_honsya(get_label_db_for_domestic):
    result = get_label_db_for_domestic._check_is_exist_data(update_datas,
                                                               'honsya')
    assert result == True


def test_check_is_exist_data_osaka(get_label_db_for_domestic):
    result = get_label_db_for_domestic._check_is_exist_data(update_datas,
                                                               'osaka')
    assert result == True
