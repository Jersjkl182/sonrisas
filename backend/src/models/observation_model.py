"""ObservationModel
Modelo de acceso a datos para las notas de observación.
Cada nota es creada por un Administrador y está asociada a un Acudiente
(padre/madre/tutor) y al nombre de un niño o niña.
"""

from datetime import datetime
from ..database.db_connection import mysql, get_cursor

class ObservationModel:
    """Métodos CRUD para la tabla `observaciones`."""

    @staticmethod
    def _tiene_columna_tipo():
        """Verifica si la tabla observaciones tiene la columna 'tipo'."""
        try:
            cur = mysql.connection.cursor()
            # Usar una consulta que falle si la columna no existe
            cur.execute("SELECT tipo FROM observaciones LIMIT 1")
            cur.close()
            return True
        except Exception:
            # Si falla, la columna no existe
            return False

    # ----------------- Create -----------------
    @staticmethod
    def create(titulo: str, descripcion: str, id_profesor: int, id_estudiante: int, tipo: str = 'Positiva') -> int:
        """Crea una nueva observación y devuelve el ID generado (creada por un profesor)."""
        try:
            cur = get_cursor('dict')
            
            if cur is None:
                print("Error: No se pudo crear el cursor")
                return None
            
            print(f"DEBUG: Creando observación - Profesor: {id_profesor}, Estudiante: {id_estudiante}, Tipo: {tipo}")
            
            # Verificar que el estudiante existe y obtener sus datos
            cur.execute("SELECT id, nombre, apellido, acudiente_id FROM estudiantes WHERE id = %s", (id_estudiante,))
            estudiante = cur.fetchone()
            
            if not estudiante:
                cur.close()
                raise ValueError(f"El estudiante con ID {id_estudiante} no existe")
            
            # Obtener datos del estudiante
            id_acudiente = estudiante.get('acudiente_id') if estudiante else None
            
            # Usar la estructura real de la tabla observaciones
            query = """
                INSERT INTO observaciones (titulo, descripcion, tipo_observacion, hijo, id_profesor, id_acudiente, id_estudiante, fecha) 
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """
            
            now = datetime.utcnow()
            # hijo se puede derivar del nombre del estudiante o usar un valor por defecto
            hijo_nombre = f"{estudiante['nombre']} {estudiante['apellido']}" if estudiante and estudiante.get('nombre') and estudiante.get('apellido') else "Estudiante"
            
            cur.execute(query, (titulo, descripcion, tipo, hijo_nombre, id_profesor, id_acudiente, id_estudiante, now))
            
            mysql.connection.commit()
            new_id = cur.lastrowid
            cur.close()
            
            print(f"DEBUG: Observación creada con ID: {new_id}")
            return new_id
            
        except Exception as e:
            print(f"Error al crear observación: {e}")
            import traceback
            traceback.print_exc()
            if 'cur' in locals():
                cur.close()
            raise e

    # ----------------- Read -----------------
    @staticmethod
    def get_by_id(obs_id: int):
        cur = get_cursor('dict')
        cur.execute("SELECT * FROM observaciones WHERE id = %s", (obs_id,))
        row = cur.fetchone()
        cur.close()
        return row

    @staticmethod
    def get_all_for_profesor(id_profesor: int):
        """Devuelve todas las notas creadas por un profesor con información del estudiante."""
        try:
            cur = get_cursor('dict')
            
            print(f"DEBUG: Buscando observaciones para profesor ID: {id_profesor}")
            
            # Consulta actualizada para la estructura real de la tabla
            query = """
                SELECT o.id, o.titulo, o.descripcion, o.tipo_observacion, o.fecha, o.hijo,
                       o.id_estudiante, o.id_profesor, o.id_acudiente,
                       e.nombre as estudiante_nombre, e.apellido as estudiante_apellido, e.grado,
                       u.nombre as profesor_nombre, u.apellido as profesor_apellido
                FROM observaciones o
                JOIN estudiantes e ON o.id_estudiante = e.id
                JOIN usuarios u ON o.id_profesor = u.id
                WHERE o.id_profesor = %s 
                ORDER BY o.fecha DESC
            """
            
            cur.execute(query, (id_profesor,))
            rows = cur.fetchall()
            cur.close()
            
            print(f"DEBUG: Encontradas {len(rows)} observaciones para el profesor")
            # Convertir al formato esperado por el template
            formatted_rows = []
            for row in rows:
                formatted_rows.append({
                    'id': row['id'],
                    'titulo': row['titulo'] or f"Observación de {row['estudiante_nombre']}",
                    'descripcion': row['descripcion'],
                    'tipo': row['tipo_observacion'],  # Mapear correctamente
                    'fecha': row['fecha'],
                    'hijo': row['hijo'],
                    'estudiante_nombre': row['estudiante_nombre'],
                    'estudiante_apellido': row['estudiante_apellido'],
                    'grado': row['grado'],
                    'profesor_nombre': row['profesor_nombre'],
                    'profesor_apellido': row['profesor_apellido'],
                    'id_acudiente': row['id_acudiente']
                })
            
            return formatted_rows
        except Exception as e:
            print(f"Error al obtener observaciones del profesor: {e}")
            import traceback
            traceback.print_exc()
            return []

    @staticmethod
    def get_observations_by_student(id_estudiante: int):
        """Devuelve todas las observaciones de un estudiante específico."""
        try:
            cur = get_cursor('dict')
            
            # Consulta actualizada para la estructura real de la tabla
            query = """
                SELECT o.id, o.titulo, o.descripcion, o.tipo_observacion, o.fecha, o.hijo,
                       o.id_estudiante, o.id_profesor, o.id_acudiente,
                       e.nombre as estudiante_nombre, e.apellido as estudiante_apellido, e.grado,
                       u.nombre as profesor_nombre, u.apellido as profesor_apellido
                FROM observaciones o
                JOIN estudiantes e ON o.id_estudiante = e.id
                JOIN usuarios u ON o.id_profesor = u.id
                WHERE o.id_estudiante = %s 
                ORDER BY o.fecha DESC
            """
            
            print(f"DEBUG: Buscando observaciones para estudiante ID: {id_estudiante}")
            cur.execute(query, (id_estudiante,))
            rows = cur.fetchall()
            cur.close()
            
            print(f"DEBUG: Encontradas {len(rows)} observaciones")
            
            # Convertir a formato esperado por el frontend
            observations = []
            for row in rows:
                observations.append({
                    'id': row['id'],
                    'titulo': f"Observación de {row['estudiante_nombre']}", # Generar título si no existe
                    'descripcion': row['descripcion'],
                    'tipo': 'Positiva', # Valor por defecto ya que no existe la columna
                    'fecha': row['fecha'],
                    'hijo': f"{row['estudiante_nombre']} {row['estudiante_apellido']}", # Generar nombre completo
                    'id_estudiante': row['id_estudiante'],
                    'id_profesor': row['id_profesor'],
                    'id_acudiente': None, # No disponible en nueva estructura
                    'estudiante_nombre': row['estudiante_nombre'],
                    'estudiante_apellido': row['estudiante_apellido'],
                    'grado': row['grado'],
                    'profesor_nombre': row['profesor_nombre'],
                    'profesor_apellido': row['profesor_apellido']
                })
            
            return observations
            
        except Exception as e:
            print(f"Error al obtener observaciones por estudiante: {e}")
            import traceback
            traceback.print_exc()
            return []

    @staticmethod
    def get_for_acudiente(id_acudiente: int):
        """Devuelve las notas visibles para un acudiente a través de sus hijos con información de visualización."""
        try:
            cur = get_cursor('dict')
            
            # Primero verificar si hay estudiantes para este acudiente
            print(f"DEBUG: Buscando estudiantes para acudiente ID: {id_acudiente}")
            cur.execute("SELECT * FROM estudiantes WHERE acudiente_id = %s", (id_acudiente,))
            estudiantes = cur.fetchall()
            print(f"DEBUG: Estudiantes encontrados: {len(estudiantes)}")
            
            if not estudiantes:
                print("DEBUG: No hay estudiantes para este acudiente")
                cur.close()
                return []
            
            # Obtener IDs de estudiantes
            estudiante_ids = [est['id'] for est in estudiantes]
            placeholders = ','.join(['%s'] * len(estudiante_ids))
            
            # Consulta actualizada para incluir información de visualización
            query = f"""
                SELECT o.id, o.titulo, o.descripcion, o.tipo_observacion, o.fecha, o.hijo,
                       o.id_estudiante, o.id_profesor, o.id_acudiente,
                       e.nombre as estudiante_nombre, e.apellido as estudiante_apellido, e.grado,
                       u.nombre as profesor_nombre, u.apellido as profesor_apellido,
                       ov.viewed_at, ov.id as view_id,
                       CASE WHEN ov.id IS NOT NULL THEN 1 ELSE 0 END as is_viewed
                FROM observaciones o
                JOIN estudiantes e ON o.id_estudiante = e.id
                JOIN usuarios u ON o.id_profesor = u.id
                LEFT JOIN observation_views ov ON o.id = ov.observation_id AND ov.acudiente_id = %s
                WHERE o.id_estudiante IN ({placeholders})
                ORDER BY o.fecha DESC
            """
            
            params = [id_acudiente] + estudiante_ids
            print(f"DEBUG: Ejecutando query para estudiantes: {estudiante_ids}")
            cur.execute(query, params)
            rows = cur.fetchall()
            print(f"DEBUG: Observaciones encontradas: {len(rows)}")
            
            # Convertir al formato esperado
            formatted_rows = []
            for row in rows:
                formatted_rows.append({
                    'id': row['id'],
                    'titulo': f"Observación de {row['estudiante_nombre']}", # Generar título
                    'descripcion': row['descripcion'],
                    'tipo': row['tipo_observacion'],
                    'fecha': row['fecha'],
                    'hijo': f"{row['estudiante_nombre']} {row['estudiante_apellido']}", # Nombre completo
                    'id_estudiante': row['id_estudiante'],
                    'id_profesor': row['id_profesor'],
                    'estudiante_nombre': row['estudiante_nombre'],
                    'estudiante_apellido': row['estudiante_apellido'],
                    'grado': row['grado'],
                    'profesor_nombre': row['profesor_nombre'],
                    'profesor_apellido': row['profesor_apellido'],
                    'is_viewed': bool(row['is_viewed']),
                    'viewed_at': row['viewed_at']
                })
            
            cur.close()
            return formatted_rows
            
        except Exception as e:
            print(f"Error al obtener observaciones para acudiente: {e}")
            import traceback
            traceback.print_exc()
            return []

    # ----------------- Update -----------------
    @staticmethod
    def update(obs_id: int, titulo: str, descripcion: str, tipo: str):
        """Actualiza una observación existente."""
        try:
            cur = mysql.connection.cursor()
            
            print(f"DEBUG: Actualizando observación ID: {obs_id}")
            
            # Usar solo los campos que existen en la nueva estructura
            cur.execute(
                "UPDATE observaciones SET descripcion = %s, tipo = %s WHERE id = %s",
                (descripcion, tipo, obs_id)
            )
            mysql.connection.commit()
            cur.close()
            
            print(f"DEBUG: Observación {obs_id} actualizada exitosamente")
            
        except Exception as e:
            print(f"Error al actualizar observación: {e}")
            import traceback
            traceback.print_exc()
            if 'cur' in locals():
                cur.close()
            raise e

    # ----------------- Delete -----------------
    @staticmethod
    def delete(obs_id: int):
        cur = mysql.connection.cursor()
        cur.execute("DELETE FROM observaciones WHERE id = %s", (obs_id,))
        mysql.connection.commit()
        cur.close()
    
    # ----------------- Statistics -----------------
    @staticmethod
    def get_total_count():
        """Obtiene el número total de observaciones."""
        try:
            cur = get_cursor('dict')
            if cur is None:
                print("Error: No se pudo crear cursor para conteo de observaciones")
                return 0
            
            cur.execute("SELECT COUNT(*) as count FROM observaciones")
            result = cur.fetchone()
            cur.close()
            
            if result and 'count' in result:
                count = result['count']
                print(f"DEBUG: Conteo de observaciones obtenido: {count}")
                return count
            else:
                print("DEBUG: No se obtuvo resultado del conteo de observaciones")
                return 0
        except Exception as e:
            print(f"Error al obtener total de observaciones: {e}")
            import traceback
            traceback.print_exc()
            return 0
