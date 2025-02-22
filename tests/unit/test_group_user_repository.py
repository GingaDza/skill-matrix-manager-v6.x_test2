import pytest
import os
import sqlite3
from datetime import datetime
from skill_matrix_manager.repositories.group_user_repository import GroupUserRepository
from skill_matrix_manager.models.data_models import Group, User

@pytest.fixture
def db_path(tmp_path):
    return str(tmp_path / "test_skill_matrix.db")

@pytest.fixture
def repository(db_path):
    repo = GroupUserRepository(db_path)
    
    # テストデータの作成
    migration_path = os.path.join(
        os.path.dirname(__file__),
        '..',
        '..',
        'src',
        'skill_matrix_manager',
        'migrations',
        '003_create_groups_users.sql'
    )
    
    with open(migration_path, 'r') as f:
        sql = f.read()
        with sqlite3.connect(db_path) as conn:
            # マイグレーションの実行（テーブル作成とテストデータの挿入）
            conn.executescript(sql)
    
    return repo

def test_get_groups(repository):
    groups = repository.get_groups()
    assert len(groups) == 2
    assert any(g.name == '開発チーム' for g in groups)
    assert any(g.name == 'デザインチーム' for g in groups)

def test_get_users_by_group(repository):
    # 開発チームのユーザーテスト
    users = repository.get_users_by_group('group1')
    assert len(users) == 2
    assert any(u.name == 'Test User 1' for u in users)
    assert any(u.name == 'Test User 2' for u in users)

    # デザインチームのユーザーテスト
    users = repository.get_users_by_group('group2')
    assert len(users) == 1
    assert users[0].name == 'Test User 3'
