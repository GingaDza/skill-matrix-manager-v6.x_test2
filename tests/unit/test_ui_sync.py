import pytest
from datetime import datetime, UTC
from PyQt5.QtWidgets import QComboBox, QListWidget, QTreeWidget, QTreeWidgetItem
from PyQt5.QtCore import Qt
from src.skill_matrix_manager.adapters.ui_sync_adapter import UISyncAdapter
from src.skill_matrix_manager.adapters.ui_protection import UIProtection

class TestUISyncAdapter:
    CURRENT_TIME = datetime(2025, 2, 19, 20, 43, 55, tzinfo=UTC)
    CURRENT_USER = "GingaDza"
    
    @pytest.fixture
    def ui_protection(self):
        protection = UIProtection()
        protection.set_current_user(self.CURRENT_USER)
        return protection
        
    @pytest.fixture
    def ui_sync(self, ui_protection):
        sync = UISyncAdapter(ui_protection)
        return sync
        
    def test_sync_group_selection(self, ui_sync, qtbot):
        # コンボボックスとリストウィジェットの作成
        combo = QComboBox()
        list_widget = QListWidget()
        
        # テストデータの追加
        test_groups = ["Group A", "Group B", "Group C"]
        combo.addItems(test_groups)
        list_widget.addItems(test_groups)
        
        # 同期のテスト
        combo.setCurrentText("Group B")
        assert ui_sync.sync_group_selection(combo, list_widget)
        assert list_widget.currentItem().text() == "Group B"
        
    def test_sync_category_tree(self, ui_sync, qtbot):
        # ソースツリーとターゲットツリーの作成
        source_tree = QTreeWidget()
        target_tree = QTreeWidget()
        
        # テストデータの追加
        source_tree.setColumnCount(2)
        category = QTreeWidgetItem(source_tree, ["Category 1"])
        skill = QTreeWidgetItem(category, ["Skill 1", "3"])
        
        # 同期のテスト
        assert ui_sync.sync_category_tree(source_tree, target_tree)
        
        # 結果の検証
        target_items = target_tree.findItems("Category 1", Qt.MatchExactly)
        assert len(target_items) > 0
        target_category = target_items[0]
        assert target_category.childCount() > 0
        target_skill = target_category.child(0)
        assert target_skill.text(0) == "Skill 1"
        assert target_skill.text(1) == "3"
