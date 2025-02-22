from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel,
    QLineEdit, QTextEdit, QPushButton, QMessageBox,
    QComboBox
)
from ...models.data_models import Category

class CategoryDialog(QDialog):
    def __init__(self, parent=None, category=None, parent_categories=None):
        super().__init__(parent)
        self.category = category
        self.parent_categories = parent_categories or []
        self.setup_ui()

    def setup_ui(self):
        self.setWindowTitle("カテゴリー" + ("編集" if self.category else "追加"))
        layout = QVBoxLayout(self)

        # カテゴリー名
        name_layout = QHBoxLayout()
        name_label = QLabel("カテゴリー名:")
        self.name_edit = QLineEdit()
        if self.category:
            self.name_edit.setText(self.category.name)
        name_layout.addWidget(name_label)
        name_layout.addWidget(self.name_edit)
        layout.addLayout(name_layout)

        # 親カテゴリー選択
        parent_layout = QHBoxLayout()
        parent_label = QLabel("親カテゴリー:")
        self.parent_combo = QComboBox()
        self.parent_combo.addItem("なし", None)
        for parent in self.parent_categories:
            if self.category and parent.id == self.category.id:
                continue  # 自分自身は親カテゴリーにできない
            self.parent_combo.addItem(parent.name, parent.id)
        if self.category and self.category.parent_id:
            index = self.parent_combo.findData(self.category.parent_id)
            if index >= 0:
                self.parent_combo.setCurrentIndex(index)
        parent_layout.addWidget(parent_label)
        parent_layout.addWidget(self.parent_combo)
        layout.addLayout(parent_layout)

        # 説明
        desc_layout = QVBoxLayout()
        desc_label = QLabel("説明:")
        self.desc_edit = QTextEdit()
        if self.category and self.category.description:
            self.desc_edit.setText(self.category.description)
        desc_layout.addWidget(desc_label)
        desc_layout.addWidget(self.desc_edit)
        layout.addLayout(desc_layout)

        # ボタン
        button_layout = QHBoxLayout()
        self.ok_button = QPushButton("OK")
        self.cancel_button = QPushButton("キャンセル")
        self.ok_button.clicked.connect(self.validate_and_accept)
        self.cancel_button.clicked.connect(self.reject)
        button_layout.addWidget(self.ok_button)
        button_layout.addWidget(self.cancel_button)
        layout.addLayout(button_layout)

        self.setLayout(layout)

    def validate_and_accept(self):
        name = self.name_edit.text().strip()
        if not name:
            QMessageBox.warning(self, "エラー", "カテゴリー名を入力してください。")
            return
        self.accept()

    def get_data(self):
        return {
            "name": self.name_edit.text().strip(),
            "description": self.desc_edit.toPlainText().strip(),
            "parent_id": self.parent_combo.currentData()
        }
