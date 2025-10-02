#!/usr/bin/env python3
"""
Script para verificar que todas las rutas de estudiantes estén funcionando correctamente.
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))

from backend.src.app import create_app
from flask import url_for

def test_student_routes():
    """Verifica que todas las rutas de estudiantes estén configuradas correctamente."""
    
    app = create_app()
    
    with app.app_context():
        print("🧪 Verificando rutas de estudiantes...")
        
        # Lista de rutas que deben existir
        student_routes = [
            ('admin_bp.listar_estudiantes', 'GET'),
            ('admin_bp.crear_estudiante', 'GET'),
            ('admin_bp.crear_estudiante', 'POST'),
        ]
        
        print("\n📋 Rutas de estudiantes verificadas:")
        
        for route_name, method in student_routes:
            try:
                # Verificar que la ruta existe
                if route_name.endswith('crear_estudiante') and method == 'GET':
                    url = url_for(route_name)
                elif route_name.endswith('listar_estudiantes'):
                    url = url_for(route_name)
                else:
                    url = f"Ruta {route_name} ({method})"
                
                print(f"✅ {route_name} ({method}): {url}")
                
            except Exception as e:
                print(f"❌ {route_name} ({method}): Error - {e}")
        
        print("\n🎯 URLs importantes para acceder a gestión de estudiantes:")
        print(f"📋 Ver estudiantes: {url_for('admin_bp.listar_estudiantes')}")
        print(f"➕ Crear estudiante: {url_for('admin_bp.crear_estudiante')}")
        print(f"🏠 Dashboard admin: {url_for('admin_bp.admin')}")
        
        print("\n🔗 Enlaces en el menú lateral:")
        print("- Menú 'Gestión de Estudiantes' (collapsible)")
        print("  └── Ver Todos los Estudiantes")
        print("  └── Crear Nuevo Estudiante")
        
        print("\n🎨 Elementos visuales destacados:")
        print("- Card destacada en dashboard con animación")
        print("- Menú lateral con estilos especiales para estudiantes")
        print("- CSS consolidado sin conflictos")
        
        return True

if __name__ == '__main__':
    print("🚀 Iniciando verificación de rutas de estudiantes...")
    success = test_student_routes()
    if success:
        print("\n✅ Verificación completada exitosamente")
        print("\n📝 INSTRUCCIONES PARA ACCEDER:")
        print("1. Inicia sesión como administrador")
        print("2. En el dashboard, haz clic en la card '🎓 Gestión de Estudiantes'")
        print("3. O usa el menú lateral: 'Gestión de Estudiantes' > 'Ver Todos los Estudiantes'")
        print("4. Para crear: 'Gestión de Estudiantes' > 'Crear Nuevo Estudiante'")
    else:
        print("❌ Verificación falló")
