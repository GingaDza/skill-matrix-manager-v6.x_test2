from PyQt5.QtCore import QObject, pyqtSignal

class EvaluationConnection(QObject):
    skill_updated = pyqtSignal(str, str, int)  # member_id, skill_id, score
    
    def __init__(self):
        super().__init__()
        self.current_time = "2025-02-21 13:31:28"
        self.current_user = "GingaDza"
    
    def handle_skill_update(self, member_id, skill_id, score):
        print(f"自動保存: メンバー {member_id} のスキル {skill_id} を {score} に更新")
        print(f"評価者: {self.current_user}")
        print(f"更新時刻: {self.current_time}")
        self.skill_updated.emit(member_id, skill_id, score)
