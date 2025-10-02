from werkzeug.security import check_password_hash
from ..models.user_model import UserModel
import jinja2

class AuthService:
    @staticmethod
    def authenticate_user(email, password):
        """Authenticates a user based on email and password."""
        user = UserModel.find_by_email(email)
        if user and check_password_hash(user['contrasena'], password):
            return user
        return None
    
    @staticmethod
    def authenticate_user_multi(login_method, usuario, password):
        """Authenticates a user based on multiple login methods (email, cedula, ppt)."""
        user = None
        
        print(f"AuthService: Buscando usuario por {login_method}: {usuario}")
        
        if login_method == 'correo':
            user = UserModel.find_by_email(usuario)
        elif login_method == 'cedula':
            user = UserModel.find_by_cedula(usuario)
        elif login_method == 'ppt':
            user = UserModel.find_by_ppt(usuario.upper())
        
        print(f"AuthService: Usuario encontrado en BD: {'Sí' if user else 'No'}")
        
        if user:
            password_valid = check_password_hash(user['contrasena'], password)
            print(f"AuthService: Contraseña válida: {'Sí' if password_valid else 'No'}")
            
            if password_valid:
                print(f"AuthService: Rol del usuario: {user['id_rol']}")
                return user
        
        return None
