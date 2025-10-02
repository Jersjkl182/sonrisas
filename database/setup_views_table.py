#!/usr/bin/env python3
"""
Script simple para crear tabla observation_views
"""

import pymysql
import os

def create_table():
    """Crea la tabla observation_views"""
    try:
        # Configuración de conexión
        connection = pymysql.connect(
            host='localhost',
            user='root',
            password='',  # Ajustar según tu configuración
            database='sonrisas_db',
            charset='utf8mb4'
        )
        
        cursor = connection.cursor()
        
        # SQL para crear la tabla
        create_sql = """
        CREATE TABLE IF NOT EXISTS observation_views (
            id INT AUTO_INCREMENT PRIMARY KEY,
            observation_id INT NOT NULL,
            acudiente_id INT NOT NULL,
            viewed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            ip_address VARCHAR(45),
            user_agent TEXT,
            INDEX idx_observation_acudiente (observation_id, acudiente_id),
            INDEX idx_acudiente_viewed (acudiente_id, viewed_at),
            UNIQUE KEY unique_view (observation_id, acudiente_id)
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
        """
        
        cursor.execute(create_sql)
        connection.commit()
        
        print("✅ Tabla observation_views creada exitosamente")
        
        # Verificar la tabla
        cursor.execute("SHOW TABLES LIKE 'observation_views'")
        result = cursor.fetchone()
        
        if result:
            print("✅ Tabla verificada en la base de datos")
            
            # Mostrar estructura
            cursor.execute("DESCRIBE observation_views")
            columns = cursor.fetchall()
            
            print("\n📋 ESTRUCTURA DE LA TABLA:")
            print("-" * 60)
            for column in columns:
                print(f"   {column[0]:<20} {column[1]:<15}")
        
        cursor.close()
        connection.close()
        
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == "__main__":
    print("🔧 CREANDO TABLA OBSERVATION_VIEWS")
    print("="*50)
    
    if create_table():
        print("\n🎯 TABLA LISTA PARA USO")
        print("La funcionalidad de visualizaciones está configurada.")
    else:
        print("\n❌ ERROR AL CREAR LA TABLA")
        print("Verifica la configuración de la base de datos.")
