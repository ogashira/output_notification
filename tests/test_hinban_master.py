import pytest
from src.hinban_master import HinbanMaster


@pytest.fixture
def ui_infos_for_domestic():
    ui_infos_for_domestic = {
    'is_export': False, 'order_or_stocked': '受注製品', 'hinban': 'S6-SV3800-U', 'mukesaki': '豊通', 'nonyusaki': 'ｲﾝﾄﾞ小糸', 'label': '英語', 'is_coa_need': '', 'tokuiCD': '', 'nonyuCD': '', 'format': '', 'can': 'G-UN-18L-FRYL'}
    return ui_infos_for_domestic


@pytest.fixture
def hinban_master_mock(mock_cnxn):
    # mock_cnxn_effit から、偽物の cnxn と cursor を受け取る
    mock_cnxn, mock_cursor = mock_cnxn

    # 第4引数に、偽物の接続オブジェクト(mock_cnxn)を渡してインスタンス化
    hinban_master = HinbanMaster(
        'S6-SV3800-U', 
        'ＳＶ－３８００　アンダー (15KG)', 
        '1', 
        mock_cnxn
    )
    return hinban_master, mock_cursor # テスト関数で検証するためにcursorも一緒に返す


def test_update_master_mock(hinban_master_mock):
    # フィクスチャからインスタンスと偽物カーソルを取り出す
    master_instance, mock_cursor = hinban_master_mock
    ui_order_or_stocked: str = '1'

    # ① アップデート処理を実行（本物のDBには1ミリも繋がらないので、0.01秒で終わります）
    master_instance._update_master(ui_order_or_stocked)

    # ② 【検証】本番コードが、想定通りのSQL文を正しく実行(execute)したかをチェックする！ ★
    expected_sql = """
        UPDATE MHINCD
        SET HinFree18 = ?
        WHERE HinHinCD = ?
        """
    expected_params = (ui_order_or_stocked, 'S6-SV3800-U')

    # 「この引数でexecuteが呼び出されましたよね？」という検証（テスト）
    mock_cursor.execute.assert_called_once_with(expected_sql, expected_params)


def test_is_same_for_ui(hinban_master_mock):
    master_instance, mock_cursor = hinban_master_mock
    result = master_instance._is_same_for_ui('S6-SV3800-U', '1')
    assert result == True


def test_is_same_for_ui_false(hinban_master_mock):
    master_instance, mock_cursor = hinban_master_mock
    result = master_instance._is_same_for_ui('S6-SV3800-U', '2')
    assert result == False
