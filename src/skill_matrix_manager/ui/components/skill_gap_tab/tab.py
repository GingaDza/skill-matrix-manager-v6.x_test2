from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QScrollArea
from typing import Dict, List
from skill_matrix_manager.utils.debug_logger import DebugLogger
from skill_matrix_manager.models.skill_data_manager import SkillDataManager
from .chart_widget import RadarChartWidget
from .progressive_target_widget import ProgressiveTargetWidget

logger = DebugLogger.get_logger()

class SkillGapTab(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        # SkillDataManagerのインスタンスを取得
        self._skill_manager = SkillDataManager()
        self._skill_hierarchy = {}
        
        logger.debug("Initializing SkillGapTab")
        self._setup_ui()
        
        # スキルデータの変更を監視
        self._skill_manager.skill_data_changed.connect(self._on_skill_data_changed)
        
        # 現在のスキルデータを取得
        self._skill_hierarchy = self._skill_manager.get_skill_hierarchy()
        if self._skill_hierarchy:
            self.set_skills(self._skill_hierarchy)

    def _setup_ui(self):
        """UIのセットアップ"""
        logger.debug("Setting up SkillGapTab UI")
        main_layout = QVBoxLayout()
        main_layout.setSpacing(10)

        # チャート表示（上部）
        self.chart_widget = RadarChartWidget("段階的目標レベル")
        main_layout.addWidget(self.chart_widget)

        # スクロール可能な目標設定エリア（下部）
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_content = QWidget()
        scroll_layout = QVBoxLayout(scroll_content)

        # 段階的目標設定ウィジェット
        self.progressive_widget = ProgressiveTargetWidget(self)
        self.progressive_widget.on_stage_changed = self._on_stage_changed
        scroll_layout.addWidget(self.progressive_widget)
        
        # 余白を追加
        scroll_layout.addStretch()
        
        scroll_area.setWidget(scroll_content)
        # スクロールエリアの高さを制限
        scroll_area.setMinimumHeight(200)
        scroll_area.setMaximumHeight(300)
        
        main_layout.addWidget(scroll_area)

        self.setLayout(main_layout)

    def _on_skill_data_changed(self, new_hierarchy: Dict[str, Dict[str, Dict[str, str]]]):
        """スキルデータが変更された時の処理"""
        logger.debug("Skill data changed, updating view")
        self._skill_hierarchy = new_hierarchy
        self.set_skills(new_hierarchy)

    def set_skills(self, skill_hierarchy: Dict[str, Dict[str, Dict[str, str]]]) -> None:
        """スキル階層構造の更新"""
        logger.debug(f"Setting skill hierarchy: {skill_hierarchy}")
        self._skill_hierarchy = skill_hierarchy
        self.progressive_widget.set_skill_hierarchy(skill_hierarchy)
        self._update_chart()

    def _on_stage_changed(self, stages: List[Dict]) -> None:
        """ステージが変更された時の処理"""
        logger.debug(f"Stage changed: {stages}")
        self._update_chart()

    def _get_current_levels(self) -> Dict[str, Dict[str, Dict[str, int]]]:
        """現在のスキルレベルを取得"""
        current_levels = {}
        for group, categories in self._skill_hierarchy.items():
            current_levels[group] = {}
            for category, skills in categories.items():
                current_levels[group][category] = {
                    skill: 1 for skill in skills.keys()
                }
        return current_levels

    def _flatten_skill_data(self, data: Dict[str, Dict[str, Dict[str, int]]]) -> Dict[str, int]:
        """階層構造のスキルデータをフラット化"""
        flattened = {}
        for group in data:
            for category in data[group]:
                for skill, level in data[group][category].items():
                    flattened[f"{group}-{category}-{skill}"] = level
        return flattened

    def _update_chart(self) -> None:
        """チャートの更新"""
        if not self._skill_hierarchy:
            logger.debug("No skill hierarchy data available")
            return

        # 現在値を取得（すべて1で初期化）
        current_values = self._get_current_levels()
        
        # ステージのスキル値を取得
        stages = self.progressive_widget.get_current_stage()
        logger.debug(f"Updating chart with {len(stages)} stages")

        # チャートカテゴリの準備（全スキルのフルパス）
        all_skills = []
        for group in self._skill_hierarchy:
            for category in self._skill_hierarchy[group]:
                for skill in self._skill_hierarchy[group][category]:
                    all_skills.append(f"{group}-{category}-{skill}")

        # 現在値をフラット化
        current_flat = self._flatten_skill_data(current_values)
        
        # ステージデータの準備
        stage_data = []
        for stage in stages:
            flattened = self._flatten_skill_data(stage["data"])
            stage_data.append({
                "time": f"{stage['time_value']}{stage['time_unit']}",
                "values": [flattened.get(skill, 1) for skill in all_skills]
            })

        # チャートの更新
        self.chart_widget.update_progressive_chart(
            categories=all_skills,
            current_values=[current_flat.get(skill, 1) for skill in all_skills],
            stages=stage_data
        )
        
        logger.debug("Chart updated")

