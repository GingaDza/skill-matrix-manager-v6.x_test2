from .base import BaseTestCase
from PyQt5.QtWidgets import QTreeWidget, QListWidget, QListWidgetItem
from PyQt5.QtCore import Qt
from src.skill_matrix_manager.models.data_models import (
    Group, User, Category, Skill, SkillLevel
)

class TestUISync(BaseTestCase):
    def setUp(self):
        super().setUp()
        # 最小限のUIコンポーネントを作成
        self.list_widget = QListWidget()
        
        # テストデータを追加
        self.item = QListWidgetItem("テストアイテム")
        self.list_widget.addItem(self.item)

    def test_list_widget_items(self):
        """リストウィジェットの項目テスト"""
        self.assertEqual(self.list_widget.count(), 1)
        self.assertEqual(self.list_widget.item(0).text(), "テストアイテム")

    def test_list_widget_selection(self):
        """リストウィジェットの選択テスト"""
        self.list_widget.setCurrentRow(0)
        self.assertEqual(self.list_widget.currentRow(), 0)
        self.assertEqual(
            self.list_widget.currentItem().text(),
            "テストアイテム"
        )

    def tearDown(self):
        self.list_widget.clear()
        self.list_widget.deleteLater()
        super().tearDown()

# tests/test_tree_widget.py を作成
cat > tests/test_tree_widget.py << 'EOL'
from .base import BaseTestCase
from PyQt5.QtWidgets import QTreeWidget, QTreeWidgetItem

class TestTreeWidget(BaseTestCase):
    def setUp(self):
        super().setUp()
        self.tree = QTreeWidget()
        self.tree.setHeaderLabels(["項目"])
        
        # テスト用のツリーアイテムを追加
        self.root = QTreeWidgetItem(["ルート"])
        self.tree.addTopLevelItem(self.root)
        
        self.child = QTreeWidgetItem(["子アイテム"])
        self.root.addChild(self.child)

    def test_tree_structure(self):
        """ツリー構造のテスト"""
        self.assertEqual(self.tree.topLevelItemCount(), 1)
        self.assertEqual(self.root.childCount(), 1)
        self.assertEqual(self.root.text(0), "ルート")
        self.assertEqual(self.child.text(0), "子アイテム")

    def tearDown(self):
        self.tree.clear()
        self.tree.deleteLater()
        super().tearDown()
