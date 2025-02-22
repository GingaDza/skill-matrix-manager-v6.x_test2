import pytest
import os
from datetime import datetime, UTC
from skill_matrix_manager.models.data_models import Group
from skill_matrix_manager.repositories.group_user_repository import GroupUserRepository

@pytest.fixture
def db_path(tmp_path):
    return str(tmp_path / "test_skill_matrix.db")

@pytest.fixture
def repository(db_path):
    return GroupUserRepository(db_path)

def test_create_group(repository):
    """グループ作成のテスト"""
    group = repository.create_group("テストグループ", "テスト用グループです")
    assert group.id is not None
    assert group.name == "テストグループ"
    assert group.description == "テスト用グループです"
    assert isinstance(group.created_at, datetime)
    assert isinstance(group.updated_at, datetime)

def test_get_group(repository):
    """グループ取得のテスト"""
    created = repository.create_group("テストグループ2")
    retrieved = repository.get_group(created.id)
    assert retrieved is not None
    assert retrieved.id == created.id
    assert retrieved.name == created.name
    assert isinstance(retrieved.created_at, datetime)
    assert isinstance(retrieved.updated_at, datetime)

def test_update_group(repository):
    """グループ更新のテスト"""
    group = repository.create_group("旧グループ名")
    old_updated_at = group.updated_at
    group.name = "新グループ名"
    success = repository.update_group(group)
    assert success
    updated = repository.get_group(group.id)
    assert updated.name == "新グループ名"
    assert updated.updated_at > old_updated_at

def test_delete_group(repository):
    """グループ削除のテスト"""
    group = repository.create_group("削除対象グループ")
    success = repository.delete_group(group.id)
    assert success
    assert repository.get_group(group.id) is None

def test_get_groups(repository):
    """全グループ取得のテスト"""
    repository.create_group("グループA")
    repository.create_group("グループB")
    groups = repository.get_groups()
    assert len(groups) >= 2
    assert all(isinstance(g, Group) for g in groups)
    assert all(isinstance(g.created_at, datetime) for g in groups)
    assert all(isinstance(g.updated_at, datetime) for g in groups)
