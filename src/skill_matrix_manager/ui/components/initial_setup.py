from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout,
                           QPushButton, QTreeWidget,
                           QTreeWidgetItem, QListWidget, QLabel,
                           QSplitter)
from PyQt5.QtCore import Qt

class InitialSetupTab(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.main_window = parent
        self.setup_ui()
        self.connect_signals()

    def setup_ui(self):
        # メインレイアウト
        main_layout = QVBoxLayout(self)

        # スプリッターを作成
        splitter = QSplitter(Qt.Horizontal)

        # グループリスト (左側のパネル)
        group_panel = QWidget()
        group_layout = QVBoxLayout(group_panel)
        group_label = QLabel("グループリスト")
        self.group_list = QListWidget()
        group_layout.addWidget(group_label)
        group_layout.addWidget(self.group_list)

        # グループリストの操作ボタン
        group_button_layout = QHBoxLayout()
        self.add_group_btn = QPushButton("追加")
        self.edit_group_btn = QPushButton("編集")
        self.delete_group_btn = QPushButton("削除")
        group_button_layout.addWidget(self.add_group_btn)
        group_button_layout.addWidget(self.edit_group_btn)
        group_button_layout.addWidget(self.delete_group_btn)
        group_layout.addLayout(group_button_layout)

        group_panel.setLayout(group_layout)
        splitter.addWidget(group_panel)

        # カテゴリー・スキルツリー (右側のパネル)
        category_panel = QWidget()
        category_layout = QVBoxLayout(category_panel)

        # タイトルラベル
        category_title_label = QLabel("カテゴリー / スキルツリー")
        category_layout.addWidget(category_title_label)

        # カテゴリー・スキルツリー
        self.category_tree = QTreeWidget()
        self.category_tree.setColumnCount(2)
        self.category_tree.setHeaderLabels(["名前", "レベル"])
        category_layout.addWidget(self.category_tree)

        # ボタンのレイアウト
        button_layout = QHBoxLayout()

        self.add_category_btn = QPushButton("カテゴリー追加")
        self.add_skill_btn = QPushButton("スキル追加")
        self.edit_btn = QPushButton("編集")
        self.delete_btn = QPushButton("削除")

        button_layout.addWidget(self.add_category_btn)
        button_layout.addWidget(self.add_skill_btn)
        button_layout.addWidget(self.edit_btn)
        button_layout.addWidget(self.delete_btn)

        category_layout.addLayout(button_layout)

        # 新規タブ追加ボタン
        self.add_tab_btn = QPushButton("新規タブ追加")
        category_layout.addWidget(self.add_tab_btn)

        category_panel.setLayout(category_layout)
        splitter.addWidget(category_panel)

        # スプリッターをメインレイアウトに追加
        main_layout.addWidget(splitter)

        # スプリッターの初期サイズを設定 (左側300px, 右側600px)
        splitter.setSizes([300, 600])

        self.setLayout(main_layout)

    def connect_signals(self):
        """シグナルの接続"""
        if self.main_window:
            self.group_list.currentItemChanged.connect(self.on_group_selected)
            self.category_tree.itemClicked.connect(self.on_category_tree_item_clicked)

    def on_group_selected(self, current, previous):
        """グループ選択時の処理"""
        if current and self.main_window:
            group_name = current.text()
            index = self.main_window.group_combo.findText(group_name)
            if index >= 0:
                self.main_window.group_combo.setCurrentIndex(index)

    def on_category_tree_item_clicked(self, item, column):
        """カテゴリーツリーアイテムクリック時の処理"""
        if item and self.main_window:
            self.main_window.on_category_tree_item_clicked(item)

    def update_category_tree(self, group_id, user_id=None):
        """カテゴリーツリーの更新"""
        if not self.main_window:
            return
        
        # UIアダプターを使用してツリーを更新
        self.main_window.ui_adapter.update_category_tree(
            self.category_tree,
            group_id,
            user_id
        )

    def update_group_list(self, groups):
        """グループリストの更新"""
        self.group_list.clear()
        for group in groups.values():
            self.group_list.addItem(group["name"])
