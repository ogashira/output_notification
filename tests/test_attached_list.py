import pytest
from src.attached_list import AttachedList
from src.fetch_data_for_list import FetchCoaMukesaki


@pytest.fixture
def get_AttachedList():
    fetch_coa_mukesaki: FetchCoaMukesaki = FetchCoaMukesaki()
    coaFormat_col, coaFormat_data = fetch_coa_mukesaki.fetch_data()
    hinban = 'S6-UV361-U'
    hin_name = 'UV-361アンダー(15KG)'
    attached_list = AttachedList(hinban, hin_name, coaFormat_col, coaFormat_data)
    return attached_list


@pytest.fixture
def get_AttachedList2():
    fetch_coa_mukesaki: FetchCoaMukesaki = FetchCoaMukesaki()
    coaFormat_col, coaFormat_data = fetch_coa_mukesaki.fetch_data()
    hinban = 'S6-UV382V-T'
    hin_name = 'UV-382Vトップ(15KG)'
    attached_list2 = AttachedList(hinban, hin_name, coaFormat_col, coaFormat_data)
    return attached_list2


def test_slice_nonyuCD_blank(get_AttachedList):
    result = get_AttachedList._slice_nonyuCD('    -> ほげ')
    assert result == ''


def test_slice_nonyuCD(get_AttachedList):
    result = get_AttachedList._slice_nonyuCD('H90013    -> ほげ')
    assert result == 'H90013'


def test_slice_tokuisaki_name(get_AttachedList):
    result = get_AttachedList._slice_tokuisaki_name('H90013    -> ほげ')
    assert result == 'ほげ'


def test_get_atena_bar(get_AttachedList):
    result = get_AttachedList._get_atena('一般品')
    assert result == '-'
def test_get_atena_asahi(get_AttachedList):
    result = get_AttachedList._get_atena('旭真空')
    assert result == '旭真空株式会社　御中'

def test_check_is_exist_data(get_AttachedList):
    result = get_AttachedList._check_is_exist_data('T0600', None)
    assert result == True

def test_check_is_exist_data2(get_AttachedList2):
    result = get_AttachedList2._check_is_exist_data('T2880', 'H172')
    assert result == True
