import unittest
from PyQt5.QtWidgets import QApplication
import sys

class BaseTestCase(unittest.TestCase):
    """テストケース基底クラス"""
    
    @classmethod
    def setUpClass(cls):
        """テストクラスの初期化"""
        if not hasattr(cls, 'app'):
            cls.app = QApplication.instance() or QApplication(sys.argv)

    def setUp(self):
        """各テストケースの前処理"""
        super().setUp()
        if not hasattr(self, 'app'):
            self.app = self.__class__.app

    def tearDown(self):
        """各テストケースの後処理"""
        self.app.processEvents()
        super().tearDown()

    @classmethod
    def tearDownClass(cls):
        """テストクラスのクリーンアップ"""
        if hasattr(cls, 'app'):
            cls.app.processEvents()
