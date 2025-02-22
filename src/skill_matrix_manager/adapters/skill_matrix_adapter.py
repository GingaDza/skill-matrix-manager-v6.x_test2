from datetime import datetime, UTC
from typing import Dict, List, Optional
from .ui_protection import UIProtection

class SkillMatrixAdapter:
    """スキルマトリックス機能のアダプター"""
    
    def __init__(self, protection: Optional[UIProtection] = None):
        self.protection = protection or UIProtection()
        self._last_update = datetime(2025, 2, 19, 20, 42, 43, tzinfo=UTC)
        self._current_user = "GingaDza"
        self._skill_levels: Dict[str, Dict[str, int]] = {}
        
    def set_skill_level(self, 
                       user_id: str,
                       skill_id: str,
                       level: int) -> bool:
        """スキルレベルの設定"""
        if not 1 <= level <= 5:
            return False
            
        if self.protection.is_component_locked(f"skill_{skill_id}"):
            return False
            
        if user_id not in self._skill_levels:
            self._skill_levels[user_id] = {}
            
        old_level = self._skill_levels[user_id].get(skill_id)
        self._skill_levels[user_id][skill_id] = level
        
        self.protection.monitor.log_change(
            f"skill_{skill_id}",
            "LEVEL_UPDATE",
            old_level,
            level,
            self._current_user
        )
        return True
