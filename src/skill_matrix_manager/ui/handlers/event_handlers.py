from PyQt5.QtCore import QTimer
from ...utils.state_monitor import state_monitor

class LoadingHandler:
    @staticmethod
    def handle_loading_start(window):
        """ローディング開始時の処理"""
        window._set_loading_state(True)
        window.status_bar.showMessage("データを読み込んでいます...")

    @staticmethod
    def handle_loading_finish(window):
        """ローディング完了時の処理"""
        window._set_loading_state(False)
        window.status_bar.showMessage("完了", 3000)

    @staticmethod
    def handle_loading_change(window, loading):
        """ローディング状態変更時の処理"""
        window._update_progress_bar(loading)


class DataHandler:
    @staticmethod
    def handle_initial_data_load(window):
        """初期データの読み込み処理"""
        try:
            window.loading_started.emit()
            
            def on_success(groups):
                try:
                    window.group_combo.clear()
                    for group in groups:
                        window.group_combo.addItem(group.name, group.id)
                    window.status_bar.showMessage("データの読み込みが完了しました", 3000)
                    
                    # グループが選択されたときのハンドラを設定
                    window._connect_signal(window.group_combo.currentIndexChanged, window._on_group_changed)
                    
                    # 状態変更を記録
                    state_monitor.emit_state_change(
                        "groups_loaded",
                        f"count: {len(groups)}"
                    )
                except Exception as e:
                    window._handle_error(e, "データの読み込み中にエラーが発生しました")
                finally:
                    window.loading_finished.emit()
                    window._set_loading_state(False)
            
            def on_error(e):
                window._handle_error(e, "データの読み込みに失敗しました")
                window.loading_finished.emit()
                window._set_loading_state(False)
            
            worker = window.AsyncWorker(window.adapter.get_groups)
            worker.finished.connect(on_success)
            worker.error.connect(on_error)
            window._active_workers.append(worker)
            worker.start()
        except Exception as e:
            window._handle_error(e, "データ読み込みの準備中にエラーが発生しました")
            window.loading_finished.emit()
            window._set_loading_state(False)

    @staticmethod
    def handle_group_change(window, index):
        """グループ選択時の処理"""
        try:
            window.user_list.clear()
            
            if index < 0:
                return
                
            group_id = window.group_combo.itemData(index)
            group_name = window.group_combo.currentText()
            
            # 状態変更を記録
            state_monitor.emit_state_change(
                "group_selected", 
                f"id: {group_id}, name: {group_name}"
            )
            
            cached_users = window.state_manager.get_cached(f"users_{group_id}")
            
            if cached_users:
                window._update_user_list(cached_users)
            else:
                window.loading_started.emit()
                window.status_bar.showMessage("ユーザー情報を読み込んでいます...")
                
                def on_success(users):
                    try:
                        window.state_manager.set_cached(f"users_{group_id}", users)
                        window._update_user_list(users)
                        window.status_bar.showMessage("ユーザー情報の読み込みが完了しました", 3000)
                        
                        # 状態変更を記録
                        state_monitor.emit_state_change(
                            "users_loaded",
                            f"group: {group_name}, count: {len(users)}"
                        )
                    except Exception as e:
                        window._handle_error(e, "ユーザー情報の処理中にエラーが発生しました")
                    finally:
                        window.loading_finished.emit()
                        window._set_loading_state(False)
                    
                def on_error(e):
                    window._handle_error(e, "ユーザー情報の読み込みに失敗しました")
                    window.loading_finished.emit()
                    window._set_loading_state(False)
                
                worker = window.AsyncWorker(window.adapter.get_users, group_id)
                worker.finished.connect(on_success)
                worker.error.connect(on_error)
                window._active_workers.append(worker)
                worker.start()
        except Exception as e:
            window._handle_error(e, "グループ選択時にエラーが発生しました")
            window.loading_finished.emit()
            window._set_loading_state(False)

    @staticmethod
    def handle_user_selection(window, row):
        """ユーザー選択時の処理"""
        if row < 0:
            return
            
        user_name = window.user_list.item(row).text()
        if hasattr(window.total_evaluation_tab, 'set_current_user'):
            window.total_evaluation_tab.set_current_user(user_name)


class ErrorHandler:
    @staticmethod
    def handle_error(window, error: Exception, message: str):
        """エラー処理の共通メソッド"""
        error_message = f"エラー: {str(error)}"
        
        # まずステータスバーのメッセージを設定
        window.status_bar.showMessage(error_message, 5000)
        window._process_events()  # UIを即時更新
        
        # エラーハンドラを呼び出し
        window.error_handler.handle_error(
            error,
            lambda msg: window.status_bar.showMessage(msg, 5000),
            window,
            "エラー"
        )
        
        # 状態変更を記録
        state_monitor.emit_state_change(
            "error_occurred",
            f"message: {message}, error: {str(error)}"
        )
        
        # ローディング状態をリセット
        window.state_manager.set_loading(False)
        window._process_events()  # 再度UIを更新
