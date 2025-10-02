# backend/src/models/student_acudiente_model.py

from ..database.db_connection import mysql, get_cursor

class StudentAcudienteModel:
    
    @staticmethod
    def get_acudientes_by_student(student_id):
        """Obtiene todos los acudientes de un estudiante"""
        try:
            cur = get_cursor('dict')
            query = """
                SELECT ea.id, ea.tipo_relacion, ea.fecha_asignacion, ea.activo,
                       u.id as acudiente_id, u.nombre, u.apellido, u.correo, u.cedula, u.ppt
                FROM estudiante_acudientes ea
                JOIN usuarios u ON ea.acudiente_id = u.id
                WHERE ea.estudiante_id = %s AND ea.activo = 1
                ORDER BY ea.tipo_relacion = 'principal' DESC, ea.fecha_asignacion ASC
            """
            cur.execute(query, (student_id,))
            acudientes = cur.fetchall()
            cur.close()
            return acudientes
        except Exception as e:
            print(f"Error al obtener acudientes del estudiante: {e}")
            return []
    
    @staticmethod
    def get_students_by_acudiente(acudiente_id):
        """Obtiene todos los estudiantes de un acudiente"""
        try:
            cur = get_cursor('dict')
            query = """
                SELECT ea.id, ea.tipo_relacion, ea.fecha_asignacion,
                       e.id as estudiante_id, e.nombre, e.apellido, e.grado, e.fecha_nacimiento,
                       p.nombre as profesor_nombre, p.apellido as profesor_apellido
                FROM estudiante_acudientes ea
                JOIN estudiantes e ON ea.estudiante_id = e.id
                LEFT JOIN usuarios p ON e.profesor_id = p.id
                WHERE ea.acudiente_id = %s AND ea.activo = 1
                ORDER BY e.grado, e.apellido, e.nombre
            """
            cur.execute(query, (acudiente_id,))
            students = cur.fetchall()
            cur.close()
            return students
        except Exception as e:
            print(f"Error al obtener estudiantes del acudiente: {e}")
            return []
    
    @staticmethod
    def assign_acudiente(student_id, acudiente_id, tipo_relacion='principal'):
        """Asigna un acudiente a un estudiante"""
        cur = None
        try:
            # Usar cursor directo
            cur = mysql.connection.cursor()
            
            # Verificar que el estudiante existe
            cur.execute("SELECT id FROM estudiantes WHERE id = %s", (student_id,))
            student_result = cur.fetchone()
            if not student_result:
                return False, "Estudiante no encontrado"
            
            # Verificar que el acudiente existe y es del rol correcto
            cur.execute("SELECT id FROM usuarios WHERE id = %s AND id_rol = 4 AND is_active = 1", (acudiente_id,))
            acudiente_result = cur.fetchone()
            if not acudiente_result:
                return False, "Acudiente no encontrado o inactivo"
            
            # Verificar que no exceda el límite de 2 acudientes
            cur.execute("""
                SELECT COUNT(*) FROM estudiante_acudientes 
                WHERE estudiante_id = %s AND activo = 1
            """, (student_id,))
            
            count_result = cur.fetchone()
            current_count = 0
            if count_result:
                if isinstance(count_result, dict):
                    # Es un DictCursor
                    current_count = int(count_result['COUNT(*)'])
                else:
                    # Es un cursor normal
                    current_count = int(count_result[0])
            
            if current_count >= 2:
                return False, "El estudiante ya tiene el máximo de 2 acudientes asignados"
            
            # Verificar que no esté ya asignado activamente
            cur.execute("""
                SELECT id FROM estudiante_acudientes 
                WHERE estudiante_id = %s AND acudiente_id = %s AND activo = 1
            """, (student_id, acudiente_id))
            
            duplicate_result = cur.fetchone()
            if duplicate_result:
                return False, "Este acudiente ya está asignado a este estudiante"
            
            # Determinar tipo de relación automáticamente
            if current_count == 0:
                final_tipo = 'principal'
            else:
                # Si ya hay uno, verificar si es principal
                cur.execute("""
                    SELECT tipo_relacion FROM estudiante_acudientes 
                    WHERE estudiante_id = %s AND activo = 1 LIMIT 1
                """, (student_id,))
                existing_result = cur.fetchone()
                if existing_result:
                    if isinstance(existing_result, dict):
                        tipo_existente = existing_result['tipo_relacion']
                    else:
                        tipo_existente = existing_result[0]
                    
                    if tipo_existente == 'principal':
                        final_tipo = 'secundario'
                    else:
                        final_tipo = 'principal'
                else:
                    final_tipo = 'principal'
            
            # Usar el tipo especificado por el usuario si es válido
            if tipo_relacion in ['principal', 'secundario']:
                final_tipo = tipo_relacion
            
            # Insertar la nueva relación
            cur.execute("""
                INSERT INTO estudiante_acudientes (estudiante_id, acudiente_id, tipo_relacion, activo, fecha_asignacion)
                VALUES (%s, %s, %s, 1, NOW())
            """, (student_id, acudiente_id, final_tipo))
            
            # Commit la transacción
            mysql.connection.commit()
            
            return True, f"Acudiente asignado como {final_tipo}"
            
        except Exception as e:
            print(f"Error al asignar acudiente: {e}")
            import traceback
            traceback.print_exc()
            return False, f"Error interno: {str(e)}"
        finally:
            # Asegurar que el cursor se cierre
            if cur:
                try:
                    cur.close()
                except:
                    pass
    
    @staticmethod
    def remove_acudiente(student_id, acudiente_id):
        """Remueve un acudiente de un estudiante"""
        try:
            cur = mysql.connection.cursor()
            
            # Marcar como inactivo en lugar de eliminar
            cur.execute("""
                UPDATE estudiante_acudientes 
                SET activo = 0 
                WHERE estudiante_id = %s AND acudiente_id = %s
            """, (student_id, acudiente_id))
            
            affected_rows = cur.rowcount
            mysql.connection.commit()
            cur.close()
            
            if affected_rows > 0:
                return True, "Acudiente removido exitosamente"
            else:
                return False, "No se encontró la relación estudiante-acudiente"
                
        except Exception as e:
            print(f"Error al remover acudiente: {e}")
            return False, f"Error al remover acudiente: {str(e)}"
    
    @staticmethod
    def change_acudiente_type(student_id, acudiente_id, new_type):
        """Cambia el tipo de relación de un acudiente (principal/secundario)"""
        try:
            cur = mysql.connection.cursor()
            
            # Si se cambia a principal, el otro debe ser secundario
            if new_type == 'principal':
                # Cambiar el actual principal a secundario
                cur.execute("""
                    UPDATE estudiante_acudientes 
                    SET tipo_relacion = 'secundario' 
                    WHERE estudiante_id = %s AND tipo_relacion = 'principal' AND activo = 1
                """, (student_id,))
            
            # Actualizar el tipo del acudiente especificado
            cur.execute("""
                UPDATE estudiante_acudientes 
                SET tipo_relacion = %s 
                WHERE estudiante_id = %s AND acudiente_id = %s AND activo = 1
            """, (new_type, student_id, acudiente_id))
            
            mysql.connection.commit()
            cur.close()
            return True, f"Tipo de relación cambiado a {new_type}"
            
        except Exception as e:
            print(f"Error al cambiar tipo de acudiente: {e}")
            return False, f"Error al cambiar tipo: {str(e)}"
    
    @staticmethod
    def get_available_acudientes(student_id=None):
        """Obtiene acudientes disponibles para asignar"""
        try:
            cur = get_cursor('dict')
            
            if student_id:
                # Excluir acudientes ya asignados a este estudiante
                query = """
                    SELECT u.id, u.nombre, u.apellido, u.correo, u.cedula, u.ppt
                    FROM usuarios u
                    WHERE u.id_rol = 4 AND u.is_active = 1
                    AND u.id NOT IN (
                        SELECT acudiente_id FROM estudiante_acudientes 
                        WHERE estudiante_id = %s AND activo = 1
                    )
                    ORDER BY u.nombre, u.apellido
                """
                cur.execute(query, (student_id,))
            else:
                # Todos los acudientes disponibles
                query = """
                    SELECT u.id, u.nombre, u.apellido, u.correo, u.cedula, u.ppt
                    FROM usuarios u
                    WHERE u.id_rol = 4 AND u.is_active = 1
                    ORDER BY u.nombre, u.apellido
                """
                cur.execute(query)
            
            acudientes = cur.fetchall()
            cur.close()
            return acudientes
            
        except Exception as e:
            print(f"Error al obtener acudientes disponibles: {e}")
            return []
    
    @staticmethod
    def get_student_acudiente_count(student_id):
        """Obtiene el número de acudientes activos de un estudiante"""
        try:
            cur = mysql.connection.cursor()
            cur.execute("""
                SELECT COUNT(*) FROM estudiante_acudientes 
                WHERE estudiante_id = %s AND activo = 1
            """, (student_id,))
            count = cur.fetchone()[0]
            cur.close()
            return count
        except Exception as e:
            print(f"Error al contar acudientes: {e}")
            return 0
