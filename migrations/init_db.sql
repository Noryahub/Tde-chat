DROP DATABASE IF EXISTS chatbot_tde;
CREATE DATABASE chatbot_tde CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE chatbot_tde;


CREATE TABLE services (
    id INT AUTO_INCREMENT PRIMARY KEY,
    service_name VARCHAR(100) NOT NULL,
    description TEXT,
    contact_info VARCHAR(150)
);


CREATE TABLE intents (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    action VARCHAR(50) NOT NULL,
    response TEXT NOT NULL,
    guide TEXT,
    service_id INT,
    FOREIGN KEY (service_id) REFERENCES services(id)
);


CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    session_id VARCHAR(50) UNIQUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);


CREATE TABLE conversations (
    id INT AUTO_INCREMENT PRIMARY KEY,

    user_id INT,
    session_id VARCHAR(50),

    user_message TEXT,
    bot_response TEXT,

    predicted_intent VARCHAR(100),
    confidence_score FLOAT,

    orientation_service VARCHAR(100),

    localisation VARCHAR(100),
    probleme VARCHAR(150),

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (user_id) REFERENCES users(id)
);


CREATE TABLE signalements (
    id INT AUTO_INCREMENT PRIMARY KEY,

    conversation_id INT,
    user_id INT,
    session_id VARCHAR(50),

    localisation VARCHAR(100),
    probleme VARCHAR(150),
    intent VARCHAR(100),

    statut ENUM('nouveau', 'en_cours', 'resolu') DEFAULT 'nouveau',

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (conversation_id) REFERENCES conversations(id),
    FOREIGN KEY (user_id) REFERENCES users(id)
);


CREATE TABLE analytics_daily (
    id INT AUTO_INCREMENT PRIMARY KEY,
    date DATE NOT NULL,
    intent VARCHAR(50),
    localisation VARCHAR(50),
    probleme VARCHAR(50),
    count INT DEFAULT 1,
    UNIQUE KEY unique_daily (date, intent, localisation, probleme)
);