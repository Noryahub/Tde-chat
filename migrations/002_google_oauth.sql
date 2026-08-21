USE chatbot_tde;

ALTER TABLE users
    MODIFY password VARCHAR(255) NULL,
    ADD COLUMN auth_provider VARCHAR(30)
        NOT NULL DEFAULT 'password'
        AFTER password,
    ADD COLUMN provider_subject VARCHAR(191)
        NULL
        AFTER auth_provider,
    ADD COLUMN email_verified BOOLEAN
        DEFAULT FALSE
        AFTER provider_subject;

CREATE UNIQUE INDEX idx_users_provider_subject
ON users(auth_provider, provider_subject);

ALTER TABLE conversations
    MODIFY session_id VARCHAR(100) NOT NULL;

ALTER TABLE signalements
    MODIFY session_id VARCHAR(100);

CREATE TABLE IF NOT EXISTS oauth_login_states (
    id INT AUTO_INCREMENT PRIMARY KEY,
    state_hash CHAR(64) NOT NULL UNIQUE,
    session_id VARCHAR(100) NOT NULL,
    redirect_path VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
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
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
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
