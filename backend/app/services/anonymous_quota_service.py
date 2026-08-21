from backend.app.repositories.anonymous_quota_repository import (
    AnonymousQuotaRepository,
    DEFAULT_ANONYMOUS_MESSAGES_LIMIT,
)


class AnonymousQuotaExceeded(Exception):
    def __init__(self, quota: dict):
        super().__init__("Anonymous quota exceeded")
        self.quota = quota


class AnonymousQuotaService:
    @staticmethod
    def ensure_session(session_id: str) -> None:
        AnonymousQuotaRepository.ensure_session(
            session_id=session_id,
            messages_limit=DEFAULT_ANONYMOUS_MESSAGES_LIMIT
        )

    @staticmethod
    def consume_message(session_id: str) -> dict:
        AnonymousQuotaService.ensure_session(session_id)

        consumed = AnonymousQuotaRepository.consume_message(session_id)
        quota = AnonymousQuotaRepository.get_quota(session_id) or {
            "messages_used": DEFAULT_ANONYMOUS_MESSAGES_LIMIT,
            "messages_limit": DEFAULT_ANONYMOUS_MESSAGES_LIMIT,
            "messages_remaining": 0,
        }

        if not consumed:
            raise AnonymousQuotaExceeded(quota)

        return quota
