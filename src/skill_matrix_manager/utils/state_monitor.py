import os
import datetime
from typing import Optional, Dict, Any

class StateMonitor:
    def __init__(self):
        self._current_user = "GingaDza"  # 直接設定
        self._current_datetime = datetime.datetime(2025, 2, 21, 12, 6, 34)  # 直接設定
        self._state: Dict[str, Any] = {}
        self._history: list = []

    @property
    def current_user(self) -> str:
        return self._current_user

    @property
    def current_datetime(self) -> datetime.datetime:
        return self._current_datetime

    def update_state(self, key: str, value: Any) -> None:
        old_value = self._state.get(key)
        self._state[key] = value
        self._history.append({
            "timestamp": datetime.datetime.utcnow(),
            "user": self.current_user,
            "key": key,
            "old_value": old_value,
            "new_value": value
        })

    def get_state(self, key: str) -> Optional[Any]:
        return self._state.get(key)

    def get_history(self) -> list:
        return self._history

    def clear_history(self) -> None:
        self._history = []

state_monitor = StateMonitor()
