from datetime import timedelta
from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from backend.app.routes.admin_routes import admin_bp
from backend.app.routes.ticket_routes import (
    ticket_bp
)
from backend.app.routes.history_routes import history_bp
from groq import Groq
import os

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

models = client.models.list()

for model in models.data:
    print(model.id)
def create_app():

    app = Flask(__name__)

    app.config["JWT_SECRET_KEY"] = (
        "change-this-secret-key"
    )

    app.config["JWT_ACCESS_TOKEN_EXPIRES"] = (
        timedelta(days=7)
    )

    jwt = JWTManager(app)

    CORS(
        app,
        resources={
            r"/*": {
                "origins": [
                    "http://localhost:3000",
                    "http://127.0.0.1:3000"
                ]
            }
        },
        supports_credentials=True
    )

    from backend.app.routes.chat_routes import chat_bp
    from backend.app.routes.auth_routes import auth_bp

    app.register_blueprint(
        chat_bp,
        url_prefix="/chat"
    )

    app.register_blueprint(
        auth_bp,
        url_prefix="/auth"
    )

    app.register_blueprint(
        ticket_bp,
        url_prefix="/api/admin"
    )
    app.register_blueprint(
        history_bp,
        url_prefix="/history"
    )
    app.register_blueprint(admin_bp)
    return app