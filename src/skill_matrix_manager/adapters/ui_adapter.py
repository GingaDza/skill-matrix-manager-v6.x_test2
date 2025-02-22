from typing import Dict, Any, Optional, List
from PyQt5.QtWidgets import QWidget, QTreeWidget, QTreeWidgetItem, QListWidget, QListWidgetItem
from PyQt5.QtCore import Qt
from ..models.data_models import Group, User, Category, Skill, SkillLevel

class UIAdapter:
    """UI-モデル間の変換を行うアダプター"""
    def __init__(self, data_model: Dict[str, List[Any]], parent: Optional[QWidget] = None):
        self.data_model = data_model
        self.parent = parent
        self._widget_to_model_map: Dict[int, Any] = {}
        self._model_to_widget_map: Dict[int, QWidget] = {}
        self._tree_widgets: List[QTreeWidget] = []
        self._list_widgets: List[QListWidget] = []

    def register_widget(self, widget: QWidget, model: Any) -> None:
        """ウィジェットとモデルの関連付け"""
        if widget is None or model is None:
            return

        widget_id = id(widget)
        model_id = id(model)
        self._widget_to_model_map[widget_id] = model
        self._model_to_widget_map[model_id] = widget

        # ウィジェットの種類に応じてリストに追加
        if isinstance(widget, QTreeWidget):
            self._tree_widgets.append(widget)
        elif isinstance(widget, QListWidget):
            self._list_widgets.append(widget)

    def create_tree_item(self, model: Any) -> QTreeWidgetItem:
        """モデルからツリーアイテムを作成"""
        if isinstance(model, Category):
            item = QTreeWidgetItem([model.name])
            for skill in model.skills:
                skill_item = QTreeWidgetItem([skill.name, str(skill.required_level.value)])
                item.addChild(skill_item)
                self.register_widget(skill_item, skill)
            self.register_widget(item, model)
            return item
        elif isinstance(model, Skill):
            item = QTreeWidgetItem([model.name, str(model.required_level.value)])
            self.register_widget(item, model)
            return item
        return None

    def create_list_item(self, model: Any) -> QListWidgetItem:
        """モデルからリストアイテムを作成"""
        if isinstance(model, Group):
            item = QListWidgetItem(model.name)
            self.register_widget(item, model)
            return item
        elif isinstance(model, User):
            item = QListWidgetItem(model.name)
            self.register_widget(item, model)
            return item
        return None

    def sync_tree_widget(self, tree_widget: QTreeWidget, models: List[Any]) -> None:
        """ツリーウィジェットとモデルを同期"""
        if not isinstance(tree_widget, QTreeWidget):
            return

        tree_widget.clear()
        for model in models:
            item = self.create_tree_item(model)
            if item:
                tree_widget.addTopLevelItem(item)
        self.register_widget(tree_widget, models)

    def sync_list_widget(self, list_widget: QListWidget, models: List[Any]) -> None:
        """リストウィジェットとモデルを同期"""
        if not isinstance(list_widget, QListWidget):
            return

        list_widget.clear()
        for model in models:
            item = self.create_list_item(model)
            if item:
                list_widget.addItem(item)
        self.register_widget(list_widget, models)

    def cleanup(self) -> None:
        """リソースのクリーンアップ"""
        self._widget_to_model_map.clear()
        self._model_to_widget_map.clear()
        
        for widget in self._tree_widgets + self._list_widgets:
            if widget and not widget.isVisible():
                widget.deleteLater()
        
        self._tree_widgets.clear()
        self._list_widgets.clear()
