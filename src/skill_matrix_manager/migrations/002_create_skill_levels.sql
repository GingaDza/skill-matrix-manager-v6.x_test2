CREATE TABLE IF NOT EXISTS skill_levels (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id TEXT NOT NULL,
    skill_id TEXT NOT NULL,
    level INTEGER NOT NULL CHECK (level BETWEEN 1 AND 5),
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users (id),
    FOREIGN KEY (skill_id) REFERENCES skills (id),
    UNIQUE(user_id, skill_id)
);

CREATE TRIGGER IF NOT EXISTS update_skill_levels_timestamp 
AFTER UPDATE ON skill_levels
BEGIN
    UPDATE skill_levels SET updated_at = CURRENT_TIMESTAMP 
    WHERE id = NEW.id;
END;
