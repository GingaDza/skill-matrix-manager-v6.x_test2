from typing import Dict, Any, Optional
from datetime import datetime, UTC
import logging

class UIChangeMonitor:
    """UIの変更を監視・記録するクラス"""
    
    def __init__(self, log_file: str = "ui_changes.log"):
        self.log_file = log_file
        self._setup_logger()
        self._start_time = datetime(2025, 2, 19, 20, 43, 55, tzinfo=UTC)
        
    def _setup_logger(self):
        self.logger = logging.getLogger("UIProtection")
        self.logger.setLevel(logging.INFO)
        handler = logging.FileHandler(self.log_file)
        formatter = logging.Formatter(
            '%(asctime)s - %(levelname)s - User: %(user)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)
        
    def log_change(self, component_id: str, change_type: str,
                   old_value: Any, new_value: Any, user: str) -> None:
        """変更をログに記録"""
        extra = {'user': user}
        self.logger.info(
            f"Component: {component_id} - Change: {change_type} - "
            f"Old: {old_value} -> New: {new_value}",
            extra=extra
        )

class UIProtection:
    """UI変更を保護・制御するクラス"""
    
    def __init__(self, monitor: Optional[UIChangeMonitor] = None):
        self.monitor = monitor or UIChangeMonitor()
        self._locked_components: Dict[str, bool] = {}
        self._current_user: Optional[str] = "GingaDza"
        self._last_change_time: Optional[datetime] = datetime(2025, 2, 19, 20, 43, 55, tzinfo=UTC)
        
    def set_current_user(self, user: str) -> None:
        """現在のユーザーを設定"""
        self._current_user = user
        self._last_change_time = datetime.now(UTC)
        
    def lock_component(self, component_id: str) -> None:
        """コンポーネントをロック"""
        self._locked_components[component_id] = True
        self.monitor.log_change(
            component_id,
            "LOCK",
            None,
            None,
            self._current_user or 'Unknown'
        )
        
    def unlock_component(self, component_id: str) -> None:
        """コンポーネントのロックを解除"""
        self._locked_components[component_id] = False
        self.monitor.log_change(
            component_id,
            "UNLOCK",
            None,
            None,
            self._current_user or 'Unknown'
        )
        
    def is_component_locked(self, component_id: str) -> bool:
        """コンポーネントのロック状態を確認"""
        return self._locked_components.get(component_id, False)
        
    def validate_change(self, component_id: str,
                       change_type: str,
                       old_value: Any,
                       new_value: Any) -> bool:
        """UI変更の妥当性を検証"""
        if self.is_component_locked(component_id):
            self.monitor.log_change(
                component_id,
                f"BLOCKED_{change_type}",
                old_value,
                new_value,
                self._current_user or 'Unknown'
            )
            return False
        
        self.monitor.log_change(
            component_id,
            f"ALLOWED_{change_type}",
            old_value,
            new_value,
            self._current_user or 'Unknown'
        )
        return True
