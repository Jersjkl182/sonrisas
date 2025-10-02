#!/usr/bin/env python3
"""
Script para verificar la estructura de la tabla estudiantes
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

try:
    import MySQLdb
except ImportError:
    import pymysql as MySQLdb

def check_student_structure():
    """Verifica la estructura de la tabla estudiantes"""
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
        
        # Mostrar estructura de la tabla estudiantes
        cursor.execute("DESCRIBE estudiantes")
        columns = cursor.fetchall()
        print(f"\n📋 Estructura de la tabla 'estudiantes':")
        for i, column in enumerate(columns, 1):
            print(f"   {i}. {column[0]} - {column[1]} - {column[2]} - {column[3]}")
        
        # Mostrar algunos datos de ejemplo
        cursor.execute("SELECT id, nombre, apellido, acudiente_id FROM estudiantes LIMIT 5")
        students = cursor.fetchall()
        print(f"\n👥 Datos de ejemplo ({len(students)} estudiantes):")
        for student in students:
            print(f"   ID: {student[0]}, Nombre: {student[1]} {student[2]}, Acudiente ID: {student[3]}")
        
        cursor.close()
        connection.close()
        
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    print("🔍 Verificando estructura de tabla estudiantes...")
    check_student_structure()
