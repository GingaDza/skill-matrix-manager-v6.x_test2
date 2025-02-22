import pytest
from PyQt5.QtWidgets import (
    QApplication, QTabWidget, QSplitter, QLabel,
    QTreeWidget, QListWidget, QPushButton
)
from skill_matrix_manager.adapters.system_management_adapter import SystemManagementAdapter

@pytest.fixture
def app():
    return QApplication([])

@pytest.fixture
def adapter():
    return SystemManagementAdapter()

def test_create_system_management_tab(app, adapter):
    tab = adapter.create_system_management_tab()
    assert isinstance(tab, QTabWidget)
    assert tab.count() == 3
    assert tab.tabText(0) == "初期設定"
    assert tab.tabText(1) == "データ入出力"
    assert tab.tabText(2) == "システム情報"

def test_create_initial_setup_tab(app, adapter):
    tab = adapter.create_initial_setup_tab()
    splitter = tab.findChild(QSplitter)
    assert splitter is not None
    assert len(splitter.sizes()) == 2
    
    # グループリストパネルのテスト
    group_panel = splitter.widget(0)
    assert group_panel is not None
    assert group_panel.findChild(QLabel).text() == "グループリスト"
    assert group_panel.findChild(QListWidget) is not None
    
    # ボタンの確認
    buttons = group_panel.findChildren(QPushButton)
    assert len(buttons) == 3
    button_texts = [btn.text() for btn in buttons]
    assert "追加" in button_texts
    assert "編集" in button_texts
    assert "削除" in button_texts
    
    # カテゴリー/スキルツリーパネルのテスト
    category_panel = splitter.widget(1)
    assert category_panel is not None
    assert category_panel.findChild(QLabel).text() == "カテゴリー / スキルツリー"
    assert category_panel.findChild(QTreeWidget) is not None
    
    # ツリーウィジェットの設定確認
    tree = category_panel.findChild(QTreeWidget)
    assert tree.columnCount() == 2
    header_texts = [tree.headerItem().text(i) for i in range(tree.columnCount())]
    assert header_texts == ["名前", "レベル"]
    
    # カテゴリパネルのボタン確認
    cat_buttons = category_panel.findChildren(QPushButton)
    assert len(cat_buttons) == 5  # カテゴリー追加、スキル追加、編集、削除、新規タブ追加
    cat_button_texts = [btn.text() for btn in cat_buttons]
    assert "カテゴリー追加" in cat_button_texts
    assert "スキル追加" in cat_button_texts
    assert "編集" in cat_button_texts
    assert "削除" in cat_button_texts
    assert "新規タブ追加" in cat_button_texts

