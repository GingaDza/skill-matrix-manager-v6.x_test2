from PyQt5.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QGroupBox,
                           QLabel, QComboBox, QPushButton, QGridLayout,
                           QScrollArea, QWidget)
from PyQt5.QtCore import Qt
from typing import Dict

class SkillInputDialog(QDialog):
    def __init__(self, time_value: int, time_unit: str, skill_data: Dict[str, Dict[str, Dict[str, str]]], parent=None):
        """
        Args:
            time_value (int): 目標期間の値
            time_unit (str): 目標期間の単位（時間/日/月/年）
            skill_data (Dict): {group: {category: {skill_name: current_level}}}
            parent: 親ウィジェット
        """
        super().__init__(parent)
        self.time_value = time_value
        self.time_unit = time_unit
        self._skill_data = skill_data
        self._skill_levels = {}
        self._current_group = None
        self._current_category = None
        self._setup_ui()
        self.setWindowTitle(f"{time_value}{time_unit}後の目標設定")
        self.resize(800, 600)

    def _setup_ui(self):
        layout = QVBoxLayout()
        
        # グループ選択
        group_layout = QHBoxLayout()
        group_label = QLabel("グループ:")
        self.group_combo = QComboBox()
        self.group_combo.addItems(self._skill_data.keys())
        self.group_combo.currentTextChanged.connect(self._on_group_changed)
        group_layout.addWidget(group_label)
        group_layout.addWidget(self.group_combo)
        layout.addLayout(group_layout)
        
        # カテゴリー選択
        category_layout = QHBoxLayout()
        category_label = QLabel("カテゴリー:")
        self.category_combo = QComboBox()
        self.category_combo.currentTextChanged.connect(self._on_category_changed)
        category_layout.addWidget(category_label)
        category_layout.addWidget(self.category_combo)
        layout.addLayout(category_layout)
        
        # スクロール可能なスキル設定エリア
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll_content = QWidget()
        self.skill_layout = QVBoxLayout(scroll_content)
        
        # スキル設定グループ
        self.skills_group = QGroupBox("スキルレベル設定")
        self.grid_layout = QGridLayout()
        self.skills_group.setLayout(self.grid_layout)
        self.skill_layout.addWidget(self.skills_group)
        
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
        
        # 初期選択
        if self.group_combo.count() > 0:
            self._on_group_changed(self.group_combo.currentText())

    def _on_group_changed(self, group_name: str):
        """グループ選択時の処理"""
        self._current_group = group_name
        self.category_combo.clear()
        if group_name in self._skill_data:
            self.category_combo.addItems(self._skill_data[group_name].keys())
            if self.category_combo.count() > 0:
                self._on_category_changed(self.category_combo.currentText())

    def _on_category_changed(self, category_name: str):
        """カテゴリー選択時の処理"""
        self._current_category = category_name
        self._update_skills()

    def _update_skills(self):
        """スキル一覧の更新"""
        # グリッドをクリア
        for i in reversed(range(self.grid_layout.count())): 
            self.grid_layout.itemAt(i).widget().setParent(None)
        
        # ヘッダー
        headers = ["スキル名", "現在のレベル", "目標レベル"]
        for col, header in enumerate(headers):
            label = QLabel(header)
            label.setStyleSheet("font-weight: bold;")
            self.grid_layout.addWidget(label, 0, col)

        if not (self._current_group and self._current_category):
            return

        # スキル入力フィールドの追加
        skills = self._skill_data[self._current_group][self._current_category]
        for row, (skill_name, current_level) in enumerate(skills.items(), 1):
            # スキル名
            self.grid_layout.addWidget(QLabel(skill_name), row, 0)
            
            # 現在のレベル
            current_label = QLabel(str(current_level))
            current_label.setAlignment(Qt.AlignCenter)
            self.grid_layout.addWidget(current_label, row, 1)
            
            # 目標レベル
            level_combo = QComboBox()
            level_combo.addItems([str(i) for i in range(1, 6)])
            level_combo.setCurrentIndex(current_level - 1)
            self.grid_layout.addWidget(level_combo, row, 2)
            
            self._skill_levels[(self._current_group, self._current_category, skill_name)] = level_combo

    def get_skill_levels(self) -> Dict[str, Dict[str, Dict[str, int]]]:
        """設定されたスキルレベルを取得"""
        result = {}
        for (group, category, skill), combo in self._skill_levels.items():
            if group not in result:
                result[group] = {}
            if category not in result[group]:
                result[group][category] = {}
            result[group][category][skill] = int(combo.currentText())
        return result
