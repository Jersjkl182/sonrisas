-- =====================================================
-- VERIFICAR ESTRUCTURA DE LA TABLA OBSERVACIONES
-- =====================================================

-- Ver la estructura completa de la tabla
DESCRIBE observaciones;

-- Ver algunas observaciones de ejemplo con todos los campos
SELECT 
    id,
    titulo,
    descripcion,
    tipo,
    tipo_observacion,
    hijo,
    id_profesor,
    id_acudiente,
    id_estudiante,
    fecha,
    leido,
    fecha_lectura,
    leido_por
FROM observaciones 
ORDER BY fecha DESC 
LIMIT 5;

-- Verificar si existen los campos nuevos
SELECT COLUMN_NAME, DATA_TYPE, IS_NULLABLE, COLUMN_DEFAULT 
FROM INFORMATION_SCHEMA.COLUMNS 
WHERE TABLE_SCHEMA = 'login' 
AND TABLE_NAME = 'observaciones'
ORDER BY ORDINAL_POSITION;

-- Contar observaciones por tipo
SELECT tipo, COUNT(*) as cantidad
FROM observaciones 
GROUP BY tipo;

-- Contar observaciones por tipo_observacion
SELECT tipo_observacion, COUNT(*) as cantidad
FROM observaciones 
GROUP BY tipo_observacion;

-- Contar observaciones por estado de lectura
SELECT 
    CASE WHEN leido = 1 THEN 'Leída' ELSE 'No leída' END as estado,
    COUNT(*) as cantidad
FROM observaciones 
GROUP BY leido;
