import json
from pathlib import Path

class DataModel:
    def __init__(self):
        self.data_dir = Path(__file__).parent.parent / 'data'
        self.groups_file = self.data_dir / 'groups.json'
        self.users_file = self.data_dir / 'users.json'
        self.skills_file = self.data_dir / 'user_skills.json'
        self._ensure_data_files()

    def _ensure_data_files(self):
        """データファイルの存在確認と初期化"""
        self.data_dir.mkdir(exist_ok=True)
        
        if not self.groups_file.exists():
            self._create_default_groups()
        
        if not self.users_file.exists():
            self._create_default_users()
            
        if not self.skills_file.exists():
            self._create_default_skills()

    def _create_default_groups(self):
        default_groups = {
            "1": {"id": "1", "name": "開発チーム"},
            "2": {"id": "2", "name": "デザインチーム"}
        }
        with open(self.groups_file, 'w', encoding='utf-8') as f:
            json.dump(default_groups, f, ensure_ascii=False, indent=2)

    def _create_default_users(self):
        default_users = {
            "1": [
                {"id": "1", "name": "山田太郎"},
                {"id": "2", "name": "鈴木一郎"}
            ],
            "2": [
                {"id": "3", "name": "佐藤花子"}
            ]
        }
        with open(self.users_file, 'w', encoding='utf-8') as f:
            json.dump(default_users, f, ensure_ascii=False, indent=2)

    def _create_default_skills(self):
        default_skills = {
            "1": {  # ユーザーID
                "プログラミング": {
                    "プログラミング基礎": {
                        "Python": "3",
                        "JavaScript": "4",
                        "Java": "2"
                    }
                }
            }
        }
        with open(self.skills_file, 'w', encoding='utf-8') as f:
            json.dump(default_skills, f, ensure_ascii=False, indent=2)

    def get_groups(self):
        """グループ一覧を取得"""
        with open(self.groups_file, 'r', encoding='utf-8') as f:
            return json.load(f)

    def get_users_by_group(self, group_id):
        """グループに所属するユーザー一覧を取得"""
        with open(self.users_file, 'r', encoding='utf-8') as f:
            users = json.load(f)
            return users.get(str(group_id), [])

    def get_user_skills(self, user_id):
        """ユーザーのスキルデータを取得"""
        with open(self.skills_file, 'r', encoding='utf-8') as f:
            skills = json.load(f)
            return skills.get(str(user_id), {})

    def save_user_skills(self, user_id, skills_data):
        """ユーザーのスキルデータを保存"""
        with open(self.skills_file, 'r+', encoding='utf-8') as f:
            skills = json.load(f)
            skills[str(user_id)] = skills_data
            f.seek(0)
            f.truncate()
            json.dump(skills, f, ensure_ascii=False, indent=2)

    def add_user(self, group_id, name):
        """ユーザーの追加"""
        try:
            with open(self.users_file, 'r+', encoding='utf-8') as f:
                users = json.load(f)
                group_users = users.get(str(group_id), [])
                
                # 新しいユーザーIDを生成
                new_id = str(max([int(user["id"]) for user in sum(users.values(), [])] + [0]) + 1)
                
                # ユーザーを追加
                group_users.append({"id": new_id, "name": name})
                users[str(group_id)] = group_users
                
                f.seek(0)
                f.truncate()
                json.dump(users, f, ensure_ascii=False, indent=2)
                return True
        except Exception as e:
            print(f"Error adding user: {e}")
            return False

    def edit_user(self, group_id, old_name, new_name):
        """ユーザーの編集"""
        try:
            with open(self.users_file, 'r+', encoding='utf-8') as f:
                users = json.load(f)
                group_users = users.get(str(group_id), [])
                
                for user in group_users:
                    if user["name"] == old_name:
                        user["name"] = new_name
                        break
                
                users[str(group_id)] = group_users
                f.seek(0)
                f.truncate()
                json.dump(users, f, ensure_ascii=False, indent=2)
                return True
        except Exception as e:
            print(f"Error editing user: {e}")
            return False

    def delete_user(self, group_id, name):
        """ユーザーの削除"""
        try:
            with open(self.users_file, 'r+', encoding='utf-8') as f:
                users = json.load(f)
                group_users = users.get(str(group_id), [])
                
                # ユーザーを検索して削除
                users[str(group_id)] = [u for u in group_users if u["name"] != name]
                
                f.seek(0)
                f.truncate()
                json.dump(users, f, ensure_ascii=False, indent=2)
                return True
        except Exception as e:
            print(f"Error deleting user: {e}")
            return False

    def add_group(self, name):
        """グループの追加"""
        try:
            with open(self.groups_file, 'r+', encoding='utf-8') as f:
                groups = json.load(f)
                
                # 新しいグループIDを生成
                new_id = str(max([int(gid) for gid in groups.keys()] + [0]) + 1)
                
                # グループを追加
                groups[new_id] = {"id": new_id, "name": name}
                
                f.seek(0)
                f.truncate()
                json.dump(groups, f, ensure_ascii=False, indent=2)
                
                # ユーザーファイルに新しいグループのエントリを追加
                with open(self.users_file, 'r+', encoding='utf-8') as uf:
                    users = json.load(uf)
                    users[new_id] = []
                    uf.seek(0)
                    uf.truncate()
                    json.dump(users, uf, ensure_ascii=False, indent=2)
                
                return True
        except Exception as e:
            print(f"Error adding group: {e}")
            return False

    def edit_group(self, group_id, new_name):
        """グループの編集"""
        try:
            with open(self.groups_file, 'r+', encoding='utf-8') as f:
                groups = json.load(f)
                
                if str(group_id) in groups:
                    groups[str(group_id)]["name"] = new_name
                    f.seek(0)
                    f.truncate()
                    json.dump(groups, f, ensure_ascii=False, indent=2)
                    return True
                return False
        except Exception as e:
            print(f"Error editing group: {e}")
            return False

    def delete_group(self, group_id):
        """グループの削除"""
        try:
            # グループの削除
            with open(self.groups_file, 'r+', encoding='utf-8') as f:
                groups = json.load(f)
                if str(group_id) in groups:
                    del groups[str(group_id)]
                    f.seek(0)
                    f.truncate()
                    json.dump(groups, f, ensure_ascii=False, indent=2)

            # グループに所属するユーザーの削除
            with open(self.users_file, 'r+', encoding='utf-8') as f:
                users = json.load(f)
                if str(group_id) in users:
                    del users[str(group_id)]
                    f.seek(0)
                    f.truncate()
                    json.dump(users, f, ensure_ascii=False, indent=2)

            return True
        except Exception as e:
            print(f"Error deleting group: {e}")
            return False
    def get_category_structure(self, group_id):
        """グループIDに基づくカテゴリー構造を取得"""
        structures = {
            "1": [  # 開発チーム
                {
                    "name": "プログラミング",
                    "skills": [
                        {
                            "name": "プログラミング基礎",
                            "skills": [
                                {"name": "Python", "level": "1"},
                                {"name": "JavaScript", "level": "1"},
                                {"name": "Java", "level": "1"}
                            ]
                        }
                    ]
                }
            ],
            "2": [  # デザインチーム
                {
                    "name": "デザイン",
                    "skills": [
                        {
                            "name": "UI/UXデザイン",
                            "skills": [
                                {"name": "Figma", "level": "1"},
                                {"name": "Adobe XD", "level": "1"}
                            ]
                        }
                    ]
                }
            ]
        }
        return structures.get(str(group_id), [])
