import pytest
from PyQt5.QtWidgets import QApplication, QTabWidget, QComboBox, QSpinBox
from skill_matrix_manager.adapters.skill_analysis_adapter import SkillAnalysisAdapter
from skill_matrix_manager.utils.chart_utils import RadarChartWidget

@pytest.fixture
def app():
    return QApplication([])

@pytest.fixture
def adapter():
    return SkillAnalysisAdapter()

def test_create_skill_analysis_tab(app, adapter):
    tab = adapter.create_skill_analysis_tab()
    assert isinstance(tab, QTabWidget)
    assert tab.count() == 2
    assert tab.tabText(0) == "総合評価"
    assert tab.tabText(1) == "スキルギャップ"

def test_create_overview_tab(app, adapter):
    tab = adapter.create_overview_tab()
    
    # グループ選択の確認
    group_combo = tab.findChild(QComboBox)
    assert group_combo is not None
    
    # レーダーチャートの確認
    radar_chart = tab.findChild(RadarChartWidget)
    assert radar_chart is not None

def test_create_skill_gap_tab(app, adapter):
    tab = adapter.create_skill_gap_tab()
    
    # コンボボックスの確認
    combos = tab.findChildren(QComboBox)
    assert len(combos) == 3  # グループ、ユーザー、時間単位
    
    # スピンボックスの確認
    spins = tab.findChildren(QSpinBox)
    assert len(spins) == 2  # 時間値、目標レベル
    
    # レーダーチャートの確認
    radar_chart = tab.findChild(RadarChartWidget)
    assert radar_chart is not None
    assert radar_chart.dual_chart == True

