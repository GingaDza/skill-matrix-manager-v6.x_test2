from datetime import datetime
from typing import List, Dict, Optional
import sqlite3
import os
from ..models.data_models import SkillLevel, User

class SkillLevelRepository:
    def __init__(self, db_path: str = "skill_matrix.db"):
        self.db_path = db_path
        self._ensure_tables()

    def _ensure_tables(self):
        try:
            migration_path = os.path.join(
                os.path.dirname(__file__),
                '..',
                'migrations',
                '002_create_skill_levels.sql'
            )
            with open(migration_path, 'r') as f:
                sql = f.read()
                with sqlite3.connect(self.db_path) as conn:
                    conn.executescript(sql)
        except Exception as e:
            print(f"Error ensuring tables: {e}")

    def get_user_skill_levels(self, user_id: str) -> Dict[str, SkillLevel]:
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    SELECT skill_id, level, updated_at
                    FROM skill_levels
                    WHERE user_id = ?
                """, (user_id,))
                
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

    def get_group_skill_levels(self, group_id: str) -> Dict[str, List[SkillLevel]]:
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    SELECT sl.skill_id, sl.level, sl.updated_at
                    FROM skill_levels sl
                    JOIN users u ON u.id = sl.user_id
                    WHERE u.group_id = ?
                """, (group_id,))
                
                result: Dict[str, List[SkillLevel]] = {}
                for row in cursor.fetchall():
                    skill_id = row[0]
                    if skill_id not in result:
                        result[skill_id] = []
                    
                    result[skill_id].append(
                        SkillLevel(
                            skill_id=skill_id,
                            level=row[1],
                            updated_at=datetime.fromisoformat(row[2])
                        )
                    )
                return result
        except Exception as e:
            print(f"Error getting group skill levels: {e}")
            return {}
