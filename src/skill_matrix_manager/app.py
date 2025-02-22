import sys
from PyQt5.QtWidgets import QApplication
from skill_matrix_manager.ui.main_window import MainWindow

def main():
    """アプリケーションのメインエントリーポイント"""
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
