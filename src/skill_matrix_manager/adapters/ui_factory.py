from typing import Type, Dict, Any
from PyQt5.QtWidgets import QWidget
from .ui_protection import UIProtectionAdapter
from .ui_validator import UIValidator

class UIFactory:
    """保護されたUIウィジェットを生成するファクトリー"""
    def __init__(self):
        self._protectors: Dict[str, UIProtectionAdapter] = {}
        self._validator = UIValidator()

    def create_protected_widget(
        self, 
        widget_class: Type[QWidget], 
        parent: QWidget = None,
        **kwargs
    ) -> QWidget:
        """保護されたウィジェットを生成"""
        widget = widget_class(parent, **kwargs)
        
        # プロテクターが存在しない場合は作成
        class_name = widget_class.__name__
        if class_name not in self._protectors:
            self._protectors[class_name] = UIProtectionAdapter(widget_class)
        
        # 構造を凍結
        protector = self._protectors[class_name]
        protector.freeze_structure(widget)
        
        return widget

    def verify_widget(self, widget: QWidget) -> bool:
        """ウィジェットの整合性を検証"""
        class_name = widget.__class__.__name__
        if class_name not in self._protectors:
            return False
        
        return self._protectors[class_name].verify_structure(widget)

    def restore_widget(self, widget: QWidget) -> None:
        """ウィジェットを元の状態に復元"""
        class_name = widget.__class__.__name__
        if class_name not in self._protectors:
            raise RuntimeError(f"プロテクターが存在しません: {class_name}")
        
        self._protectors[class_name].restore_structure(widget)
