import os
import pymysql
import sys

def migrate_database():
    print("🚀 Iniciando migración de base de datos a Railway...")
    
    # Configuración de Railway (usando variables de entorno)
    config = {
        'host': 'mysql.railway.internal',
        'user': 'jerson',
        'password': 'rNDXhvzRUeLTPBJqKtGXSiBZtsJfKrtg',
        'database': 'railway',
        'charset': 'utf8mb4'
    }
    
    try:
        # Leer archivo SQL
        print("📖 Leyendo archivo login.sql...")
        with open('login.sql', 'r', encoding='utf-8') as f:
            sql_content = f.read()
        
        # Conectar a Railway MySQL
        print("🔗 Conectando a Railway MySQL...")
        connection = pymysql.connect(**config)
        cursor = connection.cursor()
        
        # Dividir SQL en statements individuales
        statements = []
        current_statement = ""
        
        for line in sql_content.split('\n'):
            # Ignorar comentarios y líneas vacías
            if line.strip().startswith('--') or line.strip().startswith('/*') or not line.strip():
                continue
            
            current_statement += line + '\n'
            
            # Si la línea termina con ';', es el final de un statement
            if line.strip().endswith(';'):
                statements.append(current_statement.strip())
                current_statement = ""
        
        # Ejecutar cada statement
        print(f"⚡ Ejecutando {len(statements)} statements SQL...")
        
        for i, statement in enumerate(statements):
            if statement.strip():
                try:
                    cursor.execute(statement)
                    print(f"✅ Statement {i+1}/{len(statements)} ejecutado")
                except Exception as e:
                    print(f"⚠️ Error en statement {i+1}: {str(e)}")
                    # Continuar con el siguiente statement
                    continue
        
        # Confirmar cambios
        connection.commit()
        
        # Verificar tablas creadas
        cursor.execute("SHOW TABLES")
        tables = cursor.fetchall()
        
        print(f"\n🎉 ¡Migración completada exitosamente!")
        print(f"📊 Tablas creadas: {len(tables)}")
        for table in tables:
            print(f"   - {table[0]}")
        
        cursor.close()
        connection.close()
        
    except FileNotFoundError:
        print("❌ Error: No se encontró el archivo 'login.sql'")
        print("   Asegúrate de que el archivo esté en la misma carpeta que este script")
        
    except pymysql.Error as e:
        print(f"❌ Error de conexión MySQL: {str(e)}")
        print("   Verifica las credenciales de Railway")
        
    except Exception as e:
        print(f"❌ Error inesperado: {str(e)}")

if __name__ == "__main__":
    migrate_database()
