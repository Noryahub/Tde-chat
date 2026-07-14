from flask import (
    Blueprint,
    jsonify,
    request
)

from backend.app.services.ticket_service import (
    list_tickets,
    get_ticket,
    change_ticket_status,
    remove_ticket,
    get_ticket_stats,
    get_user_signalements,
    get_resolved_ticket
)

ticket_bp = Blueprint(
    "tickets",
    __name__
)

@ticket_bp.route(
    "/tickets",
    methods=["GET"]
)
def get_all_tickets_route():

    tickets = list_tickets()

    return jsonify({
        "status": "success",
        "data": tickets
    }), 200

@ticket_bp.route(
    "/tickets/<int:ticket_id>",
    methods=["GET"]
)
def get_ticket_route(ticket_id):

    ticket = get_ticket(ticket_id)

    if not ticket:

        return jsonify({
            "status": "error",
            "message": "aucun signalement"
        }), 404

    return jsonify({
        "status": "success",
        "data": ticket
    }), 200
#new get signalements
@ticket_bp.route(
    "tickets/user/<int:user_id>",
    methods=["GET"]
)
def get_user_tickets_route(user_id):

    tickets = get_user_signalements(user_id)

    if not tickets:
        return jsonify({
            "status": "error",
            "message": "Aucun ticket trouvé"
        }), 404

    return jsonify({
        "status": "success",
        "data": tickets
    }), 200

# get resolve tickets
@ticket_bp.route(
    "tickets/user/<int:user_id>/resolved",
    methods=["GET"]
)
def get_resolved_ticket_route(user_id):

    tickets = get_resolved_ticket(user_id)

    if not tickets:
        return jsonify({
            "status": "error",
            "message": "Aucun ticket résolu trouvé"
        }), 404

    return jsonify({
        "status": "success",
        "data": tickets
    }), 200
@ticket_bp.route(
    "/tickets/<int:ticket_id>/status",
    methods=["PATCH"]
)
def update_ticket_status_route(ticket_id):

    data = request.get_json() or {}

    statut = data.get("statut")

    if not statut:

        return jsonify({
            "status": "error",
            "message": "Statut manquant"
        }), 400

    try:

        change_ticket_status(
            ticket_id,
            statut
        )

        return jsonify({
            "status": "success",
            "message":
                "Statut mis à jour"
        }), 200

    except ValueError as e:

        return jsonify({
            "status": "error",
            "message": str(e)
        }), 400

@ticket_bp.route(
    "/tickets/<int:ticket_id>",
    methods=["DELETE"]
)
def delete_ticket_route(ticket_id):

    deleted = remove_ticket(
        ticket_id
    )

    if not deleted:

        return jsonify({
            "status": "error",
            "message":
                "Ticket introuvable"
        }), 404

    return jsonify({
        "status": "success",
        "message":
            "Ticket supprimé"
    }), 200

@ticket_bp.route(
    "/tickets/stats",
    methods=["GET"]
)
def ticket_stats_route():

    stats = get_ticket_stats()

    return jsonify({
        "status": "success",
        "data": stats
    }), 200