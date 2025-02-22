import logging
from datetime import datetime
from ..utils.state_monitor import state_monitor

class ErrorHandlerUtil:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.setup_logging()

    def setup_logging(self):
        """ロギングの設定"""
        logging.basicConfig(
            filename='app_log.txt',
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )

    def log_error(self, error: Exception, context: str = None):
        """エラーをログに記録"""
        error_info = {
            'timestamp': datetime.utcnow(),
            'user': state_monitor.current_user,
            'error_type': type(error).__name__,
            'error_message': str(error),
            'context': context
        }
        self.logger.error(f"Error occurred: {error_info}")
        return error_info

    def handle_error(self, error: Exception, context: str = None):
        """エラーを処理"""
        error_info = self.log_error(error, context)
        # 必要に応じて追加のエラーハンドリング処理を実装
        return error_info

error_handler = ErrorHandlerUtil()
