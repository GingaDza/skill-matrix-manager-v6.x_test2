import pytest
from datetime import datetime, UTC
from pathlib import Path
from src.skill_matrix_manager.adapters.ui_protection import (
    UIProtection,
    UIChangeMonitor
)

class TestUIProtection:
    CURRENT_TIME = datetime(2025, 2, 19, 20, 38, 52, tzinfo=UTC)
    CURRENT_USER = "GingaDza"
    
    @pytest.fixture
    def ui_monitor(self, tmp_path):
        log_file = tmp_path / "test_ui_changes.log"
        monitor = UIChangeMonitor(str(log_file))
        monitor._start_time = self.CURRENT_TIME
        return monitor
    
    @pytest.fixture
    def ui_protection(self, ui_monitor):
        protection = UIProtection(ui_monitor)
        protection.set_current_user(self.CURRENT_USER)
        protection._last_change_time = self.CURRENT_TIME
        return protection
    
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
    
    def test_user_management(self, ui_protection):
        """ユーザー管理機能のテスト"""
        # 初期ユーザーの確認
        assert ui_protection._current_user == self.CURRENT_USER
        assert ui_protection._last_change_time == self.CURRENT_TIME
        
        # 新しいユーザーの設定
        new_user = "NewUser"
        ui_protection.set_current_user(new_user)
        assert ui_protection._current_user == new_user
        
        # タイムスタンプの確認
        assert isinstance(ui_protection._last_change_time, datetime)
        assert ui_protection._last_change_time.tzinfo == UTC
    
    def test_monitor_initialization(self):
        """モニター初期化のテスト"""
        # モニターなしでの初期化
        protection = UIProtection()
        assert isinstance(protection.monitor, UIChangeMonitor)
        
        # カスタムモニターでの初期化
        custom_monitor = UIChangeMonitor("custom.log")
        protection = UIProtection(custom_monitor)
        assert protection.monitor == custom_monitor
        
    def test_current_time_and_user(self, ui_protection):
        """現在の時刻とユーザー情報のテスト"""
        assert ui_protection._current_user == self.CURRENT_USER
        assert ui_protection._last_change_time == self.CURRENT_TIME
        assert ui_protection._last_change_time.strftime('%Y-%m-%d %H:%M:%S') == '2025-02-19 20:38:52'
