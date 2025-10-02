-- Script de debug para verificar por qué no aparecen los acudientes
-- Ejecutar en phpMyAdmin en la base de datos 'login'

-- =====================================================
-- 1. VERIFICAR ESTRUCTURA DE LA TABLA USUARIOS
-- =====================================================
DESCRIBE usuarios;

-- =====================================================
-- 2. MOSTRAR TODOS LOS USUARIOS Y SUS ROLES
-- =====================================================
SELECT 
    id,
    correo,
    nombre,
    apellido,
    id_rol,
    CASE 
        WHEN id_rol = 1 THEN 'Administrador'
        WHEN id_rol = 2 THEN 'Profesor'
        WHEN id_rol = 3 THEN 'Acudiente (Rol 3)'
        WHEN id_rol = 4 THEN 'Acudiente (Rol 4)'
        ELSE CONCAT('Rol desconocido: ', id_rol)
    END as rol_nombre,
    CASE 
        WHEN EXISTS(SELECT 1 FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = 'usuarios' AND COLUMN_NAME = 'is_active' AND TABLE_SCHEMA = 'login')
        THEN (SELECT is_active FROM usuarios u2 WHERE u2.id = usuarios.id)
        ELSE 'Columna is_active no existe'
    END as estado_activo,
    fecha_registro
FROM usuarios
ORDER BY id_rol, nombre;

-- =====================================================
-- 3. CONTAR USUARIOS POR ROL
-- =====================================================
SELECT 
    id_rol,
    CASE 
        WHEN id_rol = 1 THEN 'Administrador'
        WHEN id_rol = 2 THEN 'Profesor'
        WHEN id_rol = 3 THEN 'Acudiente (Rol 3)'
        WHEN id_rol = 4 THEN 'Acudiente (Rol 4)'
        ELSE CONCAT('Rol desconocido: ', id_rol)
    END as rol_nombre,
    COUNT(*) as cantidad
FROM usuarios
GROUP BY id_rol
ORDER BY id_rol;

-- =====================================================
-- 4. VERIFICAR SI EXISTE LA COLUMNA is_active
-- =====================================================
SELECT 
    COLUMN_NAME,
    DATA_TYPE,
    IS_NULLABLE,
    COLUMN_DEFAULT
FROM INFORMATION_SCHEMA.COLUMNS 
WHERE TABLE_SCHEMA = 'login' 
    AND TABLE_NAME = 'usuarios' 
    AND COLUMN_NAME = 'is_active';

-- =====================================================
-- 5. MOSTRAR SOLO ACUDIENTES (TODOS LOS ROLES POSIBLES)
-- =====================================================
SELECT 
    id,
    correo,
    nombre,
    apellido,
    id_rol,
    fecha_registro,
    'Posible acudiente' as nota
FROM usuarios
WHERE id_rol IN (3, 4)  -- Tanto rol 3 como 4 podrían ser acudientes
ORDER BY id_rol, nombre;

-- =====================================================
-- 6. CONSULTA EXACTA QUE USA EL SISTEMA
-- =====================================================
-- Esta es la consulta que está ejecutando el sistema actualmente
SELECT 
    id, 
    correo, 
    nombre, 
    apellido, 
    fecha_registro,
    CASE 
        WHEN EXISTS(SELECT 1 FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = 'usuarios' AND COLUMN_NAME = 'is_active' AND TABLE_SCHEMA = 'login')
        THEN (SELECT is_active FROM usuarios u2 WHERE u2.id = usuarios.id)
        ELSE 1  -- Asumir activo si no existe la columna
    END as is_active_value
FROM usuarios
WHERE id_rol = 4 
    AND (
        NOT EXISTS(SELECT 1 FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = 'usuarios' AND COLUMN_NAME = 'is_active' AND TABLE_SCHEMA = 'login')
        OR is_active = 1
    )
ORDER BY nombre, apellido;

-- =====================================================
-- RESULTADO ESPERADO
-- =====================================================
SELECT 'Si no ves acudientes arriba, el problema puede ser:' as diagnostico
UNION ALL
SELECT '1. Los usuarios no tienen id_rol = 4 (revisar roles)'
UNION ALL
SELECT '2. Los usuarios están marcados como inactivos (is_active = 0)'
UNION ALL
SELECT '3. La columna is_active no existe en la tabla'
UNION ALL
SELECT '4. No hay usuarios con rol de acudiente creados';
