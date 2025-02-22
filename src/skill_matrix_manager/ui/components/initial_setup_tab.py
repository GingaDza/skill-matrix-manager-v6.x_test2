from PyQt5.QtWidgets import QWidget
from .initial_setup.base import InitialSetupBase
from .initial_setup.category_handlers import CategoryHandlers
from .initial_setup.data_handlers import DataHandlers
from .initial_setup.group_handlers import GroupHandlers
from .initial_setup.ui_components import UIComponents

class InitialSetupTab(InitialSetupBase, CategoryHandlers, DataHandlers, GroupHandlers):
    def __init__(self, parent=None):
        self.parent = parent  # MainWindowへの参照を保持
        super().__init__(parent)

    def setup_ui(self):
        """UIの初期化"""
        # 親クラス（InitialSetupBase）のsetup_uiを呼び出す
        super().setup_ui()
