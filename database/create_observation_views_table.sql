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

-- Agregar comentarios para documentación
ALTER TABLE observation_views COMMENT = 'Tabla para rastrear visualizaciones de observaciones por acudientes';
ALTER TABLE observation_views MODIFY COLUMN observation_id INT NOT NULL COMMENT 'ID de la observación vista';
ALTER TABLE observation_views MODIFY COLUMN acudiente_id INT NOT NULL COMMENT 'ID del acudiente que vio la observación';
ALTER TABLE observation_views MODIFY COLUMN viewed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT 'Fecha y hora de visualización';
ALTER TABLE observation_views MODIFY COLUMN ip_address VARCHAR(45) COMMENT 'Dirección IP desde donde se vio';
ALTER TABLE observation_views MODIFY COLUMN user_agent TEXT COMMENT 'User agent del navegador';
