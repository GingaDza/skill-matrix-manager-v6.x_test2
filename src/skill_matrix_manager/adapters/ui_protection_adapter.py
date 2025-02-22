from datetime import datetime, UTC
from typing import Dict, Any, Optional
import json
import logging
from pathlib import Path

class UIProtectionAdapter:
    """UIの構造を保護し、変更を監視・記録するアダプター"""
    
    def __init__(self):
        self._current_time = datetime(2025, 2, 19, 21, 4, 47, tzinfo=UTC)
        self._current_user = "GingaDza"
        self._locked = True
        self._original_state = None
        self._setup_logging()
        self._save_original_state()

    def _setup_logging(self):
        """ログ設定"""
        log_dir = Path("logs")
        log_dir.mkdir(exist_ok=True)
        
        logging.basicConfig(
            filename=log_dir / "ui_changes.log",
            level=logging.INFO,
            format='%(asctime)s [%(levelname)8s] %(message)s (%(filename)s:%(lineno)s)'
        )
        self.logger = logging.getLogger(__name__)

    def _save_original_state(self):
        """オリジナルのUI状態を保存"""
        self._original_state = {
            "main_layout": {
                "split_ratio": (3, 7),
                "left_panel": {
                    "widgets": [
                        {"type": "QLabel", "text": "グループ選択:"},
                        {"type": "QComboBox", "name": "group_combo"},
                        {"type": "QLabel", "text": "ユーザーリスト:"},
                        {"type": "QListWidget", "name": "user_list"},
                        {"type": "QPushButton", "text": "追加"},
                        {"type": "QPushButton", "text": "編集"},
                        {"type": "QPushButton", "text": "削除"}
                    ]
                },
                "right_panel": {
                    "tabs": [
                        {"name": "スキル分析", "subtabs": ["総合評価", "スキルギャップ"]},
                        {"name": "システム管理", "subtabs": ["初期設定", "データ入出力", "システム情報"]}
                    ]
                }
            }
        }
        
        # オリジナル状態をファイルに保存
        with open("ui_original_state.json", "w", encoding="utf-8") as f:
            json.dump(self._original_state, f, ensure_ascii=False, indent=2)

    def verify_ui_state(self, current_state: Dict[str, Any]) -> bool:
        """現在のUI状態がオリジナルと一致するか検証"""
        if self._locked and self._original_state:
            if current_state != self._original_state:
                self.logger.warning(
                    f"UI state mismatch detected by {self._current_user} at {self._current_time}"
                )
                return False
        return True

    def lock_ui(self):
        """UI構造をロック"""
        self._locked = True
        self.logger.info(f"UI locked by {self._current_user}")

    def unlock_ui(self):
        """UI構造のロックを解除（要管理者権限）"""
        self._locked = False
        self.logger.warning(f"UI unlocked by {self._current_user}")

    def can_modify(self, component_name: str) -> bool:
        """コンポーネントの変更が許可されているか確認"""
        if self._locked:
            self.logger.info(
                f"Modification attempt on {component_name} by {self._current_user} while UI is locked"
            )
            return False
        return True

    def record_change(self, component: str, change_type: str, old_value: Any, new_value: Any):
        """UI変更を記録"""
        self.logger.info(
            f"UI Change: {component} - {change_type} - "
            f"Old: {old_value} -> New: {new_value} by {self._current_user}"
        )
