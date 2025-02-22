from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QComboBox,
    QLabel, QSpinBox, QPushButton, QGridLayout, QMessageBox
)
from PyQt5.QtCore import Qt, pyqtSlot
from datetime import datetime
from ..utils.chart_utils import RadarChartWidget
from ..repositories.skill_target_repository import SkillTargetRepository
from ..repositories.skill_level_repository import SkillLevelRepository
from ..repositories.group_user_repository import GroupUserRepository
from ..models.data_models import TargetSkillLevel, SkillLevel

class SkillGapTab(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.target_repository = SkillTargetRepository()
        self.level_repository = SkillLevelRepository()
        self.group_user_repository = GroupUserRepository()
        self._setup_ui()
        self._connect_signals()
        self._load_initial_data()

    def _setup_ui(self):
        main_layout = QVBoxLayout(self)

        # 選択パネル
        selection_panel = QWidget()
        selection_layout = QGridLayout(selection_panel)

        # グループ選択
        selection_layout.addWidget(QLabel("グループ:"), 0, 0)
        self.group_combo = QComboBox()
        selection_layout.addWidget(self.group_combo, 0, 1)

        # ユーザー選択
        selection_layout.addWidget(QLabel("ユーザー:"), 0, 2)
        self.user_combo = QComboBox()
        self.user_combo.addItem("グループ全体", None)  # デフォルトオプション
        selection_layout.addWidget(self.user_combo, 0, 3)

        main_layout.addWidget(selection_panel)

        # 目標設定パネル
        target_panel = QWidget()
        target_layout = QGridLayout(target_panel)

        # 時間設定
        target_layout.addWidget(QLabel("目標達成時間:"), 0, 0)
        self.time_value = QSpinBox()
        self.time_value.setRange(1, 1000)
        target_layout.addWidget(self.time_value, 0, 1)

        self.time_unit = QComboBox()
        self.time_unit.addItems(["時間", "日", "月", "年"])
        target_layout.addWidget(self.time_unit, 0, 2)

        # 目標レベル設定
        target_layout.addWidget(QLabel("目標レベル:"), 1, 0)
        self.target_level = QSpinBox()
        self.target_level.setRange(1, 5)
        target_layout.addWidget(self.target_level, 1, 1)

        # 設定ボタン
        self.set_target_btn = QPushButton("目標を設定")
        target_layout.addWidget(self.set_target_btn, 1, 2)

        main_layout.addWidget(target_panel)

        # レーダーチャート
        self.chart = RadarChartWidget(dual_chart=True)
        main_layout.addWidget(self.chart)

        self.setLayout(main_layout)

    def _connect_signals(self):
        self.group_combo.currentIndexChanged.connect(self._on_group_changed)
        self.user_combo.currentIndexChanged.connect(self._update_chart)
        self.set_target_btn.clicked.connect(self._save_target)

    def _load_initial_data(self):
        # グループの読み込み
        groups = self.group_user_repository.get_groups()
        self.group_combo.clear()
        for group in groups:
            self.group_combo.addItem(group.name, group.id)

    @pyqtSlot(int)
    def _on_group_changed(self, index):
        if index < 0:
            return

        group_id = self.group_combo.currentData()
        
        # ユーザーリストの更新
        users = self.group_user_repository.get_users_by_group(group_id)
        self.user_combo.clear()
        self.user_combo.addItem("グループ全体", None)
        for user in users:
            self.user_combo.addItem(user.name, user.id)

        # チャートの更新
        self._update_chart()

    def _update_chart(self):
        group_id = self.group_combo.currentData()
        user_id = self.user_combo.currentData()

        targets = self.target_repository.get_targets_by_group(group_id)
        if not targets:
            return

        labels = [t.skill_id for t in targets]
        target_data = [t.level for t in targets]

        if user_id:
            # 個別ユーザーのスキルレベル
            skill_levels = self.level_repository.get_user_skill_levels(user_id)
            current_data = [
                skill_levels.get(skill_id, SkillLevel(skill_id, 1, datetime.now())).level 
                for skill_id in labels
            ]
        else:
            # グループ全体の平均スキルレベル
            group_levels = self.level_repository.get_group_skill_levels(group_id)
            current_data = [
                sum(sl.level for sl in group_levels.get(skill_id, [])) / len(group_levels.get(skill_id, [1]))
                if skill_id in group_levels else 1
                for skill_id in labels
            ]

        self.chart.set_data(current_data, labels, target_data)

    def _save_target(self):
        try:
            group_id = self.group_combo.currentData()
            if not group_id:
                QMessageBox.warning(self, "エラー", "グループを選択してください。")
                return

            target = TargetSkillLevel(
                skill_id=self.skill_id,
                category_id=self.category_id,
                group_id=group_id,
                level=self.target_level.value(),
                time_requirement=self.time_value.value(),
                time_unit=self.time_unit.currentText()
            )

            if self.target_repository.save_target(target):
                QMessageBox.information(self, "成功", "目標設定を保存しました。")
                self._update_chart()
            else:
                QMessageBox.warning(self, "エラー", "目標設定の保存に失敗しました。")

        except Exception as e:
            QMessageBox.critical(self, "エラー", f"予期せぬエラーが発生しました: {str(e)}")

