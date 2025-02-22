from PyQt5.QtWidgets import QWidget
from PyQt5.QtCore import QEvent
from functools import wraps
from .ui_monitor import UIMonitor

def protect_ui(func):
    """UIの変更を監視・保護するデコレータ"""
    @wraps(func)
    def wrapper(self, *args, **kwargs):
        result = func(self, *args, **kwargs)
        # UI設定後に状態を保存
        self._original_state = self._capture_ui_state()
        return result
    return wrapper

class FrozenWidget(QWidget):
    """UI変更を防止・監視する基底クラス"""
    def __init__(self, parent=None):
        super().__init__(parent)
        self._original_state = None
        self._ui_monitor = UIMonitor(self)
        self.installEventFilter(self._ui_monitor)

    def _capture_ui_state(self):
        """UIの状態をキャプチャ"""
        return {
            'widget_count': len(self.findChildren(QWidget)),
            'layout_type': type(self.layout()) if self.layout() else None,
            'geometry': self.geometry().getRect()
        }

    def _verify_ui_integrity(self):
        """UI構造の整合性を検証"""
        if not self._original_state:
            return True

        current_state = self._capture_ui_state()
        return (
            current_state['widget_count'] == self._original_state['widget_count'] and
            current_state['layout_type'] == self._original_state['layout_type'] and
            current_state['geometry'] == self._original_state['geometry']
        )

    def check_ui_state(self):
        """UIの状態をチェック"""
        if not self._verify_ui_integrity():
            raise RuntimeError("UIの不正な変更が検出されました")

    def event(self, event):
        """イベント処理をオーバーライド"""
        if event.type() in [QEvent.Resize, QEvent.Move]:
            self.check_ui_state()
        return super().event(event)
