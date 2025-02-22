from abc import ABC, abstractmethod
from typing import Generic, TypeVar, List, Optional, Dict, Any
from ..models.base import BaseModel
import sqlite3
import json

T = TypeVar('T', bound=BaseModel)

class BaseRepository(Generic[T], ABC):
    """基底リポジトリクラス"""
    
    def __init__(self, db_path: str):
        self.db_path = db_path
        
    def get_connection(self) -> sqlite3.Connection:
        """データベース接続を取得"""
        return sqlite3.connect(self.db_path)
        
    @abstractmethod
    def create_table(self) -> None:
        """テーブルの作成"""
        pass
        
    @abstractmethod
    def to_model(self, row: Dict[str, Any]) -> T:
        """データベースの行をモデルに変換"""
        pass
        
    def serialize(self, model: T) -> str:
        """モデルをJSON文字列に変換"""
        return json.dumps(model.to_dict())
        
    def deserialize(self, json_str: str) -> Dict[str, Any]:
        """JSON文字列をディクショナリに変換"""
        return json.loads(json_str)