from PyQt5.QtWidgets import QInputDialog, QMessageBox

class GroupHandlers:
    def add_group(self):
        name, ok = QInputDialog.getText(self, "グループ追加", "グループ名を入力してください:")
        if ok and name:
            self.group_list.addItem(name)
            self.group_categories[name] = []

    def edit_group(self):
        current_item = self.group_list.currentItem()
        if not current_item:
            return
        
        old_name = current_item.text()
        name, ok = QInputDialog.getText(
            self, "グループ編集",
            "新しいグループ名を入力してください:",
            text=old_name
        )
        
        if ok and name:
            current_item.setText(name)
            if old_name in self.group_categories:
                self.group_categories[name] = self.group_categories.pop(old_name)

    def delete_group(self):
        current_item = self.group_list.currentItem()
        if not current_item:
            return
            
        reply = QMessageBox.question(
            self, '確認',
            'このグループを削除してもよろしいですか？',
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            name = current_item.text()
            if name in self.group_categories:
                del self.group_categories[name]
            self.group_list.takeItem(self.group_list.row(current_item))
