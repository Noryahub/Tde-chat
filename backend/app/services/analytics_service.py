from backend.app.repositories.analytics_repository import AnalyticsRepository


class AnalyticsService:

    @staticmethod
    def get_dashboard_analytics():

        top_intents = (
            AnalyticsRepository.get_top_intents()
        )

        top_localisations = (
            AnalyticsRepository.get_top_localisations()
        )

        return {
            "total_conversations":
                AnalyticsRepository.get_total_conversations(),

            "signalements_nouveaux":
                AnalyticsRepository.get_signalements_nouveaux(),

            "top_intents":
                top_intents,

            "top_localisations":
                top_localisations,

            "top_problemes":
                AnalyticsRepository.get_top_problemes(),

            "conversations_par_jour":
                AnalyticsRepository.get_conversations_par_jour(),
        }

    @staticmethod
    def get_latest_signalements(limit=8):
        return (
            AnalyticsRepository
            .get_latest_signalements(limit)
        )