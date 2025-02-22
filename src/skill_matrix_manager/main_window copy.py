from PyQt5.QtWidgets import (QMainWindow, QTabWidget, QWidget, QVBoxLayout,
                           QHBoxLayout, QComboBox, QListWidget, QPushButton,
                           QLabel)
from datetime import datetime, UTC
from .ui.components.initial_setup_tab import InitialSetupTab
from .ui.components.data_io_tab import DataIOTab
from .ui.components.system_info_tab import SystemInfoTab
from .ui.components.overall_evaluation_tab import OverallEvaluationTab
from .ui.components.skill_gap_tab import SkillGapTab

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self._current_time = datetime(2025, 2, 19, 22, 21, 6, tzinfo=UTC)
        self._current_user = "GingaDza"
        self.initUI()

    def initUI(self):
        """UIの初期化"""
        self.setWindowTitle("Skill Matrix Manager")
        self.setGeometry(100, 100, 1200, 800)

        # メインウィジェット
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QHBoxLayout(central_widget)

        # 左パネル (3:7の左側)
        left_panel = QWidget()
        left_layout = QVBoxLayout(left_panel)
        
        # グループ選択コンボボックスとラベル
        group_label = QLabel("グループ選択:")
        left_layout.addWidget(group_label)
        self.group_combo = QComboBox()
        left_layout.addWidget(self.group_combo)
        
        # ユーザーリストとラベル
        user_label = QLabel("ユーザーリスト:")
        left_layout.addWidget(user_label)
        self.user_list = QListWidget()
        left_layout.addWidget(self.user_list)
        
        # ユーザー操作ボタン
        button_layout = QHBoxLayout()
        self.add_user_btn = QPushButton("追加")
        self.edit_user_btn = QPushButton("編集")
        self.delete_user_btn = QPushButton("削除")
        button_layout.addWidget(self.add_user_btn)
        button_layout.addWidget(self.edit_user_btn)
        button_layout.addWidget(self.delete_user_btn)
        left_layout.addLayout(button_layout)
        
        main_layout.addWidget(left_panel, 3)

        # 右パネル (3:7の右側)
        right_panel = QWidget()
        right_layout = QVBoxLayout(right_panel)
        self.tab_widget = QTabWidget()

        # システム管理タブ（デフォルト）
        self.system_tab = QTabWidget()
        self.initial_setup_tab = InitialSetupTab()
        self.data_io_tab = DataIOTab()
        self.system_info_tab = SystemInfoTab()
        self.system_tab.addTab(self.initial_setup_tab, "初期設定")
        self.system_tab.addTab(self.data_io_tab, "データ入出力")
        self.system_tab.addTab(self.system_info_tab, "システム情報")
        self.tab_widget.addTab(self.system_tab, "システム管理")

        # スキル分析タブ
        self.skill_analysis_tab = QTabWidget()
        self.overall_evaluation_tab = OverallEvaluationTab()
        self.skill_gap_tab = SkillGapTab()
        self.skill_analysis_tab.addTab(self.overall_evaluation_tab, "総合評価")
        self.skill_analysis_tab.addTab(self.skill_gap_tab, "スキルギャップ")
        self.tab_widget.addTab(self.skill_analysis_tab, "スキル分析")

        right_layout.addWidget(self.tab_widget)
        main_layout.addWidget(right_panel, 7)
