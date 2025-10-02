# backend/src/models/session_log_model.py
"""Modelo de acceso a datos para la tabla `session_logs`.  Registra y consulta
las sesiones de los usuarios (inicio y cierre de sesión)."""
from ..database.db_connection import mysql, get_cursor

class SessionLogModel:
    @staticmethod
    def log_login(user_id: int, ip_address: str | None = None):
        """Crea un registro de inicio de sesión y devuelve el ID insertado."""
        cur = mysql.connection.cursor()
        cur.execute(
            """INSERT INTO session_logs (user_id, ip_address) VALUES (%s, %s)""",
            (user_id, ip_address),
        )
        session_id = cur.lastrowid
        mysql.connection.commit()
        cur.close()
        return session_id

    @staticmethod
    def log_logout(session_id: int):
        """Actualiza el registro indicado con la hora de cierre de sesión."""
        cur = mysql.connection.cursor()
        cur.execute(
            """UPDATE session_logs SET logout_time = CURRENT_TIMESTAMP WHERE id = %s""",
            (session_id,),
        )
        mysql.connection.commit()
        cur.close()

    @staticmethod
    def get_all_logs():
        """Devuelve todos los registros con datos de usuario (correo)."""
        cur = get_cursor('dict')
        cur.execute(
            """
            SELECT sl.id, sl.login_time, sl.logout_time, sl.ip_address,
                   u.correo AS usuario_correo, u.id AS user_id
            FROM session_logs sl
            JOIN usuarios u ON u.id = sl.user_id
            ORDER BY sl.login_time DESC
            """
        )
        rows = cur.fetchall()
        cur.close()
        return rows

    @staticmethod
    def get_user_session_stats(user_id: int):
        """Obtiene estadísticas de sesión para un usuario específico."""
        try:
            cur = get_cursor('dict')
            
            # Obtener total de sesiones
            cur.execute(
                "SELECT COUNT(*) as total_sessions FROM session_logs WHERE user_id = %s",
                (user_id,)
            )
            total_result = cur.fetchone()
            total_sessions = total_result['total_sessions'] if total_result else 0
            
            # Obtener sesiones activas (sin logout_time)
            cur.execute(
                "SELECT COUNT(*) as active_sessions FROM session_logs WHERE user_id = %s AND logout_time IS NULL",
                (user_id,)
            )
            active_result = cur.fetchone()
            active_sessions = active_result['active_sessions'] if active_result else 0
            
            # Obtener último login
            cur.execute(
                "SELECT login_time FROM session_logs WHERE user_id = %s ORDER BY login_time DESC LIMIT 1",
                (user_id,)
            )
            last_login_result = cur.fetchone()
            last_login = last_login_result['login_time'] if last_login_result else None
            
            cur.close()
            
            return {
                'total_sessions': total_sessions,
                'active_sessions': active_sessions,
                'last_login': last_login
            }
        except Exception as e:
            print(f"Error al obtener estadísticas de sesión: {e}")
            return {
                'total_sessions': 0,
                'active_sessions': 0,
                'last_login': None
            }
    
    @staticmethod
    def get_session_statistics():
        """Obtiene estadísticas generales de sesiones para el dashboard."""
        try:
            cur = get_cursor('dict')
            
            # Total de sesiones
            cur.execute("SELECT COUNT(*) as total_sessions FROM session_logs")
            total_result = cur.fetchone()
            total_sessions = total_result['total_sessions'] if total_result else 0
            
            # Sesiones activas (sin logout_time)
            cur.execute("SELECT COUNT(*) as active_sessions FROM session_logs WHERE logout_time IS NULL")
            active_result = cur.fetchone()
            active_sessions = active_result['active_sessions'] if active_result else 0
            
            # Sesiones de hoy
            cur.execute("""
                SELECT COUNT(*) as today_sessions 
                FROM session_logs 
                WHERE DATE(login_time) = CURDATE()
            """)
            today_result = cur.fetchone()
            today_sessions = today_result['today_sessions'] if today_result else 0
            
            # Usuarios únicos hoy
            cur.execute("""
                SELECT COUNT(DISTINCT user_id) as unique_users_today 
                FROM session_logs 
                WHERE DATE(login_time) = CURDATE()
            """)
            unique_result = cur.fetchone()
            unique_users_today = unique_result['unique_users_today'] if unique_result else 0
            
            cur.close()
            
            return {
                'total_sessions': total_sessions,
                'active_sessions': active_sessions,
                'today_sessions': today_sessions,
                'unique_users_today': unique_users_today
            }
        except Exception as e:
            print(f"Error al obtener estadísticas de sesiones: {e}")
            return {
                'total_sessions': 0,
                'active_sessions': 0,
                'today_sessions': 0,
                'unique_users_today': 0
            }
    
    @staticmethod
    def get_active_sessions_count():
        """Obtiene el número de sesiones activas."""
        try:
            cur = get_cursor('dict')
            cur.execute("SELECT COUNT(*) as active_sessions FROM session_logs WHERE logout_time IS NULL")
            result = cur.fetchone()
            cur.close()
            return result['active_sessions'] if result else 0
        except Exception as e:
            print(f"Error al obtener sesiones activas: {e}")
            return 0
