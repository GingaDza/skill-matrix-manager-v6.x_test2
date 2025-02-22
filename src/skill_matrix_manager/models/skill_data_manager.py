from typing import Dict, Optional
from PyQt5.QtCore import QObject, pyqtSignal

class SkillDataManager(QObject):
    # スキルデータが変更された時のシグナル
    skill_data_changed = pyqtSignal(dict)
    
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(SkillDataManager, cls).__new__(cls)
            # 初期化
            cls._instance.skill_hierarchy = {}
        return cls._instance

    def __init__(self):
        if not hasattr(self, '_initialized'):
            super().__init__()
            self._initialized = True
            self.skill_hierarchy: Dict[str, Dict[str, Dict[str, str]]] = {}

    def set_skill_hierarchy(self, hierarchy: Dict[str, Dict[str, Dict[str, str]]]) -> None:
        """スキル階層構造の設定"""
        self.skill_hierarchy = hierarchy.copy()
        # 変更を通知
        self.skill_data_changed.emit(self.skill_hierarchy)

    def get_skill_hierarchy(self) -> Dict[str, Dict[str, Dict[str, str]]]:
        """スキル階層構造の取得"""
        return self.skill_hierarchy.copy()
