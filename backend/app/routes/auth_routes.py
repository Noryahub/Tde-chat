from flask import (
    Blueprint,
    request,
    jsonify
)

from flask_jwt_extended import (
    create_access_token,
    jwt_required,
    get_jwt_identity
)

from backend.app.services.user_service import (
    create_user,
    authenticate_user,
    get_user_by_id
)

auth_bp = Blueprint(
    "auth",
    __name__
)


# =========================================
# REGISTER
# =========================================

@auth_bp.route(
    "/register",
    methods=["POST"]
)
def register():

    data = request.get_json() or {}

    nom = data.get(
        "nom",
        ""
    ).strip()

    email = data.get(
        "email",
        ""
    ).strip().lower()

    password = data.get(
        "password",
        ""
    )

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


# =========================================
# LOGIN
# =========================================

@auth_bp.route(
    "/login",
    methods=["POST"]
)
def login():

    data = request.get_json() or {}

    email = data.get(
        "email",
        ""
    ).strip().lower()

    password = data.get(
        "password",
        ""
    )

    user = authenticate_user(
        email=email,
        password=password
    )

    if not user:

        return jsonify({
            "status": "error",
            "message": "Email ou mot de passe incorrect"
        }), 401

    token = create_access_token(
        identity=str(user["id"]),
        additional_claims={
            "role": user["role"]
        }
    )

    return jsonify({
        "status": "success",
        "message": "Connexion réussie",
        "token": token,
        "user": {
            "id": user["id"],
            "nom": user["nom"],
            "email": user["email"],
            "role": user["role"]
        }
    }), 200


# =========================================
# CURRENT USER
# =========================================

@auth_bp.route(
    "/me",
    methods=["GET"]
)
@jwt_required()
def me():

    user_id = get_jwt_identity()

    user = get_user_by_id(
        int(user_id)
    )

    if not user:

        return jsonify({
            "status": "error",
            "message": "Utilisateur introuvable"
        }), 404

    return jsonify({
        "status": "success",
        "user": user
    }), 200


# =========================================
# HEALTH CHECK AUTH
# =========================================

@auth_bp.route(
    "/verify",
    methods=["GET"]
)
@jwt_required()
def verify_token():

    return jsonify({
        "status": "success",
        "message": "Token valide"
    }), 200