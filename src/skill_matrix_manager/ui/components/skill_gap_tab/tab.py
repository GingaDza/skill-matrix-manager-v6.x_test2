from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QScrollArea
from typing import Dict, List
from skill_matrix_manager.utils.debug_logger import DebugLogger
from .chart_widget import RadarChartWidget
from .progressive_target_widget import ProgressiveTargetWidget

logger = DebugLogger.get_logger()

class SkillGapTab(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        # 初期スキルデータ
        self._skills = {
            'Python': 'プログラミング言語',
            'SQL': 'データベース',
            'Git': 'バージョン管理',
            'Docker': 'コンテナ化',
            'AWS': 'クラウドプラットフォーム'
        }  
        self._current_skills = {name: 1 for name in self._skills.keys()}  # 現在のスキルレベル（すべて1）
        logger.debug("Initializing SkillGapTab")
        self._setup_ui()
        
        # 初期値を設定
        self.set_skills(self._skills)

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
        self.progressive_widget = ProgressiveTargetWidget(self)  # selfを渡してparentを設定
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

    def set_skills(self, skills: Dict[str, str]) -> None:
        """スキル一覧の更新"""
        logger.debug(f"Skills changed: {skills}")
        self._skills = skills
        self._current_skills = {name: 1 for name in skills.keys()}  # 現在のスキルレベルをリセット
        self.progressive_widget.set_skills(skills)
        self._update_chart()

    def _on_stage_changed(self, stages: List[Dict]) -> None:
        """ステージが変更された時の処理"""
        logger.debug(f"Stage changed: {stages}")
        self._update_chart()

    def _update_chart(self) -> None:
        """チャートの更新"""
        # スキル名のリストを作成（順序を保持）
        skill_names = list(self._skills.keys())
        logger.debug(f"Skill names for chart: {skill_names}")
        
        # 現在値を設定（すべて1）
        current_values = [self._current_skills[name] for name in skill_names]
        logger.debug(f"Current values for chart: {current_values}")
        
        # ステージのスキル値を取得
        stages = self.progressive_widget.get_current_stage()
        logger.debug(f"Stages for chart: {stages}")
        
        # チャートの更新
        self.chart_widget.update_progressive_chart(
            categories=skill_names,
            current_values=current_values,
            stages=stages
        )
        
        logger.debug(f"Chart updated with {len(stages)} stages")

