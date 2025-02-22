from typing import Dict, Any, Optional, Callable
from PyQt5.QtCore import QObject, pyqtSignal
from dataclasses import dataclass
from datetime import datetime

@dataclass
class StateChange:
    component_id: str
    property_name: str
    old_value: Any
    new_value: Any
    timestamp: datetime

class StateManager(QObject):
    """アプリケーション全体の状態を管理するクラス"""
    state_changed = pyqtSignal(str, str, object)  # component_id, property_name, new_value
    
    def __init__(self):
        super().__init__()
        self._state: Dict[str, Dict[str, Any]] = {}
        self._listeners: Dict[str, List[Callable]] = {}
        self._history: List[StateChange] = []
        
    def set_state(self, component_id: str, property_name: str, value: Any) -> None:
        """状態の更新"""
        if component_id not in self._state:
            self._state[component_id] = {}
            
        old_value = self._state[component_id].get(property_name)
        self._state[component_id][property_name] = value
        
        # 変更履歴の記録
        change = StateChange(
            component_id=component_id,
            property_name=property_name,
            old_value=old_value,
            new_value=value,
            timestamp=datetime.utcnow()
        )
        self._history.append(change)
        
        # 変更通知
        self.state_changed.emit(component_id, property_name, value)
        
    def get_state(self, component_id: str, property_name: str) -> Optional[Any]:
        """状態の取得"""
        return self._state.get(component_id, {}).get(property_name)