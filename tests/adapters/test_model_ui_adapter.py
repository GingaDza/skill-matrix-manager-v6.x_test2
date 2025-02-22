import unittest
import sys
import os
from PyQt5.QtWidgets import QApplication, QTreeWidget, QTreeWidgetItem
from PyQt5.QtCore import Qt

# プロジェクトルートへのパスを追加
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

from src.skill_matrix_manager.adapters.model_ui_adapter import ModelUIAdapter
from src.skill_matrix_manager.models.data_models import Category, Skill

class TestModelUIAdapter(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.app = QApplication([])

    def setUp(self):
        self.adapter = ModelUIAdapter()
        self.tree = QTreeWidget()
        
        # テストデータの作成
        self.skill = Skill(
            id=1,
            name="Python",
            description="Pythonプログラミング",
            required_level=3
        )
        
        self.category = Category(
            id=1,
            name="プログラミング",
            description="プログラミング言語",
            skills=[self.skill]
        )

    def test_category_creation(self):
        """カテゴリー作成のテスト"""
        item = self.adapter.create_category_item(self.category)
        
        self.assertEqual(item.text(0), "プログラミング")
        self.assertEqual(item.childCount(), 1)
        
        # モデルの取得を確認
        model = self.adapter.get_model_from_item(item)
        self.assertIsInstance(model, Category)
        self.assertEqual(model.id, self.category.id)

    def test_skill_creation(self):
        """スキル作成のテスト"""
        item = self.adapter.create_skill_item(self.skill)
        
        self.assertEqual(item.text(0), "Python")
        self.assertEqual(item.text(1), "3")
        
        # モデルの取得を確認
        model = self.adapter.get_model_from_item(item)
        self.assertIsInstance(model, Skill)
        self.assertEqual(model.id, self.skill.id)

    def tearDown(self):
        self.tree.clear()
        self.tree.deleteLater()

    @classmethod
    def tearDownClass(cls):
        cls.app.quit()

if __name__ == '__main__':
    unittest.main()
