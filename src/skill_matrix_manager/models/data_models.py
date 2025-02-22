from dataclasses import dataclass, field
from typing import List, Optional, Dict
from enum import Enum
from datetime import datetime, UTC

class SkillLevel(Enum):
    """スキルレベルの定義"""
    NONE = 0
    BASIC = 1
    INTERMEDIATE = 2
    ADVANCED = 3
    EXPERT = 4
    MASTER = 5

@dataclass
class Skill:
    """スキルモデル"""
    id: int
    name: str
    category_id: Optional[int] = None  # カテゴリーIDをオプショナルに変更
    description: Optional[str] = None
    required_level: SkillLevel = SkillLevel.NONE
    max_level: SkillLevel = SkillLevel.MASTER

@dataclass
class Category:
    """カテゴリーモデル"""
    id: int
    name: str
    description: Optional[str] = None
    parent_id: Optional[int] = None
    skills: List[Skill] = field(default_factory=list)

    def add_skill(self, skill: Skill) -> None:
        """スキルをカテゴリーに追加"""
        skill.category_id = self.id
        self.skills.append(skill)

@dataclass
class Group:
    """グループモデル"""
    id: int
    name: str
    description: Optional[str] = None
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))
    users: List['User'] = field(default_factory=list)

@dataclass
class User:
    """ユーザーモデル"""
    id: int
    name: str
    email: str
    group_id: Optional[int] = None
    skills: Dict[int, SkillLevel] = field(default_factory=dict)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

@dataclass
class TargetSkillLevel:
    """目標スキルレベルモデル"""
    skill_id: int
    target_level: SkillLevel
    group_id: Optional[int] = None
    user_id: Optional[int] = None
    deadline: Optional[datetime] = None
