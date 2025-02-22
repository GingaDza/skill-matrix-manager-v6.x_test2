from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
                           QLabel, QComboBox, QSpacerItem, QSizePolicy)
from PyQt5.QtCore import pyqtSignal
from typing import Dict, List, Optional, Callable
from .skill_input_dialog import SkillInputDialog
from .stage_display_widget import StageDisplayWidget
from skill_matrix_manager.utils.debug_logger import DebugLogger

logger = DebugLogger.get_logger()

class ProgressiveTargetWidget(QWidget):
    # シグナルの定義
    on_stage_changed: Callable[[List[Dict]], None]

    def __init__(self, parent=None):
        super().__init__(parent)
        self._stages: List[Dict[str, Dict[str, Dict[str, int]]]] = []  # [時期: {グループ: {カテゴリ: {スキル: レベル}}}]
        self._time_values = [1, 3, 6, 12]  # デフォルトの時間値
        self._time_unit = "月"  # デフォルトの時間単位
        self._skill_hierarchy: Dict[str, Dict[str, Dict[str, str]]] = {}  # {グループ: {カテゴリ: {スキル: 現在レベル}}}
        self._setup_ui()
        logger.debug("ProgressiveTargetWidget initialized")

    def _setup_ui(self):
        """UIのセットアップ"""
        layout = QVBoxLayout()
        
        # 上部コントロールエリア
        control_layout = QHBoxLayout()
        
        # 時間単位選択
        time_unit_layout = QHBoxLayout()
        time_unit_label = QLabel("時間単位:")
        self.time_unit_combo = QComboBox()
        self.time_unit_combo.addItems(["時間", "日", "月", "年"])
        self.time_unit_combo.setCurrentText(self._time_unit)
        self.time_unit_combo.currentTextChanged.connect(self._on_time_unit_changed)
        time_unit_layout.addWidget(time_unit_label)
        time_unit_layout.addWidget(self.time_unit_combo)
        control_layout.addLayout(time_unit_layout)
        
        # スペーサー
        control_layout.addSpacerItem(QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum))
        
        # ステージ追加ボタン
        self.add_stage_button = QPushButton("ステージを追加")
        self.add_stage_button.clicked.connect(self._add_stage)
        control_layout.addWidget(self.add_stage_button)
        
        layout.addLayout(control_layout)
        
        # ステージ表示エリア
        self.stages_layout = QVBoxLayout()
        layout.addLayout(self.stages_layout)
        
        # 余白を追加
        layout.addStretch()
        
        self.setLayout(layout)
        logger.debug("ProgressiveTargetWidget UI setup completed")

    def set_skill_hierarchy(self, hierarchy: Dict[str, Dict[str, Dict[str, str]]]) -> None:
        """スキル階層構造の設定"""
        logger.debug(f"Setting skill hierarchy: {hierarchy}")
        self._skill_hierarchy = hierarchy
        self._clear_stages()

    def _clear_stages(self) -> None:
        """全ステージの削除"""
        logger.debug("Clearing all stages")
        self._stages.clear()
        # UIからステージウィジェットを削除
        while self.stages_layout.count():
            item = self.stages_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
        self._notify_stage_changed()

    def _add_stage(self) -> None:
        """新しいステージの追加"""
        if not self._skill_hierarchy:
            logger.warning("Cannot add stage: No skill hierarchy defined")
            return

        time_value = self._get_next_time_value()
        if time_value is None:
            logger.warning("Cannot add stage: No more time values available")
            return

        # スキル入力ダイアログを表示
        dialog = SkillInputDialog(time_value, self._time_unit, self._skill_hierarchy, self)
        if dialog.exec_():
            stage_data = dialog.get_skill_levels()
            self._add_stage_widget(time_value, stage_data)
            logger.debug(f"Added new stage with time value {time_value}")
            self._notify_stage_changed()

    def _get_next_time_value(self) -> Optional[int]:
        """次の時間値を取得"""
        used_values = [stage["time_value"] for stage in self._stages]
        available_values = [v for v in self._time_values if v not in used_values]
        return min(available_values) if available_values else None

    def _add_stage_widget(self, time_value: int, stage_data: Dict[str, Dict[str, Dict[str, int]]]) -> None:
        """ステージウィジェットの追加"""
        stage = {
            "time_value": time_value,
            "time_unit": self._time_unit,
            "data": stage_data
        }
        self._stages.append(stage)
        self._stages.sort(key=lambda x: x["time_value"])
        
        # UIを更新
        self._update_stages_ui()
        logger.debug(f"Added stage widget for time value {time_value}")

    def _update_stages_ui(self) -> None:
        """ステージUIの更新"""
        # 既存のウィジェットをクリア
        while self.stages_layout.count():
            item = self.stages_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

        # ステージウィジェットを再作成
        for stage in self._stages:
            widget = StageDisplayWidget(
                time_value=stage["time_value"],
                time_unit=stage["time_unit"],
                stage_data=stage["data"],
                parent=self
            )
            widget.delete_requested.connect(
                lambda time_val=stage["time_value"]: self._delete_stage(time_val)
            )
            self.stages_layout.addWidget(widget)
        logger.debug("Updated stages UI")

    def _delete_stage(self, time_value: int) -> None:
        """ステージの削除"""
        self._stages = [s for s in self._stages if s["time_value"] != time_value]
        self._update_stages_ui()
        self._notify_stage_changed()
        logger.debug(f"Deleted stage with time value {time_value}")

    def _on_time_unit_changed(self, new_unit: str) -> None:
        """時間単位変更時の処理"""
        logger.debug(f"Time unit changed to {new_unit}")
        self._time_unit = new_unit
        # 既存のステージの時間単位を更新
        for stage in self._stages:
            stage["time_unit"] = new_unit
        self._update_stages_ui()
        self._notify_stage_changed()

    def get_current_stage(self) -> List[Dict]:
        """現在のステージデータを取得"""
        return [
            {
                "time_value": stage["time_value"],
                "time_unit": stage["time_unit"],
                "data": stage["data"]
            }
            for stage in self._stages
        ]

    def _notify_stage_changed(self) -> None:
        """ステージ変更通知"""
        if hasattr(self, 'on_stage_changed'):
            self.on_stage_changed(self.get_current_stage())
        logger.debug("Stage change notification sent")

