import pytest
import os
from datetime import datetime
from skill_matrix_manager.repositories.skill_level_repository import SkillLevelRepository
from skill_matrix_manager.models.data_models import SkillLevel, User

@pytest.fixture
def db_path(tmp_path):
    return str(tmp_path / "test_skill_matrix.db")

@pytest.fixture
def repository(db_path):
    repo = SkillLevelRepository(db_path)
    
    # テストデータの準備
    with open(os.path.join(os.path.dirname(__file__), '..', '..', 'src', 'skill_matrix_manager', 'migrations', '002_create_skill_levels.sql'), 'r') as f:
        sql = f.read()
        import sqlite3
        with sqlite3.connect(db_path) as conn:
            conn.executescript(sql)
            # テストユーザーとスキルレベルの作成
            conn.executescript("""
                CREATE TABLE IF NOT EXISTS users (
                    id TEXT PRIMARY KEY,
                    name TEXT NOT NULL,
                    group_id TEXT NOT NULL
                );
                
                INSERT INTO users (id, name, group_id) VALUES 
                ('user1', 'Test User 1', 'group1'),
                ('user2', 'Test User 2', 'group1');
                
                INSERT INTO skill_levels (user_id, skill_id, level) VALUES 
                ('user1', 'skill1', 3),
                ('user1', 'skill2', 4),
                ('user2', 'skill1', 2);
            """)
    
    return repo

def test_get_user_skill_levels(repository):
    skill_levels = repository.get_user_skill_levels('user1')
    assert len(skill_levels) == 2
    assert skill_levels['skill1'].level == 3
    assert skill_levels['skill2'].level == 4

def test_get_group_skill_levels(repository):
    group_levels = repository.get_group_skill_levels('group1')
    assert len(group_levels) == 2  # skill1とskill2
    assert len(group_levels['skill1']) == 2  # 2人のユーザー
    assert any(sl.level == 3 for sl in group_levels['skill1'])  # user1のレベル
    assert any(sl.level == 2 for sl in group_levels['skill1'])  # user2のレベル
