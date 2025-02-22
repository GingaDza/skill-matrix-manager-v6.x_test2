import pytest
from datetime import datetime
from skill_matrix_manager.utils.state_monitor import state_monitor

@pytest.fixture(autouse=True)
def setup_test_environment():
    """テスト環境のセットアップ"""
    # テスト用の状態をセット
    state_monitor._current_datetime = datetime(2025, 2, 21, 12, 4, 58)
    state_monitor._current_user = 'GingaDza'
    
    yield
    
    # テスト後のクリーンアップ
    state_monitor.clear_history()
