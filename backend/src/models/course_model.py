# backend/src/models/course_model.py
"""Modelo de acceso a datos para la tabla `courses`. Sigue el mismo patrón que los
otros modelos del proyecto: métodos estáticos que interactúan mediante el cursor
MySQL ya configurado en `db_connection`.
"""
from ..database.db_connection import mysql

class CourseModel:
    """Operaciones CRUD para cursos."""

    @staticmethod
    def create_course(nombre, descripcion=None, fecha_inicio=None, fecha_fin=None, is_active=True):
        try:
            cur = mysql.connection.cursor()
            cur.execute(
                """
                INSERT INTO courses (nombre, descripcion, fecha_inicio, fecha_fin, is_active)
                VALUES (%s, %s, %s, %s, %s)
                """,
                (nombre, descripcion, fecha_inicio, fecha_fin, is_active)
            )
            mysql.connection.commit()
            cur.close()
            return True
        except Exception as e:
            print(f"[CourseModel] Error al crear curso: {e}")
            return False

    @staticmethod
    def get_all_courses():
        cur = mysql.connection.cursor()
        cur.execute(
            """
            SELECT id, nombre, descripcion, fecha_inicio, fecha_fin, is_active,
                   created_at, updated_at
            FROM courses
            ORDER BY created_at DESC
            """
        )
        cursos = cur.fetchall()
        cur.close()
        return cursos

    @staticmethod
    def find_by_id(course_id):
        cur = mysql.connection.cursor()
        cur.execute(
            """SELECT id, nombre, descripcion, fecha_inicio, fecha_fin, is_active
            FROM courses WHERE id = %s""",
            (course_id,)
        )
        curso = cur.fetchone()
        cur.close()
        return curso

    @staticmethod
    def update_course(course_id, nombre=None, descripcion=None, fecha_inicio=None, fecha_fin=None, is_active=None):
        try:
            cur = mysql.connection.cursor()
            query_parts = []
            params = []
            if nombre is not None:
                query_parts.append("nombre = %s")
                params.append(nombre)
            if descripcion is not None:
                query_parts.append("descripcion = %s")
                params.append(descripcion)
            if fecha_inicio is not None:
                query_parts.append("fecha_inicio = %s")
                params.append(fecha_inicio)
            if fecha_fin is not None:
                query_parts.append("fecha_fin = %s")
                params.append(fecha_fin)
            if is_active is not None:
                query_parts.append("is_active = %s")
                params.append(is_active)
            if not query_parts:
                return False
            query = f"UPDATE courses SET {', '.join(query_parts)}, updated_at = CURRENT_TIMESTAMP WHERE id = %s"
            params.append(course_id)
            cur.execute(query, tuple(params))
            mysql.connection.commit()
            cur.close()
            return True
        except Exception as e:
            print(f"[CourseModel] Error al actualizar curso: {e}")
            return False

    @staticmethod
    def delete_course(course_id):
        try:
            cur = mysql.connection.cursor()
            cur.execute("DELETE FROM courses WHERE id = %s", (course_id,))
            mysql.connection.commit()
            cur.close()
            return True
        except Exception as e:
            print(f"[CourseModel] Error al eliminar curso: {e}")
            return False
