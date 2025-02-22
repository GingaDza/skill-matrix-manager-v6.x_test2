import pytest
from datetime import datetime, UTC
from skill_matrix_manager.models.data_models import Category
from skill_matrix_manager.repositories.category_repository import CategoryRepository
from skill_matrix_manager.repositories.group_user_repository import GroupUserRepository

@pytest.fixture
def db_path(tmp_path):
    return str(tmp_path / "test_skill_matrix.db")

@pytest.fixture
def category_repository(db_path):
    return CategoryRepository(db_path)

@pytest.fixture
def group_repository(db_path):
    return GroupUserRepository(db_path)

@pytest.fixture
def test_group(group_repository):
    return group_repository.create_group("テストグループ")

def test_create_category(category_repository, test_group):
    """カテゴリー作成のテスト"""
    category = category_repository.create_category(
        name="テストカテゴリー",
        group_id=test_group.id,
        description="テスト用カテゴリーです"
    )
    assert category.id is not None
    assert category.name == "テストカテゴリー"
    assert category.group_id == test_group.id

def test_get_categories_by_group(category_repository, test_group):
    """グループ別カテゴリー取得のテスト"""
    category_repository.create_category("カテゴリー1", test_group.id)
    category_repository.create_category("カテゴリー2", test_group.id)
    
    categories = category_repository.get_categories_by_group(test_group.id)
    assert len(categories) >= 2
    assert all(isinstance(c, Category) for c in categories)
    assert all(c.group_id == test_group.id for c in categories)

def test_update_category(category_repository, test_group):
    """カテゴリー更新のテスト"""
    category = category_repository.create_category("旧カテゴリー", test_group.id)
    category.name = "新カテゴリー"
    success = category_repository.update_category(category)
    assert success
    
    categories = category_repository.get_categories_by_group(test_group.id)
    updated = next((c for c in categories if c.id == category.id), None)
    assert updated is not None
    assert updated.name == "新カテゴリー"

def test_delete_category(category_repository, test_group):
    """カテゴリー削除のテスト"""
    category = category_repository.create_category("削除カテゴリー", test_group.id)
    success = category_repository.delete_category(category.id)
    assert success
    
    categories = category_repository.get_categories_by_group(test_group.id)
    assert not any(c.id == category.id for c in categories)
