#!/usr/bin/env python3
"""
Script para crear la tabla de relación estudiante-acudientes
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

try:
    import MySQLdb
except ImportError:
    import pymysql as MySQLdb

def setup_acudientes_table():
    """Crea la tabla de relación estudiante-acudientes"""
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
        
        # Crear tabla estudiante_acudientes
        print("📋 Creando tabla estudiante_acudientes...")
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS estudiante_acudientes (
                id INT AUTO_INCREMENT PRIMARY KEY,
                estudiante_id INT NOT NULL,
                acudiente_id INT NOT NULL,
                tipo_relacion ENUM('principal', 'secundario') NOT NULL DEFAULT 'principal',
                fecha_asignacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                activo TINYINT(1) DEFAULT 1,
                
                -- Claves foráneas
                FOREIGN KEY (estudiante_id) REFERENCES estudiantes(id) ON DELETE CASCADE,
                FOREIGN KEY (acudiente_id) REFERENCES usuarios(id) ON DELETE CASCADE,
                
                -- Índices únicos para evitar duplicados
                UNIQUE KEY unique_student_acudiente (estudiante_id, acudiente_id),
                
                -- Índices para optimizar consultas
                INDEX idx_estudiante (estudiante_id),
                INDEX idx_acudiente (acudiente_id),
                INDEX idx_tipo_relacion (tipo_relacion)
            ) COMMENT = 'Tabla de relación entre estudiantes y acudientes. Máximo 2 acudientes por estudiante.'
        """)
        
        print("✅ Tabla estudiante_acudientes creada")
        
        # Migrar datos existentes
        print("📦 Migrando datos existentes...")
        cursor.execute("""
            INSERT IGNORE INTO estudiante_acudientes (estudiante_id, acudiente_id, tipo_relacion)
            SELECT id, acudiente_id, 'principal'
            FROM estudiantes 
            WHERE acudiente_id IS NOT NULL
        """)
        
        migrated_rows = cursor.rowcount
        print(f"✅ {migrated_rows} relaciones migradas")
        
        connection.commit()
        
        # Verificar datos migrados
        cursor.execute("SELECT COUNT(*) FROM estudiante_acudientes")
        total_relations = cursor.fetchone()[0]
        print(f"📊 Total de relaciones estudiante-acudiente: {total_relations}")
        
        # Mostrar algunas relaciones
        cursor.execute("""
            SELECT ea.id, e.nombre as estudiante, u.nombre as acudiente, ea.tipo_relacion
            FROM estudiante_acudientes ea
            JOIN estudiantes e ON ea.estudiante_id = e.id
            JOIN usuarios u ON ea.acudiente_id = u.id
            LIMIT 5
        """)
        
        relations = cursor.fetchall()
        print(f"\n👥 Relaciones creadas:")
        for rel in relations:
            print(f"   ID: {rel[0]} - {rel[1]} -> {rel[2]} ({rel[3]})")
        
        cursor.close()
        connection.close()
        
        print(f"\n🎯 ¡Tabla de acudientes configurada exitosamente!")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    print("🔧 Configurando tabla de acudientes...")
    setup_acudientes_table()
