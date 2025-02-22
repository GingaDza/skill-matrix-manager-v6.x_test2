import unittest
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout,
    QComboBox, QListWidget, QPushButton, QTabWidget,
    QSplitter
)
from PyQt5.QtCore import Qt

class MainWindowTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.app = QApplication.instance()
        if cls.app is None:
            cls.app = QApplication([])

    def setUp(self):
        from src.skill_matrix_manager.main_window import MainWindow
        self.window = MainWindow()
        # ウィンドウを表示してレイアウトを確実に処理
        self.window.show()
        self.app.processEvents()

    def test_splitter_ratio(self):
        """3:7の分割比率テスト"""
        splitter = self.window.findChild(QSplitter)
        self.assertIsNotNone(splitter)
        
        # スプリッターの初期サイズを明示的に設定
        total_width = 1000
        splitter.resize(total_width, splitter.height())
        self.app.processEvents()
        
        sizes = splitter.sizes()
        ratio = sizes[0] / sum(sizes)
        self.assertAlmostEqual(ratio, 0.3, delta=0.05)

    def test_left_panel_structure(self):
        """左パネルの構造テスト"""
        left_panel = self.window.findChild(QWidget, "leftPanel")
        self.assertIsNotNone(left_panel)
        
        # グループリストコンボボックス
        combo = left_panel.findChild(QComboBox)
        self.assertIsNotNone(combo)
        
        # ユーザーリスト
        user_list = left_panel.findChild(QListWidget)
        self.assertIsNotNone(user_list)
        
        # ユーザー操作ボタンの確認
        buttons = ["追加", "編集", "削除"]
        for text in buttons:
            found = False
            for btn in left_panel.findChildren(QPushButton):
                if btn.text() == text:
                    found = True
                    break
            self.assertTrue(found, f"ボタン '{text}' が見つかりません")

    def test_tab_structure(self):
        """タブ構造のテスト"""
        tab_widget = self.window.findChild(QTabWidget)
        self.assertIsNotNone(tab_widget)
        
        # メインタブの確認
        expected_tabs = [
            "システム管理",
            "スキル分析"
        ]
        
        for tab_text in expected_tabs:
            found = False
            for i in range(tab_widget.count()):
                if tab_widget.tabText(i) == tab_text:
                    found = True
                    break
            self.assertTrue(found, f"タブ '{tab_text}' が見つかりません")

    def test_system_management_subtabs(self):
        """システム管理のサブタブテスト"""
        system_tab = self.window.findChild(QWidget, "systemManagementTab")
        self.assertIsNotNone(system_tab)
        subtab_widget = system_tab.findChild(QTabWidget)
        self.assertIsNotNone(subtab_widget)
        
        expected_subtabs = [
            "初期設定タブ",
            "データ入出力タブ",
            "システム情報タブ"
        ]
        
        for subtab_text in expected_subtabs:
            found = False
            for i in range(subtab_widget.count()):
                if subtab_widget.tabText(i) == subtab_text:
                    found = True
                    break
            self.assertTrue(found, f"サブタブ '{subtab_text}' が見つかりません")

    def test_skill_analysis_subtabs(self):
        """スキル分析のサブタブテスト"""
        analysis_tab = self.window.findChild(QWidget, "skillAnalysisTab")
        self.assertIsNotNone(analysis_tab)
        subtab_widget = analysis_tab.findChild(QTabWidget)
        self.assertIsNotNone(subtab_widget)
        
        expected_subtabs = [
            "総合評価",
            "スキルギャップタブ"
        ]
        
        for subtab_text in expected_subtabs:
            found = False
            for i in range(subtab_widget.count()):
                if subtab_widget.tabText(i) == subtab_text:
                    found = True
                    break
            self.assertTrue(found, f"サブタブ '{subtab_text}' が見つかりません")

    def test_dynamic_category_tabs(self):
        """動的カテゴリータブのテスト"""
        tab_widget = self.window.findChild(QTabWidget)
        self.assertIsNotNone(tab_widget)
        
        # 現在のタブ数を記録
        initial_count = tab_widget.count()
        
        # 新規カテゴリータブの追加
        category_name = "カテゴリー1"
        self.window.add_category_tab(category_name)
        self.app.processEvents()
        
        # タブ数が増えたことを確認
        self.assertEqual(tab_widget.count(), initial_count + 1)
        
        # 追加されたタブの位置とテキストを確認
        new_tab_index = tab_widget.count() - 3  # システム管理とスキル分析の前
        self.assertEqual(tab_widget.tabText(new_tab_index), category_name)

    def tearDown(self):
        if hasattr(self, 'window'):
            self.window.close()
            self.window.deleteLater()
        self.app.processEvents()

    @classmethod
    def tearDownClass(cls):
        if cls.app:
            cls.app.processEvents()

if __name__ == '__main__':
    unittest.main()
