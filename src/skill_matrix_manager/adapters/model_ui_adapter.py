from typing import Dict, Any, Optional, List
from PyQt5.QtWidgets import QTreeWidgetItem, QTreeWidget
from ..models.category import Category
from ..models.skill import Skill

class ModelUIAdapter:
    """モデルとUI間のデータ変換を行うアダプター"""
    def __init__(self):
        self._ui_to_model_map: Dict[int, Any] = {}
        self._model_to_ui_map: Dict[int, QTreeWidgetItem] = {}

    def create_category_item(self, category: Category) -> QTreeWidgetItem:
        """カテゴリーモデルからツリーアイテムを生成"""
        item = QTreeWidgetItem([category.name, ""])
        item.setData(0, 0, category.id)
        
        # マッピングを保存
        self._ui_to_model_map[id(item)] = category
        self._model_to_ui_map[category.id] = item
        
        # スキルアイテムを追加
        for skill in category.skills:
            skill_item = self.create_skill_item(skill)
            item.addChild(skill_item)
        
        return item

    def create_skill_item(self, skill: Skill) -> QTreeWidgetItem:
        """スキルモデルからツリーアイテムを生成"""
        item = QTreeWidgetItem([skill.name, str(skill.required_level)])
        item.setData(0, 0, skill.id)
        
        # マッピングを保存
        self._ui_to_model_map[id(item)] = skill
        self._model_to_ui_map[skill.id] = item
        
        return item

    def get_model_from_item(self, item: QTreeWidgetItem) -> Optional[Any]:
        """ツリーアイテムに対応するモデルを取得"""
        return self._ui_to_model_map.get(id(item))

    def get_item_from_model_id(self, model_id: int) -> Optional[QTreeWidgetItem]:
        """モデルIDに対応するツリーアイテムを取得"""
        return self._model_to_ui_map.get(model_id)

    def update_item_from_model(self, model: Any) -> None:
        """モデルの変更をUIに反映"""
        item = self._model_to_ui_map.get(model.id)
        if not item:
            return

        if isinstance(model, Category):
            item.setText(0, model.name)
        elif isinstance(model, Skill):
            item.setText(0, model.name)
            item.setText(1, str(model.required_level))

    def sync_tree_with_models(self, tree: QTreeWidget, categories: List[Category]) -> None:
        """ツリーウィジェットとモデルを同期"""
        tree.clear()
        self._ui_to_model_map.clear()
        self._model_to_ui_map.clear()

        for category in categories:
            item = self.create_category_item(category)
            tree.addTopLevelItem(item)
