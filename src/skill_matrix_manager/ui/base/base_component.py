from PyQt5.QtWidgets import QWidget
from PyQt5.QtCore import pyqtSignal
from typing import Optional, Dict, Any
from ...utils.state_manager import StateManager

class BaseComponent(QWidget):
    """全UIコンポーネントの基底クラス"""
    
    state_changed = pyqtSignal(str, object)  # property_name, new_value
    
    def __init__(self, parent: Optional[QWidget] = None):
        super().__init__(parent)
        self._component_id = self.__class__.__name__
        self._state_manager = StateManager()
        
    def set_state(self, property_name: str, value: Any) -> None:
        """コンポーネントの状態を更新"""
        self._state_manager.set_state(self._component_id, property_name, value)
        self.state_changed.emit(property_name, value)
        
    def get_state(self, property_name: str) -> Optional[Any]:
        """コンポーネントの状態を取得"""
        return self._state_manager.get_state(self._component_id, property_name)
        
    def update_ui(self) -> None:
        """UIの更新（サブクラスで実装）"""
        pass