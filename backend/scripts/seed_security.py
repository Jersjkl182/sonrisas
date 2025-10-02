"""Script para poblar permisos básicos, crear el rol Administrador y asignarlo al usuario 1.

Uso:
    python backend/scripts/seed_security.py

Asegúrese de que las variables de entorno de la base de datos estén configuradas o
exista un archivo .env con la configuración apropiada antes de ejecutar.
"""
import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))
from src.app import create_app
from src.services.permission_service import PermissionService
from src.services.role_service import RoleService
from src.models.user_model import UserModel

# Lista de permisos base (código, descripción)
PERMISOS_BASE = [
    ("ver_roles", "Ver lista de roles"),
    ("crear_rol", "Crear rol"),
    ("editar_rol", "Editar rol"),
    ("eliminar_rol", "Eliminar rol"),
    ("ver_permisos", "Ver lista de permisos"),
    ("crear_permiso", "Crear permiso"),
    ("editar_permiso", "Editar permiso"),
    ("eliminar_permiso", "Eliminar permiso"),
]

ADMIN_ROLE_DESC = "Administrador"
ADMIN_USER_ID = 1  # Modificar si el superusuario es otro ID

def main():
    app = create_app()
    with app.app_context():
        # Crear permisos si no existen
        for codigo, desc in PERMISOS_BASE:
            if not PermissionService.get_by_code(codigo):
                PermissionService.create(codigo, desc)
                print(f"Permiso '{codigo}' creado")

        # Crear rol administrador si no existe
        admin_role = None
        for rol in RoleService.list_all():
            if rol['descripcion'] == ADMIN_ROLE_DESC:
                admin_role = rol
                break
        if not admin_role:
            admin_role_id = RoleService.create(ADMIN_ROLE_DESC)
            admin_role = RoleService.get(admin_role_id)
            print("Rol Administrador creado")
        admin_role_id = admin_role['id_rol']

        # Asociar todos los permisos al rol administrador
        existing_perms = {p['codigo'] for p in RoleService.list_permissions(admin_role_id)}
        for permiso in PermissionService.list_all():
            if permiso['codigo'] not in existing_perms:
                RoleService.add_permission(admin_role_id, permiso['id'])
        print("Permisos asignados al rol Administrador")

        # Asignar rol al usuario admin
        usuario = UserModel.find_by_id(ADMIN_USER_ID)
        if usuario:
            if admin_role_id not in set(UserModel.get_roles(ADMIN_USER_ID)):
                UserModel.add_role(ADMIN_USER_ID, admin_role_id)
                print("Rol Administrador asignado al usuario 1")
        print("Seeding completado")

if __name__ == "__main__":
    main()
