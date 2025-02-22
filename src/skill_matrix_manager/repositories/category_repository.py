from typing import List, Optional
from ..models.data_models import Category

class CategoryRepository:
    def __init__(self):
        self.categories = {}
        self.next_id = 1

    def create_category(self, name: str, group_id: str, description: str = "", parent_id: str = None) -> Category:
        """カテゴリーを作成"""
        category_id = str(self.next_id)
        self.next_id += 1
        
        category = Category(
            id=category_id,
            name=name,
            group_id=group_id,
            description=description,
            parent_id=parent_id
        )
        
        self.categories[category_id] = category
        return category

    def get_categories_by_group(self, group_id: str) -> List[Category]:
        """グループIDに紐づくカテゴリーを取得"""
        return [
            category for category in self.categories.values()
            if category.group_id == group_id
        ]

    def update_category(self, category: Category) -> Category:
        """カテゴリーを更新"""
        if category.id not in self.categories:
            raise ValueError("指定されたカテゴリーが存在しません")
        self.categories[category.id] = category
        return category

    def delete_category(self, category_id: str):
        """カテゴリーを削除"""
        if category_id in self.categories:
            # 関連する子カテゴリーも削除
            children = [
                c.id for c in self.categories.values()
                if c.parent_id == category_id
            ]
            for child_id in children:
                self.delete_category(child_id)
            
            del self.categories[category_id]

    def get_category(self, category_id: str) -> Optional[Category]:
        """カテゴリーをIDで取得"""
        return self.categories.get(category_id)
