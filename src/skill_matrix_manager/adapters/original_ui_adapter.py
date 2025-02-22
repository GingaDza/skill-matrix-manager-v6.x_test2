from datetime import datetime, UTC
from PyQt5.QtWidgets import QMessageBox, QTreeWidgetItem, QListWidgetItem
from .ui_adapter_interface import UIAdapterInterface
from ..ui.components.group_dialog import GroupDialog
from ..ui.components.category_dialog import CategoryDialog
from ..repositories.group_user_repository import GroupUserRepository
from ..repositories.category_repository import CategoryRepository
from ..models.data_models import Group, Category

class OriginalUIAdapter(UIAdapterInterface):
    def __init__(self, view):
        super().__init__(view)
        self.group_repository = GroupUserRepository()
        self.category_repository = CategoryRepository()
        self._init_ui_state()
        self.setup_connections()
        self.update_view()

    def _init_ui_state(self):
        """UIの初期状態を設定"""
        self.view.edit_group_btn.setEnabled(False)
        self.view.delete_group_btn.setEnabled(False)
        self.view.add_category_btn.setEnabled(False)
        self.view.edit_btn.setEnabled(False)
        self.view.delete_btn.setEnabled(False)

    def handle_events(self):
        """イベント処理の実装"""
        pass

    def setup_connections(self):
        """UI要素の接続設定"""
        self.view.add_group_btn.clicked.connect(self.handle_add_group)
        self.view.edit_group_btn.clicked.connect(self.handle_edit_group)
        self.view.delete_group_btn.clicked.connect(self.handle_delete_group)
        self.view.group_list.itemSelectionChanged.connect(self.handle_group_selection)
        
        self.view.add_category_btn.clicked.connect(self.handle_add_category)
        self.view.edit_btn.clicked.connect(self.handle_edit_category)
        self.view.delete_btn.clicked.connect(self.handle_delete_category)
        self.view.category_tree.itemSelectionChanged.connect(self.handle_category_selection)

    def update_view(self):
        """UI要素の更新"""
        self.update_group_list()
        self.update_category_tree()

    def update_group_list(self):
        """グループリストの更新"""
        self.view.group_list.clear()
        groups = self.group_repository.get_groups()
        for group in sorted(groups, key=lambda x: x.name):
            item = QListWidgetItem(group.name)
            self.view.group_list.addItem(item)

    def update_category_tree(self):
        """カテゴリーツリーの更新"""
        selected_group = self._get_selected_group()
        if selected_group:
            categories = self.category_repository.get_categories_by_group(selected_group.id)
            # 必ず更新を実行
            self.view.category_tree.update_tree(categories or [])
        else:
            self.view.category_tree.clear()

    def handle_add_group(self):
        """グループ追加処理"""
        dialog = GroupDialog(self.view)
        if dialog.exec_():
            data = dialog.get_data()
            try:
                self.group_repository.create_group(
                    name=data["name"],
                    description=data.get("description", "")
                )
                self.update_group_list()
            except Exception as e:
                QMessageBox.critical(
                    self.view,
                    "エラー",
                    f"グループの作成に失敗しました: {str(e)}"
                )

    def handle_edit_group(self):
        """グループ編集処理"""
        selected_group = self._get_selected_group()
        if not selected_group:
            return

        dialog = GroupDialog(self.view, selected_group)
        if dialog.exec_():
            data = dialog.get_data()
            selected_group.name = data["name"]
            selected_group.description = data.get("description", "")
            try:
                self.group_repository.update_group(selected_group)
                self.update_group_list()
            except Exception as e:
                QMessageBox.critical(
                    self.view,
                    "エラー",
                    f"グループの更新に失敗しました: {str(e)}"
                )

    def handle_delete_group(self):
        """グループ削除処理"""
        selected_group = self._get_selected_group()
        if not selected_group:
            return

        reply = QMessageBox.question(
            self.view,
            "確認",
            "選択したグループを削除してもよろしいですか？\n" +
            "（関連するカテゴリーとスキルも削除されます）",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )

        if reply == QMessageBox.Yes:
            try:
                self.group_repository.delete_group(selected_group.id)
                self.update_group_list()
                self.update_category_tree()
            except Exception as e:
                QMessageBox.critical(
                    self.view,
                    "エラー",
                    f"グループの削除に失敗しました: {str(e)}"
                )

    def handle_group_selection(self):
        """グループ選択時の処理"""
        selected_group = self._get_selected_group()
        has_selection = selected_group is not None
        
        self.view.edit_group_btn.setEnabled(has_selection)
        self.view.delete_group_btn.setEnabled(has_selection)
        self.view.add_category_btn.setEnabled(has_selection)
        
        if has_selection:
            self.update_category_tree()

    def handle_add_category(self):
        """カテゴリー追加処理"""
        selected_group = self._get_selected_group()
        if not selected_group:
            QMessageBox.warning(self.view, "警告", "グループを選択してください。")
            return

        categories = self.category_repository.get_categories_by_group(selected_group.id)
        dialog = CategoryDialog(self.view, parent_categories=categories)
        if dialog.exec_():
            data = dialog.get_data()
            try:
                self.category_repository.create_category(
                    name=data["name"],
                    group_id=selected_group.id,
                    description=data.get("description", ""),
                    parent_id=data.get("parent_id")
                )
                self.update_category_tree()
            except Exception as e:
                QMessageBox.critical(
                    self.view,
                    "エラー",
                    f"カテゴリーの作成に失敗しました: {str(e)}"
                )

    def handle_edit_category(self):
        """カテゴリー編集処理"""
        category_id = self.view.category_tree.get_selected_category_id()
        if not category_id:
            QMessageBox.warning(self.view, "警告", "編集するカテゴリーを選択してください。")
            return

        selected_group = self._get_selected_group()
        if not selected_group:
            return

        categories = self.category_repository.get_categories_by_group(selected_group.id)
        current_category = next((c for c in categories if c.id == category_id), None)
        if not current_category:
            return

        dialog = CategoryDialog(self.view, current_category, categories)
        if dialog.exec_():
            data = dialog.get_data()
            current_category.name = data["name"]
            current_category.description = data.get("description", "")
            current_category.parent_id = data.get("parent_id")
            try:
                self.category_repository.update_category(current_category)
                self.update_category_tree()
            except Exception as e:
                QMessageBox.critical(
                    self.view,
                    "エラー",
                    f"カテゴリーの更新に失敗しました: {str(e)}"
                )

    def handle_delete_category(self):
        """カテゴリー削除処理"""
        category_id = self.view.category_tree.get_selected_category_id()
        if not category_id:
            QMessageBox.warning(self.view, "警告", "削除するカテゴリーを選択してください。")
            return

        reply = QMessageBox.question(
            self.view,
            "確認",
            "選択したカテゴリーを削除してもよろしいですか？\n" +
            "（関連するスキルも削除されます）",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )

        if reply == QMessageBox.Yes:
            try:
                self.category_repository.delete_category(category_id)
                self.update_category_tree()
            except Exception as e:
                QMessageBox.critical(
                    self.view,
                    "エラー",
                    f"カテゴリーの削除に失敗しました: {str(e)}"
                )

    def handle_category_selection(self):
        """カテゴリー選択時の処理"""
        selected_category_id = self.view.category_tree.get_selected_category_id()
        self.view.edit_btn.setEnabled(selected_category_id is not None)
        self.view.delete_btn.setEnabled(selected_category_id is not None)

    def _get_selected_group(self) -> Group:
        """選択中のグループを取得"""
        current_item = self.view.group_list.currentItem()
        if current_item:
            groups = self.group_repository.get_groups()
            return next(
                (g for g in groups if g.name == current_item.text()),
                None
            )
        return None
