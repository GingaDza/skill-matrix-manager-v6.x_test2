from PyQt5.QtWidgets import QTreeWidget, QTreeWidgetItem
from PyQt5.QtCore import Qt
from ...models.data_models import Category, Skill

class CategoryTreeWidget(QTreeWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setColumnCount(2)
        self.setHeaderLabels(["名前", "レベル"])
        self.category_items = {}  # カテゴリーIDをキーにしたアイテムの辞書

    def update_tree(self, categories: list[Category], skills: list[Skill] = None):
        """ツリーの更新"""
        self.clear()
        self.category_items.clear()

        if not categories:
            return

        # カテゴリーをIDでソート
        sorted_categories = sorted(categories, key=lambda x: x.id)
        
        # まずすべてのカテゴリーをitemsに登録
        for category in sorted_categories:
            item = QTreeWidgetItem()
            item.setText(0, category.name)
            item.setData(0, Qt.UserRole, category.id)
            self.category_items[category.id] = item

        # 親子関係を構築
        for category in sorted_categories:
            item = self.category_items[category.id]
            if category.parent_id and category.parent_id in self.category_items:
                # 親カテゴリーが存在する場合は、その子として追加
                parent_item = self.category_items[category.parent_id]
                parent_item.addChild(item)
            else:
                # 親カテゴリーがない場合は、ルートとして追加
                self.addTopLevelItem(item)

    def get_selected_category_id(self) -> str:
        """選択されたカテゴリーのIDを取得"""
        current_item = self.currentItem()
        if current_item:
            return current_item.data(0, Qt.UserRole)
        return None

    def add_category(self, category: Category):
        """カテゴリーを追加"""
        item = QTreeWidgetItem()
        item.setText(0, category.name)
        item.setData(0, Qt.UserRole, category.id)
        
        if category.parent_id and category.parent_id in self.category_items:
            parent_item = self.category_items[category.parent_id]
            parent_item.addChild(item)
        else:
            self.addTopLevelItem(item)
            
        self.category_items[category.id] = item
        return item

    def remove_category(self, category_id: str):
        """カテゴリーを削除"""
        if category_id in self.category_items:
            item = self.category_items[category_id]
            parent = item.parent()
            if parent:
                parent.removeChild(item)
            else:
                index = self.indexOfTopLevelItem(item)
                self.takeTopLevelItem(index)
            del self.category_items[category_id]
