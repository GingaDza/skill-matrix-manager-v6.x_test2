from PyQt5.QtWidgets import QInputDialog, QMessageBox, QTreeWidgetItem

class CategoryHandlers:
    def add_category(self):
        if not self.check_group_selected():
            return
            
        name, ok = QInputDialog.getText(self, "カテゴリー追加", "カテゴリー名を入力してください:")
        if ok and name:
            category_item = QTreeWidgetItem(self.category_tree, [name])
            current_group = self.group_list.currentItem().text()
            if current_group in self.group_categories:
                self.group_categories[current_group].append(name)

    def add_skill(self):
        current_item = self.category_tree.currentItem()
        if not current_item:
            QMessageBox.warning(self, "警告", "カテゴリーを選択してください。")
            return

        if current_item.parent():
            current_item = current_item.parent()

        name, ok = QInputDialog.getText(self, "スキル追加", "スキル名を入力してください:")
        if ok and name:
            QTreeWidgetItem(current_item, [name])

    def edit_item(self):
        current_item = self.category_tree.currentItem()
        if not current_item:
            QMessageBox.warning(self, "警告", "編集するアイテムを選択してください。")
            return

        name, ok = QInputDialog.getText(
            self, "編集",
            "新しい名前を入力してください:",
            text=current_item.text(0)
        )
        
        if ok and name:
            current_item.setText(0, name)

    def delete_item(self):
        current_item = self.category_tree.currentItem()
        if not current_item:
            QMessageBox.warning(self, "警告", "削除するアイテムを選択してください。")
            return

        reply = QMessageBox.question(
            self, '確認',
            'このアイテムを削除してもよろしいですか？',
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            parent = current_item.parent()
            if parent:
                parent.removeChild(current_item)
            else:
                index = self.category_tree.indexOfTopLevelItem(current_item)
                self.category_tree.takeTopLevelItem(index)
