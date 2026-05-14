from frontend.services.api_client import (
    post,
    get,
    patch,
    delete
)

# =========================================
# LOGIN
# =========================================

def login(email: str, password: str):

    return post(
        "/auth/login",
        {
            "email": email,
            "password": password
        }
    )


# =========================================
# REGISTER
# =========================================

def register(
    nom: str,
    email: str,
    password: str
):

    return post(
        "/auth/register",
        {
            "nom": nom,
            "email": email,
            "password": password
        }
    )


# =========================================
# ADMIN — USERS
# =========================================

def get_all_users():

    return get(
        "/admin/users"
    )


def update_role(
    user_id: int,
    role: str
):

    return patch(
        f"/admin/users/{user_id}/role",
        {
            "role": role
        }
    )


def delete_user(user_id: int):

    return delete(
        f"/admin/users/{user_id}"
    )