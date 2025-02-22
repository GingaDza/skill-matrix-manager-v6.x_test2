from PyQt5.QtWidgets import QWidget, QTabWidget, QVBoxLayout
from .initial_setup_tab import InitialSetupTab
from .data_io_tab import DataIOTab
from .system_info_tab import SystemInfoTab

class SystemManagementTab(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout(self)
        
        # サブタブウィジェット
        self.sub_tab_widget = QTabWidget()
        
        # 初期設定タブ
        self.initial_setup_tab = InitialSetupTab(self)
        self.sub_tab_widget.addTab(self.initial_setup_tab, "初期設定")
        
        # データ入出力タブ
        self.data_io_tab = DataIOTab(self)
        self.sub_tab_widget.addTab(self.data_io_tab, "データ入出力")
        
        # システム情報タブ
        self.system_info_tab = SystemInfoTab(self)
        self.sub_tab_widget.addTab(self.system_info_tab, "システム情報")
        
        layout.addWidget(self.sub_tab_widget)
