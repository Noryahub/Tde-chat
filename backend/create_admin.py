from backend.app.services.user_service import (
    create_user,
    get_user_by_email
)

admin = get_user_by_email(
    "admin@tde.tg"
)

if not admin:

    user_id, error = create_user(
        nom="Administrateur",
        email="admin@tde.tg",
        password="Admin123!",
        role="admin"
    )

    if error:
        print(error)
    else:
        print(
            f"Admin créé avec succès (id={user_id})"
        )

else:
    print("Admin déjà existant")