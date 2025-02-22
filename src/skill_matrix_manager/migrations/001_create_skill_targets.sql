CREATE TABLE IF NOT EXISTS skill_targets (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    group_id TEXT NOT NULL,
    category_id TEXT NOT NULL,
    skill_id TEXT NOT NULL,
    target_level INTEGER NOT NULL CHECK (target_level BETWEEN 1 AND 5),
    time_requirement INTEGER NOT NULL,
    time_unit TEXT NOT NULL CHECK (time_unit IN ('時間', '日', '月', '年')),
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (group_id) REFERENCES groups (id),
    FOREIGN KEY (category_id) REFERENCES categories (id),
    FOREIGN KEY (skill_id) REFERENCES skills (id)
);

CREATE TRIGGER IF NOT EXISTS update_skill_targets_timestamp 
AFTER UPDATE ON skill_targets
BEGIN
    UPDATE skill_targets SET updated_at = CURRENT_TIMESTAMP 
    WHERE id = NEW.id;
END;
