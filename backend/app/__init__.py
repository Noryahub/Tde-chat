from flask import Flask
from flask_cors import CORS

def create_app():

    app = Flask(__name__)

    # Active CORS pour le frontend Next.js
    CORS(
        app,
        resources={
            r"/*": {
                "origins": [
                    "http://localhost:3000",
                    "http://127.0.0.1:3000"
                ]
            }
        }
    )

    # Imports des routes
    from backend.app.routes.chat_routes import chat_bp
    from backend.app.routes.auth_routes import auth_bp

    # Blueprints
    app.register_blueprint(
        chat_bp,
        url_prefix="/chat"
    )

    app.register_blueprint(
        auth_bp,
        url_prefix="/auth"
    )

    return app