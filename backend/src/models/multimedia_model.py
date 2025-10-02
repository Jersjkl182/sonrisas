# backend/src/models/multimedia_model.py

from ..database.db_connection import mysql, get_cursor
from datetime import datetime
import os

class MultimediaModel:
    """Modelo para gestionar archivos multimedia (fotos y videos) asociados a observaciones."""
    
    @staticmethod
    def create_multimedia(observation_id, filename, file_type, file_path, file_size, uploaded_by):
        """Crea un nuevo registro de archivo multimedia."""
        try:
            cur = mysql.connection.cursor()
            query = """
                INSERT INTO multimedia (observacion_id, nombre_archivo, tipo_archivo, ruta_archivo, 
                                     tamaño_archivo, fecha_subida) 
                VALUES (%s, %s, %s, %s, %s, %s)
            """
            upload_date = datetime.utcnow()
            cur.execute(query, (observation_id, filename, file_type, file_path, 
                              file_size, upload_date))
            mysql.connection.commit()
            multimedia_id = cur.lastrowid
            cur.close()
            return multimedia_id
        except Exception as e:
            print(f"Error al crear archivo multimedia: {e}")
            return None

    @staticmethod
    def get_multimedia_by_observation(observation_id):
        """Obtiene todos los archivos multimedia de una observación."""
        try:
            cur = get_cursor('dict')
            query = """
                SELECT m.id, m.observacion_id as observation_id, m.nombre_archivo as filename, 
                       m.tipo_archivo as file_type, m.ruta_archivo as file_path, 
                       m.tamaño_archivo as file_size, m.fecha_subida as upload_date
                FROM multimedia m
                WHERE m.observacion_id = %s
                ORDER BY m.fecha_subida DESC
            """
            cur.execute(query, (observation_id,))
            files = cur.fetchall()
            cur.close()
            return files
        except Exception as e:
            print(f"Error al obtener archivos multimedia: {e}")
            return []

    @staticmethod
    def get_multimedia_by_id(multimedia_id):
        """Obtiene un archivo multimedia por su ID."""
        try:
            cur = get_cursor('dict')
            query = """
                SELECT m.id, m.observacion_id as observation_id, m.nombre_archivo as filename, 
                       m.tipo_archivo as file_type, m.ruta_archivo as file_path, 
                       m.tamaño_archivo as file_size, m.fecha_subida as upload_date
                FROM multimedia m
                WHERE m.id = %s
            """
            cur.execute(query, (multimedia_id,))
            file_data = cur.fetchone()
            cur.close()
            return file_data
        except Exception as e:
            print(f"Error al obtener archivo multimedia: {e}")
            return None

    @staticmethod
    def get_multimedia_by_student(student_id):
        """Obtiene todos los archivos multimedia de un estudiante a través de sus observaciones."""
        try:
            cur = get_cursor('dict')
            query = """
                SELECT m.*, o.descripcion as observation_description, 
                       u.nombre as uploader_name, u.apellido as uploader_surname,
                       e.nombre as student_name, e.apellido as student_surname
                FROM multimedia m
                JOIN observaciones o ON m.observation_id = o.id
                JOIN estudiantes e ON o.id_estudiante = e.id
                LEFT JOIN usuarios u ON m.uploaded_by = u.id
                WHERE o.id_estudiante = %s AND m.is_active = TRUE
                ORDER BY m.upload_date DESC
            """
            cur.execute(query, (student_id,))
            files = cur.fetchall()
            cur.close()
            return files
        except Exception as e:
            print(f"Error al obtener archivos multimedia del estudiante: {e}")
            return []

    @staticmethod
    def delete_multimedia(multimedia_id):
        """Elimina un archivo multimedia (hard delete ya que no hay columna is_active)."""
        try:
            cur = mysql.connection.cursor()
            cur.execute("DELETE FROM multimedia WHERE id = %s", (multimedia_id,))
            mysql.connection.commit()
            cur.close()
            return True
        except Exception as e:
            print(f"Error al eliminar archivo multimedia: {e}")
            return False

    @staticmethod
    def get_total_multimedia_count():
        """Obtiene el número total de archivos multimedia activos."""
        try:
            cur = mysql.connection.cursor()
            cur.execute("SELECT COUNT(*) FROM multimedia WHERE is_active = TRUE")
            result = cur.fetchone()
            cur.close()
            return result[0] if result else 0
        except Exception as e:
            print(f"Error al obtener conteo de archivos multimedia: {e}")
            return 0

    @staticmethod
    def get_multimedia_stats():
        """Obtiene estadísticas de archivos multimedia."""
        try:
            cur = get_cursor('dict')
            
            # Total de archivos por tipo
            cur.execute("""
                SELECT file_type, COUNT(*) as count
                FROM multimedia 
                WHERE is_active = TRUE
                GROUP BY file_type
            """)
            type_stats = cur.fetchall()
            
            # Tamaño total de archivos
            cur.execute("""
                SELECT SUM(file_size) as total_size
                FROM multimedia 
                WHERE is_active = TRUE
            """)
            size_result = cur.fetchone()
            total_size = size_result['total_size'] if size_result and size_result['total_size'] else 0
            
            cur.close()
            
            return {
                'type_stats': type_stats,
                'total_size': total_size
            }
        except Exception as e:
            print(f"Error al obtener estadísticas de multimedia: {e}")
            return {'type_stats': [], 'total_size': 0}

    @staticmethod
    def update_file_path(multimedia_id, new_path):
        """Actualiza la ruta de un archivo multimedia."""
        try:
            cur = mysql.connection.cursor()
            cur.execute("UPDATE multimedia SET file_path = %s WHERE id = %s", (new_path, multimedia_id))
            mysql.connection.commit()
            cur.close()
            return True
        except Exception as e:
            print(f"Error al actualizar ruta del archivo: {e}")
            return False

    @staticmethod
    def validate_file_type(filename):
        """Valida si el tipo de archivo es permitido."""
        allowed_extensions = {
            'image': ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.webp'],
            'video': ['.mp4', '.avi', '.mov', '.wmv', '.flv', '.webm']
        }
        
        file_ext = os.path.splitext(filename)[1].lower()
        
        for file_type, extensions in allowed_extensions.items():
            if file_ext in extensions:
                return file_type
        
        return None

    @staticmethod
    def get_file_type_from_extension(filename):
        """Determina el tipo de archivo basado en la extensión."""
        file_ext = os.path.splitext(filename)[1].lower()
        
        image_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.webp']
        video_extensions = ['.mp4', '.avi', '.mov', '.wmv', '.flv', '.webm']
        
        if file_ext in image_extensions:
            return 'image'
        elif file_ext in video_extensions:
            return 'video'
        else:
            return 'unknown'
