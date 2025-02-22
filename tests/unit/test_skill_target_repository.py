import pytest
import os
import sqlite3
from datetime import datetime
from skill_matrix_manager.repositories.skill_target_repository import SkillTargetRepository
from skill_matrix_manager.models.data_models import TargetSkillLevel

@pytest.fixture
def db_path(tmp_path):
    return str(tmp_path / "test_skill_matrix.db")

@pytest.fixture
def repository(db_path):
    return SkillTargetRepository(db_path)

def test_save_and_get_target(repository):
    # テストデータの作成
    target = TargetSkillLevel(
        skill_id="skill1",
        category_id="cat1",
        group_id="group1",
        level=3,
        time_requirement=10,
        time_unit="時間"
    )
    
    # 保存のテスト
    assert repository.save_target(target) == True
    
    # 取得のテスト
    targets = repository.get_targets_by_group("group1")
    assert len(targets) == 1
    saved_target = targets[0]
    
    assert saved_target.skill_id == target.skill_id
    assert saved_target.category_id == target.category_id
    assert saved_target.group_id == target.group_id
    assert saved_target.level == target.level
    assert saved_target.time_requirement == target.time_requirement
    assert saved_target.time_unit == target.time_unit

def test_target_level_constraints(repository):
    # 無効なレベル値でのテスト
    invalid_target = TargetSkillLevel(
        skill_id="skill1",
        category_id="cat1",
        group_id="group1",
        level=6,  # 無効な値
        time_requirement=10,
        time_unit="時間"
    )
    
    # SQLiteのCHECK制約により保存が失敗することを確認
    assert repository.save_target(invalid_target) == False

def test_time_unit_constraints(repository):
    # 無効な時間単位でのテスト
    invalid_target = TargetSkillLevel(
        skill_id="skill1",
        category_id="cat1",
        group_id="group1",
        level=3,
        time_requirement=10,
        time_unit="無効な単位"  # 無効な値
    )
    
    # SQLiteのCHECK制約により保存が失敗することを確認
    assert repository.save_target(invalid_target) == False

