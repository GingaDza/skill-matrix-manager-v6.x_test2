import json
import sqlite3
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional
from ..models.data_models import (
    SkillLevel, Skill, Category, Group, User, TargetSkillLevel
)

class PersistenceManager:
    def __init__(self, db_path: str = "skill_matrix.db"):
        self.db_path = db_path
        self.initialize_database()

    def initialize_database(self):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            # グループテーブル
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS groups (
                    id TEXT PRIMARY KEY,
                    name TEXT NOT NULL,
                    description TEXT
                )
            """)
            
            # カテゴリーテーブル
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS categories (
                    id TEXT PRIMARY KEY,
                    name TEXT NOT NULL,
                    parent_id TEXT,
                    FOREIGN KEY (parent_id) REFERENCES categories (id)
                )
            """)
            
            # スキルテーブル
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS skills (
                    id TEXT PRIMARY KEY,
                    name TEXT NOT NULL,
                    category_id TEXT NOT NULL,
                    description TEXT,
                    FOREIGN KEY (category_id) REFERENCES categories (id)
                )
            """)
            
            # ユーザーテーブル
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    id TEXT PRIMARY KEY,
                    name TEXT NOT NULL,
                    group_id TEXT NOT NULL,
                    FOREIGN KEY (group_id) REFERENCES groups (id)
                )
            """)
            
            # スキルレベルテーブル
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS skill_levels (
                    user_id TEXT,
                    skill_id TEXT,
                    level INTEGER NOT NULL,
                    updated_at TIMESTAMP NOT NULL,
                    PRIMARY KEY (user_id, skill_id),
                    FOREIGN KEY (user_id) REFERENCES users (id),
                    FOREIGN KEY (skill_id) REFERENCES skills (id)
                )
            """)
            
            # 目標スキルレベルテーブル
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS target_skill_levels (
                    skill_id TEXT,
                    group_id TEXT,
                    level INTEGER NOT NULL,
                    time_requirement INTEGER NOT NULL,
                    time_unit TEXT NOT NULL,
                    PRIMARY KEY (skill_id, group_id),
                    FOREIGN KEY (skill_id) REFERENCES skills (id),
                    FOREIGN KEY (group_id) REFERENCES groups (id)
                )
            """)
            
            conn.commit()

    def save_group(self, group: Group) -> bool:
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute(
                    "INSERT OR REPLACE INTO groups (id, name, description) VALUES (?, ?, ?)",
                    (group.id, group.name, group.description)
                )
                return True
        except Exception as e:
            print(f"Error saving group: {e}")
            return False

    def get_group(self, group_id: str) -> Optional[Group]:
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT * FROM groups WHERE id = ?", (group_id,))
                row = cursor.fetchone()
                if row:
                    return Group(id=row[0], name=row[1], description=row[2])
                return None
        except Exception as e:
            print(f"Error getting group: {e}")
            return None

    def save_user_skill_level(self, user_id: str, skill_level: SkillLevel) -> bool:
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute(
                    """
                    INSERT OR REPLACE INTO skill_levels 
                    (user_id, skill_id, level, updated_at) 
                    VALUES (?, ?, ?, ?)
                    """,
                    (user_id, skill_level.skill_id, skill_level.level, 
                     skill_level.updated_at.isoformat())
                )
                return True
        except Exception as e:
            print(f"Error saving skill level: {e}")
            return False

    def get_user_skill_levels(self, user_id: str) -> Dict[str, SkillLevel]:
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute(
                    "SELECT skill_id, level, updated_at FROM skill_levels WHERE user_id = ?",
                    (user_id,)
                )
                return {
                    row[0]: SkillLevel(
                        skill_id=row[0],
                        level=row[1],
                        updated_at=datetime.fromisoformat(row[2])
                    )
                    for row in cursor.fetchall()
                }
        except Exception as e:
            print(f"Error getting skill levels: {e}")
            return {}

