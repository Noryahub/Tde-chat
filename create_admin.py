from frontend.services.auth_service import register
admin = get_user_by_email(
    "admin@tde.tg"
)

if not admin:
    create_user(
        nom="Administrateur",
        email="admin@tde.tg",
        password="Admin123!",
        role="admin"
    )