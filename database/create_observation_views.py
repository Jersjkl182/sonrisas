#!/usr/bin/env python3
"""
Script para crear la tabla observation_views
"""

import sys
import os

# Agregar el directorio padre al path para importar módulos
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'backend', 'src'))

from database.db_connection import mysql

def create_observation_views_table():
    """Crea la tabla observation_views"""
    print("🔧 CREANDO TABLA OBSERVATION_VIEWS")
    print("="*50)
    
    sql_script = """
    -- Tabla para rastrear qué observaciones han sido vistas por los acudientes
    CREATE TABLE IF NOT EXISTS observation_views (
        id INT AUTO_INCREMENT PRIMARY KEY,
        observation_id INT NOT NULL,
        acudiente_id INT NOT NULL,
        viewed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        ip_address VARCHAR(45),
        user_agent TEXT,
        INDEX idx_observation_acudiente (observation_id, acudiente_id),
        INDEX idx_acudiente_viewed (acudiente_id, viewed_at),
        FOREIGN KEY (observation_id) REFERENCES observaciones(id) ON DELETE CASCADE,
        FOREIGN KEY (acudiente_id) REFERENCES usuarios(id) ON DELETE CASCADE,
        UNIQUE KEY unique_view (observation_id, acudiente_id)
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
    """
    
    try:
        cur = mysql.connection.cursor()
        
        # Ejecutar el script
        cur.execute(sql_script)
        mysql.connection.commit()
        
        print("✅ Tabla observation_views creada exitosamente")
        
        # Verificar que la tabla se creó
        cur.execute("SHOW TABLES LIKE 'observation_views'")
        result = cur.fetchone()
        
        if result:
            print("✅ Tabla verificada en la base de datos")
            
            # Mostrar estructura de la tabla
            cur.execute("DESCRIBE observation_views")
            columns = cur.fetchall()
            
            print("\n📋 ESTRUCTURA DE LA TABLA:")
            print("-" * 60)
            for column in columns:
                print(f"   {column[0]:<20} {column[1]:<15} {column[2]:<10} {column[3]:<10}")
        else:
            print("❌ Error: La tabla no se creó correctamente")
        
        cur.close()
        
    except Exception as e:
        print(f"❌ Error al crear la tabla: {e}")
        import traceback
        traceback.print_exc()

def add_comments():
    """Agrega comentarios a la tabla"""
    try:
        cur = mysql.connection.cursor()
        
        comments_sql = [
            "ALTER TABLE observation_views COMMENT = 'Tabla para rastrear visualizaciones de observaciones por acudientes'",
            "ALTER TABLE observation_views MODIFY COLUMN observation_id INT NOT NULL COMMENT 'ID de la observación vista'",
            "ALTER TABLE observation_views MODIFY COLUMN acudiente_id INT NOT NULL COMMENT 'ID del acudiente que vio la observación'",
            "ALTER TABLE observation_views MODIFY COLUMN viewed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT 'Fecha y hora de visualización'",
            "ALTER TABLE observation_views MODIFY COLUMN ip_address VARCHAR(45) COMMENT 'Dirección IP desde donde se vio'",
            "ALTER TABLE observation_views MODIFY COLUMN user_agent TEXT COMMENT 'User agent del navegador'"
        ]
        
        for comment_sql in comments_sql:
            cur.execute(comment_sql)
        
        mysql.connection.commit()
        cur.close()
        
        print("✅ Comentarios agregados a la tabla")
        
    except Exception as e:
        print(f"⚠️  Advertencia al agregar comentarios: {e}")

if __name__ == "__main__":
    create_observation_views_table()
    add_comments()
    
    print("\n" + "="*50)
    print("🎯 TABLA OBSERVATION_VIEWS LISTA PARA USO")
    print("="*50)
    print("La tabla está configurada para:")
    print("✅ Rastrear visualizaciones de observaciones")
    print("✅ Asociar vistas con acudientes específicos")
    print("✅ Registrar metadatos de visualización")
    print("✅ Prevenir visualizaciones duplicadas")
    print("✅ Mantener integridad referencial")
