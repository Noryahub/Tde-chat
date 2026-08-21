DROP DATABASE IF EXISTS chatbot_tde;

CREATE DATABASE IF NOT EXISTS chatbot_tde
CHARACTER SET utf8mb4
COLLATE utf8mb4_unicode_ci;

USE chatbot_tde;

CREATE TABLE IF NOT EXISTS services (
    id INT AUTO_INCREMENT PRIMARY KEY,
    service_name VARCHAR(100) NOT NULL,
    description TEXT,
    contact_info VARCHAR(150)
);



CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,

    nom VARCHAR(100),

    email VARCHAR(191) NOT NULL UNIQUE,

    password VARCHAR(255) NULL,

    auth_provider VARCHAR(30)
    NOT NULL DEFAULT 'password',

    provider_subject VARCHAR(191) NULL,

    email_verified BOOLEAN DEFAULT FALSE,

    role ENUM(
        'user',
        'admin',
        'super_admin'
    ) DEFAULT 'user',

    is_active BOOLEAN DEFAULT TRUE,

    last_login TIMESTAMP NULL,

    created_at TIMESTAMP
    DEFAULT CURRENT_TIMESTAMP,

    updated_at TIMESTAMP
    DEFAULT CURRENT_TIMESTAMP
    ON UPDATE CURRENT_TIMESTAMP
);

CREATE INDEX idx_users_email
ON users(email);

CREATE INDEX idx_users_role
ON users(role);

CREATE UNIQUE INDEX idx_users_provider_subject
ON users(auth_provider, provider_subject);


CREATE TABLE IF NOT EXISTS intents (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    action VARCHAR(50) NOT NULL,
    response TEXT NOT NULL,
    guide TEXT,
    service_id INT,
    FOREIGN KEY (service_id)
    REFERENCES services(id)
    ON DELETE SET NULL
);
CREATE TABLE IF NOT EXISTS tickets (
    id INT AUTO_INCREMENT PRIMARY KEY,
    ticket_number VARCHAR(50) UNIQUE,
    nom VARCHAR(100),
    email VARCHAR(100),
    telephone VARCHAR(50),
    localisation VARCHAR(100),
    description TEXT,
    intent VARCHAR(100),

    statut ENUM(
        'ouvert',
        'en_cours',
        'resolu',
        'cloture'
    ) DEFAULT 'ouvert',

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    ON UPDATE CURRENT_TIMESTAMP
);
CREATE TABLE IF NOT EXISTS conversations (

    id INT AUTO_INCREMENT PRIMARY KEY,

    user_id INT NULL,

    session_id VARCHAR(100) NOT NULL,

    title VARCHAR(255),

    predicted_intent VARCHAR(100),

    confidence_score FLOAT,

    orientation_service VARCHAR(100),

    localisation VARCHAR(100),

    probleme VARCHAR(150),

    created_at TIMESTAMP
    DEFAULT CURRENT_TIMESTAMP,

    updated_at TIMESTAMP
    DEFAULT CURRENT_TIMESTAMP
    ON UPDATE CURRENT_TIMESTAMP,

    FOREIGN KEY (user_id)
    REFERENCES users(id)
    ON DELETE SET NULL
);

CREATE INDEX idx_conv_user_id
ON conversations(user_id);

CREATE INDEX idx_conv_session
ON conversations(session_id);

CREATE INDEX idx_conv_intent
ON conversations(predicted_intent);

CREATE TABLE IF NOT EXISTS anonymous_sessions (

    id INT AUTO_INCREMENT PRIMARY KEY,

    session_id VARCHAR(100) NOT NULL UNIQUE,

    messages_used INT NOT NULL DEFAULT 0,

    messages_limit INT NOT NULL DEFAULT 5,

    created_at TIMESTAMP
    DEFAULT CURRENT_TIMESTAMP,

    updated_at TIMESTAMP
    DEFAULT CURRENT_TIMESTAMP
    ON UPDATE CURRENT_TIMESTAMP
);

CREATE INDEX idx_anonymous_sessions_session
ON anonymous_sessions(session_id);

CREATE TABLE IF NOT EXISTS oauth_login_states (

    id INT AUTO_INCREMENT PRIMARY KEY,

    state_hash CHAR(64) NOT NULL UNIQUE,

    session_id VARCHAR(100) NOT NULL,

    redirect_path VARCHAR(255) NOT NULL,

    created_at TIMESTAMP
    DEFAULT CURRENT_TIMESTAMP,

    expires_at TIMESTAMP NOT NULL,

    used_at TIMESTAMP NULL
);

CREATE INDEX idx_oauth_login_states_state
ON oauth_login_states(state_hash);

CREATE INDEX idx_oauth_login_states_expires
ON oauth_login_states(expires_at);

CREATE TABLE IF NOT EXISTS oauth_exchange_codes (

    id INT AUTO_INCREMENT PRIMARY KEY,

    code_hash CHAR(64) NOT NULL UNIQUE,

    user_id INT NOT NULL,

    attached_conversations INT NOT NULL DEFAULT 0,

    created_at TIMESTAMP
    DEFAULT CURRENT_TIMESTAMP,

    expires_at TIMESTAMP NOT NULL,

    used_at TIMESTAMP NULL,

    FOREIGN KEY (user_id)
    REFERENCES users(id)
    ON DELETE CASCADE
);

CREATE INDEX idx_oauth_exchange_codes_code
ON oauth_exchange_codes(code_hash);

CREATE INDEX idx_oauth_exchange_codes_expires
ON oauth_exchange_codes(expires_at);

CREATE TABLE IF NOT EXISTS messages (

    id INT AUTO_INCREMENT PRIMARY KEY,

    conversation_id INT NOT NULL,

    role ENUM(
        'user',
        'assistant',
        'system'
    ) NOT NULL,

    content TEXT NOT NULL,

    created_at TIMESTAMP
    DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (conversation_id)
    REFERENCES conversations(id)
    ON DELETE CASCADE
);

CREATE INDEX idx_messages_conversation
ON messages(conversation_id);

CREATE INDEX idx_messages_role
ON messages(role);

CREATE TABLE IF NOT EXISTS signalements (

    id INT AUTO_INCREMENT PRIMARY KEY,

    conversation_id INT,
    user_id INT NULL,
    session_id VARCHAR(100),
    localisation VARCHAR(100),
    probleme VARCHAR(150),
    intent VARCHAR(100),
    statut ENUM(
        'nouveau',
        'en_cours',
        'resolu'
    ) DEFAULT 'nouveau',
    created_at TIMESTAMP
    DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (conversation_id)
    REFERENCES conversations(id)
    ON DELETE SET NULL,
    FOREIGN KEY (user_id)
    REFERENCES users(id)
    ON DELETE SET NULL
);

CREATE INDEX idx_signalements_statut
ON signalements(statut);

CREATE INDEX idx_signalements_localisation
ON signalements(localisation);


CREATE TABLE IF NOT EXISTS analytics_daily (

    id INT AUTO_INCREMENT PRIMARY KEY,

    date DATE NOT NULL,

    intent VARCHAR(50),

    localisation VARCHAR(50),

    probleme VARCHAR(50),

    count INT DEFAULT 1,

    UNIQUE KEY unique_daily (
        date,
        intent,
        localisation,
        probleme
    )
);

CREATE INDEX idx_analytics_date
ON analytics_daily(date);
