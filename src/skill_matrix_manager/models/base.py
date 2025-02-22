from typing import Any, Dict
from dataclasses import dataclass, asdict
import json

@dataclass
class BaseModel:
    """全モデルの基底クラス"""
    def to_dict(self) -> Dict[str, Any]:
        """モデルを辞書に変換"""
        return asdict(self)

    def to_json(self) -> str:
        """モデルをJSON文字列に変換"""
        return json.dumps(self.to_dict(), ensure_ascii=False)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'BaseModel':
        """辞書からモデルを生成"""
        return cls(**data)

    @classmethod
    def from_json(cls, json_str: str) -> 'BaseModel':
        """JSON文字列からモデルを生成"""
        return cls.from_dict(json.loads(json_str))
