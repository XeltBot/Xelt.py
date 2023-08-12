CREATE TABLE IF NOT EXISTS guild (
    id BIGINT PRIMARY KEY,
    locale VARCHAR(5) DEFAULT 'en',
    prefixes VARCHAR(255)[]
);

CREATE TABLE IF NOT EXISTS xelt_user (
    id BIGINT PRIMARY KEY,
    username VARCHAR(255),
    background_color VARCHAR(255) DEFAULT '#000000'
);

CREATE TABLE IF NOT EXISTS tr_record (
    id SERIAL PRIMARY KEY,
    total_games_played INT DEFAULT 0,
    avg_accuracy FLOAT DEFAULT 0.0,
    current_level INT DEFAULT 0,
    xp INT DEFAULT 0,
    time_played INT DEFAULT 0,
    user_id BIGINT UNIQUE REFERENCES xelt_user (id) ON DELETE CASCADE ON UPDATE NO ACTION
);
