from src.convert_data_structure import ConvertDataStructure
from src.get_idx import GetIdx

def test_convert_2d_list_to_1d_dict():
    cols = ['a', 'b', 'c']
    data = [['1', '2', '3'], ['4', '5', '6']]
    cols2 = ['mukesaki_nam', 'mukesaki_kbn', 'tokuiCD']
    data2 = [
            ['本社', '01', None], 
            ['大阪', '02', None],
            ['製造', '03', None],
            ['豊通', '04', 'T1210']
            ]
    result = ConvertDataStructure.convert_2d_list_to_1d_dict(cols, data, 'a', 'b')
    result2 = ConvertDataStructure.convert_2d_list_to_1d_dict(cols, data, 'a', 'c')
    result3 = ConvertDataStructure.convert_2d_list_to_1d_dict(
            cols2, data2, 'mukesaki_nam', 'mukesaki_kbn')
    assert result == {'1': '2', '4': '5'}
    assert result2 == {'1': '3', '4': '6'}
    assert result3 == {'本社': '01', '大阪': '02', '製造': '03', '豊通': '04'}


