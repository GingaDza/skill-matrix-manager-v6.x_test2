from abc import ABC, abstractmethod
from typing import Any, Dict, Optional
from datetime import datetime
from .ui_protection import UIProtection, UIChangeMonitor

class UIAdapterInterface(ABC):
    """UIアダプターの基底インターフェース"""
    
    def __init__(self):
        self.monitor = UIChangeMonitor()
        self.protection = UIProtection(self.monitor)
        self._component_id: str = self.__class__.__name__
        
    @abstractmethod
    def initialize_ui(self) -> bool:
        """UIの初期化処理"""
        pass
        
    @abstractmethod
    def update_view(self, data: Dict[str, Any]) -> bool:
        """ビューの更新処理"""
        pass
        
    def protect_ui_change(self, change_type: str,
                         old_value: Any,
                         new_value: Any) -> bool:
        """UI変更の保護チェック"""
        return self.protection.validate_change(
            self._component_id,
            change_type,
            old_value,
            new_value
        )
