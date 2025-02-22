import pytest
from PyQt5.QtWidgets import QApplication, QTabWidget
from skill_matrix_manager.ui.main_window import MainWindow

@pytest.fixture
def app():
    return QApplication([])

@pytest.fixture
def main_window(app):
    return MainWindow()

def test_initial_tabs(main_window):
    """初期タブの確認"""
    tab_widget = main_window.tab_widget
    assert tab_widget.count() == 2
    assert tab_widget.tabText(0) == "スキル分析"
    assert tab_widget.tabText(1) == "システム管理"

def test_system_management_subtabs(main_window):
    """システム管理タブのサブタブ確認"""
    system_tab = main_window.system_management_tab
    subtabs = system_tab.findChild(QTabWidget)
    assert subtabs is not None
    assert subtabs.count() == 3
    assert subtabs.tabText(0) == "初期設定"
    assert subtabs.tabText(1) == "データ入出力"
    assert subtabs.tabText(2) == "システム情報"

def test_main_window_layout(main_window):
    """メインウィンドウのレイアウト確認"""
    # グループ選択コンボボックスの存在確認
    assert main_window.group_combo is not None
    
    # ユーザーリストの存在確認
    assert main_window.user_list is not None

