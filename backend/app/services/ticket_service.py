from backend.app.repositories.ticket_repository import (
    get_all_tickets,
    get_ticket_by_id,
    get_resolved_ticket_by_user,
    get_ticket_by_user,
    update_ticket_status,
    delete_ticket,
    count_tickets,
    count_open_tickets,
    count_in_progress_tickets,
    count_resolved_tickets
)
def list_tickets():
    return get_all_tickets()
#get ticket by id
def get_ticket(ticket_id):

    ticket = get_ticket_by_id(ticket_id)

    if not ticket:
        return None

    return ticket
ALLOWED_STATUS = [
    "ouvert",
    "en_cours",
    "resolu",
    "cloture"
]

#get ticket(SIGNALEMENT) by user
def get_user_signalements(user_id):
    ticket = get_ticket_by_user(user_id)
    if not ticket:
        return None
    return ticket

#GET TICKETS RESOLUT BY USER
def get_resolved_ticket(user_id):
    ticket = get_resolved_ticket_by_user(user_id)
    if not ticket:
        return None
    return ticket

def change_ticket_status(
    ticket_id,
    statut
):

    if statut not in ALLOWED_STATUS:
        raise ValueError(
            "Statut invalide"
        )

    return update_ticket_status(
        ticket_id,
        statut
    )
def remove_ticket(ticket_id):

    ticket = get_ticket_by_id(ticket_id)

    if not ticket:
        return False

    delete_ticket(ticket_id)

    return True

def remove_ticket(ticket_id):

    ticket = get_ticket_by_id(ticket_id)

    if not ticket:
        return False

    delete_ticket(ticket_id)

    return True

def get_ticket_stats():

    return {
        "total":
            count_tickets()["count"],

        "ouvert":
            count_open_tickets()["count"],

        "en_cours":
            count_in_progress_tickets()["count"],

        "resolu":
            count_resolved_tickets()["count"]
    }
