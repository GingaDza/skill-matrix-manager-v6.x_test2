import unittest
from PyQt5.QtWidgets import QApplication, QTreeWidget, QTreeWidgetItem
from src.skill_matrix_manager.adapters.ui_adapter import UIAdapter
from src.skill_matrix_manager.models.data_models import (
    Group, User, Category, Skill, SkillLevel
)

class TestDataSync(unittest.TestCase):
    def setUp(self):
        self.app = QApplication([])
        self.data_model = {
            'groups': [Group(id=1, name="開発チーム")],
            'users': [User(id=1, name="テストユーザー", email="test@example.com")]
        }
        self.ui_adapter = UIAdapter(self.data_model)

    def test_group_user_relation(self):
        """グループとユーザーの関連テスト"""
        group = self.data_model['groups'][0]
        user = self.data_model['users'][0]
        user.group_id = group.id
        group.users.append(user)

        self.assertEqual(user.group_id, group.id)
        self.assertIn(user, group.users)

    def test_user_skills_save_load(self):
        """ユーザースキルのセーブ/ロードテスト"""
        user = self.data_model['users'][0]
        category = Category(id=1, name="プログラミング")
        skill = Skill(id=1, name="Python")
        category.add_skill(skill)  # カテゴリーにスキルを追加
        user.skills[skill.id] = SkillLevel.ADVANCED

        self.assertEqual(user.skills[skill.id], SkillLevel.ADVANCED)
        self.assertEqual(skill.category_id, category.id)

    def tearDown(self):
        self.app.quit()

class TestUIAdapter(unittest.TestCase):
    def setUp(self):
        self.app = QApplication([])
        category = Category(id=1, name="プログラミング")
        skill = Skill(id=1, name="Python")
        category.add_skill(skill)
        
        self.data_model = {
            'categories': [category]
        }
        self.ui_adapter = UIAdapter(self.data_model)
        
        # ツリーウィジェットの設定
        self.tree = QTreeWidget()
        self.tree.setHeaderLabels(["名前", "レベル"])
        
        # カテゴリーをツリーに追加
        category_item = QTreeWidgetItem([category.name])
        self.tree.addTopLevelItem(category_item)
        
        # スキルをカテゴリーの子として追加
        skill_item = QTreeWidgetItem([skill.name, str(skill.required_level.value)])
        category_item.addChild(skill_item)
        
        self.ui_adapter.register_widget(category_item, category)
        self.ui_adapter.register_widget(skill_item, skill)

    def test_category_structure(self):
        """カテゴリー構造の整合性テスト"""
        category = self.data_model['categories'][0]
        self.assertEqual(category.name, "プログラミング")
        self.assertEqual(len(category.skills), 1)
        self.assertEqual(category.skills[0].name, "Python")
        
        # ツリー構造の確認
        root_item = self.tree.topLevelItem(0)
        self.assertEqual(root_item.text(0), category.name)
        self.assertEqual(root_item.childCount(), 1)
        self.assertEqual(root_item.child(0).text(0), "Python")

    def tearDown(self):
        self.tree.clear()
        self.tree.deleteLater()
        self.app.quit()

if __name__ == '__main__':
    unittest.main()
