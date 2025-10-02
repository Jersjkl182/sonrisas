# backend/src/app.py

import os
from flask import Flask, session, render_template, redirect, url_for, current_app # Asegúrate de que 'current_app' esté importado
from flask_mail import Mail  # Importar Flask-Mail
from flask_wtf.csrf import CSRFProtect, generate_csrf  # Protección CSRF y generador de token
import jinja2

from .database.db_connection import mysql
from .utils.config import Config
from .routes.main_routes import main_bp
from .routes.auth_routes import auth_bp
from .routes.admin_routes import admin_bp
from .routes.observation_routes import obs_bp
from .routes.student_acudiente_routes import student_acudiente_bp

# Inicializa Flask-Mail. Esto lo hace accesible en los Blueprints.
mail = Mail()
csrf = CSRFProtect()  # Instancia global de CSRFProtect

def create_app():
    app = Flask(__name__)

    # Carga la configuración desde la clase Config
    app.config.from_object(Config)

    # Inicializa Flask-Mail con la aplicación
    mail.init_app(app)

    # Inicializa CSRFProtect
    csrf.init_app(app)

    # Agrega la función generate_csrf al contexto global de Jinja
    app.jinja_env.globals['csrf_token'] = generate_csrf
    app.mail = mail # <--- ¡¡¡ESTA ES LA LÍNEA CRUCIAL QUE FALTABA O NO ESTABA EN EL LUGAR CORRECTO!!!
                    # Esto asigna la instancia de Mail a la aplicación para que current_app.mail funcione.

    # Inicializa Flask-MySQLdb con la aplicación
    mysql.init_app(app)

    # --- Configuración de Carpetas de Frontend y Archivos Estáticos ---
    # Obtén la ruta absoluta del archivo actual (backend/src/app.py)
    current_dir = os.path.abspath(os.path.dirname(__file__))

    # Sube dos niveles para alcanzar la raíz del proyecto (Teaching NOTES BD 1.6)
    project_root = os.path.dirname(os.path.dirname(current_dir))

    # Construye la ruta completa a la carpeta 'frontend/template' para archivos HTML
    template_dir = os.path.join(project_root, 'frontend', 'template')

    # Construye la ruta completa a la carpeta 'frontend/static' para archivos estáticos
    static_dir = os.path.join(project_root, 'frontend', 'static')
    # Actualiza las carpetas de plantillas y estáticos de la aplicación Flask
    app.template_folder = template_dir
    app.static_folder = static_dir
    # --- FIN DE CONFIGURACIÓN DE CARPETAS ---

    # Registra los blueprints
    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(admin_bp, url_prefix='/admin')
    app.register_blueprint(obs_bp)
    app.register_blueprint(student_acudiente_bp)

    # Configurar ruta para servir archivos de uploads
    from flask import send_from_directory

    @app.route('/uploads/<path:filename>')
    def uploaded_file(filename):
        """Sirve archivos subidos desde la carpeta uploads."""
        uploads_dir = os.path.join(project_root, 'uploads')
        return send_from_directory(uploads_dir, filename)

    # Manejadores de errores (opcional, pero buena práctica)
    @app.errorhandler(404)
    def pagina_no_encontrada(error):
        return render_template('404.html'), 404

    @app.errorhandler(500)
    def error_servidor(error):
        return render_template('500.html'), 500

    # Ruta por defecto para la raíz
    @app.route('/')
    def home():
        # Redirige a la ruta 'index' de tu Blueprint 'main_bp'
        # Asegúrate de que 'main_bp.home' (o 'main_bp.index' si realmente existe) es la ruta correcta
        # En tu caso, 'main_bp.home' parece ser el correcto según el error anterior
        return redirect(url_for('main_bp.home')) # Aquí también asegúrate que sea 'home' o 'index'

    return app

# Bloque para ejecutar la aplicación directamente (útil para desarrollo)
if __name__ == '__main__':
    app_instance = create_app()
    
    # Configuración básica de logging para ver mensajes en la consola
    import logging
    logging.basicConfig(level=logging.DEBUG) 

    app_instance.run(debug=True) # debug=True es solo para desarrollo