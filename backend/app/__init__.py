from datetime import timedelta
from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from backend.app.routes.admin_routes import admin_bp

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
    app.register_blueprint(admin_bp)
    return app