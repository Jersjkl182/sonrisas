-- Crear tabla para relación muchos a muchos entre estudiantes y acudientes
-- Máximo 2 acudientes por estudiante

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
);

-- Migrar datos existentes de la tabla estudiantes
INSERT INTO estudiante_acudientes (estudiante_id, acudiente_id, tipo_relacion)
SELECT id, acudiente_id, 'principal'
FROM estudiantes 
WHERE acudiente_id IS NOT NULL;

-- Crear trigger para limitar máximo 2 acudientes por estudiante
DELIMITER //

CREATE TRIGGER limit_acudientes_per_student
BEFORE INSERT ON estudiante_acudientes
FOR EACH ROW
BEGIN
    DECLARE acudiente_count INT;
    
    -- Contar acudientes activos para este estudiante
    SELECT COUNT(*) INTO acudiente_count
    FROM estudiante_acudientes 
    WHERE estudiante_id = NEW.estudiante_id AND activo = 1;
    
    -- Si ya tiene 2 acudientes, no permitir insertar más
    IF acudiente_count >= 2 THEN
        SIGNAL SQLSTATE '45000' 
        SET MESSAGE_TEXT = 'Un estudiante no puede tener más de 2 acudientes activos';
    END IF;
END//

DELIMITER ;

-- Comentarios para documentación
ALTER TABLE estudiante_acudientes 
COMMENT = 'Tabla de relación entre estudiantes y acudientes. Máximo 2 acudientes por estudiante.';
