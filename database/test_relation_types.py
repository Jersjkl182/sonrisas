#!/usr/bin/env python3
"""
Script para probar los tipos de relación
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

try:
    import MySQLdb
except ImportError:
    import pymysql as MySQLdb

def test_relation_types():
    """Prueba los tipos de relación"""
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
        
        print("\n🔍 PROBANDO TIPOS DE RELACIÓN:")
        
        # Mostrar relaciones actuales
        print("\n📊 Relaciones actuales:")
        cursor.execute("""
            SELECT e.nombre as estudiante, u.nombre as acudiente, ea.tipo_relacion
            FROM estudiante_acudientes ea
            JOIN estudiantes e ON ea.estudiante_id = e.id
            JOIN usuarios u ON ea.acudiente_id = u.id
            WHERE ea.activo = 1
            ORDER BY e.nombre, ea.tipo_relacion = 'principal' DESC
        """)
        
        relations = cursor.fetchall()
        for rel in relations:
            icon = "👑" if rel[2] == 'principal' else "🤝"
            print(f"   {icon} {rel[0]} -> {rel[1]} ({rel[2]})")
        
        # Verificar que ambos tipos existen
        print("\n🏷️  Verificando tipos de relación disponibles:")
        cursor.execute("SELECT DISTINCT tipo_relacion FROM estudiante_acudientes WHERE activo = 1")
        types = cursor.fetchall()
        
        available_types = [t[0] for t in types]
        
        if 'principal' in available_types:
            print("   ✅ Tipo 'principal' disponible")
        else:
            print("   ❌ Tipo 'principal' NO encontrado")
        
        if 'secundario' in available_types:
            print("   ✅ Tipo 'secundario' disponible")
        else:
            print("   ❌ Tipo 'secundario' NO encontrado")
        
        # Contar por tipo
        print("\n📈 Estadísticas por tipo:")
        cursor.execute("""
            SELECT tipo_relacion, COUNT(*) as cantidad
            FROM estudiante_acudientes 
            WHERE activo = 1
            GROUP BY tipo_relacion
        """)
        
        stats = cursor.fetchall()
        for stat in stats:
            icon = "👑" if stat[0] == 'principal' else "🤝"
            print(f"   {icon} {stat[0].capitalize()}: {stat[1]} relaciones")
        
        # Verificar estudiantes con ambos tipos
        print("\n👥 Estudiantes con ambos tipos de acudientes:")
        cursor.execute("""
            SELECT e.nombre,
                   COUNT(CASE WHEN ea.tipo_relacion = 'principal' THEN 1 END) as principales,
                   COUNT(CASE WHEN ea.tipo_relacion = 'secundario' THEN 1 END) as secundarios
            FROM estudiantes e
            LEFT JOIN estudiante_acudientes ea ON e.id = ea.estudiante_id AND ea.activo = 1
            GROUP BY e.id
            HAVING principales > 0 OR secundarios > 0
        """)
        
        student_stats = cursor.fetchall()
        for stat in student_stats:
            status = ""
            if stat[1] > 0 and stat[2] > 0:
                status = "✅ Completo"
            elif stat[1] > 0:
                status = "⚠️  Solo principal"
            elif stat[2] > 0:
                status = "⚠️  Solo secundario"
            
            print(f"   {status} {stat[0]}: {stat[1]} principal(es), {stat[2]} secundario(s)")
        
        cursor.close()
        connection.close()
        
        print(f"\n🎯 Verificación de tipos de relación completada!")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    print("🧪 Probando tipos de relación...")
    test_relation_types()
