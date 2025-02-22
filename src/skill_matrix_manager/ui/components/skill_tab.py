from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout,
                           QLabel, QComboBox, QGroupBox)
from PyQt5.QtChart import QChartView, QChart, QPolarChart, QValueAxis, QSplineSeries
from PyQt5.QtCore import Qt

class SkillTab(QWidget):
    def __init__(self, category_name, skills, parent=None):
        super().__init__(parent)
        self.category_name = category_name
        self.skills = skills
        self.setup_ui()
        self.setup_chart()
        self.connect_signals()

    def setup_ui(self):
        layout = QVBoxLayout(self)

        # ユーザー情報グループ
        user_group = QGroupBox("ユーザー情報")
        user_layout = QVBoxLayout()
        self.user_label = QLabel()
        user_layout.addWidget(self.user_label)
        user_group.setLayout(user_layout)
        layout.addWidget(user_group)

        # スキルレベル設定グループ
        skills_group = QGroupBox("スキルレベル設定")
        skills_layout = QVBoxLayout()

        self.skill_combos = {}
        for skill_name in self.skills:
            skill_layout = QHBoxLayout()
            label = QLabel(skill_name)
            combo = QComboBox()
            combo.setObjectName("skill_level_combo")
            for i in range(1, 6):
                combo.addItem(str(i))
            
            skill_layout.addWidget(label)
            skill_layout.addWidget(combo)
            skills_layout.addLayout(skill_layout)
            self.skill_combos[skill_name] = combo

        skills_group.setLayout(skills_layout)
        layout.addWidget(skills_group)

        # チャートビュー
        self.chart_view = QChartView()
        self.chart_view.setObjectName("radar_chart")
        self.chart_view.setMinimumSize(400, 300)
        layout.addWidget(self.chart_view)

        self.setLayout(layout)

    def setup_chart(self):
        """レーダーチャートの設定"""
        chart = QPolarChart()
        
        # 軸の設定
        angular_axis = QValueAxis()
        angular_axis.setTickCount(len(self.skills) + 1)
        angular_axis.setLabelFormat("%d")
        chart.addAxis(angular_axis, QPolarChart.PolarOrientationAngular)

        radial_axis = QValueAxis()
        radial_axis.setRange(0, 5)
        radial_axis.setTickCount(6)
        chart.addAxis(radial_axis, QPolarChart.PolarOrientationRadial)

        # 目標値のシリーズ
        self.target_series = QSplineSeries()
        self.target_series.setName("目標値")
        chart.addSeries(self.target_series)
        self.target_series.attachAxis(angular_axis)
        self.target_series.attachAxis(radial_axis)

        # 現在値のシリーズ
        self.current_series = QSplineSeries()
        self.current_series.setName("現在値")
        chart.addSeries(self.current_series)
        self.current_series.attachAxis(angular_axis)
        self.current_series.attachAxis(radial_axis)

        self.chart_view.setChart(chart)

    def connect_signals(self):
        """シグナルの接続"""
        for combo in self.skill_combos.values():
            combo.currentTextChanged.connect(self.update_chart)

    def update_chart(self):
        """チャートの更新"""
        self.current_series.clear()
        for i, (skill_name, combo) in enumerate(self.skill_combos.items()):
            angle = (360 * i) / len(self.skills)
            value = int(combo.currentText())
            self.current_series.append(angle, value)
        
        # シリーズを閉じる
        first_point = self.current_series.at(0)
        self.current_series.append(360, first_point.y())

    def set_user_info(self, user_name):
        """ユーザー情報の設定"""
        self.user_label.setText(f"ユーザー: {user_name}")

    def set_skill_levels(self, levels):
        """スキルレベルの設定"""
        for skill_name, level in levels.items():
            if skill_name in self.skill_combos:
                self.skill_combos[skill_name].setCurrentText(str(level))
