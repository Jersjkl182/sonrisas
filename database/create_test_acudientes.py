#!/usr/bin/env python3
"""
Script para crear acudientes de prueba
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

try:
    import MySQLdb
except ImportError:
    import pymysql as MySQLdb

from werkzeug.security import generate_password_hash

def create_test_acudientes():
    """Crea acudientes de prueba"""
    try:
        connection = MySQLdb.connect(
            host='localhost',
            user='root',
            password='',
            database='login',
            charset='utf8mb4'
        )
        
        cursor = connection.cursor()
        print("✅ Conexión establecida")
        
        # Acudientes de prueba
        test_acudientes = [
            {
                'nombre': 'Maria',
                'apellido': 'Rodriguez',
                'correo': 'maria.rodriguez@email.com',
                'cedula': '12345678',
                'password': '123456'
            },
            {
                'nombre': 'Carlos',
                'apellido': 'Gonzalez',
                'correo': 'carlos.gonzalez@email.com',
                'cedula': '87654321',
                'password': '123456'
            },
            {
                'nombre': 'Ana',
                'apellido': 'Martinez',
                'correo': 'ana.martinez@email.com',
                'ppt': 'PPT123456789',
                'password': '123456'
            },
            {
                'nombre': 'Luis',
                'apellido': 'Perez',
                'correo': 'luis.perez@email.com',
                'cedula': '11223344',
                'password': '123456'
            }
        ]
        
        created_count = 0
        
        for acudiente in test_acudientes:
            # Verificar si ya existe
            cursor.execute("SELECT id FROM usuarios WHERE correo = %s", (acudiente['correo'],))
            if cursor.fetchone():
                print(f"⚠️  {acudiente['nombre']} {acudiente['apellido']} ya existe")
                continue
            
            # Crear hash de contraseña
            password_hash = generate_password_hash(acudiente['password'])
            
            # Insertar acudiente
            cursor.execute("""
                INSERT INTO usuarios (nombre, apellido, correo, cedula, ppt, contrasena, id_rol, is_active)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """, (
                acudiente['nombre'],
                acudiente['apellido'],
                acudiente['correo'],
                acudiente.get('cedula'),
                acudiente.get('ppt'),
                password_hash,
                4,  # id_rol para acudiente
                1   # is_active
            ))
            
            created_count += 1
            print(f"✅ Creado: {acudiente['nombre']} {acudiente['apellido']}")
        
        connection.commit()
        
        # Mostrar todos los acudientes
        cursor.execute("""
            SELECT id, nombre, apellido, correo, cedula, ppt
            FROM usuarios 
            WHERE id_rol = 4 AND is_active = 1
            ORDER BY nombre
        """)
        
        acudientes = cursor.fetchall()
        print(f"\n👨‍👩‍👧‍👦 Acudientes disponibles ({len(acudientes)}):")
        for acudiente in acudientes:
            doc = f"Cédula: {acudiente[4]}" if acudiente[4] else f"PPT: {acudiente[5]}" if acudiente[5] else "Sin documento"
            print(f"   ID: {acudiente[0]} - {acudiente[1]} {acudiente[2]} ({acudiente[3]}) - {doc}")
        
        cursor.close()
        connection.close()
        
        print(f"\n🎯 {created_count} acudientes creados exitosamente!")
        print(f"   Contraseña para todos: 123456")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    print("👨‍👩‍👧‍👦 Creando acudientes de prueba...")
    create_test_acudientes()
