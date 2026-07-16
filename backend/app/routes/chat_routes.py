from flask import Blueprint, request, jsonify

from flask_jwt_extended import (
    jwt_required,
    get_jwt_identity
)

from backend.app.services.chatbot_service import (
    process_message
)

# Création du blueprint AVANT les routes
chat_bp = Blueprint(
    "chat",
    __name__
)
@chat_bp.route("/", methods=["POST"])
@jwt_required(optional=True)
def handle_chat():

    data = request.get_json() or {}

    user_message = data.get("message")
    session_id = data.get("session_id")
    #recuperation de l'id de conversation depuis le frontend
    conversation_id = data.get("conversation_id")

    identity = get_jwt_identity()

    user_id = (
        int(identity)
        if identity is not None
        else None
    )

    if not user_message:

        return jsonify({
            "status": "error",
            "message": "Message manquant"
        }), 400

    result = process_message(
        user_message=user_message,
        session_id=session_id,
        user_id=user_id,
        conversation_id=conversation_id
)

    return jsonify({
        "status": "success",
        "data": result
    }), 200