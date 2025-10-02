# backend/src/models/registration_request_model.py

from ..database.db_connection import mysql

class RegistrationRequestModel:
    @staticmethod
    def create_request(nombre, correo, celular, nombre_colegio, cantidad_estudiantes):
        """
        Guarda una nueva solicitud de registro en la base de datos.
        Retorna True si la inserción fue exitosa, False en caso contrario.
        """
        try:
            cur = mysql.connection.cursor()
            query = """
                INSERT INTO solicitudes_registro 
                (nombre, correo, celular, nombre_colegio, cantidad_estudiantes, estado) 
                VALUES (%s, %s, %s, %s, %s, %s)
            """
            # El estado por defecto en la DB es 'pendiente', pero lo pasamos explícitamente para claridad
            cur.execute(query, (nombre, correo, celular, nombre_colegio, cantidad_estudiantes, 'pendiente'))
            mysql.connection.commit()
            cur.close()
            return True
        except Exception as e:
            print(f"Error al crear solicitud de registro en RegistrationRequestModel: {e}")
            # Puedes loggear el error de forma más robusta en producción
            return False

    @staticmethod
    def find_by_email(correo):
        """
        Busca una solicitud de registro por correo electrónico.
        Retorna la solicitud si la encuentra, None en caso contrario.
        """
        cur = mysql.connection.cursor()
        cur.execute('SELECT id, nombre, correo, celular, nombre_colegio, cantidad_estudiantes, fecha_solicitud, estado FROM solicitudes_registro WHERE correo = %s', (correo,))
        request = cur.fetchone()
        cur.close()
        return request

    @staticmethod
    def get_all_pending_requests():
        """
        Obtiene todas las solicitudes de registro con estado 'pendiente'.
        """
        cur = mysql.connection.cursor()
        cur.execute('SELECT id, nombre, correo, celular, nombre_colegio, cantidad_estudiantes, fecha_solicitud, estado FROM solicitudes_registro WHERE estado = %s ORDER BY fecha_solicitud DESC', ('pendiente',))
        requests = cur.fetchall()
        cur.close()
        return requests

    @staticmethod
    def get_request_by_id(request_id):
        """
        Obtiene una solicitud de registro por su ID.
        """
        cur = mysql.connection.cursor()
        cur.execute('SELECT id, nombre, correo, celular, nombre_colegio, cantidad_estudiantes, fecha_solicitud, estado FROM solicitudes_registro WHERE id = %s', (request_id,))
        request = cur.fetchone()
        cur.close()
        return request

    @staticmethod
    def update_request_status(request_id, new_status):
        """
        Actualiza el estado de una solicitud de registro.
        """
        try:
            cur = mysql.connection.cursor()
            cur.execute('UPDATE solicitudes_registro SET estado = %s WHERE id = %s', (new_status, request_id))
            mysql.connection.commit()
            cur.close()
            return True
        except Exception as e:
            print(f"Error al actualizar estado de solicitud en RegistrationRequestModel: {e}")
            return False

    @staticmethod
    def delete_request(request_id):
        """
        Elimina una solicitud de registro de la base de datos.
        """
        try:
            cur = mysql.connection.cursor()
            cur.execute('DELETE FROM solicitudes_registro WHERE id = %s', (request_id,))
            mysql.connection.commit()
            cur.close()
            return True
        except Exception as e:
            print(f"Error al eliminar solicitud de registro en RegistrationRequestModel: {e}")
            return False