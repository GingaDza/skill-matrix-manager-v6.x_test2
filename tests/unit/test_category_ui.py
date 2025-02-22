import pytest
from PyQt5.QtWidgets import QApplication, QTreeWidgetItem
from PyQt5.QtCore import Qt
from skill_matrix_manager.ui.components.category_dialog import CategoryDialog
from skill_matrix_manager.ui.components.category_tree import CategoryTreeWidget
from skill_matrix_manager.models.data_models import Category, Group
from skill_matrix_manager.adapters.original_ui_adapter import OriginalUIAdapter
from skill_matrix_manager.views.initial_setup_tab import InitialSetupTab
from skill_matrix_manager.repositories.group_user_repository import GroupUserRepository
from skill_matrix_manager.repositories.category_repository import CategoryRepository

@pytest.fixture(scope="session")
def app():
    """テスト用のQApplicationインスタンスを作成"""
    app = QApplication([])
    yield app
    app.quit()

@pytest.fixture
def initial_setup_tab(app):
    """InitialSetupTabインスタンスを作成"""
    tab = InitialSetupTab()
    yield tab
    tab.deleteLater()

@pytest.fixture
def test_adapter(app, initial_setup_tab):
    """テスト用のUIアダプターを作成"""
    adapter = OriginalUIAdapter(initial_setup_tab)
    yield adapter

@pytest.fixture
def category_tree(app):
    """テスト用のカテゴリーツリーを作成"""
    tree = CategoryTreeWidget()
    yield tree
    tree.deleteLater()

def test_category_dialog_create(app):
    """カテゴリー作成ダイアログのテスト"""
    dialog = CategoryDialog()
    try:
        assert dialog.windowTitle() == "カテゴリー追加"
        assert dialog.name_edit.text() == ""
        assert dialog.desc_edit.toPlainText() == ""
        assert dialog.parent_combo.currentData() is None
    finally:
        dialog.deleteLater()

def test_category_dialog_edit(app):
    """カテゴリー編集ダイアログのテスト"""
    category = Category(
        id="test",
        name="テストカテゴリー",
        group_id="group1",
        description="テスト用"
    )
    dialog = CategoryDialog(category=category)
    try:
        assert dialog.windowTitle() == "カテゴリー編集"
        assert dialog.name_edit.text() == "テストカテゴリー"
        assert dialog.desc_edit.toPlainText() == "テスト用"
    finally:
        dialog.deleteLater()

def test_category_tree_update(category_tree):
    """カテゴリーツリー更新のテスト"""
    categories = [
        Category(id="1", name="親カテゴリー1", group_id="g1"),
        Category(id="2", name="子カテゴリー1", group_id="g1", parent_id="1"),
        Category(id="3", name="親カテゴリー2", group_id="g1")
    ]
    
    category_tree.update_tree(categories)
    
    # 基本的な検証
    assert category_tree.topLevelItemCount() == 2, "トップレベルアイテムの数が正しくありません"
    assert len(category_tree.category_items) == 3, "カテゴリーアイテムの総数が正しくありません"

    # カテゴリーの存在を確認
    for category in categories:
        assert category.id in category_tree.category_items, f"カテゴリー {category.name} が見つかりません"
        item = category_tree.category_items[category.id]
        assert item.text(0) == category.name, f"カテゴリー {category.name} の表示名が正しくありません"

    # 親子関係を確認
    child_category = next(c for c in categories if c.parent_id)
    child_item = category_tree.category_items[child_category.id]
    parent_item = child_item.parent()
    
    assert parent_item is not None, "子カテゴリーの親アイテムが見つかりません"
    assert parent_item.text(0) == "親カテゴリー1", "親カテゴリーの名前が正しくありません"

def test_adapter_category_buttons_state(test_adapter):
    """カテゴリー操作ボタンの状態テスト"""
    # 初期状態では編集・削除ボタンが無効
    assert not test_adapter.view.edit_btn.isEnabled()
    assert not test_adapter.view.delete_btn.isEnabled()
    assert not test_adapter.view.add_category_btn.isEnabled()

    # グループを選択してカテゴリー追加ボタンが有効になることを確認
    group = test_adapter.group_repository.create_group("テストグループ")
    test_adapter.update_group_list()
    test_adapter.view.group_list.setCurrentRow(0)
    assert test_adapter.view.add_category_btn.isEnabled()

def test_adapter_category_tree_update(test_adapter):
    """アダプターのカテゴリーツリー更新テスト"""
    # グループとカテゴリーを作成
    group = test_adapter.group_repository.create_group("テストグループ")
    print(f"\nCreated group: {group.id}, {group.name}")
    
    # カテゴリーを作成
    category = test_adapter.category_repository.create_category(
        name="テストカテゴリー",
        group_id=group.id,
        description="テスト用カテゴリー"
    )
    print(f"Created category: {category.id}, {category.name}, group_id={category.group_id}")
    
    # グループを選択してツリーを更新
    test_adapter.update_group_list()
    test_adapter.view.group_list.setCurrentRow(0)
    
    # リポジトリの状態を確認
    categories = test_adapter.category_repository.get_categories_by_group(group.id)
    print(f"Categories in repository: {len(categories)}")
    for cat in categories:
        print(f"- {cat.id}: {cat.name}")
    
    # ツリーの状態を確認
    print(f"Tree top level items: {test_adapter.view.category_tree.topLevelItemCount()}")
    
    # 基本的な検証
    assert len(categories) > 0, "カテゴリーが作成されていません"
    assert test_adapter.view.category_tree.topLevelItemCount() > 0, "ツリーにアイテムが表示されていません"
    
    # カテゴリーの表示を確認
    found = False
    for i in range(test_adapter.view.category_tree.topLevelItemCount()):
        item = test_adapter.view.category_tree.topLevelItem(i)
        print(f"Tree item {i}: {item.text(0)}")
        if item.text(0) == "テストカテゴリー":
            found = True
            break
    
    assert found, "作成したカテゴリーがツリーに表示されていません"
