import threading
import unittest
from pathlib import Path
from unittest.mock import patch

from flask import Flask
from flask_jwt_extended import JWTManager, create_access_token

from backend.app.routes.chat_routes import chat_bp
from backend.app.services.anonymous_quota_service import (
    AnonymousQuotaExceeded,
    AnonymousQuotaService,
)


class InMemoryAtomicQuotaRepository:
    lock = threading.Lock()
    sessions = {}

    @classmethod
    def reset(cls):
        cls.sessions = {}

    @classmethod
    def ensure_session(cls, session_id, messages_limit=5):
        with cls.lock:
            cls.sessions.setdefault(
                session_id,
                {
                    "messages_used": 0,
                    "messages_limit": messages_limit,
                }
            )

    @classmethod
    def consume_message(cls, session_id):
        with cls.lock:
            quota = cls.sessions[session_id]
            if quota["messages_used"] >= quota["messages_limit"]:
                return False
            quota["messages_used"] += 1
            return True

    @classmethod
    def get_quota(cls, session_id):
        with cls.lock:
            quota = cls.sessions[session_id]
            return {
                "messages_used": quota["messages_used"],
                "messages_limit": quota["messages_limit"],
                "messages_remaining": max(
                    quota["messages_limit"] - quota["messages_used"],
                    0
                ),
            }


class AnonymousQuotaServiceTest(unittest.TestCase):
    def setUp(self):
        InMemoryAtomicQuotaRepository.reset()

    def test_new_anonymous_session_starts_at_zero_of_five(self):
        with patch(
            "backend.app.services.anonymous_quota_service.AnonymousQuotaRepository",
            InMemoryAtomicQuotaRepository
        ):
            AnonymousQuotaService.ensure_session("session_test")

            quota = InMemoryAtomicQuotaRepository.get_quota("session_test")

            self.assertEqual(quota["messages_used"], 0)
            self.assertEqual(quota["messages_limit"], 5)
            self.assertEqual(quota["messages_remaining"], 5)

    def test_first_fifth_and_sixth_anonymous_messages(self):
        with patch(
            "backend.app.services.anonymous_quota_service.AnonymousQuotaRepository",
            InMemoryAtomicQuotaRepository
        ):
            quota = AnonymousQuotaService.consume_message("session_test")
            self.assertEqual(quota["messages_used"], 1)
            self.assertEqual(quota["messages_remaining"], 4)

            for _ in range(4):
                quota = AnonymousQuotaService.consume_message("session_test")

            self.assertEqual(quota["messages_used"], 5)
            self.assertEqual(quota["messages_remaining"], 0)

            with self.assertRaises(AnonymousQuotaExceeded) as exc:
                AnonymousQuotaService.consume_message("session_test")

            self.assertEqual(exc.exception.quota["messages_used"], 5)
            self.assertEqual(exc.exception.quota["messages_remaining"], 0)

    def test_refresh_keeps_quota_for_same_session_id(self):
        with patch(
            "backend.app.services.anonymous_quota_service.AnonymousQuotaRepository",
            InMemoryAtomicQuotaRepository
        ):
            for _ in range(3):
                AnonymousQuotaService.consume_message("session_refresh")

            AnonymousQuotaService.ensure_session("session_refresh")
            quota = InMemoryAtomicQuotaRepository.get_quota("session_refresh")

            self.assertEqual(quota["messages_used"], 3)
            self.assertEqual(quota["messages_remaining"], 2)

    def test_concurrent_requests_with_one_remaining_allow_only_one(self):
        InMemoryAtomicQuotaRepository.sessions["session_race"] = {
            "messages_used": 4,
            "messages_limit": 5,
        }
        results = []

        def consume():
            try:
                AnonymousQuotaService.consume_message("session_race")
                results.append("allowed")
            except AnonymousQuotaExceeded:
                results.append("blocked")

        with patch(
            "backend.app.services.anonymous_quota_service.AnonymousQuotaRepository",
            InMemoryAtomicQuotaRepository
        ):
            threads = [
                threading.Thread(target=consume),
                threading.Thread(target=consume),
            ]
            for thread in threads:
                thread.start()
            for thread in threads:
                thread.join()

        quota = InMemoryAtomicQuotaRepository.get_quota("session_race")

        self.assertEqual(results.count("allowed"), 1)
        self.assertEqual(results.count("blocked"), 1)
        self.assertEqual(quota["messages_used"], 5)
        self.assertEqual(quota["messages_remaining"], 0)


