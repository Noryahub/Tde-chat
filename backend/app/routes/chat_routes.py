from flask import Blueprint, request, jsonify
from backend.app.services.chatbot_service import process_message

chat_bp = Blueprint("chat", __name__)

@chat_bp.route("/", methods=["POST"])
def handle_chat():

    data = request.get_json()

    user_message = data.get("message")
    user_id = data.get("user_id")
    session_id = data.get("session_id")

    if not user_id:
        return jsonify({
            "status": "error",
            "message": "Utilisateur non authentifié"
        }), 401

    response = process_message(user_message, session_id, user_id) #suvi du processus (nlp, ml, ...)

    return jsonify({
        "status": "success",
        "response": response
    })