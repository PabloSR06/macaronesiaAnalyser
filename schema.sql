Drop database if exists macaronesia;
CREATE DATABASE macaronesia;
-- Clubs Table
CREATE TABLE IF NOT EXISTS clubs (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL UNIQUE
);

-- Archers Table
CREATE TABLE IF NOT EXISTS archers (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    club_id INT NOT NULL,
    FOREIGN KEY (club_id) REFERENCES clubs(id),
    registration_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Categories Table
CREATE TABLE IF NOT EXISTS categories (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(50) NOT NULL UNIQUE
);

-- Seasons Table
CREATE TABLE IF NOT EXISTS seasons (
    id INT AUTO_INCREMENT PRIMARY KEY,
    year YEAR NOT NULL,
    location VARCHAR(50) NOT NULL,
    UNIQUE (year, location)
);

-- Rounds Table
CREATE TABLE IF NOT EXISTS rounds  (
    id INT AUTO_INCREMENT PRIMARY KEY,
    season_id INT NOT NULL,
    round_number INT NOT NULL,
    round_date DATE NULL,
    FOREIGN KEY (season_id) REFERENCES seasons(id),
    UNIQUE (season_id, round_number)
);

-- Round Results Table
CREATE TABLE IF NOT EXISTS results (
    id INT AUTO_INCREMENT PRIMARY KEY,
    round_id INT NOT NULL,
    archer_id INT NOT NULL,
    category_id INT NOT NULL,
    score INT NOT NULL,
    FOREIGN KEY (round_id) REFERENCES rounds(id),
    FOREIGN KEY (archer_id) REFERENCES archers(id),
    FOREIGN KEY (category_id) REFERENCES categories(id),
    UNIQUE (round_id, archer_id, category_id)
);
