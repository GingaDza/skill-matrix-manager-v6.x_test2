import pytest
import os
from datetime import datetime
from skill_matrix_manager.utils.persistence_manager import PersistenceManager
from skill_matrix_manager.models.data_models import (
    Group, User, SkillLevel, Skill, Category
)

@pytest.fixture
def db_path(tmp_path):
    return str(tmp_path / "test_skill_matrix.db")

@pytest.fixture
def manager(db_path):
    return PersistenceManager(db_path)

def test_save_and_get_group(manager):
    group = Group(id="g1", name="Test Group", description="Test Description")
    assert manager.save_group(group)
    
    retrieved = manager.get_group("g1")
    assert retrieved is not None
    assert retrieved.id == group.id
    assert retrieved.name == group.name
    assert retrieved.description == group.description

def test_save_and_get_skill_level(manager):
    skill_level = SkillLevel(
        skill_id="s1",
        level=3,
        updated_at=datetime.now()
    )
    assert manager.save_user_skill_level("u1", skill_level)
    
    levels = manager.get_user_skill_levels("u1")
    assert "s1" in levels
    assert levels["s1"].level == 3
    assert levels["s1"].skill_id == "s1"

