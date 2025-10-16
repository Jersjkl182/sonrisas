-- =====================================================
-- ACTUALIZACIÓN PARA SISTEMA DE LECTURA DE OBSERVACIONES
-- =====================================================

-- Agregar campo 'leido' a la tabla observaciones
ALTER TABLE `observaciones` 
ADD COLUMN `leido` TINYINT(1) NOT NULL DEFAULT 0 COMMENT 'Estado de lectura: 0=No leído, 1=Leído';

-- Agregar campo 'fecha_lectura' para registrar cuándo se marcó como leído
ALTER TABLE `observaciones` 
ADD COLUMN `fecha_lectura` TIMESTAMP NULL DEFAULT NULL COMMENT 'Fecha y hora cuando se marcó como leído';

-- Agregar campo 'leido_por' para saber quién lo marcó como leído
ALTER TABLE `observaciones` 
ADD COLUMN `leido_por` INT(11) NULL DEFAULT NULL COMMENT 'ID del usuario que marcó como leído';

-- Agregar índice para mejorar consultas por estado de lectura
ALTER TABLE `observaciones` 
ADD INDEX `idx_leido` (`leido`);

-- Agregar índice para consultas por fecha de lectura
ALTER TABLE `observaciones` 
ADD INDEX `idx_fecha_lectura` (`fecha_lectura`);

-- Agregar clave foránea para el usuario que marcó como leído
ALTER TABLE `observaciones` 
ADD CONSTRAINT `fk_observaciones_leido_por` 
FOREIGN KEY (`leido_por`) REFERENCES `usuarios` (`id`) ON DELETE SET NULL;

-- =====================================================
-- DATOS DE EJEMPLO (OPCIONAL)
-- =====================================================

-- Marcar algunas observaciones existentes como leídas (opcional)
-- UPDATE `observaciones` SET `leido` = 1, `fecha_lectura` = NOW(), `leido_por` = 1 WHERE `id` = 1;

-- =====================================================
-- CONSULTAS ÚTILES PARA EL SISTEMA
-- =====================================================

-- Ver todas las observaciones con su estado de lectura
-- SELECT o.*, u.nombre as leido_por_nombre 
-- FROM observaciones o 
-- LEFT JOIN usuarios u ON o.leido_por = u.id 
-- ORDER BY o.fecha DESC;

-- Contar observaciones leídas vs no leídas
-- SELECT 
--     SUM(CASE WHEN leido = 1 THEN 1 ELSE 0 END) as leidas,
--     SUM(CASE WHEN leido = 0 THEN 1 ELSE 0 END) as no_leidas,
--     COUNT(*) as total
-- FROM observaciones;

-- Ver observaciones no leídas de un acudiente específico
-- SELECT * FROM observaciones 
-- WHERE id_acudiente = ? AND leido = 0 
-- ORDER BY fecha DESC;

-- Ver observaciones leídas recientemente
-- SELECT o.*, u.nombre as leido_por_nombre 
-- FROM observaciones o 
-- LEFT JOIN usuarios u ON o.leido_por = u.id 
-- WHERE o.leido = 1 AND o.fecha_lectura >= DATE_SUB(NOW(), INTERVAL 7 DAY)
-- ORDER BY o.fecha_lectura DESC;
