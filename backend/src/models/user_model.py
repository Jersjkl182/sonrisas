# backend/src/models/user_model.py

from ..database.db_connection import mysql, get_cursor

class UserModel:
    @staticmethod
    def find_by_email(email):
        """Busca un usuario por correo electrónico, incluyendo nombre, apellido y estado activo."""
        cur = mysql.connection.cursor()
        # Estructura real: la columna se llama 'email'
        cur.execute('SELECT id, correo, contrasena, id_rol, nombre, apellido, is_active FROM usuarios WHERE correo = %s', (email,))
        account = cur.fetchone()
        cur.close()
        return account

    @staticmethod
    def find_by_id(user_id):
        """Busca un usuario por su ID, incluyendo nombre, apellido y estado activo."""
        cur = mysql.connection.cursor()
        # Asegúrate de que los nombres de las columnas coincidan exactamente con tu base de datos
        # Nota: ¡Aquí también te faltan 'nombre' y 'apellido' en el SELECT si quieres recuperarlos!
        cur.execute('SELECT id, correo, contrasena, id_rol, nombre, apellido, is_active FROM usuarios WHERE id = %s', (user_id,))
        user = cur.fetchone()
        cur.close()
        return user

    @staticmethod
    def find_by_cedula(cedula):
        """Busca un usuario por cédula de ciudadanía."""
        try:
            cur = mysql.connection.cursor()
            cur.execute('SELECT id, correo, contrasena, id_rol, nombre, apellido, is_active FROM usuarios WHERE cedula = %s', (cedula,))
            user = cur.fetchone()
            cur.close()
            return user
        except Exception as e:
            if "cedula" in str(e):
                print(f"Columna 'cedula' no existe en la tabla usuario: {e}")
                return None
            else:
                print(f"Error al buscar usuario por cédula: {e}")
                return None

    @staticmethod
    def find_by_ppt(ppt):
        """Busca un usuario por PPT (Permiso de Protección Temporal)."""
        try:
            cur = mysql.connection.cursor()
            cur.execute('SELECT id, correo, contrasena, id_rol, nombre, apellido, is_active FROM usuarios WHERE ppt = %s', (ppt,))
            user = cur.fetchone()
            cur.close()
            return user
        except Exception as e:
            if "ppt" in str(e):
                print(f"Columna 'ppt' no existe en la tabla usuario: {e}")
                return None
            else:
                print(f"Error al buscar usuario por PPT: {e}")
                return None

    @staticmethod
    # MODIFICACIÓN CLAVE AQUÍ: Añadir 'nombre' y 'apellido' como parámetros
    def create_user(correo, hashed_password, id_rol, nombre, apellido, is_active=True):
        """Crea un nuevo usuario en la base de datos con nombre, apellido y estado activo."""
        try:
            cur = mysql.connection.cursor()
            # Asegúrate de que los nombres de las columnas coincidan exactamente con tu base de datos
            # y el orden de los %s coincida con el orden de las variables
            cur.execute('INSERT INTO usuarios (correo, contrasena, id_rol, nombre, apellido, is_active) VALUES (%s, %s, %s, %s, %s, %s)',
                        # MODIFICACIÓN CLAVE AQUÍ: Asegurar que los valores se pasen en el orden correcto
                        (correo, hashed_password, id_rol, nombre, apellido, is_active))
            mysql.connection.commit()
            cur.close()
            return True
        except Exception as e:
            # En un entorno de producción, usa un logger en lugar de print
            print(f"Error al crear usuario en UserModel: {e}")
            return False

    @staticmethod
    def create_user_with_documents(correo, hashed_password, id_rol, nombre, apellido, cedula=None, ppt=None, is_active=True):
        """Crea un nuevo usuario en la base de datos con documentos de identidad."""
        try:
            cur = mysql.connection.cursor()
            cur.execute('INSERT INTO usuarios (correo, contrasena, id_rol, nombre, apellido, cedula, ppt, is_active) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)',
                        (correo, hashed_password, id_rol, nombre, apellido, cedula, ppt, is_active))
            mysql.connection.commit()
            cur.close()
            return True
        except Exception as e:
            print(f"Error al crear usuario con documentos en UserModel: {e}")
            return False

    @staticmethod
    def get_all_users():
        """Obtiene todos los usuarios de la base de datos, incluyendo nombre, apellido y estado activo."""
        cur = mysql.connection.cursor()
        # Asegúrate de que los nombres de las columnas coincidan exactamente con tu base de datos
        # Nota: Aquí también te faltan 'nombre' y 'apellido' en el SELECT si quieres recuperarlos!
        cur.execute('SELECT id, correo, nombre, apellido, id_rol, cedula, ppt, is_active FROM usuarios')
        users = cur.fetchall()
        cur.close()
        return users

    @staticmethod
    def update_user(user_id, correo=None, hashed_password=None, id_rol=None, nombre=None, apellido=None, is_active=None):
        """Actualiza un usuario existente en la base de datos con nombre, apellido y estado activo."""
        try:
            cur = mysql.connection.cursor()
            query_parts = []
            params = []

            if correo is not None:
                query_parts.append('correo = %s')
                params.append(correo)
            if hashed_password is not None:
                query_parts.append('contrasena = %s')
                params.append(hashed_password)
            if id_rol is not None:
                query_parts.append('id_rol = %s')
                params.append(id_rol) # Movido aquí para mantener el orden
            if nombre is not None: # Nuevo campo para actualizar el nombre
                query_parts.append('nombre = %s')
                params.append(nombre)
            if apellido is not None: # Nuevo campo para actualizar el apellido
                query_parts.append('apellido = %s')
                params.append(apellido)
            if is_active is not None: # Nuevo campo para actualizar el estado activo
                query_parts.append('is_active = %s')
                params.append(is_active)
            
            if not query_parts:
                return False

            query = f'UPDATE usuarios SET {", ".join(query_parts)} WHERE id = %s'
            params.append(user_id)

            cur.execute(query, tuple(params))
            mysql.connection.commit()
            cur.close()
            return True
        except Exception as e:
            print(f"Error al actualizar usuario en UserModel: {e}")
            return False

    @staticmethod
    def update_user_with_documents(user_id, correo=None, hashed_password=None, id_rol=None, nombre=None, apellido=None, cedula=None, ppt=None, is_active=None):
        """Actualiza un usuario existente en la base de datos incluyendo documentos de identidad."""
        try:
            cur = mysql.connection.cursor()
            query_parts = []
            params = []

            if correo is not None:
                query_parts.append('correo = %s')
                params.append(correo)
            if hashed_password is not None:
                query_parts.append('contrasena = %s')
                params.append(hashed_password)
            if id_rol is not None:
                query_parts.append('id_rol = %s')
                params.append(id_rol)
            if nombre is not None:
                query_parts.append('nombre = %s')
                params.append(nombre)
            if apellido is not None:
                query_parts.append('apellido = %s')
                params.append(apellido)
            if cedula is not None:
                query_parts.append('cedula = %s')
                params.append(cedula)
            if ppt is not None:
                query_parts.append('ppt = %s')
                params.append(ppt)
            if is_active is not None:
                query_parts.append('is_active = %s')
                params.append(is_active)
            
            # Si no se seleccionó documento, limpiar ambos campos
            if cedula is None and ppt is None:
                query_parts.append('cedula = NULL')
                query_parts.append('ppt = NULL')
            
            if not query_parts:
                return False

            query = f'UPDATE usuarios SET {", ".join(query_parts)} WHERE id = %s'
            params.append(user_id)

            cur.execute(query, tuple(params))
            mysql.connection.commit()
            cur.close()
            return True
        except Exception as e:
            print(f"Error al actualizar usuario con documentos en UserModel: {e}")
            return False

    @staticmethod
    def delete_user(user_id):
        """Elimina un usuario de la base de datos."""
        try:
            cur = mysql.connection.cursor()
            cur.execute('DELETE FROM usuarios WHERE id = %s', (user_id,))
            mysql.connection.commit()
            cur.close()
            return True
        except Exception as e:
            print(f"Error al eliminar usuario en UserModel: {e}")
            return False

    @staticmethod
    def get_rol_name(id_rol):
        """Obtiene el nombre del rol basado en su ID."""
        roles = {
            1: "Administrador",
            2: "Profesor",
            4: "Acudiente"
        }
        return roles.get(id_rol, "Desconocido")

    # ---------- Nuevos métodos de roles/permisos ----------

    @staticmethod
    def get_roles(user_id: int):
        """Devuelve los ID de roles asignados al usuario."""
        cur = mysql.connection.cursor()
        cur.execute("SELECT id_rol FROM usuario_roles WHERE usuario_id = %s", (user_id,))
        rows = cur.fetchall()
        cur.close()
        return [r[0] for r in rows] if rows else []

    @staticmethod
    def add_role(user_id: int, id_rol: int):
        cur = mysql.connection.cursor()
        cur.execute("INSERT IGNORE INTO usuario_roles (usuario_id, id_rol) VALUES (%s, %s)", (user_id, id_rol))
        mysql.connection.commit()
        cur.close()

    @staticmethod
    def remove_role(user_id: int, id_rol: int):
        cur = mysql.connection.cursor()
        cur.execute("DELETE FROM usuario_roles WHERE usuario_id = %s AND id_rol = %s", (user_id, id_rol))
        mysql.connection.commit()
        cur.close()

    @staticmethod
    def has_permission(user_id: int, codigo_permiso: str) -> bool:
        """Comprueba si el usuario posee un permiso (por cualquiera de sus roles)."""
        cur = mysql.connection.cursor()
        query = (
            "SELECT 1 FROM usuario_roles ur "
            "JOIN rol_permisos rp ON ur.id_rol = rp.id_rol "
            "JOIN permisos p ON rp.permiso_id = p.id "
            "WHERE ur.usuario_id = %s AND p.codigo = %s LIMIT 1"
        )
        cur.execute(query, (user_id, codigo_permiso))
        result = cur.fetchone()
        cur.close()
        return bool(result)

    @staticmethod
    def get_total_users_count():
        """Obtiene el número total de usuarios en el sistema."""
        try:
            cur = get_cursor('dict')
            if cur is None:
                print("Error: No se pudo crear cursor para conteo de usuarios")
                return 0
            
            cur.execute('SELECT COUNT(*) as count FROM usuarios')
            result = cur.fetchone()
            cur.close()
            
            if result and 'count' in result:
                count = result['count']
                print(f"DEBUG: Conteo de usuarios obtenido: {count}")
                return count
            else:
                print("DEBUG: No se obtuvo resultado del conteo de usuarios")
                return 0
        except Exception as e:
            print(f"Error al obtener el conteo de usuarios: {e}")
            import traceback
            traceback.print_exc()
            return 0

    @staticmethod
    def get_users_by_role(id_rol):
        """Obtiene todos los usuarios con un rol específico."""
        try:
            cur = mysql.connection.cursor()
            
            print(f"DEBUG: Buscando usuarios con rol {id_rol}")
            
            # Consulta simple sin fecha_registro (columna no existe)
            query = '''
                SELECT id, correo, nombre, apellido
                FROM usuarios
                WHERE id_rol = %s
                ORDER BY nombre, apellido
            '''
            
            print(f"DEBUG: Ejecutando consulta: {query}")
            print(f"DEBUG: Con parámetro id_rol = {id_rol}")
            
            cur.execute(query, (id_rol,))
            rows = cur.fetchall()
            
            print(f"DEBUG: Consulta ejecutada. Filas obtenidas: {len(rows)}")
            
            # Debug adicional: mostrar estructura de las filas
            if rows:
                print(f"DEBUG: Estructura de la primera fila: {rows[0]}")
                print(f"DEBUG: Tipo de la primera fila: {type(rows[0])}")
                print(f"DEBUG: Longitud de la primera fila: {len(rows[0])}")
            else:
                print("DEBUG: No se encontraron filas. Verificando si hay usuarios con ese rol...")
                # Consulta de verificación
                cur.execute("SELECT COUNT(*) FROM usuarios WHERE id_rol = %s", (id_rol,))
                count = cur.fetchone()[0]
                print(f"DEBUG: Conteo directo de usuarios con rol {id_rol}: {count}")
                
                if count == 0:
                    print("DEBUG: No hay usuarios con ese rol en la base de datos")
                else:
                    print("DEBUG: Hay usuarios con ese rol, pero la consulta no los devuelve")
            
            # Convertir a lista de diccionarios
            users = []
            for i, row in enumerate(rows):
                if isinstance(row, dict):
                    # Los datos ya vienen como diccionario
                    user_dict = {
                        'id': row.get('id'),
                        'correo': row.get('correo'),
                        'nombre': row.get('nombre'),
                        'apellido': row.get('apellido'),
                        'fecha_registro': None,  # No existe en la tabla
                        'activo': 1  # Asumir activo por defecto
                    }
                else:
                    # Los datos vienen como tupla (fallback)
                    user_dict = {
                        'id': row[0],
                        'correo': row[1],
                        'nombre': row[2],
                        'apellido': row[3],
                        'fecha_registro': None,  # No existe en la tabla
                        'activo': 1  # Asumir activo por defecto
                    }
                
                users.append(user_dict)
                print(f"DEBUG: Usuario {i+1}: {user_dict['nombre']} {user_dict['apellido']} (ID: {user_dict['id']}, Email: {user_dict['correo']})")
            
            cur.close()
            print(f"DEBUG: Retornando {len(users)} usuarios")
            return users
            
        except Exception as e:
            print(f"ERROR al obtener usuarios por rol {id_rol}: {e}")
            import traceback
            traceback.print_exc()
            return []