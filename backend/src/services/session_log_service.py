# backend/src/services/session_log_service.py
"""Servicio para los registros de sesión."""
from ..models.session_log_model import SessionLogModel

class SessionLogService:
    @staticmethod
    def log_login(user_id: int, ip_address: str | None = None):
        return SessionLogModel.log_login(user_id, ip_address)

    @staticmethod
    def log_logout(session_id: int):
        SessionLogModel.log_logout(session_id)

    @staticmethod
    def get_all_logs():
        return SessionLogModel.get_all_logs()
    
    @staticmethod
    def get_session_statistics():
        """Obtiene estadísticas de sesiones para el dashboard."""
        return SessionLogModel.get_session_statistics()
    
    @staticmethod
    def get_active_sessions_count():
        """Obtiene el número de sesiones activas."""
        return SessionLogModel.get_active_sessions_count()
