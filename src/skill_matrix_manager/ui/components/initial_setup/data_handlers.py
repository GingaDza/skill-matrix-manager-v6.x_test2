from PyQt5.QtWidgets import QTreeWidgetItem

class DataHandlers:
    def setup_initial_data(self):
        sample_groups = ["グループA", "グループB", "グループC"]
        self.group_list.addItems(sample_groups)
        
        self.group_categories = {
            "グループA": ["プログラミング"],
            "グループB": ["コミュニケーション"],
            "グループC": ["プログラミング", "コミュニケーション"]
        }
        
        categories = {
            "プログラミング": ["Python", "Java", "JavaScript"],
            "コミュニケーション": ["プレゼンテーション", "文書作成", "英語"]
        }
        
        for category, skills in categories.items():
            category_item = QTreeWidgetItem(self.category_tree, [category])
            for skill in skills:
                QTreeWidgetItem(category_item, [skill])

    def filter_categories(self, group_name):
        for i in range(self.category_tree.topLevelItemCount()):
            item = self.category_tree.topLevelItem(i)
            item.setHidden(
                group_name not in self.group_categories or 
                item.text(0) not in self.group_categories[group_name]
            )
