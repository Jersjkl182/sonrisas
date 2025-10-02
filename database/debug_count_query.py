#!/usr/bin/env python3
"""
Script para debuggear la consulta COUNT
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

try:
    import MySQLdb
except ImportError:
    import pymysql as MySQLdb

def debug_count_query():
    """Debug de la consulta COUNT"""
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
        
        # Probar la consulta COUNT exacta
        print(f"\n🔍 Probando consulta COUNT para estudiante {student_id}:")
        query = """
            SELECT COUNT(*) FROM estudiante_acudientes 
            WHERE estudiante_id = %s AND activo = 1
        """
        print(f"Query: {query}")
        print(f"Parámetros: ({student_id},)")
        
        cursor.execute(query, (student_id,))
        result = cursor.fetchone()
        
        print(f"Resultado fetchone(): {result}")
        print(f"Tipo de resultado: {type(result)}")
        
        if result:
            print(f"result[0]: {result[0]}")
            print(f"Tipo de result[0]: {type(result[0])}")
        else:
            print("❌ result es None!")
        
        # Probar sin parámetros
        print(f"\n🔍 Probando consulta sin WHERE:")
        cursor.execute("SELECT COUNT(*) FROM estudiante_acudientes")
        total_result = cursor.fetchone()
        print(f"Total registros: {total_result}")
        
        # Mostrar todos los registros
        print(f"\n📋 Todos los registros de estudiante_acudientes:")
        cursor.execute("SELECT * FROM estudiante_acudientes")
        all_records = cursor.fetchall()
        for record in all_records:
            print(f"   {record}")
        
        cursor.close()
        connection.close()
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    print("🔍 Debuggeando consulta COUNT...")
    debug_count_query()
