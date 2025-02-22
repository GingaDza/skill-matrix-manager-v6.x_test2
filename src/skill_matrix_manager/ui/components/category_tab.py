from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QTreeWidget,
                           QTreeWidgetItem, QLabel)
from datetime import datetime, UTC
from ...adapters.ui_protection import UIProtection

class CategoryTab(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._current_time = datetime(2025, 2, 19, 20, 50, 28, tzinfo=UTC)
        self._current_user = "GingaDza"
        self.ui_protection = UIProtection()
        self.setup_ui()
    
    def setup_ui(self):
        """UIの初期設定"""
        layout = QVBoxLayout(self)
        
        # ユーザー情報
        user_info = QLabel(f"現在のユーザー: {self._current_user}")
        layout.addWidget(user_info)
        
        # スキルツリー
        self.skill_tree = QTreeWidget()
        self.skill_tree.setHeaderLabels(["スキル", "レベル"])
        layout.addWidget(self.skill_tree)
        
        # 保護設定
        self.ui_protection.monitor.log_change(
            "category_tab",
            "INIT",
            None,
            None,
            self._current_user
        )
