from PyQt5.QtWidgets import QTabWidget
from ..skill_evaluation_tab import SkillEvaluationTab

class TabHandlers:
    def __init__(self, tab_widget: QTabWidget):
        self.tab_widget = tab_widget
        self.evaluation_tabs = {}
        self.current_member = None
        self.timestamp = "2025-02-21 14:09:39"
        self.username = "GingaDza"
        self.category_tabs_end_index = 0

    def add_new_tab(self, category_name, skills):
        """新しい評価タブを追加"""
        if category_name in self.evaluation_tabs:
            self.tab_widget.setCurrentWidget(self.evaluation_tabs[category_name])
            return self.evaluation_tabs[category_name]

        evaluation_tab = SkillEvaluationTab(category_name, skills)
        if self.current_member:
            evaluation_tab.set_member(*self.current_member)

        self.evaluation_tabs[category_name] = evaluation_tab
        self.tab_widget.insertTab(self.category_tabs_end_index, evaluation_tab, category_name)
        self.category_tabs_end_index += 1
        return evaluation_tab

    def on_member_selected(self, member_id, member_name, member_group):
        """メンバーが選択された時の処理"""
        self.current_member = (member_id, member_name, member_group)
        for tab in self.evaluation_tabs.values():
            tab.set_member(member_id, member_name, member_group)
