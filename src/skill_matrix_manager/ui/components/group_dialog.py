from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel,
    QLineEdit, QTextEdit, QPushButton, QMessageBox
)

class GroupDialog(QDialog):
    def __init__(self, parent=None, group=None):
        super().__init__(parent)
        self.group = group
        self.setup_ui()

    def setup_ui(self):
        self.setWindowTitle("グループ" + ("編集" if self.group else "追加"))
        layout = QVBoxLayout(self)

        # グループ名
        name_layout = QHBoxLayout()
        name_label = QLabel("グループ名:")
        self.name_edit = QLineEdit()
        if self.group:
            self.name_edit.setText(self.group.name)
        name_layout.addWidget(name_label)
        name_layout.addWidget(self.name_edit)
        layout.addLayout(name_layout)

        # 説明
        desc_layout = QVBoxLayout()
        desc_label = QLabel("説明:")
        self.desc_edit = QTextEdit()
        if self.group and self.group.description:
            self.desc_edit.setText(self.group.description)
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
            QMessageBox.warning(self, "エラー", "グループ名を入力してください。")
            return
        self.accept()

    def get_data(self):
        return {
            "name": self.name_edit.text().strip(),
            "description": self.desc_edit.toPlainText().strip()
        }
