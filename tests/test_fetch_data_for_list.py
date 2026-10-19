import pytest
from src.fetch_data_for_list import FetchGhsDb
from src.instance_factory import InstanceFactory

@pytest.fixture
def get_fetchGhsDb():
    fetchGhsDb = InstanceFactory.get_fetchGhsDb('S6-SV3400A-U-EX')
    return fetchGhsDb

@pytest.fixture
def get_fetchFishKubun():
    fetchFishKubun = InstanceFactory.get_fetchFishKubun()
    return fetchFishKubun


@pytest.fixture
def get_fetchFireKubun():
    fetchFireKubun = InstanceFactory.get_fetchFireKubun()
    return fetchFireKubun


@pytest.fixture
def get_fetchUnsouKubun():
    fetchUnsouKubun = InstanceFactory.get_fetchUnsouKubun()
    return fetchUnsouKubun


@pytest.fixture
def get_fetchMukesaki():
    fetchMukesaki = InstanceFactory.get_fetchMukesaki()
    return fetchMukesaki


def test_fetchGhsDb(get_fetchGhsDb):
    col, data = get_fetchGhsDb.fetch_data()
    assert data == [
                ['ｸﾗｽ3', '○', '×']
                ]

def test_fetchFishKubun(get_fetchFishKubun):
    col, data = get_fetchFishKubun.fetch_data()
    assert col == ['fish_display', 'fish_kbn']
    assert data == [['〇', '01'], ['F', '02']]


def test_fetchFireKubun(get_fetchFireKubun):
    col, data = get_fetchFireKubun.fetch_data()
    assert col == ['fire_display', 'fire_kbn']
    assert data == [['ｸﾗｽ9', '01'], 
                    ['ｸﾗｽ6.1', '02'],
                    ['ｸﾗｽ4.1', '03'],
                    ['〇', '04'],
                    ]


def test_fetchUnsouKubun(get_fetchUnsouKubun):
    col, data = get_fetchUnsouKubun.fetch_data()
    assert col == ['unsou_display', 'unsou_kbn']
    assert data == [['船', '01'], ['エア', '02']]


def test_fetchMukesaki(get_fetchMukesaki):
    col, data = get_fetchMukesaki.fetch_data()
    assert col == ['mukesaki_nam', 'mukesaki_kbn', 'tokuiCD']
    assert data[:4] == [
            ['本社', '01', None], 
            ['大阪', '02', None],
            ['製造', '03', None],
            ['豊通', '04', 'T1210']
            ]


