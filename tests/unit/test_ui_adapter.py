import pytest
from PyQt5.QtWidgets import QApplication, QWidget
from skill_matrix_manager.adapters.original_ui_adapter import OriginalUIAdapter

@pytest.fixture
def app():
    return QApplication([])

@pytest.fixture
def parent_widget(app):
    return QWidget()

def test_ui_adapter_initialization(parent_widget):
    adapter = OriginalUIAdapter(parent_widget)
    assert adapter.parent == parent_widget
    assert isinstance(adapter.config, dict)
    assert 'window_size' in adapter.config
    assert 'split_ratio' in adapter.config
    assert 'tab_order' in adapter.config

def test_create_main_layout(parent_widget):
    adapter = OriginalUIAdapter(parent_widget)
    layout = adapter.create_main_layout()
    assert layout is not None
