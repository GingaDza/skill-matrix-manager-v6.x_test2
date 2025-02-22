class DebugLogger:
    _instance = None

    def __init__(self, name="DebugLogger"):
        self.name = name

    @classmethod
    def get_logger(cls, name="DebugLogger"):
        if cls._instance is None:
            cls._instance = cls(name)
        return cls._instance

    def debug(self, message):
        print(f"[DEBUG][{self.name}] {message}")

    def info(self, message):
        print(f"[INFO][{self.name}] {message}")

    def error(self, message):
        print(f"[ERROR][{self.name}] {message}")