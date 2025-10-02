-- Script para crear la tabla user_audit_logs
-- Esta tabla registra las acciones de auditoría realizadas por administradores sobre usuarios

USE login;

CREATE TABLE IF NOT EXISTS user_audit_logs (
    id INT AUTO_INCREMENT PRIMARY KEY,
    admin_id INT NOT NULL,
    user_id INT NOT NULL,
    accion VARCHAR(50) NOT NULL,
    detalles TEXT,
    fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_admin_id (admin_id),
    INDEX idx_user_id (user_id),
    INDEX idx_fecha (fecha),
    INDEX idx_accion (accion),
    FOREIGN KEY (admin_id) REFERENCES usuarios(id) ON DELETE CASCADE,
    FOREIGN KEY (user_id) REFERENCES usuarios(id) ON DELETE CASCADE
);

-- Insertar algunos registros de ejemplo (opcional)
-- INSERT INTO user_audit_logs (admin_id, user_id, accion, detalles) VALUES
-- (1, 2, 'crear', 'Usuario creado por administrador'),
-- (1, 3, 'editar', 'Datos del usuario actualizados'),
-- (1, 4, 'restablecer', 'Contraseña restablecida');
