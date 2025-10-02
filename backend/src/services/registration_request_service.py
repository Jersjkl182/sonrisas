# backend/src/services/registration_request_service.py

from ..models.registration_request_model import RegistrationRequestModel
from ..models.user_model import UserModel # Necesario para crear un usuario a partir de una solicitud
from werkzeug.security import generate_password_hash # Necesario para hashear contraseñas al aprobar
import random
import string

class RegistrationRequestService:
    @staticmethod
    def get_all_pending_requests():
        """
        Obtiene todas las solicitudes de registro pendientes.
        """
        return RegistrationRequestModel.get_all_pending_requests()

    @staticmethod
    def get_request_details(request_id):
        """
        Obtiene los detalles de una solicitud específica por su ID.
        """
        return RegistrationRequestModel.get_request_by_id(request_id)

    @staticmethod
    def _generate_random_password(length=12):
        """
        Genera una contraseña aleatoria y segura.
        """
        characters = string.ascii_letters + string.digits + string.punctuation
        password = ''.join(random.choice(characters) for i in range(length))
        return password

    @staticmethod
    def approve_request(request_id, id_rol):
        """
        Aprueba una solicitud de registro:
        1. Crea un nuevo usuario en la tabla 'usuarios'.
        2. Actualiza el estado de la solicitud a 'aprobada'.
        3. Genera y retorna la contraseña temporal para el usuario (IMPORTANTE para el administrador).
        Retorna (True, contraseña_temporal) si es exitoso, (False, None) en caso contrario.
        """
        request_data = RegistrationRequestModel.get_request_by_id(request_id)
        if not request_data or request_data['estado'] != 'pendiente':
            print(f"DEBUG: Solicitud {request_id} no encontrada o no está pendiente.")
            return False, None

        # Verificar si ya existe un usuario con este correo (doble verificación por seguridad)
        if UserModel.find_by_email(request_data['correo']):
            print(f"DEBUG: Ya existe un usuario con el correo {request_data['correo']}. No se puede aprobar la solicitud.")
            # Opcional: Actualizar el estado de la solicitud a 'rechazada' si ya existe el usuario
            RegistrationRequestModel.update_request_status(request_id, 'rechazada')
            return False, None

        # Generar una contraseña temporal segura
        temp_password = RegistrationRequestService._generate_random_password()
        hashed_password = generate_password_hash(temp_password)

        # Crear el nuevo usuario en la tabla 'usuarios'
        user_created = UserModel.create_user(
            correo=request_data['correo'],
            hashed_password=hashed_password,
            id_rol=id_rol, # El administrador define el rol
            nombre=request_data['nombre'],
            apellido=None, # Tu tabla de solicitudes no tiene apellido, lo dejamos None
            is_active=True # Por defecto, la cuenta creada está activa
        )

        if user_created:
            # Actualizar el estado de la solicitud a 'aprobada'
            request_status_updated = RegistrationRequestModel.update_request_status(request_id, 'aprobada')
            if request_status_updated:
                print(f"DEBUG: Solicitud {request_id} aprobada y usuario creado: {request_data['correo']}")
                return True, temp_password
            else:
                print(f"ERROR: Usuario creado para {request_data['correo']} pero falló al actualizar estado de solicitud {request_id}.")
                # Considera aquí una lógica de rollback o notificación de error crítico
                return False, None
        else:
            print(f"ERROR: Falló la creación del usuario para la solicitud {request_id}.")
            return False, None

    @staticmethod
    def reject_request(request_id):
        """
        Rechaza una solicitud de registro actualizando su estado a 'rechazada'.
        """
        return RegistrationRequestModel.update_request_status(request_id, 'rechazada')

    @staticmethod
    def delete_request(request_id):
        """
        Elimina una solicitud de registro de la base de datos (independientemente de su estado).
        """
        return RegistrationRequestModel.delete_request(request_id)