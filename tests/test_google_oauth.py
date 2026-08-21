import unittest
from unittest.mock import patch

from backend.app.services.google_oauth_service import (
    GoogleOAuthError,
    complete_google_callback,
    exchange_login_code,
    start_google_oauth
)


class GoogleOAuthServiceTest(unittest.TestCase):
    def test_start_creates_state_and_returns_google_url(self):
        with patch(
            "backend.app.services.google_oauth_service.GOOGLE_CLIENT_ID",
            "client-id"
        ), patch(
            "backend.app.services.google_oauth_service.GOOGLE_CLIENT_SECRET",
            "client-secret"
        ), patch(
            "backend.app.services.google_oauth_service.create_oauth_state"
        ) as create_state:
            result = start_google_oauth(
                session_id="session_abc",
                redirect_path="/user/chat"
            )

        self.assertIn("https://accounts.google.com", result["auth_url"])
        self.assertIn("state=", result["auth_url"])
        create_state.assert_called_once()
        self.assertEqual(
            create_state.call_args.kwargs["session_id"],
            "session_abc"
        )

    def test_invalid_state_cookie_is_refused(self):
        with self.assertRaises(GoogleOAuthError) as exc:
            complete_google_callback(
                code="google-code",
                state="state-a",
                cookie_state="state-b"
            )

        self.assertEqual(exc.exception.code, "invalid_oauth_state")

    def test_expired_or_reused_state_is_refused(self):
        with patch(
            "backend.app.services.google_oauth_service.GOOGLE_CLIENT_ID",
            "client-id"
        ), patch(
            "backend.app.services.google_oauth_service.GOOGLE_CLIENT_SECRET",
            "client-secret"
        ), patch(
            "backend.app.services.google_oauth_service.consume_oauth_state",
            return_value=None
        ):
            with self.assertRaises(GoogleOAuthError) as exc:
                complete_google_callback(
                    code="google-code",
                    state="state-a",
                    cookie_state="state-a"
                )

        self.assertEqual(exc.exception.code, "invalid_oauth_state")

    def test_google_email_not_verified_is_refused(self):
        with patch(
            "backend.app.services.google_oauth_service.GOOGLE_CLIENT_ID",
            "client-id"
        ), patch(
            "backend.app.services.google_oauth_service.GOOGLE_CLIENT_SECRET",
            "client-secret"
        ), patch(
            "backend.app.services.google_oauth_service.consume_oauth_state",
            return_value={
                "session_id": "session_abc",
                "redirect_path": "/user/chat"
            }
        ), patch(
            "backend.app.services.google_oauth_service._exchange_authorization_code",
            return_value={"id_token": "id-token"}
        ), patch(
            "backend.app.services.google_oauth_service._validate_id_token",
            return_value={
                "sub": "google-sub",
                "email": "user@example.com",
                "email_verified": False
            }
        ):
            with self.assertRaises(GoogleOAuthError) as exc:
                complete_google_callback(
                    code="google-code",
                    state="state-a",
                    cookie_state="state-a"
                )

        self.assertEqual(exc.exception.code, "google_email_not_verified")

    def test_new_google_user_attaches_anonymous_conversations(self):
        with patch(
            "backend.app.services.google_oauth_service.GOOGLE_CLIENT_ID",
            "client-id"
        ), patch(
            "backend.app.services.google_oauth_service.GOOGLE_CLIENT_SECRET",
            "client-secret"
        ), patch(
            "backend.app.services.google_oauth_service.consume_oauth_state",
            return_value={
                "session_id": "session_abc",
                "redirect_path": "/user/chat"
            }
        ), patch(
            "backend.app.services.google_oauth_service._exchange_authorization_code",
            return_value={"id_token": "id-token"}
        ), patch(
            "backend.app.services.google_oauth_service._validate_id_token",
            return_value={
                "sub": "google-sub",
                "email": "user@example.com",
                "name": "User Example",
                "email_verified": True
            }
        ), patch(
            "backend.app.services.google_oauth_service.get_or_create_google_user",
            return_value=(
                {
                    "id": 42,
                    "nom": "User Example",
                    "email": "user@example.com",
                    "role": "user"
                },
                None
            )
        ) as get_or_create_user, patch(
            "backend.app.services.google_oauth_service.attach_anonymous_conversations",
            return_value=5
        ) as attach_conversations, patch(
            "backend.app.services.google_oauth_service.create_exchange_code"
        ) as create_code:
            result = complete_google_callback(
                code="google-code",
                state="state-a",
                cookie_state="state-a"
            )

        get_or_create_user.assert_called_once()
        attach_conversations.assert_called_once_with(
            session_id="session_abc",
            user_id=42
        )
        create_code.assert_called_once()
        self.assertEqual(result["attached_conversations"], 5)
        self.assertTrue(result["exchange_code"])

    def test_existing_google_user_uses_same_attach_path(self):
        with patch(
            "backend.app.services.google_oauth_service.GOOGLE_CLIENT_ID",
            "client-id"
        ), patch(
            "backend.app.services.google_oauth_service.GOOGLE_CLIENT_SECRET",
            "client-secret"
        ), patch(
            "backend.app.services.google_oauth_service.consume_oauth_state",
            return_value={
                "session_id": "session_existing",
                "redirect_path": "/user/chat"
            }
        ), patch(
            "backend.app.services.google_oauth_service._exchange_authorization_code",
            return_value={"id_token": "id-token"}
        ), patch(
            "backend.app.services.google_oauth_service._validate_id_token",
            return_value={
                "sub": "known-sub",
                "email": "known@example.com",
                "name": "Known User",
                "email_verified": True
            }
        ), patch(
            "backend.app.services.google_oauth_service.get_or_create_google_user",
            return_value=(
                {
                    "id": 42,
                    "nom": "Known User",
                    "email": "known@example.com",
                    "role": "user"
                },
                None
            )
        ), patch(
            "backend.app.services.google_oauth_service.attach_anonymous_conversations",
            return_value=1
        ) as attach_conversations, patch(
            "backend.app.services.google_oauth_service.create_exchange_code"
        ):
            complete_google_callback(
                code="google-code",
                state="state-a",
                cookie_state="state-a"
            )

        attach_conversations.assert_called_once_with(
            session_id="session_existing",
            user_id=42
        )

    def test_missing_session_authenticates_and_attaches_zero_conversation(self):
        with patch(
            "backend.app.services.google_oauth_service.GOOGLE_CLIENT_ID",
            "client-id"
        ), patch(
            "backend.app.services.google_oauth_service.GOOGLE_CLIENT_SECRET",
            "client-secret"
        ), patch(
            "backend.app.services.google_oauth_service.consume_oauth_state",
            return_value={
                "session_id": "session_empty",
                "redirect_path": "/user/chat"
            }
        ), patch(
            "backend.app.services.google_oauth_service._exchange_authorization_code",
            return_value={"id_token": "id-token"}
        ), patch(
            "backend.app.services.google_oauth_service._validate_id_token",
            return_value={
                "sub": "google-sub",
                "email": "user@example.com",
                "name": "User Example",
                "email_verified": True
            }
        ), patch(
            "backend.app.services.google_oauth_service.get_or_create_google_user",
            return_value=(
                {
                    "id": 42,
                    "nom": "User Example",
                    "email": "user@example.com",
                    "role": "user"
                },
                None
            )
        ), patch(
            "backend.app.services.google_oauth_service.attach_anonymous_conversations",
            return_value=0
        ), patch(
            "backend.app.services.google_oauth_service.create_exchange_code"
        ):
            result = complete_google_callback(
                code="google-code",
                state="state-a",
                cookie_state="state-a"
            )

        self.assertEqual(result["attached_conversations"], 0)

    def test_exchange_code_is_one_time(self):
        with patch(
            "backend.app.services.google_oauth_service.consume_exchange_code",
            side_effect=[
                {
                    "user_id": 42,
                    "attached_conversations": 2
                },
                None
            ]
        ), patch(
            "backend.app.services.google_oauth_service.get_user_by_id",
            return_value={
                "id": 42,
                "nom": "User Example",
                "email": "user@example.com",
                "role": "user"
            }
        ):
            result = exchange_login_code("exchange-code")
            self.assertEqual(result["attached_conversations"], 2)

            with self.assertRaises(GoogleOAuthError) as exc:
                exchange_login_code("exchange-code")

        self.assertEqual(exc.exception.code, "invalid_exchange_code")


if __name__ == "__main__":
    unittest.main()
