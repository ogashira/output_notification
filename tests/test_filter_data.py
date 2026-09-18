import pytest
from filter_data import FilterData
from get_idx import GetIdx, ogaColumnIndexError
from fetch_data_for_list import FetchHinban
from instance_factory import InstanceFactory

@pytest.fixture
def fetch_hinban():
    fetch_hinban = InstanceFactory.get_fetchHinban()
    return fetch_hinban


def test_filter_data_from_2d_list(fetch_hinban):
    col, data = fetch_hinban.fetch_data()
    col_name = 'hinban'
    str_to_filter = 'S6-SV3800-U'

    idx = GetIdx.get_idx(col, col_name)
    if idx == -1:
        raise ogaColumnIndexError(f'{col_name}のカラムが不正です。')

    result = FilterData.filter_data_from_2d_list(data, col, col_name, str_to_filter)

    assert result[0] == 'S6-SV3800-U'
    assert result[2] == 15000
    assert result[3] == "2"

