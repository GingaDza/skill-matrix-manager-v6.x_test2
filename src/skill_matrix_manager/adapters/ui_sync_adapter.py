from typing import Optional
from datetime import datetime, UTC
from PyQt5.QtWidgets import QComboBox, QListWidget, QTreeWidget, QTreeWidgetItem
from PyQt5.QtCore import Qt
from .ui_protection import UIProtection

class UISyncAdapter:
    """UIコンポーネント間の同期を管理するアダプター"""
    
    def __init__(self, protection: Optional[UIProtection] = None):
        self.protection = protection or UIProtection()
        self._last_sync = datetime(2025, 2, 19, 20, 42, 43, tzinfo=UTC)
        self._current_user = "GingaDza"
        
    def sync_group_selection(self, 
                           combo: QComboBox, 
                           list_widget: QListWidget) -> bool:
        """グループ選択の同期"""
        if self.protection.is_component_locked("group_sync"):
            return False
            
        try:
            selected_group = combo.currentText()
            # リストウィジェットの選択を更新
            for i in range(list_widget.count()):
                if list_widget.item(i).text() == selected_group:
                    list_widget.setCurrentRow(i)
                    return True
            return False
        except Exception as e:
            self.protection.monitor.log_change(
                "group_sync",
                "SYNC_ERROR",
                None,
                str(e),
                self._current_user
            )
            return False
            
    def sync_category_tree(self,
                          source_tree: QTreeWidget,
                          target_tree: QTreeWidget) -> bool:
        """カテゴリーツリーの同期"""
        if self.protection.is_component_locked("category_sync"):
            return False
            
        try:
            target_tree.clear()
            self._sync_tree_items(source_tree.invisibleRootItem(),
                                target_tree.invisibleRootItem())
            return True
        except Exception as e:
            self.protection.monitor.log_change(
                "category_sync",
                "SYNC_ERROR",
                None,
                str(e),
                self._current_user
            )
            return False
            
    def _sync_tree_items(self, source_item: QTreeWidgetItem,
                        target_item: QTreeWidgetItem) -> None:
        """ツリーアイテムの再帰的同期"""
        for i in range(source_item.childCount()):
            source_child = source_item.child(i)
            child_data = [source_child.text(j) for j in range(source_child.columnCount())]
            target_child = QTreeWidgetItem(target_item, child_data)
            self._sync_tree_items(source_child, target_child)
