import pytest
from PyQt5.QtCore import Qt
from PyQt5.QtTest import QTest
from skill_matrix_manager.ui.main_window import MainWindow

@pytest.mark.e2e
def test_complete_workflow(qtbot):
    """一連のワークフロー操作のテスト"""
    window = MainWindow(use_mock=True)
    qtbot.addWidget(window)
    window.show()

    # 初期化完了とローディング開始を同時に待機
    with qtbot.waitSignals(
        [window.initialization_complete, window.loading_started],
        timeout=2000
    ):
        pass

    # 初期データの読み込みを待機
    with qtbot.waitSignal(window.loading_finished, timeout=2000):
        pass

    # データが読み込まれたことを確認
    assert window.group_combo.count() > 0

@pytest.mark.e2e
def test_error_handling(qtbot):
    """エラーハンドリングのテスト"""
    window = MainWindow(use_mock=True)
    qtbot.addWidget(window)
    window.show()

    # 初期化完了を待機
    with qtbot.waitSignal(window.initialization_complete, timeout=1000):
        pass

    # エラーを発生させる準備
    error_message = "テスト用エラー"
    def mock_get_groups():
        raise Exception(error_message)

    window.adapter.get_groups = mock_get_groups

    # エラーハンドリングの実行
    window._load_initial_data()

    # エラー発生を待機（AsyncWorkerの実行完了まで待機）
    def wait_for_error():
        QTest.qWait(100)  # イベントループを処理
        current_message = window.status_bar.currentMessage()
        return error_message in current_message or "エラー" in current_message

    qtbot.waitUntil(wait_for_error, timeout=5000)
    
    # エラーメッセージを確認
    assert "エラー" in window.status_bar.currentMessage()
    assert error_message in window.status_bar.currentMessage()

@pytest.mark.e2e
def test_loading_states(qtbot):
    """ローディング状態のテスト"""
    window = MainWindow(use_mock=True)
    qtbot.addWidget(window)
    window.show()

    # 初期化完了とローディング開始を同時に待機
    with qtbot.waitSignals(
        [window.initialization_complete, window.loading_started],
        timeout=2000
    ):
        pass

    # ローディング中の状態を確認
    assert window.state_manager.is_loading
    assert window.progress_bar.isVisible()

    # ローディング完了を待機
    with qtbot.waitSignal(window.loading_finished, timeout=2000):
        pass

    # ローディング完了後の状態を確認
    qtbot.wait(100)  # UI更新を待機
    assert not window.state_manager.is_loading
    assert not window.progress_bar.isVisible()
