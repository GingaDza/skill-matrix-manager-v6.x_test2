from PyQt5.QtCore import QObject, QRunnable, pyqtSignal, QThreadPool
from typing import Any, Callable, Dict
import traceback
import sys

class WorkerSignals(QObject):
    finished = pyqtSignal()
    error = pyqtSignal(tuple)
    result = pyqtSignal(object)
    progress = pyqtSignal(int)

class AsyncWorker(QRunnable):
    """非同期処理を実行するワーカークラス"""
    
    def __init__(self, fn: Callable, *args, **kwargs):
        super().__init__()
        self.fn = fn
        self.args = args
        self.kwargs = kwargs
        self.signals = WorkerSignals()
        
    def run(self):
        """ワーカーの実行"""
        try:
            result = self.fn(*self.args, **self.kwargs)
            self.signals.result.emit(result)
        except Exception:
            traceback.print_exc()
            exctype, value = sys.exc_info()[:2]
            self.signals.error.emit((exctype, value, traceback.format_exc()))
        finally:
            self.signals.finished.emit()

class AsyncTaskManager:
    """非同期タスクを管理するマネージャークラス"""
    
    def __init__(self):
        self.threadpool = QThreadPool()
        
    def execute(self, fn: Callable, 
                on_result: Callable[[Any], None] = None,
                on_error: Callable[[tuple], None] = None,
                *args, **kwargs) -> None:
        """非同期タスクの実行"""
        worker = AsyncWorker(fn, *args, **kwargs)
        
        if on_result:
            worker.signals.result.connect(on_result)
        if on_error:
            worker.signals.error.connect(on_error)
            
        self.threadpool.start(worker)