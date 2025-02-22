import sqlite3
from typing import List, Tuple
import os
import re

class MigrationManager:
    """データベースマイグレーションを管理するクラス"""
    
    def __init__(self, db_path: str, migrations_dir: str):
        self.db_path = db_path
        self.migrations_dir = migrations_dir
        
    def get_applied_migrations(self) -> List[str]:
        """適用済みマイグレーションの取得"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # マイグレーション管理テーブルの作成
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS migrations (
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                applied_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        cursor.execute("SELECT name FROM migrations ORDER BY id")
        return [row[0] for row in cursor.fetchall()]
        
    def get_pending_migrations(self) -> List[Tuple[str, str]]:
        """未適用のマイグレーションを取得"""
        applied = set(self.get_applied_migrations())
        pending = []
        
        for filename in sorted(os.listdir(self.migrations_dir)):
            if filename.endswith('.sql'):
                name = os.path.splitext(filename)[0]
                if name not in applied:
                    with open(os.path.join(self.migrations_dir, filename)) as f:
                        pending.append((name, f.read()))
                        
        return pending
        
    def apply_migrations(self) -> None:
        """未適用のマイグレーションを実行"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        for name, sql in self.get_pending_migrations():
            cursor.execute(sql)
            cursor.execute("INSERT INTO migrations (name) VALUES (?)", (name,))
            
        conn.commit()