from datetime import datetime
from typing import Optional, List, Dict
import sqlite3
import os
from ..models.data_models import TargetSkillLevel

class SkillTargetRepository:
    def __init__(self, db_path: str = "skill_matrix.db"):
        self.db_path = db_path
        self._ensure_tables()

    def _ensure_tables(self):
        try:
            migration_path = os.path.join(
                os.path.dirname(__file__),
                '..',
                'migrations',
                '001_create_skill_targets.sql'
            )
            with open(migration_path, 'r') as f:
                sql = f.read()
                with sqlite3.connect(self.db_path) as conn:
                    conn.executescript(sql)
        except Exception as e:
            print(f"Error ensuring tables: {e}")

    def save_target(self, target: TargetSkillLevel) -> bool:
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    INSERT OR REPLACE INTO skill_targets 
                    (group_id, category_id, skill_id, target_level, time_requirement, time_unit)
                    VALUES (?, ?, ?, ?, ?, ?)
                """, (
                    target.group_id,
                    target.category_id,
                    target.skill_id,
                    target.level,
                    target.time_requirement,
                    target.time_unit
                ))
                return True
        except Exception as e:
            print(f"Error saving target: {e}")
            return False

    def get_targets_by_group(self, group_id: str) -> List[TargetSkillLevel]:
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    SELECT skill_id, target_level, time_requirement, time_unit, category_id
                    FROM skill_targets
                    WHERE group_id = ?
                """, (group_id,))
                
                return [
                    TargetSkillLevel(
                        skill_id=row[0],
                        level=row[1],
                        time_requirement=row[2],
                        time_unit=row[3],
                        category_id=row[4],
                        group_id=group_id
                    )
                    for row in cursor.fetchall()
                ]
        except Exception as e:
            print(f"Error getting targets: {e}")
            return []
