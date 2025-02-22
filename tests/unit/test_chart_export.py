import pytest
import os
import json
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import QSize
from skill_matrix_manager.utils.chart_utils import RadarChartWidget
from skill_matrix_manager.utils.chart_export import ChartExporter

@pytest.fixture
def app():
    return QApplication([])

@pytest.fixture
def chart_widget(app):
    widget = RadarChartWidget()
    widget.resize(400, 400)
    test_data = [3, 4, 2, 5, 1]
    test_labels = ["Python", "Java", "C++", "JavaScript", "Go"]
    widget.set_data(test_data, test_labels)
    return widget

@pytest.fixture
def exporter(chart_widget):
    return ChartExporter(chart_widget)

def test_export_as_image(tmp_path, exporter, monkeypatch):
    # exportsディレクトリをtmp_pathに変更
    monkeypatch.setattr(exporter, 'export_dir', tmp_path)
    
    filename = "test_chart.png"
    filepath = exporter.export_as_image(filename)
    assert filepath is not None
    assert os.path.exists(filepath)
    assert filepath.endswith(".png")
    assert os.path.getsize(filepath) > 0

def test_export_as_pdf(tmp_path, exporter, monkeypatch):
    # exportsディレクトリをtmp_pathに変更
    monkeypatch.setattr(exporter, 'export_dir', tmp_path)
    
    filename = "test_chart.pdf"
    filepath = exporter.export_as_pdf(filename)
    assert filepath is not None
    assert os.path.exists(filepath)
    assert filepath.endswith(".pdf")
    assert os.path.getsize(filepath) > 0

def test_export_data_as_json(tmp_path, exporter, monkeypatch):
    # exportsディレクトリをtmp_pathに変更
    monkeypatch.setattr(exporter, 'export_dir', tmp_path)
    
    data = {
        "labels": ["Python", "Java", "C++", "JavaScript", "Go"],
        "data": [3, 4, 2, 5, 1],
        "target_data": None
    }
    filename = "test_data.json"
    filepath = exporter.export_data_as_json(data, filename)
    assert filepath is not None
    assert os.path.exists(filepath)
    assert filepath.endswith(".json")
    
    # JSONファイルの内容を検証
    with open(filepath, 'r', encoding='utf-8') as f:
        saved_data = json.load(f)
        assert saved_data == data

