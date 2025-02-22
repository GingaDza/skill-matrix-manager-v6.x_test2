from typing import List, Optional
from ..models.data_models import Group

class GroupUserRepository:
    def __init__(self):
        self.groups = {}
        self.next_id = 1

    def create_group(self, name: str, description: str = "") -> Group:
        """グループを作成"""
        group_id = str(self.next_id)
        self.next_id += 1

        group = Group(
            id=group_id,
            name=name,
            description=description
        )
        self.groups[group_id] = group
        return group

    def get_groups(self) -> List[Group]:
        """全グループを取得"""
        return list(self.groups.values())

    def get_group(self, group_id: str) -> Optional[Group]:
        """グループをIDで取得"""
        return self.groups.get(group_id)

    def update_group(self, group: Group) -> Group:
        """グループを更新"""
        if group.id not in self.groups:
            raise ValueError("指定されたグループが存在しません")
        self.groups[group.id] = group
        return group

    def delete_group(self, group_id: str):
        """グループを削除"""
        if group_id in self.groups:
            del self.groups[group_id]
