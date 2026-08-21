import os


GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID", "")
GOOGLE_CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET", "")
GOOGLE_CALLBACK_URL = os.getenv(
    "GOOGLE_CALLBACK_URL",
    "http://127.0.0.1:5000/auth/google/callback"
)
FRONTEND_URL = os.getenv(
    "FRONTEND_URL",
    "http://localhost:3000"
).rstrip("/")

OAUTH_STATE_COOKIE_NAME = "assistant_tde_oauth_state"
OAUTH_STATE_TTL_SECONDS = int(os.getenv("OAUTH_STATE_TTL_SECONDS", "300"))
OAUTH_EXCHANGE_CODE_TTL_SECONDS = int(
    os.getenv("OAUTH_EXCHANGE_CODE_TTL_SECONDS", "300")
)
OAUTH_COOKIE_SECURE = os.getenv(
    "OAUTH_COOKIE_SECURE",
    "false"
).lower() == "true"

ALLOWED_OAUTH_REDIRECT_PATHS = {
    "/user/chat",
}
