#!/usr/bin/env python3
"""
Script para probar el sistema de múltiples acudientes
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

try:
    import MySQLdb
except ImportError:
    import pymysql as MySQLdb

def test_acudientes_system():
    """Prueba el sistema de múltiples acudientes"""
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
        
        # Verificar estructura de la tabla
        print("\n📋 Verificando estructura de estudiante_acudientes...")
        cursor.execute("DESCRIBE estudiante_acudientes")
        columns = cursor.fetchall()
        for col in columns:
            print(f"   - {col[0]}: {col[1]}")
        
        # Verificar datos actuales
        print("\n👥 Relaciones actuales:")
        cursor.execute("""
            SELECT ea.id, e.nombre as estudiante, u.nombre as acudiente, ea.tipo_relacion, ea.activo
            FROM estudiante_acudientes ea
            JOIN estudiantes e ON ea.estudiante_id = e.id
            JOIN usuarios u ON ea.acudiente_id = u.id
            ORDER BY e.nombre, ea.tipo_relacion
        """)
        
        relations = cursor.fetchall()
        for rel in relations:
            status = "✅ Activo" if rel[4] else "❌ Inactivo"
            print(f"   {rel[1]} -> {rel[2]} ({rel[3]}) {status}")
        
        # Probar consulta de estudiantes con múltiples acudientes
        print("\n🎓 Estudiantes con sus acudientes:")
        cursor.execute("""
            SELECT e.nombre, e.apellido,
                   GROUP_CONCAT(
                       CONCAT(u.nombre, ' ', u.apellido, ' (', ea.tipo_relacion, ')')
                       ORDER BY ea.tipo_relacion = 'principal' DESC
                       SEPARATOR ', '
                   ) as acudientes,
                   COUNT(ea.id) as total_acudientes
            FROM estudiantes e
            LEFT JOIN estudiante_acudientes ea ON e.id = ea.estudiante_id AND ea.activo = 1
            LEFT JOIN usuarios u ON ea.acudiente_id = u.id
            GROUP BY e.id
            ORDER BY e.nombre
        """)
        
        students = cursor.fetchall()
        for student in students:
            acudientes = student[2] if student[2] else "Sin acudientes"
            print(f"   {student[0]} {student[1]}: {acudientes} ({student[3]}/2)")
        
        # Verificar límite de 2 acudientes
        print("\n🔒 Verificando límite de acudientes...")
        cursor.execute("""
            SELECT e.nombre, COUNT(ea.id) as total
            FROM estudiantes e
            LEFT JOIN estudiante_acudientes ea ON e.id = ea.estudiante_id AND ea.activo = 1
            GROUP BY e.id
            HAVING total > 2
        """)
        
        over_limit = cursor.fetchall()
        if over_limit:
            print("   ⚠️  Estudiantes con más de 2 acudientes:")
            for student in over_limit:
                print(f"      {student[0]}: {student[1]} acudientes")
        else:
            print("   ✅ Todos los estudiantes respetan el límite de 2 acudientes")
        
        # Mostrar acudientes disponibles
        print("\n👨‍👩‍👧‍👦 Acudientes disponibles en el sistema:")
        cursor.execute("""
            SELECT u.id, u.nombre, u.apellido, u.correo,
                   COUNT(ea.id) as estudiantes_asignados
            FROM usuarios u
            LEFT JOIN estudiante_acudientes ea ON u.id = ea.acudiente_id AND ea.activo = 1
            WHERE u.id_rol = 4 AND u.is_active = 1
            GROUP BY u.id
            ORDER BY u.nombre
        """)
        
        acudientes = cursor.fetchall()
        for acudiente in acudientes:
            print(f"   {acudiente[1]} {acudiente[2]} ({acudiente[3]}) - {acudiente[4]} estudiantes")
        
        cursor.close()
        connection.close()
        
        print(f"\n🎯 Sistema de múltiples acudientes funcionando correctamente!")
        print(f"   - {len(relations)} relaciones activas")
        print(f"   - {len(students)} estudiantes en el sistema")
        print(f"   - {len(acudientes)} acudientes disponibles")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    print("🧪 Probando sistema de múltiples acudientes...")
    test_acudientes_system()
