CREATE TABLE IF NOT EXISTS guild (
    id BIGINT PRIMARY KEY,
    locale TEXT NOT NULL DEFAULT 'en'
);

CREATE TABLE IF NOT EXISTS tr_user (
    id BIGINT PRIMARY KEY,
    username VARCHAR,
    background_color VARCHAR DEFAULT '#000000'
);

CREATE TABLE IF NOT EXISTS tr_record (
    id SERIAL PRIMARY KEY,
    user_id BIGINT NOT NULL,
    total_games_played INT DEFAULT 0,
    avg_accuracy FLOAT DEFAULT 0.0,
    current_level INT DEFAULT 0,
    xp INT DEFAULT 0,
    time_played INT DEFAULT 0,
    CONSTRAINT fk_user FOREIGN KEY (user_id) REFERENCES tr_user (id) ON DELETE CASCADE
);
