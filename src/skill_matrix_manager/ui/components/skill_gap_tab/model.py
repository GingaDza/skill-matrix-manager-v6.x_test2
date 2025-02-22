from typing import Dict, Optional

class SkillGapModel:
    def __init__(self):
        self._skill_hierarchy: Dict[str, Dict[str, Dict[str, str]]] = {}  # {group: {category: {skill_name: level}}}
        self._target_values: Dict[str, Dict[str, Dict[str, int]]] = {}  # {group: {category: {skill_name: target_value}}}
        self._user_values: Dict[str, Dict[str, Dict[str, int]]] = {}  # {group: {category: {skill_name: user_value}}}
        self._progressive_targets: Dict[str, Dict[str, Dict[str, Dict[str, int]]]] = {}  # {time_key: {group: {category: {skill_name: target_value}}}}
        self._time_unit: str = "時間"

    @property
    def skill_hierarchy(self) -> Dict[str, Dict[str, Dict[str, str]]]:
        return self._skill_hierarchy.copy()

    @property
    def target_values(self) -> Dict[str, Dict[str, Dict[str, int]]]:
        return self._target_values.copy()

    @property
    def user_values(self) -> Dict[str, Dict[str, Dict[str, int]]]:
        return self._user_values.copy()

    @property
    def progressive_targets(self) -> Dict[str, Dict[str, Dict[str, Dict[str, int]]]]:
        return {k: v.copy() for k, v in self._progressive_targets.items()}

    @property
    def time_unit(self) -> str:
        return self._time_unit

    def set_skill_hierarchy(self, hierarchy: Dict[str, Dict[str, Dict[str, str]]]) -> None:
        """スキル階層構造の設定"""
        self._skill_hierarchy = hierarchy.copy()
        # 新しい階層構造に基づいて、ターゲット値と現在値を初期化
        self._initialize_values()

    def _initialize_values(self) -> None:
        """値の初期化"""
        self._target_values = {}
        self._user_values = {}
        for group, categories in self._skill_hierarchy.items():
            self._target_values[group] = {}
            self._user_values[group] = {}
            for category, skills in categories.items():
                self._target_values[group][category] = {skill: 1 for skill in skills.keys()}
                self._user_values[group][category] = {skill: 1 for skill in skills.keys()}

    def set_target(self, group: str, category: str, skill_name: str, value: int) -> None:
        """目標値の設定"""
        if not 1 <= value <= 5:
            raise ValueError("Target value must be between 1 and 5")
        if group not in self._target_values:
            self._target_values[group] = {}
        if category not in self._target_values[group]:
            self._target_values[group][category] = {}
        self._target_values[group][category][skill_name] = value

    def set_user_value(self, group: str, category: str, skill_name: str, value: int) -> None:
        """現在値の設定"""
        if not 1 <= value <= 5:
            raise ValueError("User value must be between 1 and 5")
        if group not in self._user_values:
            self._user_values[group] = {}
        if category not in self._user_values[group]:
            self._user_values[group][category] = {}
        self._user_values[group][category][skill_name] = value

    def get_target(self, group: str, category: str, skill_name: str) -> int:
        """目標値の取得"""
        try:
            return self._target_values[group][category][skill_name]
        except KeyError:
            return 1

    def get_user_value(self, group: str, category: str, skill_name: str) -> int:
        """現在値の取得"""
        try:
            return self._user_values[group][category][skill_name]
        except KeyError:
            return 1

    def set_time_unit(self, unit: str) -> None:
        """時間単位の設定"""
        if unit not in ["時間", "日", "月", "年"]:
            raise ValueError("Invalid time unit")
        self._time_unit = unit

    def set_progressive_target(self, time_key: str, targets: Dict[str, Dict[str, Dict[str, int]]]) -> None:
        """段階的目標の設定"""
        self._progressive_targets[time_key] = targets.copy()

    def get_all_skills(self) -> Dict[str, Dict[str, Dict[str, str]]]:
        """全スキルの取得"""
        return self.skill_hierarchy

    def get_categories_for_group(self, group: str) -> Dict[str, Dict[str, str]]:
        """グループ内のカテゴリー一覧を取得"""
        return self._skill_hierarchy.get(group, {}).copy()

    def get_skills_for_category(self, group: str, category: str) -> Dict[str, str]:
        """カテゴリー内のスキル一覧を取得"""
        return self._skill_hierarchy.get(group, {}).get(category, {}).copy()
