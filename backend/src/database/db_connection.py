"""Módulo de conexión a MySQL.

Intentamos utilizar ``flask_mysqldb`` con el conector nativo ``mysqlclient``.  Si
no está disponible (por ejemplo en Windows con versiones recientes de Python),
realizamos un *fallback* automático a ``PyMySQL`` instalándolo como sustituto de
``MySQLdb``.
"""

# Intentamos registrar PyMySQL como reemplazo del driver nativo, esto permite que
# ``flask_mysqldb`` funcione incluso cuando ``mysqlclient`` no está compilado
# para la versión de Python del usuario.
try:
    import MySQLdb  # noqa: F401
except ModuleNotFoundError:
    # ``mysqlclient`` / ``MySQLdb`` no está instalado, hacemos fallback.
    import pymysql
    pymysql.install_as_MySQLdb()
    import MySQLdb  # Ahora MySQLdb está disponible

from flask_mysqldb import MySQL

mysql = MySQL()

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
        if cursor_type == 'dict':
            return mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        else:
            return mysql.connection.cursor()
    except Exception as e:
        print(f"Error al crear cursor: {e}")
        return None