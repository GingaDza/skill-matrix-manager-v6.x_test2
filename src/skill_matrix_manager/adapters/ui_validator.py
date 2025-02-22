from typing import Any, Dict, Optional
from datetime import datetime

class UIChangeValidator:
    """UI変更の妥当性を検証するクラス"""
    
    def __init__(self):
        self.validation_rules: Dict[str, Dict[str, Any]] = {}
        
    def add_validation_rule(self, 
                          component_id: str,
                          rule_type: str,
                          validation_func: callable) -> None:
        """検証ルールの追加"""
        if component_id not in self.validation_rules:
            self.validation_rules[component_id] = {}
        self.validation_rules[component_id][rule_type] = validation_func
        
    def validate_change(self,
                       component_id: str,
                       change_type: str,
                       old_value: Any,
                       new_value: Any) -> tuple[bool, Optional[str]]:
        """変更の妥当性検証"""
        if component_id in self.validation_rules:
            if change_type in self.validation_rules[component_id]:
                validation_func = self.validation_rules[component_id][change_type]
                try:
                    result = validation_func(old_value, new_value)
                    if isinstance(result, tuple):
                        return result
                    return result, None
                except Exception as e:
                    return False, str(e)
        return True, None