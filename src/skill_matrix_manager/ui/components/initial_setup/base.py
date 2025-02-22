from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QListWidget,
    QPushButton, QLabel, QSplitter, QTreeWidget,
    QTreeWidgetItem, QInputDialog, QMessageBox
)
from PyQt5.QtCore import Qt
from .ui_components import UIComponents

class InitialSetupBase(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.main_window = parent
        self.group_categories = {}
        self.setup_ui()
        self.setup_initial_data()
        self.group_list.itemSelectionChanged.connect(self.on_group_selection_changed)

    def setup_ui(self):
        """UIの初期化"""
        main_layout = QVBoxLayout(self)
        
        splitter = QSplitter(Qt.Horizontal)
        main_layout.addWidget(splitter)
        
        # 左側のパネル（グループリスト）
        left_panel = QWidget()
        left_layout = QVBoxLayout(left_panel)
        
        group_label = QLabel("グループ")
        left_layout.addWidget(group_label)
        
        self.group_list = QListWidget()
        left_layout.addWidget(self.group_list)
        
        group_buttons = QHBoxLayout()
        add_group_btn = QPushButton("追加")
        edit_group_btn = QPushButton("編集")
        delete_group_btn = QPushButton("削除")
        
        add_group_btn.clicked.connect(self.add_group)
        edit_group_btn.clicked.connect(self.edit_group)
        delete_group_btn.clicked.connect(self.delete_group)
        
        group_buttons.addWidget(add_group_btn)
        group_buttons.addWidget(edit_group_btn)
        group_buttons.addWidget(delete_group_btn)
        left_layout.addLayout(group_buttons)
        
        splitter.addWidget(left_panel)
        
        # 右側のパネル（カテゴリーツリー）
        right_panel = QWidget()
        right_layout = QVBoxLayout(right_panel)
        
        category_label = QLabel("カテゴリー")
        right_layout.addWidget(category_label)
        
        self.category_tree = QTreeWidget()
        self.category_tree.setHeaderLabel("カテゴリーとスキル")
        right_layout.addWidget(self.category_tree)
        
        category_buttons = QHBoxLayout()
        add_category_btn = QPushButton("カテゴリー追加")
        add_skill_btn = QPushButton("スキル追加")
        edit_item_btn = QPushButton("編集")
        delete_item_btn = QPushButton("削除")
        
        add_category_btn.clicked.connect(self.add_category)
        add_skill_btn.clicked.connect(self.add_skill)
        edit_item_btn.clicked.connect(self.edit_item)
        delete_item_btn.clicked.connect(self.delete_item)
        
        category_buttons.addWidget(add_category_btn)
        category_buttons.addWidget(add_skill_btn)
        category_buttons.addWidget(edit_item_btn)
        category_buttons.addWidget(delete_item_btn)
        right_layout.addLayout(category_buttons)
        
        # UIコンポーネント（新規タブ追加ボタン）をカテゴリーパネルの最下部に追加
        self.ui_components = UIComponents(self.main_window)  # MainWindowを渡す
        right_layout.addWidget(self.ui_components.widget)
        
        splitter.addWidget(right_panel)
        
        # スプリッターの初期サイズ比を設定
        splitter.setSizes([200, 400])

    def check_group_selected(self):
        if not self.group_list.currentItem():
            QMessageBox.warning(self, "警告", "グループを選択してください。")
            return False
        return True

    def on_group_selection_changed(self):
        current_group = self.group_list.currentItem()
        if current_group:
            group_name = current_group.text()
            self.filter_categories(group_name)
