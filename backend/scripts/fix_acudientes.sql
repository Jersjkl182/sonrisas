-- Script para corregir problemas comunes con acudientes
-- Ejecutar en phpMyAdmin en la base de datos 'login'

-- =====================================================
-- 1. AGREGAR COLUMNA is_active SI NO EXISTE
-- =====================================================
SET @column_exists = (
  SELECT COUNT(*) 
  FROM INFORMATION_SCHEMA.COLUMNS 
  WHERE TABLE_SCHEMA = 'login' 
    AND TABLE_NAME = 'usuarios' 
    AND COLUMN_NAME = 'is_active'
);

SET @sql = IF(@column_exists = 0, 
  'ALTER TABLE usuarios ADD COLUMN is_active TINYINT(1) DEFAULT 1',
  'SELECT "Columna is_active ya existe" as mensaje'
);
PREPARE stmt FROM @sql;
EXECUTE stmt;
DEALLOCATE PREPARE stmt;

-- =====================================================
-- 2. ACTUALIZAR TODOS LOS USUARIOS EXISTENTES COMO ACTIVOS
-- =====================================================
UPDATE usuarios SET is_active = 1 WHERE is_active IS NULL OR is_active = 0;

-- =====================================================
-- 3. VERIFICAR/CORREGIR ROLES DE ACUDIENTES
-- =====================================================
-- Si tienes usuarios que deberían ser acudientes pero tienen rol diferente,
-- puedes corregirlos aquí. Por ejemplo, si creaste acudientes con rol 3:

-- Mostrar usuarios que podrían ser acudientes
SELECT 
    id,
    correo,
    nombre,
    apellido,
    id_rol,
    'Verificar si debería ser acudiente (rol 4)' as nota
FROM usuarios
WHERE id_rol = 3;

-- Si quieres cambiar usuarios de rol 3 a rol 4 (descomenta la siguiente línea):
-- UPDATE usuarios SET id_rol = 4 WHERE id_rol = 3;

-- =====================================================
-- 4. CREAR ACUDIENTES DE EJEMPLO SI NO EXISTEN
-- =====================================================
-- Solo insertar si no hay acudientes
INSERT IGNORE INTO usuarios (correo, contrasena, id_rol, nombre, apellido, is_active, fecha_registro) 
SELECT * FROM (
    SELECT 'maria.gonzalez@email.com' as correo, '$2b$12$example.hash.here' as contrasena, 4 as id_rol, 'María' as nombre, 'González' as apellido, 1 as is_active, NOW() as fecha_registro
    UNION ALL
    SELECT 'carlos.rodriguez@email.com', '$2b$12$example.hash.here', 4, 'Carlos', 'Rodríguez', 1, NOW()
    UNION ALL
    SELECT 'ana.martinez@email.com', '$2b$12$example.hash.here', 4, 'Ana', 'Martínez', 1, NOW()
) as tmp
WHERE NOT EXISTS (SELECT 1 FROM usuarios WHERE id_rol = 4 LIMIT 1);

-- =====================================================
-- 5. VERIFICAR RESULTADO FINAL
-- =====================================================
SELECT 
    'Acudientes encontrados:' as resultado,
    COUNT(*) as cantidad
FROM usuarios 
WHERE id_rol = 4 AND is_active = 1;

SELECT 
    id,
    correo,
    nombre,
    apellido,
    id_rol,
    is_active,
    fecha_registro
FROM usuarios 
WHERE id_rol = 4 AND is_active = 1
ORDER BY nombre, apellido;

-- =====================================================
-- 6. CONSULTA DE PRUEBA (LA MISMA QUE USA EL SISTEMA)
-- =====================================================
SELECT 
    id, 
    correo, 
    nombre, 
    apellido, 
    fecha_registro, 
    is_active
FROM usuarios
WHERE id_rol = 4 AND is_active = 1
ORDER BY nombre, apellido;
