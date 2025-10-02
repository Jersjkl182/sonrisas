"""Módulo de conexión a MySQL utilizando Py MySQL puro para compatibilidad con Railway."""

import pymysql
from flask import g, current_app

# Configurar Py MySQL para usar el charset correcto
pymysql.install_as_MySQLdb()

class MySQLConnection:
    def __init__(self, app=None):
        self.app = app
        if app is not None:
            self.init_app(app)
    
    def init_app(self, app):
        """Inicializa la conexión MySQL con la aplicación Flask."""
        app.teardown_appcontext(self.close_db)
    
    def get_connection(self):
        """Obtiene una conexión a la base de datos."""
        if 'db_connection' not in g:
            try:
                g.db_connection = pymysql.connect(
                    host=current_app.config['MYSQL_HOST'],
                    user=current_app.config['MYSQL_USER'],
                    password=current_app.config['MYSQL_PASSWORD'],
                    database=current_app.config['MYSQL_DB'],
                    port=current_app.config['MYSQL_PORT'],
                    charset='utf8mb4',
                    cursorclass=pymysql.cursors.DictCursor,
                    autocommit=True
                )
            except Exception as e:
                current_app.logger.error(f"Error conectando a MySQL: {e}")
                raise
        
        return g.db_connection
    
    def close_db(self, error):
        """Cierra la conexión a la base de datos."""
        db = g.pop('db_connection', None)
        if db is not None:
            db.close()
    
    @property
    def connection(self):
        """Propiedad para mantener compatibilidad con Flask-MySQLdb."""
        return self.get_connection()

# Instancia global para mantener compatibilidad
mysql = MySQLConnection()

# Helper function para obtener cursor con manejo de errores
def get_cursor(cursor_type='dict'):
    """
    Obtiene un cursor de base de datos con manejo de errores.
    
    Args:
        cursor_type (str): 'dict' para DictCursor, 'default' para cursor normal
    
    Returns:
        cursor: Cursor de base de datos
    """
    try:
        connection = mysql.get_connection()
        if cursor_type == 'dict':
            return connection.cursor(pymysql.cursors.DictCursor)
        else:
            return connection.cursor()
    except Exception as e:
        current_app.logger.error(f"Error al crear cursor: {e}")
        return None

def get_connection():
    """Función helper para obtener conexión directa."""
    return mysql.get_connection()
