from dataclasses import dataclass
from typing import Optional
from .base import BaseModel

@dataclass
class Skill(BaseModel):
    """スキルモデル"""
    id: int
    name: str
    category_id: int
    description: Optional[str] = None
    required_level: int = 0
    max_level: int = 5
