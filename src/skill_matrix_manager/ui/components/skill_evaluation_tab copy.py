import os
import plotly.graph_objects as go
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QGroupBox, QFormLayout, 
    QLabel, QGridLayout, QComboBox, QHBoxLayout, QSpacerItem, QSizePolicy
)
from PyQt5.QtCore import QUrl, Qt, pyqtSignal
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtGui import QFont
import tempfile
from datetime import datetime

class SkillEvaluationTab(QWidget):
    skill_updated = pyqtSignal(str, str, int)  # member_id, skill_id, score

    def __init__(self, category_name, skills, parent=None):
        super().__init__(parent)
        self.category_name = category_name
        self.skills = skills
        self.current_values = [1] * len(skills)
        self.target_values = [5] * len(skills)
        self.skill_combos = []
        self.target_combos = []
        self.temp_files = []
        self.is_dark_mode = True
        self.current_member_id = None
        self.current_member_name = None
        self.current_member_group = None
        self.evaluations = {}  # {member_id: {skill_id: score}}
        self.last_update_time = "2025-02-21 13:31:28"
        self.current_user = "GingaDza"
        
        # 既存の色設定はそのまま維持
        self.dark_colors = {
            'current': {
                'line': 'rgb(189, 147, 249)',
                'fill': 'rgba(189, 147, 249, 0.3)',
                'text': '現在のスキル (1-5)'
            },
            'target': {
                'line': 'rgb(255, 184, 108)',
                'fill': 'rgba(255, 184, 108, 0.1)',
                'text': '目標スキル (1-5)'
            },
            'background': 'rgb(40, 42, 54)',
            'grid': 'rgb(68, 71, 90)',
            'text': 'rgb(248, 248, 242)',
            'paper_bg': 'rgb(40, 42, 54)',
            'plot_bg': 'rgb(40, 42, 54)'
        }

        self.light_colors = {
            'current': {
                'line': 'rgb(147, 112, 219)',
                'fill': 'rgba(147, 112, 219, 0.3)',
                'text': '現在のスキル (1-5)'
            },
            'target': {
                'line': 'rgb(251, 140, 0)',
                'fill': 'rgba(251, 140, 0, 0.1)',
                'text': '目標スキル (1-5)'
            },
            'background': 'rgb(255, 255, 255)',
            'grid': 'rgb(238, 238, 238)',
            'text': 'rgb(60, 64, 67)',
            'paper_bg': 'rgb(255, 255, 255)',
            'plot_bg': 'rgb(255, 255, 255)'
        }
        
        self.colors = self.dark_colors if self.is_dark_mode else self.light_colors
        
        # スタイルシートは既存のものを維持
        self.setStyleSheet("""
            QWidget {
                background-color: rgb(40, 42, 54);
                color: rgb(248, 248, 242);
            }
            QGroupBox {
                margin-top: 1.2em;
                border: 1px solid rgb(68, 71, 90);
                border-radius: 4px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 7px;
                padding: 0 5px;
                background-color: rgb(40, 42, 54);
                color: rgb(248, 248, 242);
            }
            QComboBox {
                background-color: rgb(68, 71, 90);
                border: 1px solid rgb(98, 114, 164);
                border-radius: 4px;
                padding: 2px;
                color: rgb(248, 248, 242);
            }
            QComboBox::drop-down {
                border: none;
            }
            QComboBox::down-arrow {
                image: none;
            }
        """)
        
        self._setup_ui()

    def set_member(self, member_id, member_name, member_group):
        """メンバーが選択された時の処理"""
        self.current_member_id = member_id
        self.current_member_name = member_name
        self.current_member_group = member_group
        
        # ユーザー情報の更新
        self.user_info_group.setTitle(f"評価対象: {member_name}")
        self.user_name_label.setText(f"メンバー: {member_name} ({member_group})")
        self.date_label.setText(f"最終更新: {self.last_update_time}")
        
        # 保存済みの評価を読み込む
        self.load_member_evaluations()

    def load_member_evaluations(self):
        """メンバーの評価データを読み込む"""
        if not self.current_member_id:
            return

        member_evals = self.evaluations.get(self.current_member_id, {})
        for i, skill in enumerate(self.skills):
            score = member_evals.get(skill, 1)
            self.current_values[i] = score
            self.skill_combos[i].setCurrentText(str(score))

        self.update_chart()

    def on_skill_level_changed(self, index, value):
        """スキルレベルが変更された時の処理（自動保存含む）"""
        try:
            self.current_values[index] = int(value)
            
            # 自動保存の処理
            if self.current_member_id:
                skill_id = self.skills[index]
                score = int(value)
                
                if self.current_member_id not in self.evaluations:
                    self.evaluations[self.current_member_id] = {}
                
                self.evaluations[self.current_member_id][skill_id] = score
                
                # 保存時刻の更新
                self.last_update_time = "2025-02-21 13:31:28"
                self.date_label.setText(f"最終更新: {self.last_update_time}")
                
                # シグナル発信
                self.skill_updated.emit(self.current_member_id, skill_id, score)
            
            self.update_chart()
            
        except (ValueError, IndexError) as e:
            print(f"Error updating skill level: {e}")

    def _setup_ui(self):
        main_layout = QVBoxLayout()
        main_layout.setSpacing(10)
        
        # 上部コンテナ
        top_container = QWidget()
        top_layout = QHBoxLayout(top_container)
        top_layout.setSpacing(10)
        
        # ユーザー情報セクション
        self.user_info_group = QGroupBox("評価対象: 未選択")
        user_layout = QFormLayout()
        user_layout.setSpacing(10)
        user_layout.setContentsMargins(10, 15, 10, 10)
        
        self.user_name_label = QLabel("メンバー: 未選択")
        self.date_label = QLabel(f"最終更新: {self.last_update_time}")
        self.evaluator_label = QLabel(f"評価者: {self.current_user}")
        
        user_layout.addRow(self.user_name_label)
        user_layout.addRow(self.date_label)
        user_layout.addRow(self.evaluator_label)
        self.user_info_group.setLayout(user_layout)
        
        self.user_info_group.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Minimum)
        top_layout.addWidget(self.user_info_group)
        
        # 既存のUI部分はそのまま維持...
        # (スキル評価セクション、チャートなどの実装は変更なし)

        self.setLayout(main_layout)
        self.update_chart()

    # その他の既存メソッド（create_radar_chart, update_chart, closeEvent など）は
    # そのまま維持
