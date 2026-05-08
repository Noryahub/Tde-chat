from flask import Blueprint, Flask, request, jsonify

from backend.app.services.user_service import create_user, authenticate_user

app = Flask(__name__)

auth_bp = Blueprint("auth", __name__)
@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    user_id, error = create_user(email, password)
    if error:
            return jsonify({"status": "error", "message": error}), 400
    return jsonify({"status": "success", "message": "Utilisateur créé avec succès", "user_id": user_id}), 201

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    user_id = authenticate_user(email, password)
    if not user_id:
        return jsonify({ "status": "error", "message": "Email ou mot de passe incorrect" }), 401
    return jsonify({"status": "success", "message": "Connexion réussie", "user_id": user_id}), 200
