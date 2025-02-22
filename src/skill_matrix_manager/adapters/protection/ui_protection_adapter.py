from datetime import datetime, UTC
import json
import logging
from pathlib import Path
from typing import Dict, Any, List, Tuple

class UIProtectionAdapter:
    def __init__(self):
        self._current_time = datetime(2025, 2, 19, 21, 7, 56, tzinfo=UTC)
        self._current_user = "GingaDza"
        self._setup_logging()
        self._load_original_structure()
        self._locked = True

    def _setup_logging(self):
        """ログ設定"""
        log_path = Path("src/skill_matrix_manager/logs/ui_changes.log")
        log_path.parent.mkdir(exist_ok=True)
        
        logging.basicConfig(
            filename=log_path,
            level=logging.INFO,
            format='%(asctime)s [%(levelname)s] %(message)s'
        )
        self.logger = logging.getLogger(__name__)

    def _load_original_structure(self):
        """オリジナルのUI構造を読み込み"""
        structure_path = Path("src/skill_matrix_manager/adapters/protection/ui_structure.json")
        with structure_path.open('r', encoding='utf-8') as f:
            self._original_structure = json.load(f)

    def verify_layout(self, current_layout: Dict[str, Any]) -> bool:
        """レイアウトの検証"""
        if not self._locked:
            return True

        original = self._original_structure["main_layout"]
        if current_layout["split_ratio"] != original["split_ratio"]:
            self._log_violation("split_ratio", original["split_ratio"], current_layout["split_ratio"])
            return False
        return True

    def verify_tab_order(self, tabs: List[str]) -> bool:
        """タブ順序の検証"""
        if not self._locked:
            return True

        original_order = self._original_structure["main_layout"]["right_panel"]["tab_order"]
        if tabs != original_order:
            self._log_violation("tab_order", original_order, tabs)
            return False
        return True

    def can_add_category_tab(self) -> bool:
        """カテゴリータブの追加可否判定"""
        return True  # カテゴリータブの動的追加は常に許可

    def _log_violation(self, component: str, expected: Any, actual: Any):
        """違反のログ記録"""
        self.logger.warning(
            f"UI Violation detected:\n"
            f"Component: {component}\n"
            f"Expected: {expected}\n"
            f"Actual: {actual}\n"
            f"User: {self._current_user}\n"
            f"Time: {self._current_time}"
        )

    def lock_ui(self):
        """UI構造をロック"""
        self._locked = True
        self.logger.info(f"UI locked by {self._current_user}")

    def unlock_ui(self):
        """UI構造のロック解除（管理者のみ）"""
        self._locked = False
        self.logger.warning(f"UI unlocked by {self._current_user}")

    def record_change(self, component: str, action: str, details: Dict[str, Any]):
        """UI変更の記録"""
        self.logger.info(
            f"UI Change:\n"
            f"Component: {component}\n"
            f"Action: {action}\n"
            f"Details: {json.dumps(details, ensure_ascii=False)}\n"
            f"User: {self._current_user}\n"
            f"Time: {self._current_time}"
        )
