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
    get_ticket_stats
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
            "message": "Ticket introuvable"
        }), 404

    return jsonify({
        "status": "success",
        "data": ticket
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