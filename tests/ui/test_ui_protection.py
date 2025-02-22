import pytest
from datetime import datetime
from PyQt5.QtWidgets import QWidget
from src.skill_matrix_manager.adapters.ui_protection import UIProtectionAdapter

class TestUIProtection:
    @pytest.fixture
    def ui_protection(self, tmp_path):
        log_file = tmp_path / "test_ui_changes.log"
        return UIProtectionAdapter(str(log_file))
    
    @pytest.fixture
    def test_widget(self):
        return QWidget()
    
    def test_component_locking(self, ui_protection):
        """コンポーネントのロック機能のテスト"""
        component_id = "test_component"
        
        # 初期状態の確認
        assert not ui_protection.is_component_locked(component_id)
        
        # ロックの設定
        ui_protection.lock_component(component_id)
        assert ui_protection.is_component_locked(component_id)
        
        # ロックの解除
        ui_protection.unlock_component(component_id)
        assert not ui_protection.is_component_locked(component_id)
    
    def test_change_validation(self, ui_protection):
        """変更の妥当性検証のテスト"""
        component_id = "test_component"
        ui_protection.set_current_user("GingaDza")
        
        # ロックされていない状態での変更
        assert ui_protection.validate_change(
            component_id,
            "UPDATE",
            "old_value",
            "new_value"
        )
        
        # ロックされた状態での変更
        ui_protection.lock_component(component_id)
        assert not ui_protection.validate_change(
            component_id,
            "UPDATE",
            "old_value",
            "new_value"
        )
