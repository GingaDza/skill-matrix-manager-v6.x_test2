import unittest
from PyQt5.QtWidgets import QApplication, QVBoxLayout
from src.skill_matrix_manager.ui.components.initial_setup_tab import InitialSetupTab

class TestUIIntegrity(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.app = QApplication([])

    def setUp(self):
        self.tab = InitialSetupTab()

    def test_original_layout_maintained(self):
        """オリジナルレイアウトが維持されているか確認"""
        self.assertIsInstance(
            self.tab.layout(),
            QVBoxLayout,
            "メインレイアウトがQVBoxLayoutではありません"
        )
        self.tab.check_ui_state()

    def test_required_widgets_exist(self):
        """必要なウィジェットが存在するか確認"""
        required_widgets = [
            'group_list', 'category_tree',
            'add_group_btn', 'edit_group_btn', 'delete_group_btn',
            'add_category_btn', 'add_skill_btn',
            'edit_btn', 'delete_btn', 'add_tab_btn'
        ]

        for widget_name in required_widgets:
            self.assertTrue(
                hasattr(self.tab, widget_name),
                f"必要なウィジェット {widget_name} が見つかりません"
            )

    def tearDown(self):
        self.tab.deleteLater()

    @classmethod
    def tearDownClass(cls):
        cls.app.quit()
