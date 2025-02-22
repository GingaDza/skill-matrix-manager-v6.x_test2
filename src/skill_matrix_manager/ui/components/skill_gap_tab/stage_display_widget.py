from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QGridLayout
from PyQt5.QtCore import Qt
from typing import Dict

class StageDisplayWidget(QWidget):
    def __init__(self, stage_data: Dict, parent=None):
        super().__init__(parent)
        self.stage_data = stage_data
        self._setup_ui()

    def _setup_ui(self):
        layout = QVBoxLayout()
        
        # 期間表示
        period_label = QLabel(f"{self.stage_data['time']}{self.stage_data['unit']}後の目標")
        period_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(period_label)
        
        # スキルレベル表示
        skills_grid = QGridLayout()
        skills_grid.setColumnStretch(1, 1)  # 説明列を伸縮可能に
        
        # ヘッダー
        skills_grid.addWidget(QLabel("スキル"), 0, 0)
        skills_grid.addWidget(QLabel("レベル"), 0, 1)
        
        # スキルデータ
        for row, (skill, level) in enumerate(self.stage_data['targets'].items(), start=1):
            skills_grid.addWidget(QLabel(skill), row, 0)
            level_label = QLabel(str(level))
            level_label.setAlignment(Qt.AlignCenter)
            skills_grid.addWidget(level_label, row, 1)
        
        layout.addLayout(skills_grid)
        self.setLayout(layout)

    def update_data(self, new_data: Dict):
        """表示データを更新"""
        self.stage_data = new_data
        # UIを再構築
        while self.layout().count():
            item = self.layout().takeAt(0)
            if item.widget():
                item.widget().deleteLater()
        self._setup_ui()
