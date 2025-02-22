import pytest
from PyQt5.QtWidgets import QApplication, QComboBox, QSpinBox
from skill_matrix_manager.adapters.skill_gap_adapter import SkillGapTab
from skill_matrix_manager.utils.chart_utils import RadarChartWidget

@pytest.fixture
def app():
    return QApplication([])

@pytest.fixture
def gap_tab(app):
    return SkillGapTab()

def test_skill_gap_tab_creation(gap_tab):
    # コンボボックスの確認
    assert len(gap_tab.findChildren(QComboBox)) == 4  # グループ、ユーザー、カテゴリー、時間単位
    
    # スピンボックスの確認
    spinboxes = gap_tab.findChildren(QSpinBox)
    assert len(spinboxes) == 2  # 時間値、目標レベル
    
    time_value = gap_tab.time_value
    assert time_value.minimum() == 1
    assert time_value.maximum() == 1000
    
    target_level = gap_tab.target_level
    assert target_level.minimum() == 1
    assert target_level.maximum() == 5

    # レーダーチャートの確認
    chart = gap_tab.chart
    assert isinstance(chart, RadarChartWidget)
    assert chart.dual_chart == True  # 二重チャートの確認

