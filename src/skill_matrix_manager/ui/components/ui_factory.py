from PyQt5.QtWidgets import QWidget, QTabWidget
from typing import Optional

class UIComponentFactory:
    @staticmethod
    def create_tab(tab_type: str, parent: Optional[QWidget] = None) -> QTabWidget:
        tab = QTabWidget(parent)
        # タブの設定はオリジナルを維持
        return tab

    @staticmethod
    def create_panel(panel_type: str, parent: Optional[QWidget] = None) -> QWidget:
        panel = QWidget(parent)
        # パネルの設定はオリジナルを維持
        return panel
