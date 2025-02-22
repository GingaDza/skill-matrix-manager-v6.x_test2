import pytest
from datetime import datetime, UTC
from src.skill_matrix_manager.adapters.skill_matrix_adapter import SkillMatrixAdapter
from src.skill_matrix_manager.adapters.ui_protection import UIProtection

class TestSkillMatrixAdapter:
    CURRENT_TIME = datetime(2025, 2, 19, 20, 41, 32, tzinfo=UTC)
    CURRENT_USER = "GingaDza"
    
    @pytest.fixture
    def ui_protection(self):
        protection = UIProtection()
        protection.set_current_user(self.CURRENT_USER)
        return protection
        
    @pytest.fixture
    def skill_matrix(self, ui_protection):
        matrix = SkillMatrixAdapter(ui_protection)
        return matrix
        
    def test_set_skill_level(self, skill_matrix):
        # 正常系のテスト
        assert skill_matrix.set_skill_level("user1", "skill1", 3)
        
        # 範囲外の値のテスト
        assert not skill_matrix.set_skill_level("user1", "skill1", 0)
        assert not skill_matrix.set_skill_level("user1", "skill1", 6)
        
        # ロックされた状態のテスト
        skill_matrix.protection.lock_component("skill_skill1")
        assert not skill_matrix.set_skill_level("user1", "skill1", 4)
