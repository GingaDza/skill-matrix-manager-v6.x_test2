-- グループテーブルの作成
CREATE TABLE IF NOT EXISTS groups (
    id TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    description TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- ユーザーテーブルの作成
CREATE TABLE IF NOT EXISTS users (
    id TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    group_id TEXT NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (group_id) REFERENCES groups (id)
);

-- グループのタイムスタンプ更新トリガー
CREATE TRIGGER IF NOT EXISTS update_groups_timestamp 
AFTER UPDATE ON groups
BEGIN
    UPDATE groups SET updated_at = CURRENT_TIMESTAMP 
    WHERE id = NEW.id;
END;

-- ユーザーのタイムスタンプ更新トリガー
CREATE TRIGGER IF NOT EXISTS update_users_timestamp 
AFTER UPDATE ON users
BEGIN
    UPDATE users SET updated_at = CURRENT_TIMESTAMP 
    WHERE id = NEW.id;
END;

-- テストデータの挿入（開発環境のみ）
INSERT OR IGNORE INTO groups (id, name, description) VALUES
('group1', '開発チーム', 'ソフトウェア開発チーム'),
('group2', 'デザインチーム', 'UIUXデザインチーム');

-- テストユーザーの挿入（開発環境のみ）
INSERT OR IGNORE INTO users (id, name, group_id) VALUES
('user1', 'Test User 1', 'group1'),
('user2', 'Test User 2', 'group1'),
('user3', 'Test User 3', 'group2');
