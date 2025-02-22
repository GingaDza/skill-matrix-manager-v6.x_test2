from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
                           QLabel, QTreeWidget, QTreeWidgetItem)
from PyQt5.QtCore import pyqtSignal
from typing import Dict
from skill_matrix_manager.utils.debug_logger import DebugLogger

logger = DebugLogger.get_logger()

class StageDisplayWidget(QWidget):
    # 削除リクエストのシグナル
    delete_requested = pyqtSignal()

    def __init__(self, time_value: int, time_unit: str, 
                 stage_data: Dict[str, Dict[str, Dict[str, int]]], parent=None):
        """
        Args:
            time_value (int): ステージの時間値
            time_unit (str): 時間単位（時間/日/月/年）
            stage_data (Dict): {グループ: {カテゴリー: {スキル: レベル}}}
            parent: 親ウィジェット
        """
        super().__init__(parent)
        self.time_value = time_value
        self.time_unit = time_unit
        self.stage_data = stage_data
        self._setup_ui()
        logger.debug(f"StageDisplayWidget initialized for {time_value}{time_unit}")

    def _setup_ui(self):
        """UIのセットアップ"""
        layout = QVBoxLayout()
        
        # ヘッダー部分
        header_layout = QHBoxLayout()
        
        # タイトル
        title = QLabel(f"{self.time_value}{self.time_unit}後の目標")
        title.setStyleSheet("font-weight: bold; font-size: 14px;")
        header_layout.addWidget(title)
        
        # スペーサーを追加
        header_layout.addStretch()
        
        # 削除ボタン
        delete_button = QPushButton("削除")
        delete_button.clicked.connect(self.delete_requested.emit)
        header_layout.addWidget(delete_button)
        
        layout.addLayout(header_layout)
        
        # スキルツリーの表示
        tree = QTreeWidget()
        tree.setHeaderLabels(["項目", "目標レベル"])
        tree.setColumnCount(2)
        
        # データをツリーに追加
        for group, categories in self.stage_data.items():
            group_item = QTreeWidgetItem(tree, [group, ""])
            group_item.setExpanded(True)
            
            for category, skills in categories.items():
                category_item = QTreeWidgetItem(group_item, [category, ""])
                category_item.setExpanded(True)
                
                for skill_name, level in skills.items():
                    skill_item = QTreeWidgetItem(category_item, [skill_name, str(level)])
        
        # カラムサイズの調整
        tree.setColumnWidth(0, 250)  # スキル名カラムを広めに
        tree.setColumnWidth(1, 100)  # レベルカラムは狭めに
        
        layout.addWidget(tree)
        self.setLayout(layout)
        logger.debug(f"UI setup completed for stage {self.time_value}{self.time_unit}")

    def get_time_value(self) -> int:
        """時間値を取得"""
        return self.time_value

    def get_time_unit(self) -> str:
        """時間単位を取得"""
        return self.time_unit

    def get_stage_data(self) -> Dict[str, Dict[str, Dict[str, int]]]:
        """ステージデータを取得"""
        return self.stage_data.copy()

    def update_time_unit(self, new_unit: str) -> None:
        """時間単位の更新"""
        logger.debug(f"Updating time unit from {self.time_unit} to {new_unit}")
        self.time_unit = new_unit
        # タイトルの更新
        title = self.findChild(QLabel)
        if title:
            title.setText(f"{self.time_value}{self.time_unit}後の目標")
