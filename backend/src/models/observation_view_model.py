"""ObservationViewModel
Modelo para gestionar las visualizaciones de observaciones por parte de los acudientes.
"""

from datetime import datetime
from ..database.db_connection import mysql, get_cursor

class ObservationViewModel:
    """Métodos para gestionar las visualizaciones de observaciones."""

    @staticmethod
    def mark_as_viewed(observation_id: int, acudiente_id: int, ip_address: str = None, user_agent: str = None):
        """Marca una observación como vista por un acudiente."""
        try:
            cur = get_cursor('dict')
            
            if cur is None:
                print("Error: No se pudo crear el cursor")
                return False
            
            # Usar INSERT ... ON DUPLICATE KEY UPDATE para evitar duplicados
            query = """
                INSERT INTO observation_views (observation_id, acudiente_id, viewed_at, ip_address, user_agent)
                VALUES (%s, %s, %s, %s, %s)
                ON DUPLICATE KEY UPDATE 
                    viewed_at = VALUES(viewed_at),
                    ip_address = VALUES(ip_address),
                    user_agent = VALUES(user_agent)
            """
            
            now = datetime.utcnow()
            cur.execute(query, (observation_id, acudiente_id, now, ip_address, user_agent))
            mysql.connection.commit()
            cur.close()
            
            print(f"DEBUG: Observación {observation_id} marcada como vista por acudiente {acudiente_id}")
            return True
            
        except Exception as e:
            print(f"Error al marcar observación como vista: {e}")
            import traceback
            traceback.print_exc()
            if 'cur' in locals():
                cur.close()
            return False

    @staticmethod
    def is_viewed_by_acudiente(observation_id: int, acudiente_id: int):
        """Verifica si una observación ha sido vista por un acudiente."""
        try:
            cur = get_cursor('dict')
            
            if cur is None:
                return False
            
            query = """
                SELECT id, viewed_at 
                FROM observation_views 
                WHERE observation_id = %s AND acudiente_id = %s
            """
            
            cur.execute(query, (observation_id, acudiente_id))
            result = cur.fetchone()
            cur.close()
            
            return result is not None
            
        except Exception as e:
            print(f"Error al verificar si observación fue vista: {e}")
            return False

    @staticmethod
    def get_viewed_observations_for_acudiente(acudiente_id: int):
        """Obtiene todas las observaciones vistas por un acudiente."""
        try:
            cur = get_cursor('dict')
            
            if cur is None:
                return []
            
            query = """
                SELECT ov.observation_id, ov.viewed_at,
                       o.titulo, o.descripcion, o.tipo_observacion, o.fecha,
                       e.nombre as estudiante_nombre, e.apellido as estudiante_apellido
                FROM observation_views ov
                JOIN observaciones o ON ov.observation_id = o.id
                JOIN estudiantes e ON o.id_estudiante = e.id
                WHERE ov.acudiente_id = %s
                ORDER BY ov.viewed_at DESC
            """
            
            cur.execute(query, (acudiente_id,))
            results = cur.fetchall()
            cur.close()
            
            return results
            
        except Exception as e:
            print(f"Error al obtener observaciones vistas: {e}")
            return []

    @staticmethod
    def get_unviewed_observations_for_acudiente(acudiente_id: int):
        """Obtiene las observaciones no vistas por un acudiente."""
        try:
            cur = get_cursor('dict')
            
            if cur is None:
                return []
            
            # Obtener estudiantes del acudiente
            cur.execute("SELECT id FROM estudiantes WHERE acudiente_id = %s", (acudiente_id,))
            estudiantes = cur.fetchall()
            
            if not estudiantes:
                cur.close()
                return []
            
            estudiante_ids = [est['id'] for est in estudiantes]
            placeholders = ','.join(['%s'] * len(estudiante_ids))
            
            query = f"""
                SELECT o.id, o.titulo, o.descripcion, o.tipo_observacion, o.fecha, o.hijo,
                       e.nombre as estudiante_nombre, e.apellido as estudiante_apellido,
                       u.nombre as profesor_nombre, u.apellido as profesor_apellido
                FROM observaciones o
                JOIN estudiantes e ON o.id_estudiante = e.id
                JOIN usuarios u ON o.id_profesor = u.id
                LEFT JOIN observation_views ov ON o.id = ov.observation_id AND ov.acudiente_id = %s
                WHERE o.id_estudiante IN ({placeholders}) AND ov.id IS NULL
                ORDER BY o.fecha DESC
            """
            
            params = [acudiente_id] + estudiante_ids
            cur.execute(query, params)
            results = cur.fetchall()
            cur.close()
            
            return results
            
        except Exception as e:
            print(f"Error al obtener observaciones no vistas: {e}")
            return []

    @staticmethod
    def get_view_statistics_for_acudiente(acudiente_id: int):
        """Obtiene estadísticas de visualización para un acudiente."""
        try:
            cur = get_cursor('dict')
            
            if cur is None:
                return {'total': 0, 'viewed': 0, 'unviewed': 0}
            
            # Obtener estudiantes del acudiente
            cur.execute("SELECT id FROM estudiantes WHERE acudiente_id = %s", (acudiente_id,))
            estudiantes = cur.fetchall()
            
            if not estudiantes:
                cur.close()
                return {'total': 0, 'viewed': 0, 'unviewed': 0}
            
            estudiante_ids = [est['id'] for est in estudiantes]
            placeholders = ','.join(['%s'] * len(estudiante_ids))
            
            # Total de observaciones
            query_total = f"""
                SELECT COUNT(*) as total
                FROM observaciones o
                WHERE o.id_estudiante IN ({placeholders})
            """
            cur.execute(query_total, estudiante_ids)
            total_result = cur.fetchone()
            total = total_result['total'] if total_result else 0
            
            # Observaciones vistas
            query_viewed = f"""
                SELECT COUNT(*) as viewed
                FROM observaciones o
                JOIN observation_views ov ON o.id = ov.observation_id
                WHERE o.id_estudiante IN ({placeholders}) AND ov.acudiente_id = %s
            """
            params_viewed = estudiante_ids + [acudiente_id]
            cur.execute(query_viewed, params_viewed)
            viewed_result = cur.fetchone()
            viewed = viewed_result['viewed'] if viewed_result else 0
            
            cur.close()
            
            unviewed = total - viewed
            
            return {
                'total': total,
                'viewed': viewed,
                'unviewed': unviewed,
                'percentage_viewed': round((viewed / total * 100) if total > 0 else 0, 1)
            }
            
        except Exception as e:
            print(f"Error al obtener estadísticas de visualización: {e}")
            return {'total': 0, 'viewed': 0, 'unviewed': 0, 'percentage_viewed': 0}

    @staticmethod
    def get_recent_views_for_acudiente(acudiente_id: int, limit: int = 10):
        """Obtiene las visualizaciones más recientes de un acudiente."""
        try:
            cur = get_cursor('dict')
            
            if cur is None:
                return []
            
            query = """
                SELECT ov.observation_id, ov.viewed_at,
                       o.titulo, o.descripcion, o.tipo_observacion, o.fecha,
                       e.nombre as estudiante_nombre, e.apellido as estudiante_apellido,
                       u.nombre as profesor_nombre, u.apellido as profesor_apellido
                FROM observation_views ov
                JOIN observaciones o ON ov.observation_id = o.id
                JOIN estudiantes e ON o.id_estudiante = e.id
                JOIN usuarios u ON o.id_profesor = u.id
                WHERE ov.acudiente_id = %s
                ORDER BY ov.viewed_at DESC
                LIMIT %s
            """
            
            cur.execute(query, (acudiente_id, limit))
            results = cur.fetchall()
            cur.close()
            
            return results
            
        except Exception as e:
            print(f"Error al obtener visualizaciones recientes: {e}")
            return []

    @staticmethod
    def bulk_mark_as_viewed(observation_ids: list, acudiente_id: int, ip_address: str = None, user_agent: str = None):
        """Marca múltiples observaciones como vistas de una vez."""
        try:
            cur = get_cursor('dict')
            
            if cur is None or not observation_ids:
                return False
            
            now = datetime.utcnow()
            
            # Preparar datos para inserción múltiple
            values = []
            for obs_id in observation_ids:
                values.append((obs_id, acudiente_id, now, ip_address, user_agent))
            
            query = """
                INSERT INTO observation_views (observation_id, acudiente_id, viewed_at, ip_address, user_agent)
                VALUES (%s, %s, %s, %s, %s)
                ON DUPLICATE KEY UPDATE 
                    viewed_at = VALUES(viewed_at),
                    ip_address = VALUES(ip_address),
                    user_agent = VALUES(user_agent)
            """
            
            cur.executemany(query, values)
            mysql.connection.commit()
            cur.close()
            
            print(f"DEBUG: {len(observation_ids)} observaciones marcadas como vistas por acudiente {acudiente_id}")
            return True
            
        except Exception as e:
            print(f"Error al marcar observaciones como vistas en lote: {e}")
            import traceback
            traceback.print_exc()
            if 'cur' in locals():
                cur.close()
            return False
