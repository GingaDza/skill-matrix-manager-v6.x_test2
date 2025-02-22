import unittest
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import Qt
from PyQt5.QtTest import QTest
from src.skill_matrix_manager.ui.main_window import MainWindow

class TestTabManagement(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.app = QApplication([])

    def setUp(self):
        self.window = MainWindow()

    def test_add_new_tab(self):
        """新規タブ追加のテスト"""
        initial_tab_count = self.window.tab_widget.count()
        
        # 新規カテゴリータブを追加
        new_tab = self.window.add_category_tab("テストカテゴリー")
        
        # タブ数が増えたことを確認
        self.assertEqual(
            self.window.tab_widget.count(),
            initial_tab_count + 1,
            "新規タブが追加されていません"
        )
        
        # 追加されたタブが最初の位置にあることを確認
        self.assertEqual(
            self.window.tab_widget.tabText(0),
            "テストカテゴリー",
            "新規タブが正しい位置に追加されていません"
        )

    def test_tab_content(self):
        """新規タブの内容テスト"""
        initial_tab_count = len(self.window.category_tabs)
        
        # 新規タブ追加ボタンをクリック
        QTest.mouseClick(self.window.initial_setup_tab.add_tab_btn, Qt.LeftButton)
        
        # タブが追加されたことを確認
        self.assertEqual(
            len(self.window.category_tabs),
            initial_tab_count + 1,
            "カテゴリータブが追加されていません"
        )
        
        # 追加されたタブが存在することを確認
        new_tab = self.window.category_tabs[-1]
        self.assertIsNotNone(new_tab, "新規タブが正しく追加されていません")

    def tearDown(self):
        self.window.deleteLater()

    @classmethod
    def tearDownClass(cls):
        cls.app.quit()
