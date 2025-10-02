# backend/src/models/user_audit_log_model.py
"""Modelo para registrar y consultar logs de auditoría relacionados con acciones sobre usuarios.

Tabla: user_audit_logs (id, admin_id, user_id, accion, detalles, fecha)
"""
from ..database.db_connection import mysql, get_cursor

class UserAuditLogModel:
    @staticmethod
    def create_log(admin_id: int, user_id: int, accion: str, detalles: str = None):
        try:
            cur = mysql.connection.cursor()
            cur.execute(
                """INSERT INTO user_audit_logs (admin_id, user_id, accion, detalles)
                   VALUES (%s, %s, %s, %s)""",
                (admin_id, user_id, accion, detalles)
            )
            mysql.connection.commit()
            cur.close()
            return True
        except Exception as e:
            print(f"[UserAuditLogModel] Error al crear log: {e}")
            return False

    @staticmethod
    def get_all_logs():
        """Devuelve los registros con correos de admin y usuario."""
        cur = get_cursor('dict')
        query = (
            "SELECT l.*, "
            "a.correo AS admin_correo, "
            "u.correo AS user_correo "
            "FROM user_audit_logs l "
            "LEFT JOIN usuarios a ON l.admin_id = a.id "
            "LEFT JOIN usuarios u ON l.user_id = u.id "
            "ORDER BY l.fecha DESC"
        )
        cur.execute(query)
        logs = cur.fetchall()
        cur.close()
        return logs

    @staticmethod
    def get_logs_filtered(start_date=None, end_date=None, accion=None, admin_id=None, q=None, offset=0, limit=25):
        """Devuelve logs aplicando filtros opcionales y paginación."""
        cur = get_cursor('dict')
        base_query = (
            "SELECT l.*, a.correo AS admin_correo, u.correo AS user_correo "
            "FROM user_audit_logs l "
            "LEFT JOIN usuarios a ON l.admin_id = a.id "
            "LEFT JOIN usuarios u ON l.user_id = u.id "
        )
        conditions = []
        params = []
        if start_date:
            conditions.append("l.fecha >= %s")
            params.append(start_date)
        if end_date:
            conditions.append("l.fecha <= %s")
            params.append(end_date)
        if accion:
            conditions.append("l.accion = %s")
            params.append(accion)
        if admin_id:
            conditions.append("l.admin_id = %s")
            params.append(admin_id)
        if q:
            conditions.append("(l.detalles LIKE %s OR a.correo LIKE %s OR u.correo LIKE %s OR l.accion LIKE %s)")
            like = f"%{q}%"
            params.extend([like, like, like, like])
        if conditions:
            base_query += " WHERE " + " AND ".join(conditions)
        base_query += " ORDER BY l.fecha DESC LIMIT %s OFFSET %s"
        params.extend([limit, offset])
        cur.execute(base_query, tuple(params))
        logs = cur.fetchall()
        cur.close()
        return logs

    @staticmethod
    def get_users_created_by_admin(admin_id: int):
        """Obtiene el número de usuarios creados por un administrador específico."""
        try:
            cur = mysql.connection.cursor()
            cur.execute(
                "SELECT COUNT(*) FROM user_audit_logs WHERE admin_id = %s AND accion = 'crear_usuario'",
                (admin_id,)
            )
            result = cur.fetchone()
            cur.close()
            return result[0] if result else 0
        except Exception as e:
            print(f"Error al obtener usuarios creados por admin: {e}")
            return 0

    @staticmethod
    def get_total_modifications_by_admin(admin_id: int):
        """Obtiene el número total de modificaciones realizadas por un administrador."""
        try:
            cur = mysql.connection.cursor()
            cur.execute(
                "SELECT COUNT(*) FROM user_audit_logs WHERE admin_id = %s",
                (admin_id,)
            )
            result = cur.fetchone()
            cur.close()
            return result[0] if result else 0
        except Exception as e:
            print(f"Error al obtener modificaciones por admin: {e}")
            return 0
    
    @staticmethod
    def get_recent_activity(limit=5):
        """Obtiene la actividad reciente para el dashboard."""
        try:
            cur = get_cursor('dict')
            # Primero intentar con fecha_hora, luego con created_at como fallback
            try:
                cur.execute("""
                    SELECT 
                        ual.accion,
                        ual.detalles,
                        ual.fecha_hora,
                        admin.correo as admin_correo,
                        admin.nombre as admin_nombre,
                        user.correo as user_correo,
                        user.nombre as user_nombre
                    FROM user_audit_logs ual
                    JOIN usuarios admin ON ual.admin_id = admin.id
                    LEFT JOIN usuarios user ON ual.user_id = user.id
                    ORDER BY ual.fecha_hora DESC
                    LIMIT %s
                """, (limit,))
            except Exception as e:
                if "fecha_hora" in str(e):
                    # Intentar con created_at si fecha_hora no existe
                    cur.execute("""
                        SELECT 
                            ual.accion,
                            ual.detalles,
                            ual.created_at as fecha_hora,
                            admin.correo as admin_correo,
                            admin.nombre as admin_nombre,
                            user.correo as user_correo,
                            user.nombre as user_nombre
                        FROM user_audit_logs ual
                        JOIN usuarios admin ON ual.admin_id = admin.id
                        LEFT JOIN usuarios user ON ual.user_id = user.id
                        ORDER BY ual.created_at DESC
                        LIMIT %s
                    """, (limit,))
                else:
                    raise e
            
            activities = cur.fetchall()
            cur.close()
            
            # Formatear las actividades para el dashboard
            formatted_activities = []
            for activity in activities:
                activity_type = 'user'
                activity_title = f"Acción: {activity['accion']}"
                activity_description = activity['detalles'] or f"Usuario afectado: {activity['user_correo'] or 'N/A'}"
                
                if activity['accion'] == 'crear':
                    activity_type = 'user'
                    activity_title = "Nuevo usuario creado"
                    activity_description = f"Se creó el usuario {activity['user_correo'] or 'N/A'}"
                elif activity['accion'] == 'editar':
                    activity_type = 'session'
                    activity_title = "Usuario modificado"
                    activity_description = f"Se editó el usuario {activity['user_correo'] or 'N/A'}"
                elif activity['accion'] == 'eliminar':
                    activity_type = 'observation'
                    activity_title = "Usuario eliminado"
                    activity_description = f"Se eliminó el usuario {activity['user_correo'] or 'N/A'}"
                
                formatted_activities.append({
                    'type': activity_type,
                    'title': activity_title,
                    'description': activity_description,
                    'time': activity['fecha_hora'],
                    'admin': activity['admin_correo']
                })
            
            return formatted_activities
        except Exception as e:
            print(f"Error al obtener actividad reciente: {e}")
            import traceback
            traceback.print_exc()
            return []
