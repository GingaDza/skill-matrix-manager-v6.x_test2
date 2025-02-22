import pytest
from PyQt5.QtWidgets import QApplication, QPushButton, QTreeWidget
from skill_matrix_manager.adapters.original_ui_adapter import OriginalUIAdapter
from skill_matrix_manager.views.initial_setup_tab import InitialSetupTab

@pytest.fixture
def app():
    return QApplication([])

@pytest.fixture
def initial_setup_tab(app):
    return InitialSetupTab()

@pytest.fixture
def adapter(initial_setup_tab):
    return OriginalUIAdapter(initial_setup_tab)

def test_adapter_initialization(adapter, initial_setup_tab):
    """アダプターの初期化テスト"""
    assert adapter.view == initial_setup_tab
    assert isinstance(adapter.view.add_group_btn, QPushButton)
    assert isinstance(adapter.view.category_tree, QTreeWidget)

def test_button_connections(adapter):
    """ボタン接続のテスト"""
    # 各ボタンのシグナル接続数を確認
    assert adapter.view.add_group_btn.receivers(adapter.view.add_group_btn.clicked) > 0
    assert adapter.view.edit_group_btn.receivers(adapter.view.edit_group_btn.clicked) > 0
    assert adapter.view.delete_group_btn.receivers(adapter.view.delete_group_btn.clicked) > 0
    assert adapter.view.add_category_btn.receivers(adapter.view.add_category_btn.clicked) > 0
    assert adapter.view.add_skill_btn.receivers(adapter.view.add_skill_btn.clicked) > 0
    assert adapter.view.add_tab_btn.receivers(adapter.view.add_tab_btn.clicked) > 0

def test_event_handlers_exist(adapter):
    """イベントハンドラーの存在確認"""
    assert hasattr(adapter, 'handle_add_group')
    assert hasattr(adapter, 'handle_edit_group')
    assert hasattr(adapter, 'handle_delete_group')
    assert hasattr(adapter, 'handle_add_category')
    assert hasattr(adapter, 'handle_add_skill')
    assert hasattr(adapter, 'handle_add_tab')

def test_view_update_methods_exist(adapter):
    """ビュー更新メソッドの存在確認"""
    assert hasattr(adapter, 'update_view')
    assert hasattr(adapter, 'update_group_list')
    assert hasattr(adapter, 'update_category_tree')
