# backend/src/services/user_service.py

from werkzeug.security import generate_password_hash
from ..models.user_model import UserModel
from ..models.registration_request_model import RegistrationRequestModel # <-- Importa el nuevo modelo
import jinja2

import random, string

class UserService:
    @staticmethod
    def create_new_user(correo, password, id_rol, nombre=None, apellido=None, is_active=True):
        """
        Lógica de negocio para crear un nuevo usuario,
        incluyendo el hasheo de la contraseña y la verificación de usuarios existentes,
        con nombre, apellido y estado activo.
        """
        # Verificar si el usuario ya existe en la tabla de usuarios activos
        existing_user = UserModel.find_by_email(correo)
        if existing_user:
            return False # El usuario ya existe

        hashed_password = generate_password_hash(password)
        return UserModel.create_user(correo, hashed_password, id_rol, nombre, apellido, is_active)

    @staticmethod
    def create_new_user_with_documents(correo, password, id_rol, nombre=None, apellido=None, cedula=None, ppt=None, is_active=True):
        """
        Lógica de negocio para crear un nuevo usuario con documentos de identidad,
        incluyendo el hasheo de la contraseña y la verificación de usuarios existentes.
        """
        # Verificar si el usuario ya existe por correo
        existing_user = UserModel.find_by_email(correo)
        if existing_user:
            return False # El usuario ya existe

        hashed_password = generate_password_hash(password)
        return UserModel.create_user_with_documents(correo, hashed_password, id_rol, nombre, apellido, cedula, ppt, is_active)

    @staticmethod
    def get_all_users_with_roles():
        """
        Obtiene todos los usuarios y les asigna el nombre del rol.
        """
        users = UserModel.get_all_users()
        users_with_roles = []
        for user in users:
            user_dict = dict(user) 
            user_dict['rol_nombre'] = UserModel.get_rol_name(user_dict['id_rol'])
            users_with_roles.append(user_dict)
        return users_with_roles

    @staticmethod
    def update_user(user_id, correo=None, new_password=None, id_rol=None, nombre=None, apellido=None, is_active=None):
        """
        Lógica de negocio para actualizar un usuario.
        Hashea la nueva contraseña si se proporciona.
        Verifica si el nuevo correo ya existe para otro usuario.
        Permite actualizar el estado activo (is_active).
        """
        if correo:
            existing_user_with_email = UserModel.find_by_email(correo)
            if existing_user_with_email and existing_user_with_email['id'] != user_id:
                return False # El correo ya está en uso por otro usuario

        hashed_password = generate_password_hash(new_password) if new_password else None
        return UserModel.update_user(user_id, correo, hashed_password, id_rol, nombre, apellido, is_active)

    @staticmethod
    def update_user_with_documents(user_id, correo=None, new_password=None, id_rol=None, nombre=None, apellido=None, cedula=None, ppt=None, is_active=None):
        """
        Lógica de negocio para actualizar un usuario con documentos de identidad.
        Hashea la nueva contraseña si se proporciona.
        Verifica si el nuevo correo ya existe para otro usuario.
        """
        if correo:
            existing_user_with_email = UserModel.find_by_email(correo)
            if existing_user_with_email and existing_user_with_email['id'] != user_id:
                return False # El correo ya está en uso por otro usuario

        hashed_password = generate_password_hash(new_password) if new_password else None
        return UserModel.update_user_with_documents(user_id, correo, hashed_password, id_rol, nombre, apellido, cedula, ppt, is_active)

    @staticmethod
    def reset_password(user_id, length: int = 10):
        """Genera una contraseña temporal, la guarda hasheada y la devuelve."""
        temp_password = ''.join(random.choices(string.ascii_letters + string.digits, k=length))
        hashed = generate_password_hash(temp_password)
        success = UserModel.update_user(user_id, hashed_password=hashed)
        if success:
            return True, temp_password
        return False, None

    @staticmethod
    def delete_user(user_id):
        """
        Lógica de negocio para eliminar un usuario.
        """
        return UserModel.delete_user(user_id)

    @staticmethod
    def create_registration_request(nombre, correo, celular, nombre_colegio, cantidad_estudiantes):
        """
        Guarda una nueva solicitud de registro en la base de datos.
        Verifica si ya existe una solicitud pendiente o un usuario con ese correo.
        """
        # 1. Verificar si ya existe un usuario activo con este correo
        existing_user = UserModel.find_by_email(correo)
        if existing_user:
            print(f"DEBUG: Ya existe un usuario activo con el correo {correo}. No se crea la solicitud.")
            return False # Ya existe un usuario con este correo

        # 2. Verificar si ya existe una solicitud PENDIENTE con este correo
        existing_request = RegistrationRequestModel.find_by_email(correo)
        if existing_request and existing_request['estado'] == 'pendiente':
            print(f"DEBUG: Ya existe una solicitud PENDIENTE para el correo {correo}.")
            return False # Ya existe una solicitud pendiente

        # Si no existe ni usuario ni solicitud pendiente, crear la nueva solicitud
        return RegistrationRequestModel.create_request(nombre, correo, celular, nombre_colegio, cantidad_estudiantes)

    @staticmethod
    def get_users_by_role(id_rol):
        """
        Obtiene todos los usuarios con un rol específico.
        """
        return UserModel.get_users_by_role(id_rol)

    @staticmethod
    def get_all_acudientes():
        """
        Obtiene todos los usuarios con rol de acudiente (id_rol = 4).
        """
        return UserModel.get_users_by_role(4)