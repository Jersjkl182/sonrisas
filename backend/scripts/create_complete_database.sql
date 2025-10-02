-- Script completo para crear todas las tablas del proyecto Sonrisas
-- Ejecutar en phpMyAdmin en la base de datos 'login'

-- =====================================================
-- TABLA: estudiantes
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
  KEY `idx_activo` (`activo`),
  CONSTRAINT `fk_estudiantes_profesor` FOREIGN KEY (`profesor_id`) REFERENCES `usuarios` (`id`) ON DELETE CASCADE,
  CONSTRAINT `fk_estudiantes_acudiente` FOREIGN KEY (`acudiente_id`) REFERENCES `usuarios` (`id`) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- =====================================================
-- TABLA: multimedia (para archivos futuros)
-- =====================================================
CREATE TABLE IF NOT EXISTS `multimedia` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `observacion_id` int(11) NOT NULL,
  `nombre_archivo` varchar(255) NOT NULL,
  `ruta_archivo` varchar(500) NOT NULL,
  `tipo_archivo` enum('imagen','video','audio','documento') NOT NULL,
  `tamaño_archivo` int(11) DEFAULT NULL,
  `fecha_subida` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `idx_observacion_id` (`observacion_id`),
  KEY `idx_tipo_archivo` (`tipo_archivo`),
  CONSTRAINT `fk_multimedia_observacion` FOREIGN KEY (`observacion_id`) REFERENCES `observaciones` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- =====================================================
-- TABLA: notificaciones
-- =====================================================
CREATE TABLE IF NOT EXISTS `notificaciones` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `usuario_id` int(11) NOT NULL,
  `tipo` enum('info','success','warning','error') NOT NULL DEFAULT 'info',
  `titulo` varchar(255) NOT NULL,
  `mensaje` text NOT NULL,
  `leida` tinyint(1) NOT NULL DEFAULT 0,
  `fecha_creacion` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `fecha_lectura` timestamp NULL DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `idx_usuario_id` (`usuario_id`),
  KEY `idx_leida` (`leida`),
  KEY `idx_tipo` (`tipo`),
  KEY `idx_fecha_creacion` (`fecha_creacion`),
  CONSTRAINT `fk_notificaciones_usuario` FOREIGN KEY (`usuario_id`) REFERENCES `usuarios` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- =====================================================
-- ACTUALIZAR TABLA: observaciones (agregar id_estudiante)
-- =====================================================
-- Primero verificar si la columna ya existe
SET @column_exists = (
  SELECT COUNT(*) 
  FROM INFORMATION_SCHEMA.COLUMNS 
  WHERE TABLE_SCHEMA = 'login' 
    AND TABLE_NAME = 'observaciones' 
    AND COLUMN_NAME = 'id_estudiante'
);

-- Agregar columna si no existe
SET @sql = IF(@column_exists = 0, 
  'ALTER TABLE observaciones ADD COLUMN id_estudiante int(11) DEFAULT NULL AFTER id_acudiente',
  'SELECT "Columna id_estudiante ya existe" as mensaje'
);
PREPARE stmt FROM @sql;
EXECUTE stmt;
DEALLOCATE PREPARE stmt;

-- Agregar índice y foreign key si la columna fue creada
SET @sql = IF(@column_exists = 0, 
  'ALTER TABLE observaciones ADD KEY idx_id_estudiante (id_estudiante)',
  'SELECT "Índice ya existe" as mensaje'
);
PREPARE stmt FROM @sql;
EXECUTE stmt;
DEALLOCATE PREPARE stmt;

SET @sql = IF(@column_exists = 0, 
  'ALTER TABLE observaciones ADD CONSTRAINT fk_observaciones_estudiante FOREIGN KEY (id_estudiante) REFERENCES estudiantes (id) ON DELETE CASCADE',
  'SELECT "Foreign key ya existe" as mensaje'
);
PREPARE stmt FROM @sql;
EXECUTE stmt;
DEALLOCATE PREPARE stmt;

-- =====================================================
-- ACTUALIZAR TABLA: observaciones (agregar tipo_observacion)
-- =====================================================
-- Verificar si la columna tipo_observacion existe
SET @tipo_column_exists = (
  SELECT COUNT(*) 
  FROM INFORMATION_SCHEMA.COLUMNS 
  WHERE TABLE_SCHEMA = 'login' 
    AND TABLE_NAME = 'observaciones' 
    AND COLUMN_NAME = 'tipo_observacion'
);

-- Agregar columna tipo_observacion si no existe
SET @sql = IF(@tipo_column_exists = 0, 
  'ALTER TABLE observaciones ADD COLUMN tipo_observacion enum("Positiva","Mejora","Neutral") DEFAULT "Positiva" AFTER descripcion',
  'SELECT "Columna tipo_observacion ya existe" as mensaje'
);
PREPARE stmt FROM @sql;
EXECUTE stmt;
DEALLOCATE PREPARE stmt;

