from typing import List
from ..models.data_models import Group, User

class MockAPI:
    """テスト用のモックAPI"""
    def __init__(self):
        self.groups = [
            Group(id=1, name="開発チーム"),
            Group(id=2, name="デザインチーム")
        ]
        self.users = {
            1: [
                User(name="山田太郎", group_id=1),
                User(name="鈴木一郎", group_id=1)
            ],
            2: [
                User(name="佐藤花子", group_id=2),
                User(name="田中美咲", group_id=2)
            ]
        }

    def get_groups(self) -> List[Group]:
        """グループ一覧を取得"""
        return self.groups

    def get_users(self, group_id: int) -> List[User]:
        """指定されたグループのユーザー一覧を取得"""
        return self.users.get(group_id, [])
