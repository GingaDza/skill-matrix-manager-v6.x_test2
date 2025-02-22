class DebugLogger:
    _instance = None

    @classmethod
    def get_logger(cls):
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    @staticmethod
    def log(message: str) -> None:
        print(f"[DEBUG] {message}")

    def debug(self, message: str) -> None:
        self.log(message)

    def info(self, message: str) -> None:
        print(f"[INFO] {message}")

    def warning(self, message: str) -> None:
        print(f"[WARNING] {message}")

    def error(self, message: str) -> None:
        print(f"[ERROR] {message}")
