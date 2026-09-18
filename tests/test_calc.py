import pytest
# src フォルダから Calc クラスをインポート
from calc import Calc

# --- 1. テスト用の共通準備（Fixture） ---
@pytest.fixture
def calc():
    """テストごとに毎回、初期値0の新しいCalcインスタンスを作成して返す"""
    return Calc(initial_value=0)


# --- 2. クラスを使ったテストのグループ化 ---
    
def test_add(calc):
    # 引数にフィクスチャ名（calc）を書くだけで、初期値0のインスタンスが自動で渡されます
    result = calc.add(5)
    assert result == 5
    assert calc.value == 5

def test_subtract(calc):
    result = calc.subtract(3)
    assert result == -3
    assert calc.value == -3

def test_multiple_operations(calc):
    # 連続でメソッドを呼び出すテスト
    calc.add(10)
    result = calc.subtract(4)
    assert result == 6

