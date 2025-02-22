from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QPushButton,
                           QTreeWidget, QTreeWidgetItem, QLabel,
                           QListWidget, QHBoxLayout, QComboBox)
from .initial_setup import InitialSetupTab

class LeftPanel:
    @staticmethod
    def setup(main_window):
        """左パネルのセットアップ"""
        left_panel = QWidget()
        layout = QVBoxLayout(left_panel)

        # グループ選択
        group_label = QLabel("グループ選択")
        main_window.group_combo = QComboBox()
        layout.addWidget(group_label)
        layout.addWidget(main_window.group_combo)

        # ユーザーリスト
        user_label = QLabel("ユーザーリスト")
        main_window.user_list = QListWidget()
        layout.addWidget(user_label)
        layout.addWidget(main_window.user_list)

        # ユーザー操作ボタン
        user_button_layout = QHBoxLayout()
        main_window.add_user_btn = QPushButton("追加")
        main_window.edit_user_btn = QPushButton("編集")
        main_window.delete_user_btn = QPushButton("削除")
        
        user_button_layout.addWidget(main_window.add_user_btn)
        user_button_layout.addWidget(main_window.edit_user_btn)
        user_button_layout.addWidget(main_window.delete_user_btn)
        layout.addLayout(user_button_layout)

        left_panel.setLayout(layout)
        main_window.splitter.addWidget(left_panel)

class RightPanel:
    @staticmethod
    def setup(main_window):
        """右パネルのセットアップ"""
        # 初期設定タブの作成
        main_window.initial_setup_tab = InitialSetupTab(main_window)
        main_window.splitter.addWidget(main_window.initial_setup_tab)
