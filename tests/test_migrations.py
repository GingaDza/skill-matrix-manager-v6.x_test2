import unittest
import json
from pathlib import Path
from src.skill_matrix_manager.models.data_model import DataModel

class TestDataMigrations(unittest.TestCase):
    def setUp(self):
        self.data_model = DataModel()
        self.test_data_dir = Path(__file__).parent / 'test_data'
        self.test_data_dir.mkdir(exist_ok=True)

    def test_data_structure(self):
        """データ構造の整合性テスト"""
        # グループデータの構造テスト
        groups = self.data_model.get_groups()
        self.assertIsInstance(groups, dict)
        for group_id, group in groups.items():
            self.assertIn('id', group)
            self.assertIn('name', group)

        # ユーザーデータの構造テスト
        for group_id in groups:
            users = self.data_model.get_users_by_group(group_id)
            self.assertIsInstance(users, list)
            for user in users:
                self.assertIn('id', user)
                self.assertIn('name', user)

    def tearDown(self):
        # テストデータのクリーンアップ
        if self.test_data_dir.exists():
            for file in self.test_data_dir.glob('*'):
                file.unlink()
            self.test_data_dir.rmdir()

if __name__ == '__main__':
    unittest.main()

    def test_data_file_creation(self):
        """データファイル作成テスト"""
        # データファイルの存在確認
        self.assertTrue(self.data_model.groups_file.exists())
        self.assertTrue(self.data_model.users_file.exists())
        self.assertTrue(self.data_model.skills_file.exists())

    def test_data_file_format(self):
        """データファイルのフォーマットテスト"""
        # グループファイルのJSON形式テスト
        with open(self.data_model.groups_file, 'r', encoding='utf-8') as f:
            groups_data = json.load(f)
            self.assertIsInstance(groups_data, dict)

        # ユーザーファイルのJSON形式テスト
        with open(self.data_model.users_file, 'r', encoding='utf-8') as f:
            users_data = json.load(f)
            self.assertIsInstance(users_data, dict)

        # スキルファイルのJSON形式テスト
        with open(self.data_model.skills_file, 'r', encoding='utf-8') as f:
            skills_data = json.load(f)
            self.assertIsInstance(skills_data, dict)

    def test_default_data_creation(self):
        """デフォルトデータ作成テスト"""
        # データファイルを一時的に削除
        self.data_model.groups_file.unlink(missing_ok=True)
        self.data_model.users_file.unlink(missing_ok=True)
        self.data_model.skills_file.unlink(missing_ok=True)

        # 新しいDataModelインスタンスを作成（デフォルトデータが生成される）
        new_data_model = DataModel()

        # デフォルトデータの検証
        groups = new_data_model.get_groups()
        self.assertGreater(len(groups), 0)

        # デフォルトユーザーの検証
        for group_id in groups:
            users = new_data_model.get_users_by_group(group_id)
            self.assertIsInstance(users, list)
