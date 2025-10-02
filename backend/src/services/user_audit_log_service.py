# backend/src/services/user_audit_log_service.py
"""Servicio para registrar auditoría de acciones de administración sobre usuarios."""
from ..models.user_audit_log_model import UserAuditLogModel

class UserAuditLogService:
    @staticmethod
    def log(admin_id: int, user_id: int, accion: str, detalles: str = None):
        """Crea un registro de auditoría.
        Acciones válidas: crear | editar | eliminar | restablecer
        """
        return UserAuditLogModel.create_log(admin_id, user_id, accion, detalles)

    @staticmethod
    def get_all():
        return UserAuditLogModel.get_all_logs()

    @staticmethod
    def get_filtered(start_date=None, end_date=None, accion=None, admin_id=None, q=None, offset=0, limit=25):
        return UserAuditLogModel.get_logs_filtered(start_date, end_date, accion, admin_id, q, offset, limit)

    @staticmethod
    def get_admins():
        from ..database.db_connection import mysql
        from ..database.db_connection import get_cursor
        cur = get_cursor('dict')
        cur.execute("SELECT DISTINCT a.id, a.correo FROM user_audit_logs l JOIN usuarios a ON l.admin_id = a.id ORDER BY a.correo")
        admins = cur.fetchall()
        cur.close()
        return admins
    
    @staticmethod
    def get_recent_activity(limit=5):
        """Obtiene la actividad reciente para el dashboard."""
        return UserAuditLogModel.get_recent_activity(limit)
