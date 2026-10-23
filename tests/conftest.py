import pytest
from _pytest.monkeypatch import MonkeyPatch
from unittest.mock import MagicMock
from src.instance_factory import InstanceFactory


@pytest.fixture(scope="function")
def mock_cnxn(monkeypatch):
    # 100%偽物の「接続」と「カーソル」オブジェクトを作る
    mock_cnxn = MagicMock()
    mock_cursor = MagicMock()

    '''
    【最重要】withステートメントcursor() の __enter__() が mock_cursor を返すように紐付ける
    mock_cnxn.cursor()の戻り値(mock_cnxn.cursor.return_value)の、
    さらに__enter__()の戻り値(__enter__.return_value)をmock_cursorに紐付ける
    withステートメントを使っていなかったら
    mock_cnxn.cursor.return_value = mock_cursor で良い。
    '''
    mock_cnxn.cursor.return_value.__enter__.return_value = mock_cursor

    '''
    # 3. 本番コードが get_cnxn() を呼び出したら、この偽物の接続を返すように上書き
    monkeypatch.setattr(
        "sql_server_effit_addmin.SqlServer.get_cnxn", 
        lambda self: mock_cnxn
    )
'''
    # テスト関数側で「どんなSQLが流れたか」を検証できるように、
    # 偽物の 接続(cnxn) と カーソル(cursor) をセットで貸し出す
    yield mock_cnxn, mock_cursor


@pytest.fixture(scope="session", autouse=True)
def close_db_connections_after_all_tests():
    """
    全テストの実行前後に自動実行されるフィクスチャ。
    yield より前がテスト開始前、yield より後が全テスト終了後に実行されます。
    """
    yield
    # 全テスト終了時に接続をクローズ
    InstanceFactory.delete_cnxn()

'''
• scope="session": テストセッション全体で1回だけ有効になります。
• autouse=True: 各テスト関数の引数に書かなくても、自動的に適用されます。
• yield: テスト実行を挟み、全テストが完了した直後に InstanceFactory.
delete_cnxn() が呼び出されます。
''' 
