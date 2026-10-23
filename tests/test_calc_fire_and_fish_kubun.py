import pytest
from src.calc_fire_and_fish_kubun import CalcFireAndFishKubun
from src.get_idx import GetIdx

@pytest.fixture
def get_calc_fireAndFishKubun():
    ghs_col = ['ghs_class', 'ghs_fire', 'ghs_fish']
    ghs_data = ['ｸﾗｽ3', '○', '×']
    can_hinban = 'G-UN-18L-FRYL'
    is_exist_fire_print = True
    is_exist_fish_print = True
    calc_fireAndFishKubun = CalcFireAndFishKubun(ghs_col, ghs_data, 
                                                 can_hinban, is_exist_fire_print, 
                                                 is_exist_fish_print)
    return calc_fireAndFishKubun

@pytest.fixture
def get_calc_fireAndFishKubun2():
    ghs_col = ['ghs_class', 'ghs_fire', 'ghs_fish']
    ghs_data = ['ｸﾗｽ4.1', '○', '×']
    can_hinban = 'G-UN-18L-FRYL'
    is_exist_fire_print = True
    is_exist_fish_print = True
    calc_fireAndFishKubun = CalcFireAndFishKubun(ghs_col, ghs_data, 
                                                 can_hinban, is_exist_fire_print, 
                                                 is_exist_fish_print)
    return calc_fireAndFishKubun

@pytest.fixture
def get_calc_fireAndFishKubun3():
    ghs_col = ['ghs_class', 'ghs_fire', 'ghs_fish']
    ghs_data = ['ｸﾗｽ4.1', '×', '×']
    can_hinban = 'G-UN-18L-FRYL'
    is_exist_fire_print = False
    is_exist_fish_print = True
    calc_fireAndFishKubun = CalcFireAndFishKubun(ghs_col, ghs_data, 
                                                 can_hinban, is_exist_fire_print, 
                                                 is_exist_fish_print)
    return calc_fireAndFishKubun

@pytest.fixture
def get_calc_fireAndFishKubun4():
    ghs_col = ['ghs_class', 'ghs_fire', 'ghs_fish']
    ghs_data = ['ｸﾗｽ4.1', '○', '×']
    can_hinban = 'G-UN-18L-FRYL'
    is_exist_fire_print = False
    is_exist_fish_print = True
    calc_fireAndFishKubun = CalcFireAndFishKubun(ghs_col, ghs_data, 
                                                 can_hinban, is_exist_fire_print, 
                                                 is_exist_fish_print)
    return calc_fireAndFishKubun

def test_init(get_calc_fireAndFishKubun):

    assert get_calc_fireAndFishKubun.is_need_fire == True
    assert get_calc_fireAndFishKubun.is_need_fish == False
    assert get_calc_fireAndFishKubun.class_rank == 'ｸﾗｽ3'

def test_calc_fire_kubun(get_calc_fireAndFishKubun):
    fire_kbn = get_calc_fireAndFishKubun.calc_fire_nam()
    assert fire_kbn == ''

def test_calc_fire_kubun2(get_calc_fireAndFishKubun2):
    fire_kbn = get_calc_fireAndFishKubun2.calc_fire_nam()
    assert fire_kbn == 'ｸﾗｽ4.1'

def test_calc_fire_kubun3(get_calc_fireAndFishKubun3):
    fire_kbn = get_calc_fireAndFishKubun3.calc_fire_nam()
    assert fire_kbn == 'ｸﾗｽ4.1'

def test_calc_fire_kubun4(get_calc_fireAndFishKubun4):
    fire_kbn = get_calc_fireAndFishKubun4.calc_fire_nam()
    assert fire_kbn == '○'


'''
ここからcalc_fish_kubunのテスト>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
'''
@pytest.fixture
def get_calc_fireAndFishKubun5():
    ghs_col = ['ghs_class', 'ghs_fire', 'ghs_fish']
    ghs_data = ['ｸﾗｽ3', '○', '×']
    can_hinban = 'G-UN-18L-FRYL'
    is_exist_fire_print = False
    is_exist_fish_print = True
    calc_fireAndFishKubun = CalcFireAndFishKubun(ghs_col, ghs_data, 
                                                 can_hinban, is_exist_fire_print, 
                                                 is_exist_fish_print)
    return calc_fireAndFishKubun

def test_calc_fish_kubun5(get_calc_fireAndFishKubun5):
    fish_kbn = get_calc_fireAndFishKubun5.calc_fish_nam()
    assert fish_kbn == ''


@pytest.fixture
def get_calc_fireAndFishKubun6():
    ghs_col = ['ghs_class', 'ghs_fire', 'ghs_fish']
    ghs_data = ['ｸﾗｽ3', '○', '×']
    can_hinban = 'G-UN-18L-FRYL'
    is_exist_fire_print = False
    is_exist_fish_print = False
    calc_fireAndFishKubun = CalcFireAndFishKubun(ghs_col, ghs_data, 
                                                 can_hinban, is_exist_fire_print, 
                                                 is_exist_fish_print)
    return calc_fireAndFishKubun

def test_calc_fish_kubun6(get_calc_fireAndFishKubun6):
    fish_kbn = get_calc_fireAndFishKubun6.calc_fish_nam()
    assert fish_kbn == ''


@pytest.fixture
def get_calc_fireAndFishKubun7():
    ghs_col = ['ghs_class', 'ghs_fire', 'ghs_fish']
    ghs_data = ['ｸﾗｽ3', '○', '○']
    can_hinban = 'G-UN-18L-FRYL'
    is_exist_fire_print = False
    is_exist_fish_print = True
    calc_fireAndFishKubun = CalcFireAndFishKubun(ghs_col, ghs_data, 
                                                 can_hinban, is_exist_fire_print, 
                                                 is_exist_fish_print)
    return calc_fireAndFishKubun

def test_calc_fish_kubun7(get_calc_fireAndFishKubun7):
    fish_kbn = get_calc_fireAndFishKubun7.calc_fish_nam()
    assert fish_kbn == 'F'


@pytest.fixture
def get_calc_fireAndFishKubun8():
    ghs_col = ['ghs_class', 'ghs_fire', 'ghs_fish']
    ghs_data = ['ｸﾗｽ3', '○', '○']
    can_hinban = 'G-UN-18L-FRYL'
    is_exist_fire_print = False
    is_exist_fish_print = False
    calc_fireAndFishKubun = CalcFireAndFishKubun(ghs_col, ghs_data, 
                                                 can_hinban, is_exist_fire_print, 
                                                 is_exist_fish_print)
    return calc_fireAndFishKubun

def test_calc_fish_kubun8(get_calc_fireAndFishKubun8):
    fish_kbn = get_calc_fireAndFishKubun8.calc_fish_nam()
    assert fish_kbn == '○'
