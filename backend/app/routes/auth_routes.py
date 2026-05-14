from flask import Blueprint, request, jsonify

from backend.app.services.user_service import (
    create_user,
    authenticate_user
)

auth_bp = Blueprint("auth", __name__)
# REGISTER
@auth_bp.route("/register", methods=["POST"])
def register():

    data = request.get_json()

    nom = data.get("nom")
    email = data.get("email")
    password = data.get("password")

    user_id, error = create_user(
        email=email,
        password=password,
        nom=nom
    )

    if error:

        return jsonify({
            "status": "error",
            "message": error
        }), 400

    return jsonify({
        "status": "success",
        "message": "Utilisateur créé avec succès",
        "user_id": user_id
    }), 201
# LOGIN
@auth_bp.route("/login", methods=["POST"])
def login():

    data = request.get_json()

    email = data.get("email")
    password = data.get("password")

    user = authenticate_user(
        email=email,
        password=password
    )

    if not user:

        return jsonify({
            "status": "error",
            "message": "Email ou mot de passe incorrect"
        }), 401

    return jsonify({
        "status": "success",
        "message": "Connexion réussie",
        "user": {
            "id": user["id"],
            "role": user["role"]
        }
    }), 200