# backend/src/models/student_model.py

from ..database.db_connection import mysql, get_cursor

class StudentModel:
    @staticmethod
    def create_student(nombre, apellido, fecha_nacimiento, grado, profesor_id, acudiente_id=None, 
                      fecha_matricula=None, eps=None, condicion_especiales=None):
        """Crea un nuevo estudiante en la base de datos."""
        try:
            cur = mysql.connection.cursor()
            cur.execute('''
                INSERT INTO estudiantes (nombre, apellido, fecha_nacimiento, grado, profesor_id, acudiente_id, 
                                       fecha_registro, fecha_matricula, eps, condicion_especiales, activo) 
                VALUES (%s, %s, %s, %s, %s, %s, NOW(), %s, %s, %s, TRUE)
            ''', (nombre, apellido, fecha_nacimiento, grado, profesor_id, acudiente_id, 
                  fecha_matricula, eps, condicion_especiales))
            mysql.connection.commit()
            student_id = cur.lastrowid
            cur.close()
            return student_id
        except Exception as e:
            print(f"Error al crear estudiante: {e}")
            return None

    @staticmethod
    def get_students_by_professor(profesor_id):
        """Obtiene todos los estudiantes del sistema (no solo del profesor específico)."""
        try:
            cur = get_cursor('dict')
            
            # Debug: Imprimir información
            print(f"DEBUG StudentModel: Obteniendo TODOS los estudiantes del sistema")
            
            # Consulta para obtener TODOS los estudiantes, no solo del profesor
            query = """
                SELECT e.*, 
                       a.nombre as acudiente_nombre, 
                       a.apellido as acudiente_apellido,
                       a.correo as acudiente_email,
                       p.nombre as profesor_nombre,
                       p.apellido as profesor_apellido
                FROM estudiantes e
                LEFT JOIN usuarios a ON e.acudiente_id = a.id
                LEFT JOIN usuarios p ON e.profesor_id = p.id
                ORDER BY e.grado, e.apellido, e.nombre
            """
            
            print(f"DEBUG StudentModel: Ejecutando consulta para todos los estudiantes")
            cur.execute(query)
            students = cur.fetchall()
            
            print(f"DEBUG StudentModel: Estudiantes encontrados: {len(students)}")
            for student in students:
                print(f"  - ID: {student.get('id')}, Nombre: {student.get('nombre')} {student.get('apellido')}, Grado: {student.get('grado')}")
            
            cur.close()
            return students
        except Exception as e:
            print(f"Error al obtener estudiantes: {e}")
            import traceback
            traceback.print_exc()
            return []

    @staticmethod
    def get_students_by_professor_only(profesor_id):
        """Obtiene solo los estudiantes asignados a un profesor específico (para gestión del profesor)."""
        try:
            cur = get_cursor('dict')
            query = """
                SELECT e.*, 
                       a.nombre as acudiente_nombre, 
                       a.apellido as acudiente_apellido,
                       a.correo as acudiente_email
                FROM estudiantes e
                LEFT JOIN usuarios a ON e.acudiente_id = a.id
                WHERE e.profesor_id = %s
                ORDER BY e.apellido, e.nombre
            """
            cur.execute(query, (profesor_id,))
            students = cur.fetchall()
            cur.close()
            return students
        except Exception as e:
            print(f"Error al obtener estudiantes del profesor: {e}")
            return []

    @staticmethod
    def get_all_students():
        """Obtiene todos los estudiantes con información de acudientes y profesor."""
        try:
            cur = get_cursor('dict')
            # Consulta para obtener TODOS los estudiantes con sus acudientes
            query = """
                SELECT e.*, 
                       p.nombre as profesor_nombre,
                       p.apellido as profesor_apellido,
                       GROUP_CONCAT(
                           CONCAT(a.nombre, ' ', a.apellido, ' (', ea.tipo_relacion, ')')
                           ORDER BY ea.tipo_relacion = 'principal' DESC
                           SEPARATOR ', '
                       ) as acudientes_nombres,
                       GROUP_CONCAT(
                           a.correo
                           ORDER BY ea.tipo_relacion = 'principal' DESC
                           SEPARATOR ', '
                       ) as acudientes_emails,
                       COUNT(ea.id) as total_acudientes
                FROM estudiantes e
                LEFT JOIN usuarios p ON e.profesor_id = p.id
                LEFT JOIN estudiante_acudientes ea ON e.id = ea.estudiante_id AND ea.activo = 1
                LEFT JOIN usuarios a ON ea.acudiente_id = a.id
                GROUP BY e.id
                ORDER BY e.grado, e.apellido, e.nombre
            """
            cur.execute(query)
            students = cur.fetchall()
            cur.close()
            return students
        except Exception as e:
            print(f"Error al obtener todos los estudiantes: {e}")
            return []

    @staticmethod
    def get_students_by_acudiente(acudiente_id):
        """Obtiene todos los estudiantes asociados a un acudiente."""
        try:
            cur = get_cursor('dict')
            query = """
                SELECT e.*, 
                       u.nombre as profesor_nombre, 
                       u.apellido as profesor_apellido,
                       u.correo as profesor_email
                FROM estudiantes e
                LEFT JOIN usuarios u ON e.profesor_id = u.id
                WHERE e.acudiente_id = %s
                ORDER BY e.apellido, e.nombre
            """
            print(f"DEBUG: Ejecutando consulta para acudiente_id: {acudiente_id}")
            cur.execute(query, (acudiente_id,))
            students = cur.fetchall()
            print(f"DEBUG: Estudiantes encontrados: {len(students)}")
            cur.close()
            return students
        except Exception as e:
            print(f"Error al obtener estudiantes del acudiente: {e}")
            return []

    @staticmethod
    def get_student_by_id(student_id):
        """Obtiene un estudiante por su ID."""
        try:
            cur = get_cursor('dict')
            cur.execute('''
                SELECT e.id, e.nombre, e.apellido, e.fecha_nacimiento, e.grado,
                       e.profesor_id, e.acudiente_id,
                       u1.nombre as profesor_nombre, u1.apellido as profesor_apellido,
                       u2.nombre as acudiente_nombre, u2.apellido as acudiente_apellido,
                       u2.correo as acudiente_email, e.fecha_registro
                FROM estudiantes e
                LEFT JOIN usuarios u1 ON e.profesor_id = u1.id
                LEFT JOIN usuarios u2 ON e.acudiente_id = u2.id
                WHERE e.id = %s
            ''', (student_id,))
            student = cur.fetchone()
            cur.close()
            return student
        except Exception as e:
            print(f"Error al obtener estudiante: {e}")
            return None

    @staticmethod
    def update_student(student_id, nombre=None, apellido=None, fecha_nacimiento=None, 
                      grado=None, profesor_id=None, acudiente_id=None, fecha_matricula=None, 
                      eps=None, condicion_especiales=None):
        """Actualiza la información de un estudiante."""
        try:
            cur = mysql.connection.cursor()
            query_parts = []
            params = []

            if nombre is not None:
                query_parts.append('nombre = %s')
                params.append(nombre)
            if apellido is not None:
                query_parts.append('apellido = %s')
                params.append(apellido)
            if fecha_nacimiento is not None:
                query_parts.append('fecha_nacimiento = %s')
                params.append(fecha_nacimiento)
            if grado is not None:
                query_parts.append('grado = %s')
                params.append(grado)
            if profesor_id is not None:
                query_parts.append('profesor_id = %s')
                params.append(profesor_id)
            if acudiente_id is not None:
                query_parts.append('acudiente_id = %s')
                params.append(acudiente_id)
            if fecha_matricula is not None:
                query_parts.append('fecha_matricula = %s')
                params.append(fecha_matricula)
            if eps is not None:
                query_parts.append('eps = %s')
                params.append(eps)
            if condicion_especiales is not None:
                query_parts.append('condicion_especiales = %s')
                params.append(condicion_especiales)

            if not query_parts:
                return False

            query = f'UPDATE estudiantes SET {", ".join(query_parts)} WHERE id = %s'
            params.append(student_id)

            cur.execute(query, tuple(params))
            mysql.connection.commit()
            cur.close()
            return True
        except Exception as e:
            print(f"Error al actualizar estudiante: {e}")
            return False

    @staticmethod
    def assign_acudiente(student_id, acudiente_id):
        """Asigna un acudiente a un estudiante."""
        try:
            cur = mysql.connection.cursor()
            cur.execute('UPDATE estudiantes SET acudiente_id = %s WHERE id = %s', 
                       (acudiente_id, student_id))
            mysql.connection.commit()
            cur.close()
            return True
        except Exception as e:
            print(f"Error al asignar acudiente: {e}")
            return False

    @staticmethod
    def get_students_without_acudiente(profesor_id):
        """Obtiene estudiantes sin acudiente asignado para un profesor."""
        try:
            cur = mysql.connection.cursor()
            cur.execute('''
                SELECT id, nombre, apellido, grado, fecha_nacimiento
                FROM estudiantes 
                WHERE profesor_id = %s AND acudiente_id IS NULL
                ORDER BY nombre, apellido
            ''', (profesor_id,))
            students = cur.fetchall()
            cur.close()
            return students
        except Exception as e:
            print(f"Error al obtener estudiantes sin acudiente: {e}")
            return []

    @staticmethod
    def delete_student(student_id):
        """Elimina un estudiante de la base de datos."""
        try:
            cur = mysql.connection.cursor()
            cur.execute('DELETE FROM estudiantes WHERE id = %s', (student_id,))
            mysql.connection.commit()
            cur.close()
            return True
        except Exception as e:
            print(f"Error al eliminar estudiante: {e}")
            return False

    @staticmethod
    def get_total_students_count():
        """Obtiene el número total de estudiantes en el sistema."""
        try:
            cur = mysql.connection.cursor()
            cur.execute('SELECT COUNT(*) FROM estudiantes')
            result = cur.fetchone()
            cur.close()
            return result[0] if result else 0
        except Exception as e:
            print(f"Error al obtener el conteo de estudiantes: {e}")
            return 0

    @staticmethod
    def get_students_count_by_professor(profesor_id):
        """Obtiene el número de estudiantes asignados a un profesor."""
        try:
            cur = mysql.connection.cursor()
            cur.execute('SELECT COUNT(*) FROM estudiantes WHERE profesor_id = %s', (profesor_id,))
            result = cur.fetchone()
            cur.close()
            return result[0] if result else 0
        except Exception as e:
            print(f"Error al obtener el conteo de estudiantes del profesor: {e}")
            return 0
