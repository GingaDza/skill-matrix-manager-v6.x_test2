from datetime import datetime, UTC
from PyQt5.QtWidgets import QWidget, QTreeWidget

class UIValidator:
    def __init__(self):
        self._current_time = datetime(2025, 2, 19, 22, 16, 42, tzinfo=UTC)
        self._current_user = "GingaDza"
        self.validation_results = []

    def validate_initial_setup_tab(self, tab: QWidget) -> bool:
        """初期設定タブの要素を検証"""
        try:
            # 左パネル検証
            self._validate_left_panel(tab)
            
            # 右パネル検証
            self._validate_right_panel(tab)
            
            # 結果を表示
            self._print_validation_results()
            
            return all(result[0] for result in self.validation_results)
            
        except Exception as e:
            print(f"Validation error: {str(e)}")
            return False

    def _validate_left_panel(self, tab):
        """左パネルの要素を検証"""
        # グループリストラベルの確認
        self._validate_component(
            hasattr(tab, 'group_list'), 
            "グループリスト表示領域"
        )
        
        # 操作ボタンの確認
        buttons = ['add_group_btn', 'edit_group_btn', 'delete_group_btn']
        for btn in buttons:
            self._validate_component(
                hasattr(tab, btn), 
                f"操作ボタン: {btn}"
            )

    def _validate_right_panel(self, tab):
        """右パネルの要素を検証"""
        # カテゴリーツリーの確認
        if hasattr(tab, 'category_tree'):
            tree: QTreeWidget = tab.category_tree
            self._validate_component(
                tree.columnCount() == 2,
                "ツリー表示領域（2列）"
            )

        # 操作ボタンの確認
        buttons = [
            'add_category_btn', 'add_skill_btn',
            'edit_btn', 'delete_btn', 'add_tab_btn'
        ]
        for btn in buttons:
            self._validate_component(
                hasattr(tab, btn),
                f"操作ボタン: {btn}"
            )

    def _validate_component(self, condition: bool, component_name: str):
        """コンポーネントの存在を検証"""
        status = "✓" if condition else "✗"
        self.validation_results.append((condition, f"{status} {component_name}"))

    def _print_validation_results(self):
        """検証結果を表示"""
        print(f"\nUI Validation Results ({self._current_time} UTC)")
        print(f"User: {self._current_user}")
        print("-" * 50)
        
        # 左パネルの結果
        print("\n左パネル:")
        for result in self.validation_results[:4]:  # 左パネルの結果
            print(result[1])
            
        # 右パネルの結果
        print("\n右パネル:")
        for result in self.validation_results[4:]:  # 右パネルの結果
            print(result[1])
