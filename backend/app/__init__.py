from flask import Flask

def create_app():
    app = Flask(__name__)

    # Imports à l'intérieur — ne s'exécutent que quand create_app() est appelé
    from backend.app.routes.chat_routes import chat_bp
    from backend.app.routes.auth_routes import auth_bp

    app.register_blueprint(chat_bp, url_prefix="/chat")
    app.register_blueprint(auth_bp, url_prefix="/auth")

    return app