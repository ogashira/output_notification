from src.label_identification import LabelIdentification

def test_create_tokuiCDs_dict():
    label_identification = LabelIdentification(
        ['mukesaki_kbn', 'nonyusaki_kbn', 'nonyuAlphabet', 
         'nonyuNoMin', 'nonyuNoMax'],
        ['04', '09', 'THS', '5', '12'],
        'T0210', 'タイスタンレー'
    )
    result = label_identification.create_tokuiCDs_dict()
    assert result == {'T0210': ['THS05', 'THS06', 'THS07', 'THS08', 
                                'THS09', 'THS10', 'THS11', 'THS12']}

