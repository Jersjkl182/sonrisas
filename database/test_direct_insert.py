#!/usr/bin/env python3
"""
Script para probar inserción directa en estudiante_acudientes
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

try:
    import MySQLdb
except ImportError:
    import pymysql as MySQLdb

def test_direct_insert():
    """Prueba inserción directa"""
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
        
        # Obtener un estudiante y un acudiente disponible
        cursor.execute("SELECT id, nombre, apellido FROM estudiantes LIMIT 1")
        student = cursor.fetchone()
        if not student:
            print("❌ No hay estudiantes")
            return
        
        student_id = student[0]
        print(f"📚 Estudiante: {student[1]} {student[2]} (ID: {student_id})")
        
        # Mostrar acudientes ya asignados
        cursor.execute("""
            SELECT u.nombre, u.apellido, ea.tipo_relacion
            FROM estudiante_acudientes ea
            JOIN usuarios u ON ea.acudiente_id = u.id
            WHERE ea.estudiante_id = %s AND ea.activo = 1
        """, (student_id,))
        
        assigned = cursor.fetchall()
        print(f"📋 Acudientes ya asignados:")
        for acud in assigned:
            print(f"   - {acud[0]} {acud[1]} ({acud[2]})")
        
        # Obtener acudientes disponibles (que no estén ya asignados a este estudiante)
        cursor.execute("""
            SELECT u.id, u.nombre, u.apellido 
            FROM usuarios u 
            WHERE u.id_rol = 4 AND u.is_active = 1
            AND u.id NOT IN (
                SELECT acudiente_id FROM estudiante_acudientes 
                WHERE estudiante_id = %s AND activo = 1
            )
            LIMIT 1
        """, (student_id,))
        
        acudiente = cursor.fetchone()
        if not acudiente:
            print("❌ No hay acudientes disponibles")
            return
        
        acudiente_id = acudiente[0]
        print(f"👨‍👩‍👧‍👦 Acudiente: {acudiente[1]} {acudiente[2]} (ID: {acudiente_id})")
        
        # Verificar cuántos acudientes tiene actualmente
        cursor.execute("""
            SELECT COUNT(*) FROM estudiante_acudientes 
            WHERE estudiante_id = %s AND activo = 1
        """, (student_id,))
        
        current_count = cursor.fetchone()[0]
        print(f"📊 Acudientes actuales: {current_count}")
        
        if current_count >= 2:
            print("⚠️  Ya tiene 2 acudientes, no se puede agregar más")
            return
        
        # Determinar tipo
        tipo_relacion = 'principal' if current_count == 0 else 'secundario'
        print(f"🏷️  Tipo de relación: {tipo_relacion}")
        
        # Insertar
        print(f"🔄 Insertando relación...")
        cursor.execute("""
            INSERT INTO estudiante_acudientes (estudiante_id, acudiente_id, tipo_relacion, activo, fecha_asignacion)
            VALUES (%s, %s, %s, 1, NOW())
        """, (student_id, acudiente_id, tipo_relacion))
        
        insert_id = cursor.lastrowid
        print(f"✅ Insertado con ID: {insert_id}")
        
        connection.commit()
        
        # Verificar inserción
        cursor.execute("""
            SELECT ea.id, e.nombre as estudiante, u.nombre as acudiente, ea.tipo_relacion
            FROM estudiante_acudientes ea
            JOIN estudiantes e ON ea.estudiante_id = e.id
            JOIN usuarios u ON ea.acudiente_id = u.id
            WHERE ea.id = %s
        """, (insert_id,))
        
        result = cursor.fetchone()
        if result:
            print(f"🎯 Verificación exitosa: {result[1]} -> {result[2]} ({result[3]})")
        else:
            print("❌ No se pudo verificar la inserción")
        
        cursor.close()
        connection.close()
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    print("🧪 Probando inserción directa...")
    test_direct_insert()
