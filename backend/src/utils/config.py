import datetime
import os
import jinja2
import urllib.parse

class Config:
    # --- Configuración de MySQL ---
    # Para producción (Railway/Heroku), usar variables de entorno
    MYSQL_HOST = os.environ.get('MYSQL_HOST', 'localhost')
    MYSQL_USER = os.environ.get('MYSQL_USER', 'root')
    MYSQL_PASSWORD = os.environ.get('MYSQL_PASSWORD', '')
    MYSQL_DB = os.environ.get('MYSQL_DB', 'login')
    MYSQL_PORT = int(os.environ.get('MYSQL_PORT', 3306))
    MYSQL_CURSORCLASS = 'DictCursor'
    
    # Para Railway MySQL, también soportar DATABASE_URL
    DATABASE_URL = os.environ.get('DATABASE_URL')
    if DATABASE_URL and DATABASE_URL.startswith('mysql://'):
        # Parsear DATABASE_URL para Railway
        url = urllib.parse.urlparse(DATABASE_URL)
        MYSQL_HOST = url.hostname
        MYSQL_USER = url.username
        MYSQL_PASSWORD = url.password
        MYSQL_DB = url.path[1:]  # Remover el '/' inicial
        MYSQL_PORT = url.port or 3306
    
    # --- Configuración de Sesiones ---
    SESSION_TYPE = 'filesystem'
    PERMANENT_SESSION_LIFETIME = datetime.timedelta(minutes=30)

    SECRET_KEY = os.environ.get('FLASK_SECRET_KEY', "una_clave_secreta_super_segura_y_aleatoria_para_TeachingNotes_2025!")

    # --- Configuración de CSRF ---
    WTF_CSRF_ENABLED = True
    WTF_CSRF_TIME_LIMIT = None  # Sin límite de tiempo para el token CSRF

    # --- Configuración de Email ---
    MAIL_SERVER = os.environ.get('MAIL_SERVER', 'smtp.gmail.com')
    MAIL_PORT = int(os.environ.get('MAIL_PORT', 587)) 
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS', 'True').lower() in ('true', '1', 't') 
    MAIL_USE_SSL = os.environ.get('MAIL_USE_SSL', 'False').lower() in ('true', '1', 't') 
    
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME', 'teachingnotes14@gmail.com') 
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD', 'rwrq awhe suez jrmi') 

    MAIL_DEFAULT_SENDER = os.environ.get('MAIL_DEFAULT_SENDER', 'teachingnotes14@gmail.com')
    MAIL_DEFAULT_CHARSET = 'utf-8'
    
    # --- Configuración de Producción ---
    DEBUG = os.environ.get('FLASK_DEBUG', 'False').lower() in ('true', '1', 't')
    TESTING = False
