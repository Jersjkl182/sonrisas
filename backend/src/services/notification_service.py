# backend/src/services/notification_service.py
"""Servicio para el sistema de notificaciones."""
from ..models.notification_model import NotificationModel

class NotificationService:
    """Servicio para gestionar notificaciones del sistema."""
    
    @staticmethod
    def create_notification(title: str, message: str, type: str = 'info', priority: str = 'normal'):
        """Crea una nueva notificación."""
        return NotificationModel.create_notification(title, message, type, priority)
    
    @staticmethod
    def get_dashboard_notifications():
        """Obtiene notificaciones para el dashboard."""
        try:
            # Obtener notificaciones recientes
            recent_notifications = NotificationModel.get_recent_notifications(5)
            
            # Obtener notificaciones de salud del sistema
            health_notifications = NotificationModel.get_system_health_notifications()
            
            # Generar alertas automáticas si es necesario
            NotificationModel.generate_system_alerts()
            
            # Combinar todas las notificaciones
            # Asegurar que recent_notifications sea una lista
            if recent_notifications is None:
                recent_notifications = []
            elif isinstance(recent_notifications, tuple):
                recent_notifications = list(recent_notifications)
            
            # Asegurar que health_notifications sea una lista
            if health_notifications is None:
                health_notifications = []
            elif isinstance(health_notifications, tuple):
                health_notifications = list(health_notifications)
            
            health_notifications_formatted = [
                {
                    'id': f'health_{i}',
                    'title': notif['title'],
                    'message': notif['message'],
                    'type': notif['type'],
                    'priority': notif['priority'],
                    'created_at': 'now',
                    'is_read': 0
                }
                for i, notif in enumerate(health_notifications)
            ]
            
            all_notifications = recent_notifications + health_notifications_formatted
            
            return {
                'notifications': all_notifications,
                'unread_count': NotificationModel.get_unread_count(),
                'total_count': len(all_notifications)
            }
        except Exception as e:
            print(f"Error al obtener notificaciones del dashboard: {e}")
            return {
                'notifications': [],
                'unread_count': 0,
                'total_count': 0
            }
    
    @staticmethod
    def mark_as_read(notification_id: int):
        """Marca una notificación como leída."""
        return NotificationModel.mark_as_read(notification_id)
    
    @staticmethod
    def mark_all_as_read():
        """Marca todas las notificaciones como leídas."""
        return NotificationModel.mark_all_as_read()
    
    @staticmethod
    def cleanup_old_notifications():
        """Limpia notificaciones antiguas."""
        return NotificationModel.delete_old_notifications(30)
    
    @staticmethod
    def create_user_activity_notification(action: str, user_email: str, admin_email: str):
        """Crea notificación para actividad de usuario."""
        action_messages = {
            'crear': f'Nuevo usuario creado: {user_email} por {admin_email}',
            'editar': f'Usuario modificado: {user_email} por {admin_email}',
            'eliminar': f'Usuario eliminado: {user_email} por {admin_email}',
            'restablecer': f'Contraseña restablecida para: {user_email} por {admin_email}'
        }
        
        message = action_messages.get(action, f'Acción {action} realizada en {user_email}')
        notification_type = 'warning' if action == 'eliminar' else 'info'
        priority = 'high' if action == 'eliminar' else 'normal'
        
        return NotificationModel.create_notification(
            f'Actividad de Usuario - {action.title()}',
            message,
            notification_type,
            priority
        )
    
    @staticmethod
    def create_session_notification(session_count: int):
        """Crea notificación para actividad de sesiones."""
        if session_count > 20:
            return NotificationModel.create_notification(
                'Alta actividad de sesiones',
                f'Se detectaron {session_count} sesiones activas simultáneas.',
                'warning',
                'normal'
            )
        return None
    
    @staticmethod
    def create_system_notification(title: str, message: str, type: str = 'info'):
        """Crea notificación del sistema."""
        return NotificationModel.create_notification(title, message, type, 'normal')
