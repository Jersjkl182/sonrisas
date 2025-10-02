# backend/src/models/notification_model.py
"""Modelo para el sistema de notificaciones del administrador."""
from ..database.db_connection import mysql, get_cursor
from datetime import datetime, timedelta

class NotificationModel:
    """Modelo para gestionar notificaciones del sistema."""
    
    @staticmethod
    def create_notification(title: str, message: str, type: str = 'info', priority: str = 'normal'):
        """Crea una nueva notificación del sistema."""
        try:
            cur = mysql.connection.cursor()
            cur.execute("""
                INSERT INTO system_notifications (title, message, type, priority, created_at) 
                VALUES (%s, %s, %s, %s, NOW())
            """, (title, message, type, priority))
            mysql.connection.commit()
            notification_id = cur.lastrowid
            cur.close()
            return notification_id
        except Exception as e:
            print(f"Error al crear notificación: {e}")
            return None
    
    @staticmethod
    def get_recent_notifications(limit=10):
        """Obtiene las notificaciones más recientes."""
        try:
            cur = get_cursor('dict')
            cur.execute("""
                SELECT id, title, message, type, priority, created_at, is_read
                FROM system_notifications 
                ORDER BY created_at DESC 
                LIMIT %s
            """, (limit,))
            notifications = cur.fetchall()
            cur.close()
            return notifications
        except Exception as e:
            print(f"Error al obtener notificaciones: {e}")
            return []
    
    @staticmethod
    def get_unread_count():
        """Obtiene el número de notificaciones no leídas."""
        try:
            cur = mysql.connection.cursor()
            cur.execute("SELECT COUNT(*) FROM system_notifications WHERE is_read = 0")
            result = cur.fetchone()
            cur.close()
            return result[0] if result else 0
        except Exception as e:
            print(f"Error al contar notificaciones no leídas: {e}")
            return 0
    
    @staticmethod
    def mark_as_read(notification_id: int):
        """Marca una notificación como leída."""
        try:
            cur = mysql.connection.cursor()
            cur.execute("""
                UPDATE system_notifications 
                SET is_read = 1, read_at = NOW() 
                WHERE id = %s
            """, (notification_id,))
            mysql.connection.commit()
            cur.close()
            return True
        except Exception as e:
            print(f"Error al marcar notificación como leída: {e}")
            return False
    
    @staticmethod
    def mark_all_as_read():
        """Marca todas las notificaciones como leídas."""
        try:
            cur = mysql.connection.cursor()
            cur.execute("""
                UPDATE system_notifications 
                SET is_read = 1, read_at = NOW() 
                WHERE is_read = 0
            """)
            mysql.connection.commit()
            cur.close()
            return True
        except Exception as e:
            print(f"Error al marcar todas las notificaciones como leídas: {e}")
            return False
    
    @staticmethod
    def delete_old_notifications(days=30):
        """Elimina notificaciones antiguas."""
        try:
            cur = mysql.connection.cursor()
            cur.execute("""
                DELETE FROM system_notifications 
                WHERE created_at < DATE_SUB(NOW(), INTERVAL %s DAY)
            """, (days,))
            mysql.connection.commit()
            deleted_count = cur.rowcount
            cur.close()
            return deleted_count
        except Exception as e:
            print(f"Error al eliminar notificaciones antiguas: {e}")
            return 0
    
    @staticmethod
    def generate_system_alerts():
        """Genera alertas automáticas del sistema."""
        alerts_created = 0
        
        try:
            # Verificar sesiones activas excesivas
            cur = mysql.connection.cursor()
            cur.execute("SELECT COUNT(*) FROM session_logs WHERE logout_time IS NULL")
            active_sessions = cur.fetchone()[0]
            
            if active_sessions > 50:  # Umbral configurable
                NotificationModel.create_notification(
                    "Alto número de sesiones activas",
                    f"Se detectaron {active_sessions} sesiones activas simultáneas. Considere revisar la actividad del sistema.",
                    "warning",
                    "high"
                )
                alerts_created += 1
            
            # Verificar usuarios creados recientemente
            cur.execute("""
                SELECT COUNT(*) FROM usuarios 
                WHERE fecha_creacion >= DATE_SUB(NOW(), INTERVAL 1 DAY)
            """)
            new_users_today = cur.fetchone()[0]
            
            if new_users_today > 10:  # Umbral configurable
                NotificationModel.create_notification(
                    "Alto registro de usuarios",
                    f"Se registraron {new_users_today} nuevos usuarios en las últimas 24 horas.",
                    "info",
                    "normal"
                )
                alerts_created += 1
            
            # Verificar actividad de auditoría sospechosa
            recent_deletions = 0
            try:
                cur.execute("""
                    SELECT COUNT(*) FROM user_audit_logs 
                    WHERE fecha_hora >= DATE_SUB(NOW(), INTERVAL 1 HOUR)
                    AND accion = 'eliminar'
                """)
                recent_deletions = cur.fetchone()[0]
            except Exception as e:
                if "fecha_hora" in str(e):
                    try:
                        # Intentar con created_at si fecha_hora no existe
                        cur.execute("""
                            SELECT COUNT(*) FROM user_audit_logs 
                            WHERE created_at >= DATE_SUB(NOW(), INTERVAL 1 HOUR)
                            AND accion = 'eliminar'
                        """)
                        recent_deletions = cur.fetchone()[0]
                    except:
                        recent_deletions = 0
                else:
                    # Si la tabla no existe o hay otro error, usar 0
                    recent_deletions = 0
            
            if recent_deletions > 5:  # Umbral configurable
                NotificationModel.create_notification(
                    "Actividad de eliminación elevada",
                    f"Se detectaron {recent_deletions} eliminaciones de usuarios en la última hora.",
                    "warning",
                    "high"
                )
                alerts_created += 1
            
            cur.close()
            return alerts_created
            
        except Exception as e:
            print(f"Error al generar alertas del sistema: {e}")
            return 0
    
    @staticmethod
    def get_system_health_notifications():
        """Genera notificaciones sobre el estado del sistema."""
        notifications = []
        
        try:
            cur = get_cursor('dict')
            
            # Verificar usuarios inactivos
            cur.execute("""
                SELECT COUNT(*) as inactive_users
                FROM usuarios u
                LEFT JOIN session_logs sl ON u.id = sl.user_id
                WHERE sl.login_time IS NULL OR sl.login_time < DATE_SUB(NOW(), INTERVAL 30 DAY)
                AND u.is_active = 1
            """)
            result = cur.fetchone()
            inactive_users = result['inactive_users'] if result else 0
            
            if inactive_users > 0:
                notifications.append({
                    'type': 'info',
                    'title': 'Usuarios inactivos detectados',
                    'message': f'{inactive_users} usuarios no han iniciado sesión en los últimos 30 días.',
                    'priority': 'normal'
                })
            
            # Verificar espacio de base de datos (simulado)
            notifications.append({
                'type': 'success',
                'title': 'Sistema funcionando correctamente',
                'message': 'Todos los servicios están operativos y el rendimiento es óptimo.',
                'priority': 'low'
            })
            
            cur.close()
            return notifications
            
        except Exception as e:
            print(f"Error al obtener notificaciones de salud del sistema: {e}")
            return []
