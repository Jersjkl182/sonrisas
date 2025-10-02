#!/usr/bin/env python3
"""
Script para debuggear las relaciones existentes
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

try:
    import MySQLdb
except ImportError:
    import pymysql as MySQLdb

def debug_relations():
    """Debug de las relaciones"""
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
        
        # Mostrar todas las relaciones
        print("\n📋 Todas las relaciones en estudiante_acudientes:")
        cursor.execute("""
            SELECT ea.id, ea.estudiante_id, ea.acudiente_id, ea.tipo_relacion, ea.activo,
                   e.nombre as estudiante, u.nombre as acudiente
            FROM estudiante_acudientes ea
            LEFT JOIN estudiantes e ON ea.estudiante_id = e.id
            LEFT JOIN usuarios u ON ea.acudiente_id = u.id
            ORDER BY ea.estudiante_id, ea.tipo_relacion
        """)
        
        relations = cursor.fetchall()
        for rel in relations:
            status = "✅ Activo" if rel[4] else "❌ Inactivo"
            print(f"   ID: {rel[0]} - Estudiante: {rel[5]} (ID: {rel[1]}) -> Acudiente: {rel[6]} (ID: {rel[2]}) - {rel[3]} - {status}")
        
        # Contar por estudiante
        print("\n📊 Conteo por estudiante:")
        cursor.execute("""
            SELECT e.id, e.nombre, e.apellido,
                   COUNT(ea.id) as total_relaciones,
                   COUNT(CASE WHEN ea.activo = 1 THEN 1 END) as activas
            FROM estudiantes e
            LEFT JOIN estudiante_acudientes ea ON e.id = ea.estudiante_id
            GROUP BY e.id
            ORDER BY e.nombre
        """)
        
        counts = cursor.fetchall()
        for count in counts:
            print(f"   {count[1]} {count[2]} (ID: {count[0]}) - Total: {count[3]}, Activas: {count[4]}")
        
        # Verificar estudiante específico (ID 6)
        print(f"\n🔍 Detalle del estudiante ID 6:")
        cursor.execute("""
            SELECT ea.*, u.nombre, u.apellido
            FROM estudiante_acudientes ea
            JOIN usuarios u ON ea.acudiente_id = u.id
            WHERE ea.estudiante_id = 6
        """)
        
        student_6_relations = cursor.fetchall()
        for rel in student_6_relations:
            status = "✅ Activo" if rel[4] else "❌ Inactivo"
            print(f"   Acudiente: {rel[5]} {rel[6]} - Tipo: {rel[3]} - {status}")
        
        cursor.close()
        connection.close()
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    print("🔍 Debuggeando relaciones...")
    debug_relations()