class ChatRouteQuotaTest(unittest.TestCase):
    def setUp(self):
        self.app = Flask(__name__)
        self.app.config["JWT_SECRET_KEY"] = "test-secret"
        JWTManager(self.app)
        self.app.register_blueprint(chat_bp, url_prefix="/chat")
        self.client = self.app.test_client()

    def test_anonymous_allowed_response_includes_quota(self):
        quota = {
            "messages_used": 1,
            "messages_limit": 5,
            "messages_remaining": 4,
        }

        with patch(
            "backend.app.routes.chat_routes.AnonymousQuotaService.consume_message",
            return_value=quota
        ), patch(
            "backend.app.routes.chat_routes.process_message",
            return_value={
                "response": "ok",
                "intent": "test",
                "conversation_id": 1,
                "ticket_proposal": False,
            }
        ):
            response = self.client.post(
                "/chat/",
                json={
                    "message": "bonjour",
                    "session_id": "session_route",
                    "conversation_id": None,
                }
            )

        payload = response.get_json()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(payload["data"]["quota"], quota)

    def test_anonymous_quota_exceeded_returns_429(self):
        with patch(
            "backend.app.routes.chat_routes.AnonymousQuotaService.consume_message",
            side_effect=AnonymousQuotaExceeded({
                "messages_used": 5,
                "messages_limit": 5,
                "messages_remaining": 0,
            })
        ), patch(
            "backend.app.routes.chat_routes.process_message"
        ) as process_message:
            response = self.client.post(
                "/chat/",
                json={
                    "message": "bonjour",
                    "session_id": "session_full",
                    "conversation_id": None,
                }
            )

        payload = response.get_json()

        self.assertEqual(response.status_code, 429)
        self.assertEqual(payload["error"], "anonymous_quota_exceeded")
        self.assertEqual(payload["messages_remaining"], 0)
        process_message.assert_not_called()

    def test_authenticated_user_does_not_consume_anonymous_quota(self):
        with self.app.app_context():
            token = create_access_token(identity="123")

        with patch(
            "backend.app.routes.chat_routes.AnonymousQuotaService.consume_message"
        ) as consume_message, patch(
            "backend.app.routes.chat_routes.process_message",
            return_value={
                "response": "ok",
                "intent": "test",
                "conversation_id": 1,
                "ticket_proposal": False,
            }
        ):
            response = self.client.post(
                "/chat/",
                headers={
                    "Authorization": f"Bearer {token}",
                },
                json={
                    "message": "bonjour",
                    "session_id": "session_auth",
                    "conversation_id": None,
                }
            )

        payload = response.get_json()

        self.assertEqual(response.status_code, 200)
        self.assertNotIn("quota", payload["data"])
        consume_message.assert_not_called()


class FrontendSessionBehaviorTest(unittest.TestCase):
    def test_new_conversation_does_not_regenerate_session_id(self):
        chat_context = Path(
            "frontend/context/ChatContext.tsx"
        ).read_text(encoding="utf-8")

        start = chat_context.index("function newConversation()")
        end = chat_context.index("function createConversation", start)
        new_conversation_block = chat_context[start:end]

        self.assertNotIn("crypto.randomUUID", new_conversation_block)
        self.assertNotIn("saveSessionId", new_conversation_block)
        self.assertNotIn("setSessionId", new_conversation_block)
        self.assertIn("setConversationId(null)", new_conversation_block)
        self.assertIn("setSelectedConversationId(null)", new_conversation_block)


if __name__ == "__main__":
    unittest.main()
