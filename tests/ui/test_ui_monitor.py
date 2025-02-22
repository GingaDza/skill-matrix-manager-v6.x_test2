import unittest
from PyQt5.QtWidgets import QApplication, QPushButton
from PyQt5.QtCore import QRect
from src.skill_matrix_manager.ui.base.ui_monitor import UIMonitor
import os
import time

class TestUIMonitor(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.app = QApplication([])

    def setUp(self):
        self.button = QPushButton("Test")
        self.monitor = UIMonitor()
        self.button.installEventFilter(self.monitor)

    def test_state_capture(self):
        """状態キャプチャのテスト"""
        state = self.monitor.capture_widget_state(self.button)
        self.assertIn('geometry', state)
        self.assertIn('visible', state)
        self.assertIn('enabled', state)

    def test_change_detection(self):
        """変更検出のテスト"""
        # 初期状態を記録
        self.monitor.check_ui_changes(self.button)
        
        # ウィジェットを変更
        self.button.setGeometry(QRect(0, 0, 200, 50))
        time.sleep(1)  # 変更検出の時間間隔を確保
        
        # 変更を確認
        self.monitor.check_ui_changes(self.button)
        
        # ログファイルの存在を確認
        self.assertTrue(os.path.exists('ui_changes.log'))

    def tearDown(self):
        self.button.deleteLater()

    @classmethod
    def tearDownClass(cls):
        cls.app.quit()
        # テスト後にログファイルを削除
        if os.path.exists('ui_changes.log'):
            os.remove('ui_changes.log')
