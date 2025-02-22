from datetime import datetime, UTC
from typing import Dict, Any, Optional
from ..config.ui_structure import UILayout

class UILayoutProtection:
    """UI構造の保護を担当するクラス"""
    
    def __init__(self):
        self._current_time = datetime(2025, 2, 19, 20, 52, 56, tzinfo=UTC)
        self._current_user = "GingaDza"
        self._layout = UILayout()
        self._locked = True

    def verify_tab_structure(self, tabs: Dict[str, list]) -> bool:
        """タブの順序を検証"""
        main_tabs = tabs.get("main_tabs", [])
        
        # カテゴリータブが先頭にあることを確認
        category_tabs = [tab for tab in main_tabs if tab.startswith("category_")]
        if not category_tabs or main_tabs.index(category_tabs[0]) != 0:
            return False
            
        # スキル分析とシステム管理タブの順序を確認
        if "skill_analysis" not in main_tabs or "system_management" not in main_tabs:
            return False
            
        skill_analysis_index = main_tabs.index("skill_analysis")
        system_management_index = main_tabs.index("system_management")
        
        return skill_analysis_index < system_management_index
