-- Script para crear solo las tablas faltantes más importantes
-- Ejecutar en phpMyAdmin en la base de datos 'login'

-- =====================================================
-- TABLA: estudiantes (PRINCIPAL - REQUERIDA)
-- =====================================================
CREATE TABLE IF NOT EXISTS `estudiantes` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `nombre` varchar(100) NOT NULL,
  `apellido` varchar(100) NOT NULL,
  `fecha_nacimiento` date DEFAULT NULL,
  `grado` varchar(50) DEFAULT NULL,
  `profesor_id` int(11) NOT NULL,
  `acudiente_id` int(11) DEFAULT NULL,
  `fecha_registro` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `activo` tinyint(1) DEFAULT 1,
  PRIMARY KEY (`id`),
  KEY `idx_profesor_id` (`profesor_id`),
  KEY `idx_acudiente_id` (`acudiente_id`),
  CONSTRAINT `fk_estudiantes_profesor` FOREIGN KEY (`profesor_id`) REFERENCES `usuarios` (`id`) ON DELETE CASCADE,
  CONSTRAINT `fk_estudiantes_acudiente` FOREIGN KEY (`acudiente_id`) REFERENCES `usuarios` (`id`) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- =====================================================
-- DATOS DE EJEMPLO PARA ESTUDIANTES
-- =====================================================
INSERT INTO `estudiantes` (`nombre`, `apellido`, `fecha_nacimiento`, `grado`, `profesor_id`, `acudiente_id`) VALUES
('Ana María', 'González', '2015-03-15', '3° Primaria', 2, 4),
('Carlos Eduardo', 'Rodríguez', '2014-07-22', '4° Primaria', 2, NULL),
('Sofía', 'Martínez', '2016-01-10', '2° Primaria', 2, 4),
('Diego Alejandro', 'López', '2015-11-05', '3° Primaria', 2, NULL),
('Valentina', 'Hernández', '2014-09-18', '4° Primaria', 2, NULL);

-- =====================================================
-- ACTUALIZAR TABLA observaciones (agregar id_estudiante)
-- =====================================================
ALTER TABLE `observaciones` 
ADD COLUMN `id_estudiante` int(11) DEFAULT NULL AFTER `id_acudiente`,
ADD COLUMN `tipo_observacion` enum('Positiva','Mejora','Neutral') DEFAULT 'Positiva' AFTER `descripcion`;

-- Agregar índices
ALTER TABLE `observaciones` 
ADD KEY `idx_id_estudiante` (`id_estudiante`),
ADD CONSTRAINT `fk_observaciones_estudiante` FOREIGN KEY (`id_estudiante`) REFERENCES `estudiantes` (`id`) ON DELETE CASCADE;

-- =====================================================
-- ACTUALIZAR OBSERVACIONES EXISTENTES
-- =====================================================
UPDATE `observaciones` SET `id_estudiante` = 1, `tipo_observacion` = 'Positiva' WHERE `id` = 1;
UPDATE `observaciones` SET `id_estudiante` = 2, `tipo_observacion` = 'Mejora' WHERE `id` = 2;
UPDATE `observaciones` SET `id_estudiante` = 3, `tipo_observacion` = 'Positiva' WHERE `id` = 3;

-- =====================================================
-- VERIFICAR CREACIÓN
-- =====================================================
SELECT 'Tabla estudiantes creada exitosamente' as resultado;
SELECT COUNT(*) as 'Total estudiantes' FROM estudiantes;
SELECT COUNT(*) as 'Total observaciones' FROM observaciones;
