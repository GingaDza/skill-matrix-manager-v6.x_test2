import unittest
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import Qt
from src.skill_matrix_manager.ui.components.initial_setup_tab import InitialSetupTab
from src.skill_matrix_manager.utils.ui_validator import UIValidator

class TestInitialSetupTab(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.app = QApplication([])

    def setUp(self):
        self.tab = InitialSetupTab()
        self.validator = UIValidator()

    def test_ui_structure(self):
        """UI構造の検証"""
        self.assertTrue(
            self.validator.validate_initial_setup_tab(self.tab),
            "UI構造の検証に失敗しました"
        )

    def test_tree_widget_columns(self):
        """ツリーウィジェットのカラム設定検証"""
        tree = self.tab.category_tree
        self.assertEqual(tree.columnCount(), 2)
        headers = [tree.headerItem().text(i) for i in range(tree.columnCount())]
        self.assertEqual(headers, ["名前", "レベル"])

    @classmethod
    def tearDownClass(cls):
        cls.app.quit()
