from backend.app.repositories.history_repository import HistoryRepository

class HistoryService:
    @staticmethod
    def get_user_messages(user_id):
        #on recupere tous les elements de la table message : content, role ect ...
       messages = HistoryRepository.get_messages_by_user(user_id)
       return messages