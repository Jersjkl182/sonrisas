from functools import wraps
from flask import session, flash, redirect, url_for
import jinja2

def login_required(f):
    """Decorator to check if the user is logged in."""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'logueado' not in session:
            flash('Please log in to access this page', 'danger')
            return redirect(url_for('main_bp.inicio_sesion')) # Redirect to login route in main_bp
        return f(*args, **kwargs)
    return decorated_function

def role_required(allowed_roles):
    """Decorator to check user roles."""
    def decorator(f):
        @wraps(f)
        @login_required # Ensure login_required is applied first
        def decorated_function(*args, **kwargs):
            if session.get('id_rol') not in allowed_roles:
                flash('You do not have permission to access this page', 'warning')
                return redirect(url_for('main_bp.home')) # Redirect to home route in main_bp
            return f(*args, **kwargs)
        return decorated_function
    return decorator

# ------------------------------------------------------------------
# Decorador basado en permisos
# ------------------------------------------------------------------
from ..models.user_model import UserModel  # import tardío para evitar ciclos

def permission_required(codigo_permiso):
    """Decorator que comprueba si el usuario tiene el permiso indicado."""
    def decorator(f):
        @wraps(f)
        @login_required
        def decorated_function(*args, **kwargs):
            user_id = session.get('id')
            if not user_id or not UserModel.has_permission(user_id, codigo_permiso):
                flash('No tiene permiso para realizar esta acción', 'warning')
                return redirect(url_for('main_bp.home'))
            return f(*args, **kwargs)
        return decorated_function
    return decorator
