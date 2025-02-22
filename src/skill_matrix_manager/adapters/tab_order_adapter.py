from datetime import datetime, UTC
from typing import List
from PyQt5.QtWidgets import QTabWidget

class TabOrderAdapter:
    """タブの配置順序を制御するアダプター"""
    
    def __init__(self):
        self._current_time = datetime(2025, 2, 19, 20, 54, 17, tzinfo=UTC)
        self._current_user = "GingaDza"
        self.main_tab_order = [
            "カテゴリー",  # カテゴリータブ（動的に追加）
            "スキル分析",
            "システム管理"
        ]
    
    def apply_tab_order(self, tab_widget: QTabWidget) -> None:
        """タブの順序を適用"""
        # システム管理タブを一時的に最後に移動
        system_tab_index = self._find_tab_index(tab_widget, "システム管理")
        if system_tab_index >= 0:
            system_tab = tab_widget.widget(system_tab_index)
            system_tab_text = tab_widget.tabText(system_tab_index)
            tab_widget.removeTab(system_tab_index)
            tab_widget.addTab(system_tab, system_tab_text)
        
        # スキル分析タブをカテゴリータブの後に移動
        skill_tab_index = self._find_tab_index(tab_widget, "スキル分析")
        if skill_tab_index >= 0:
            skill_tab = tab_widget.widget(skill_tab_index)
            skill_tab_text = tab_widget.tabText(skill_tab_index)
            tab_widget.removeTab(skill_tab_index)
            # カテゴリータブの後に挿入
            category_count = self._count_category_tabs(tab_widget)
            tab_widget.insertTab(category_count, skill_tab, skill_tab_text)
    
    def _find_tab_index(self, tab_widget: QTabWidget, tab_text: str) -> int:
        """指定したタブのインデックスを検索"""
        for i in range(tab_widget.count()):
            if tab_widget.tabText(i) == tab_text:
                return i
        return -1
    
    def _count_category_tabs(self, tab_widget: QTabWidget) -> int:
        """カテゴリータブの数をカウント"""
        count = 0
        for i in range(tab_widget.count()):
            if tab_widget.tabText(i).startswith("カテゴリー"):
                count += 1
        return count
