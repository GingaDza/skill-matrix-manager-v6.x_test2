import pytest
from PyQt5.QtWidgets import QApplication, QMessageBox
from PyQt5.QtCore import Qt
from skill_matrix_manager.ui.components.group_dialog import GroupDialog
from skill_matrix_manager.views.initial_setup_tab import InitialSetupTab
from skill_matrix_manager.adapters.original_ui_adapter import OriginalUIAdapter
from skill_matrix_manager.models.data_models import Group

@pytest.fixture
def app():
    return QApplication([])

@pytest.fixture
def initial_setup_tab(app):
    return InitialSetupTab()

@pytest.fixture
def adapter(initial_setup_tab):
    return OriginalUIAdapter(initial_setup_tab)

def test_group_dialog_create(app):
    """グループ作成ダイアログのテスト"""
    dialog = GroupDialog()
    assert dialog.windowTitle() == "グループ追加"
    assert dialog.name_edit.text() == ""
    assert dialog.desc_edit.toPlainText() == ""

def test_group_dialog_edit(app):
    """グループ編集ダイアログのテスト"""
    group = Group(id="test", name="テストグループ", description="テスト用")
    dialog = GroupDialog(group=group)
    assert dialog.windowTitle() == "グループ編集"
    assert dialog.name_edit.text() == "テストグループ"
    assert dialog.desc_edit.toPlainText() == "テスト用"

def test_adapter_group_list_update(adapter):
    """グループリスト更新のテスト"""
    adapter.repository.create_group("テストグループ1")
    adapter.repository.create_group("テストグループ2")
    adapter.update_group_list()
    assert adapter.view.group_list.count() >= 2

def test_group_buttons_state(adapter):
    """グループ操作ボタンの状態テスト"""
    # 初期状態では編集・削除ボタンが無効
    assert not adapter.view.edit_group_btn.isEnabled()
    assert not adapter.view.delete_group_btn.isEnabled()
    
    # グループを追加して選択
    adapter.repository.create_group("テストグループ")
    adapter.update_group_list()
    adapter.view.group_list.setCurrentRow(0)
    
    # ボタンが有効になることを確認
    assert adapter.view.edit_group_btn.isEnabled()
    assert adapter.view.delete_group_btn.isEnabled()
