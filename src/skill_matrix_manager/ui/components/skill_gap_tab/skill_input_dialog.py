from PyQt5.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QGroupBox,
                           QLabel, QComboBox, QPushButton, QGridLayout,
                           QScrollArea, QWidget)
from PyQt5.QtCore import Qt
from typing import Dict

class SkillInputDialog(QDialog):
    def __init__(self, time_value: int, time_unit: str, skills: Dict[str, str], parent=None):
        super().__init__(parent)
        self.time_value = time_value
        self.time_unit = time_unit
        self._skills = skills
        self._skill_levels = {}
        self._setup_ui()
        self.setWindowTitle(f"{time_value}{time_unit}後の目標設定")
        self.resize(600, 400)

    def _setup_ui(self):
        layout = QVBoxLayout()
        
        # スクロール可能なエリアの作成
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll_content = QWidget()
        scroll_layout = QVBoxLayout(scroll_content)
        
        # スキルレベル設定グループ
        skills_group = QGroupBox("スキルレベル設定")
        grid_layout = QGridLayout()
        
        # ヘッダー
        headers = ["スキル名", "現在のレベル", "目標レベル"]
        for col, header in enumerate(headers):
            label = QLabel(header)
            label.setStyleSheet("font-weight: bold;")
            grid_layout.addWidget(label, 0, col)

        # スキル入力フィールドの追加
        row = 1
        for skill_name in self._skills.keys():
            # スキル名
            grid_layout.addWidget(QLabel(skill_name), row, 0)
            
            # 現在のレベル（表示のみ）
            current_level = QLabel("1")  # 現在値は1固定
            current_level.setAlignment(Qt.AlignCenter)
            grid_layout.addWidget(current_level, row, 1)
            
            # 目標レベル（コンボボックス）
            level_combo = QComboBox()
            level_combo.addItems([str(i) for i in range(1, 6)])  # レベル1-5
            level_combo.setCurrentIndex(0)  # デフォルトはレベル1
            grid_layout.addWidget(level_combo, row, 2)
            
            self._skill_levels[skill_name] = level_combo
            row += 1
        
        skills_group.setLayout(grid_layout)
        scroll_layout.addWidget(skills_group)
        
        scroll.setWidget(scroll_content)
        layout.addWidget(scroll)
        
        # ボタンエリア
        button_layout = QHBoxLayout()
        ok_button = QPushButton("設定")
        ok_button.clicked.connect(self.accept)
        cancel_button = QPushButton("キャンセル")
        cancel_button.clicked.connect(self.reject)
        
        button_layout.addStretch()
        button_layout.addWidget(ok_button)
        button_layout.addWidget(cancel_button)
        layout.addLayout(button_layout)
        
        self.setLayout(layout)

    def get_skill_levels(self) -> dict:
        """設定されたスキルレベルを取得"""
        return {skill: int(combo.currentText()) 
                for skill, combo in self._skill_levels.items()}

