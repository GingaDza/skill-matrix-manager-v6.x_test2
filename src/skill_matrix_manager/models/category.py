from dataclasses import dataclass
from typing import List, Optional
from .base import BaseModel
from .skill import Skill

@dataclass
class Category(BaseModel):
    """カテゴリーモデル"""
    id: int
    name: str
    description: Optional[str] = None
    parent_id: Optional[int] = None
    skills: List[Skill] = None

    def __post_init__(self):
        self.skills = self.skills or []
