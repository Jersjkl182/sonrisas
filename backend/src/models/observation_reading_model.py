"""
Modelo para gestionar las lecturas de observaciones por parte de los acudientes
Permite registrar cuando un acudiente ha leído una observación y consultar el estado
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

try:
    import MySQLdb
except ImportError:
    import pymysql as MySQLdb

from database.db_connection import get_cursor

class ObservationReadingModel:
    
    @staticmethod
    def mark_as_read(observation_id, acudiente_id, ip_address=None, user_agent=None):
        """
        Marca una observación como leída por un acudiente
        
        Args:
            observation_id (int): ID de la observación
            acudiente_id (int): ID del acudiente
            ip_address (str, optional): Dirección IP del acudiente
            user_agent (str, optional): User agent del navegador
            
        Returns:
            bool: True si se marcó correctamente, False en caso contrario
        """
        try:
            cursor = get_cursor()
            
            # Usar INSERT IGNORE para evitar duplicados
            query = """
                INSERT IGNORE INTO observation_readings 
                (observation_id, acudiente_id, ip_address, user_agent, read_at)
                VALUES (%s, %s, %s, %s, NOW())
            """
            
            cursor.execute(query, (observation_id, acudiente_id, ip_address, user_agent))
            cursor.connection.commit()
            
            # Verificar si se insertó una nueva fila
            rows_affected = cursor.rowcount
            cursor.close()
            
            return rows_affected > 0
            
        except Exception as e:
            print(f"Error al marcar observación como leída: {e}")
            return False
    
    @staticmethod
    def is_read_by_acudiente(observation_id, acudiente_id):
        """
        Verifica si una observación ha sido leída por un acudiente específico
        
        Args:
            observation_id (int): ID de la observación
            acudiente_id (int): ID del acudiente
            
        Returns:
            dict: Información de lectura o None si no ha sido leída
        """
        try:
            cursor = get_cursor('dict')
            
            query = """
                SELECT id, read_at, ip_address
                FROM observation_readings
                WHERE observation_id = %s AND acudiente_id = %s
                LIMIT 1
            """
            
            cursor.execute(query, (observation_id, acudiente_id))
            result = cursor.fetchone()
            cursor.close()
            
            return result
            
        except Exception as e:
            print(f"Error al verificar lectura de observación: {e}")
            return None
    
    @staticmethod
    def get_reading_status_for_observation(observation_id):
        """
        Obtiene el estado de lectura de una observación por todos los acudientes relacionados
        
        Args:
            observation_id (int): ID de la observación
            
        Returns:
            dict: Estado de lectura con información detallada
        """
        try:
            cursor = get_cursor('dict')
            
            # Obtener información de la observación y el acudiente relacionado
            query = """
                SELECT 
                    o.id as observation_id,
                    o.titulo,
                    o.id_acudiente,
                    u.nombre as acudiente_nombre,
                    u.apellido as acudiente_apellido,
                    u.correo as acudiente_correo,
                    or_read.read_at,
                    or_read.ip_address,
                    CASE 
                        WHEN or_read.id IS NOT NULL THEN 'leida'
                        ELSE 'no_leida'
                    END as estado_lectura
                FROM observaciones o
                LEFT JOIN usuarios u ON o.id_acudiente = u.id
                LEFT JOIN observation_readings or_read ON o.id = or_read.observation_id AND o.id_acudiente = or_read.acudiente_id
                WHERE o.id = %s
            """
            
            cursor.execute(query, (observation_id,))
            result = cursor.fetchone()
            cursor.close()
            
            return result
            
        except Exception as e:
            print(f"Error al obtener estado de lectura: {e}")
            return None
    
    @staticmethod
    def get_unread_observations_for_acudiente(acudiente_id):
        """
        Obtiene las observaciones no leídas para un acudiente específico
        
        Args:
            acudiente_id (int): ID del acudiente
            
        Returns:
            list: Lista de observaciones no leídas
        """
        try:
            cursor = get_cursor('dict')
            
            query = """
                SELECT 
                    o.id,
                    o.titulo,
                    o.descripcion,
                    o.tipo_observacion,
                    o.fecha,
                    o.hijo,
                    u_prof.nombre as profesor_nombre,
                    u_prof.apellido as profesor_apellido
                FROM observaciones o
                LEFT JOIN usuarios u_prof ON o.id_profesor = u_prof.id
                LEFT JOIN observation_readings or_read ON o.id = or_read.observation_id AND or_read.acudiente_id = %s
                WHERE o.id_acudiente = %s 
                AND or_read.id IS NULL
                ORDER BY o.fecha DESC
            """
            
            cursor.execute(query, (acudiente_id, acudiente_id))
            results = cursor.fetchall()
            cursor.close()
            
            return results if results else []
            
        except Exception as e:
            print(f"Error al obtener observaciones no leídas: {e}")
            return []
    
    @staticmethod
    def get_reading_statistics_for_profesor(profesor_id):
        """
        Obtiene estadísticas de lectura de observaciones para un profesor
        
        Args:
            profesor_id (int): ID del profesor
            
        Returns:
            dict: Estadísticas de lectura
        """
        try:
            cursor = get_cursor('dict')
            
            query = """
                SELECT 
                    COUNT(o.id) as total_observaciones,
                    COUNT(or_read.id) as observaciones_leidas,
                    COUNT(o.id) - COUNT(or_read.id) as observaciones_no_leidas,
                    ROUND((COUNT(or_read.id) / COUNT(o.id)) * 100, 2) as porcentaje_lectura
                FROM observaciones o
                LEFT JOIN observation_readings or_read ON o.id = or_read.observation_id AND o.id_acudiente = or_read.acudiente_id
                WHERE o.id_profesor = %s
                AND o.id_acudiente IS NOT NULL
            """
            
            cursor.execute(query, (profesor_id,))
            result = cursor.fetchone()
            cursor.close()
            
            return result if result else {
                'total_observaciones': 0,
                'observaciones_leidas': 0,
                'observaciones_no_leidas': 0,
                'porcentaje_lectura': 0
            }
            
        except Exception as e:
            print(f"Error al obtener estadísticas de lectura: {e}")
            return {
                'total_observaciones': 0,
                'observaciones_leidas': 0,
                'observaciones_no_leidas': 0,
                'porcentaje_lectura': 0
            }
    
    @staticmethod
    def get_observations_with_reading_status(profesor_id):
        """
        Obtiene todas las observaciones de un profesor con su estado de lectura
        
        Args:
            profesor_id (int): ID del profesor
            
        Returns:
            list: Lista de observaciones con estado de lectura
        """
        try:
            cursor = get_cursor('dict')
            
            query = """
                SELECT 
                    o.id,
                    o.titulo,
                    o.descripcion,
                    o.tipo_observacion,
                    o.fecha,
                    o.hijo,
                    o.id_acudiente,
                    u_acud.nombre as acudiente_nombre,
                    u_acud.apellido as acudiente_apellido,
                    u_acud.correo as acudiente_correo,
                    or_read.read_at,
                    CASE 
                        WHEN or_read.id IS NOT NULL THEN 'leida'
                        WHEN o.id_acudiente IS NULL THEN 'sin_acudiente'
                        ELSE 'no_leida'
                    END as estado_lectura,
                    CASE 
                        WHEN or_read.id IS NOT NULL THEN '✅'
                        WHEN o.id_acudiente IS NULL THEN '⚠️'
                        ELSE '❌'
                    END as icono_estado
                FROM observaciones o
                LEFT JOIN usuarios u_acud ON o.id_acudiente = u_acud.id
                LEFT JOIN observation_readings or_read ON o.id = or_read.observation_id AND o.id_acudiente = or_read.acudiente_id
                WHERE o.id_profesor = %s
                ORDER BY o.fecha DESC
            """
            
            cursor.execute(query, (profesor_id,))
            results = cursor.fetchall()
            cursor.close()
            
            return results if results else []
            
        except Exception as e:
            print(f"Error al obtener observaciones con estado de lectura: {e}")
            return []
