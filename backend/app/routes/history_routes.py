from flask import (
    Blueprint,
    jsonify,
    request
)
from backend.app.services.history_service import HistoryService

history_bp = Blueprint(
    "history",
    __name__
)
@history_bp.route('/user/<int:user_id>', methods=['GET'])
def get_user_history_route(user_id):
    history = HistoryService.get_user_messages(user_id)
    if not history:
        return jsonify({
            "status": "error",
            "message": "Aucun historique utilisateur "
        }), 404

    return jsonify({
        "status": "success",
        "data": history
    }), 200