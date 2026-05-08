DROP DATABASE IF EXISTS chatbot_tde;
CREATE DATABASE chatbot_tde;
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

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (user_id) REFERENCES users(id)
);

