#!/usr/bin/env python3
"""
Script para arreglar la restricción UNIQUE
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

try:
    import MySQLdb
except ImportError:
    import pymysql as MySQLdb

def fix_unique_constraint():
    """Arregla la restricción UNIQUE para permitir reasignaciones"""
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
        
        # Eliminar la restricción UNIQUE actual
        print("🔧 Eliminando restricción UNIQUE actual...")
        try:
            cursor.execute("ALTER TABLE estudiante_acudientes DROP INDEX unique_student_acudiente")
            print("✅ Restricción eliminada")
        except Exception as e:
            print(f"⚠️  No se pudo eliminar la restricción (puede que no exista): {e}")
        
        # Crear nueva restricción UNIQUE que incluya el campo activo
        print("🔧 Creando nueva restricción UNIQUE...")
        cursor.execute("""
            ALTER TABLE estudiante_acudientes 
            ADD CONSTRAINT unique_active_student_acudiente 
            UNIQUE (estudiante_id, acudiente_id, activo)
        """)
        print("✅ Nueva restricción creada")
        
        # Alternativamente, podemos limpiar las relaciones inactivas duplicadas
        print("🧹 Limpiando relaciones inactivas duplicadas...")
        
        # Reactivar relaciones inactivas si no hay conflicto
        cursor.execute("""
            UPDATE estudiante_acudientes ea1
            SET activo = 1
            WHERE ea1.activo = 0
            AND NOT EXISTS (
                SELECT 1 FROM estudiante_acudientes ea2 
                WHERE ea2.estudiante_id = ea1.estudiante_id 
                AND ea2.acudiente_id = ea1.acudiente_id 
                AND ea2.activo = 1
                AND ea2.id != ea1.id
            )
        """)
        
        reactivated = cursor.rowcount
        print(f"✅ {reactivated} relaciones reactivadas")
        
        connection.commit()
        
        # Verificar el resultado
        print("\n📊 Estado final:")
        cursor.execute("""
            SELECT ea.id, e.nombre as estudiante, u.nombre as acudiente, ea.tipo_relacion, ea.activo
            FROM estudiante_acudientes ea
            JOIN estudiantes e ON ea.estudiante_id = e.id
            JOIN usuarios u ON ea.acudiente_id = u.id
            ORDER BY e.nombre, ea.activo DESC
        """)
        
        relations = cursor.fetchall()
        for rel in relations:
            status = "✅ Activo" if rel[4] else "❌ Inactivo"
            print(f"   {rel[1]} -> {rel[2]} ({rel[3]}) {status}")
        
        cursor.close()
        connection.close()
        
        print(f"\n🎯 Restricción UNIQUE arreglada!")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    print("🔧 Arreglando restricción UNIQUE...")
    fix_unique_constraint()
