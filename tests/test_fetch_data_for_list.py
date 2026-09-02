import pytest

from src.fetch_data_for_list import FetchCans

@pytest.fixture
def fetch_cans():
    return FetchCans()

def test_fetch_data(fetch_cans):
    result = fetch_cans.fetch_data()
    assert result['cans_for_export']['G-UN-18L-FRYL'] == {'fire_print': True, 'fish_print': True}
