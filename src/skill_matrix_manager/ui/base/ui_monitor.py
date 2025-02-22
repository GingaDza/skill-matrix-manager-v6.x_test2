from PyQt5.QtCore import QObject, QEvent
import logging
import datetime

# ロギングの設定
logging.basicConfig(
    filename='ui_changes.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

class UIMonitor(QObject):
    """UIの変更を監視するイベントフィルター"""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.original_state = {}
        self.last_check = datetime.datetime.now(datetime.UTC)  # utcnowの代わりにUTCを使用

    def eventFilter(self, obj, event):
        """イベントをフィルタリングし、UI変更を検出"""
        if event.type() in [QEvent.Move, QEvent.Resize, QEvent.ChildAdded, QEvent.ChildRemoved]:
            current_time = datetime.datetime.now(datetime.UTC)
            if (current_time - self.last_check).total_seconds() >= 1:  # 1秒間隔でチェック
                self.check_ui_changes(obj)
                self.last_check = current_time

        return super().eventFilter(obj, event)

    def check_ui_changes(self, widget):
        """ウィジェットの状態変更を確認"""
        current_state = self.capture_widget_state(widget)
        widget_id = id(widget)

        if widget_id in self.original_state:
            if self.original_state[widget_id] != current_state:
                self.log_ui_change(widget, self.original_state[widget_id], current_state)
        else:
            self.original_state[widget_id] = current_state

    def capture_widget_state(self, widget):
        """ウィジェットの現在の状態を取得"""
        return {
            'geometry': widget.geometry().getRect(),
            'visible': widget.isVisible(),
            'enabled': widget.isEnabled(),
            'style_sheet': widget.styleSheet(),
            'children_count': len(widget.findChildren(QObject))
        }

    def log_ui_change(self, widget, old_state, new_state):
        """UI変更をログに記録"""
        changes = []
        for key in old_state:
            if old_state[key] != new_state[key]:
                changes.append(f"{key}: {old_state[key]} -> {new_state[key]}")

        if changes:
            widget_info = f"{widget.__class__.__name__}({widget.objectName() or 'unnamed'})"
            logging.info(f"UI変更検出: {widget_info}\n" + "\n".join(changes))