-- =====================================================
-- DATOS DE EJEMPLO PARA ESTUDIANTES
-- =====================================================
INSERT IGNORE INTO `estudiantes` (`id`, `nombre`, `apellido`, `fecha_nacimiento`, `grado`, `profesor_id`, `acudiente_id`, `fecha_registro`, `activo`) VALUES
(1, 'Ana María', 'González', '2015-03-15', '3° Primaria', 2, 4, '2024-01-15 10:00:00', 1),
(2, 'Carlos Eduardo', 'Rodríguez', '2014-07-22', '4° Primaria', 2, NULL, '2024-01-16 11:30:00', 1),
(3, 'Sofía', 'Martínez', '2016-01-10', '2° Primaria', 2, 4, '2024-01-17 09:15:00', 1),
(4, 'Diego Alejandro', 'López', '2015-11-05', '3° Primaria', 2, NULL, '2024-01-18 14:20:00', 1),
(5, 'Valentina', 'Hernández', '2014-09-18', '4° Primaria', 2, NULL, '2024-01-19 08:45:00', 1);

-- =====================================================
-- DATOS DE EJEMPLO PARA OBSERVACIONES ACTUALIZADAS
-- =====================================================
-- Actualizar observaciones existentes para incluir id_estudiante
UPDATE `observaciones` SET 
  `id_estudiante` = 1,
  `tipo_observacion` = 'Positiva'
WHERE `id` = 1;

UPDATE `observaciones` SET 
  `id_estudiante` = 2,
  `tipo_observacion` = 'Mejora'
WHERE `id` = 2;

UPDATE `observaciones` SET 
  `id_estudiante` = 3,
  `tipo_observacion` = 'Positiva'
WHERE `id` = 3;

-- Insertar observaciones adicionales de ejemplo
INSERT IGNORE INTO `observaciones` (`id`, `id_profesor`, `id_acudiente`, `id_estudiante`, `descripcion`, `tipo_observacion`, `fecha`) VALUES
(4, 2, 4, 1, 'Ana María mostró excelente participación en la clase de matemáticas. Resolvió todos los ejercicios correctamente y ayudó a sus compañeros.', 'Positiva', '2024-01-20 10:30:00'),
(5, 2, NULL, 2, 'Carlos necesita mejorar su atención durante las explicaciones. Se distrae con facilidad y no completa las tareas a tiempo.', 'Mejora', '2024-01-21 11:15:00'),
(6, 2, 4, 3, 'Sofía demostró gran creatividad en el proyecto de ciencias naturales. Su presentación fue muy organizada y clara.', 'Positiva', '2024-01-22 14:00:00'),
(7, 2, NULL, 4, 'Diego mostró una actitud colaborativa durante el trabajo en equipo. Ayudó a organizar el grupo y cumplió con sus responsabilidades.', 'Positiva', '2024-01-23 09:45:00'),
(8, 2, NULL, 5, 'Valentina necesita practicar más la lectura en voz alta. Su comprensión es buena pero debe mejorar la fluidez.', 'Mejora', '2024-01-24 13:20:00');

-- =====================================================
-- DATOS DE EJEMPLO PARA NOTIFICACIONES
-- =====================================================
INSERT IGNORE INTO `notificaciones` (`id`, `usuario_id`, `tipo`, `titulo`, `mensaje`, `leida`, `fecha_creacion`) VALUES
(1, 1, 'info', 'Nuevo usuario registrado', 'Se ha registrado un nuevo profesor en el sistema', 0, '2024-01-25 10:00:00'),
(2, 1, 'warning', 'Sesiones activas altas', 'Hay más de 10 sesiones activas simultáneamente', 0, '2024-01-25 11:30:00'),
(3, 1, 'success', 'Sistema actualizado', 'El sistema se ha actualizado correctamente', 1, '2024-01-25 12:15:00'),
(4, 1, 'info', 'Nueva observación creada', 'El profesor Juan Pérez ha creado una nueva observación', 0, '2024-01-25 14:20:00'),
(5, 1, 'error', 'Error en el sistema', 'Se detectó un error en el módulo de reportes', 0, '2024-01-25 15:45:00');

-- =====================================================
-- VERIFICACIÓN DE TABLAS CREADAS
-- =====================================================
SELECT 'Verificando tablas creadas...' as mensaje;

SELECT 
  TABLE_NAME as 'Tabla',
  TABLE_ROWS as 'Filas',
  CREATE_TIME as 'Fecha Creación'
FROM INFORMATION_SCHEMA.TABLES 
WHERE TABLE_SCHEMA = 'login' 
  AND TABLE_NAME IN ('estudiantes', 'multimedia', 'notificaciones', 'observaciones', 'usuarios', 'session_logs', 'user_audit_logs')
ORDER BY TABLE_NAME;

SELECT 'Script ejecutado exitosamente. Todas las tablas han sido creadas.' as resultado;
