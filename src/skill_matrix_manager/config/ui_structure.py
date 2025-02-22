from dataclasses import dataclass
from typing import List
from datetime import datetime, UTC

@dataclass
class UILayout:
    CURRENT_TIME = datetime(2025, 2, 19, 20, 52, 56, tzinfo=UTC)
    CURRENT_USER = "GingaDza"
    
    # メイン画面の分割比率
    MAIN_SPLIT_RATIO = (3, 7)
    
    # タブの順序定義
    TAB_ORDER = [
        "category_tabs",  # カテゴリータブが先頭
        "skill_analysis",
        "system_management"
    ]
    
    # 左パネルの構成
    LEFT_PANEL = {
        "top": "group_combo",
        "middle": "user_list",
        "bottom": ["add_user_btn", "edit_user_btn", "delete_user_btn"]
    }
