#!/usr/bin/env python3
"""
Script para probar asignación directa sin Flask
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

try:
    import MySQLdb
except ImportError:
    import pymysql as MySQLdb

def test_assignment_direct():
    """Prueba asignación directa"""
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
        
        student_id = 7
        acudiente_id = 12  # Maria Rodriguez
        
        print(f"📚 Estudiante ID: {student_id}")
        print(f"👨‍👩‍👧‍👦 Acudiente ID: {acudiente_id}")
        
        # Verificar que el estudiante existe
        cursor.execute("SELECT id FROM estudiantes WHERE id = %s", (student_id,))
        student_result = cursor.fetchone()
        if not student_result:
            print("❌ Estudiante no encontrado")
            return
        print("✅ Estudiante encontrado")
        
        # Verificar que el acudiente existe
        cursor.execute("SELECT id FROM usuarios WHERE id = %s AND id_rol = 4 AND is_active = 1", (acudiente_id,))
        acudiente_result = cursor.fetchone()
        if not acudiente_result:
            print("❌ Acudiente no encontrado")
            return
        print("✅ Acudiente encontrado")
        
        # Verificar límite de acudientes
        cursor.execute("""
            SELECT COUNT(*) FROM estudiante_acudientes 
            WHERE estudiante_id = %s AND activo = 1
        """, (student_id,))
        
        result = cursor.fetchone()
        current_count = result[0] if result else 0
        print(f"📊 Acudientes actuales: {current_count}")
        
        if current_count >= 2:
            print("❌ Ya tiene 2 acudientes")
            return
        
        # Verificar duplicados
        cursor.execute("""
            SELECT id FROM estudiante_acudientes 
            WHERE estudiante_id = %s AND acudiente_id = %s AND activo = 1
        """, (student_id, acudiente_id))
        
        duplicate_result = cursor.fetchone()
        if duplicate_result:
            print("❌ Acudiente ya asignado")
            return
        print("✅ No hay duplicados")
        
        # Determinar tipo
        if current_count == 0:
            tipo_relacion = 'principal'
        else:
            cursor.execute("""
                SELECT tipo_relacion FROM estudiante_acudientes 
                WHERE estudiante_id = %s AND activo = 1 LIMIT 1
            """, (student_id,))
            existing_result = cursor.fetchone()
            if existing_result and existing_result[0] == 'principal':
                tipo_relacion = 'secundario'
            else:
                tipo_relacion = 'principal'
        
        print(f"🏷️  Tipo de relación: {tipo_relacion}")
        
        # Insertar
        insert_query = """
            INSERT INTO estudiante_acudientes (estudiante_id, acudiente_id, tipo_relacion, activo, fecha_asignacion)
            VALUES (%s, %s, %s, 1, NOW())
        """
        
        cursor.execute(insert_query, (student_id, acudiente_id, tipo_relacion))
        insert_id = cursor.lastrowid
        print(f"✅ Insertado con ID: {insert_id}")
        
        connection.commit()
        cursor.close()
        connection.close()
        
        print("🎯 ¡Asignación exitosa!")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    print("🧪 Probando asignación directa...")
    test_assignment_direct()
