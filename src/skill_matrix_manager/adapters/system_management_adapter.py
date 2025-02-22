from .ui_adapter_interface import UIAdapterInterface
from PyQt5.QtWidgets import QWidget

class SystemManagementAdapter(UIAdapterInterface):
    def __init__(self, view: QWidget):
        super().__init__(view)
        self.setup_connections()

    def setup_connections(self):
        """システム管理タブのUI接続を設定"""
        pass

    def update_view(self):
        """システム管理タブのUI更新"""
        pass

