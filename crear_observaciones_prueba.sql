-- =====================================================
-- CREAR OBSERVACIONES DE PRUEBA PARA ANGELO CURIEL
-- =====================================================

-- Primero, vamos a verificar los datos del estudiante Angelo Curiel
SELECT * FROM estudiantes WHERE nombre = 'Angelo' AND apellido = 'Curiel';

-- Obtener el ID del profesor y acudiente asociados
SELECT 
    e.id as estudiante_id,
    e.nombre,
    e.apellido,
    e.profesor_id,
    e.acudiente_id,
    p.nombre as profesor_nombre,
    a.nombre as acudiente_nombre
FROM estudiantes e
LEFT JOIN usuarios p ON e.profesor_id = p.id
LEFT JOIN usuarios a ON e.acudiente_id = a.id
WHERE e.nombre = 'Angelo' AND e.apellido = 'Curiel';

-- =====================================================
-- INSERTAR OBSERVACIONES DE CADA TIPO
-- =====================================================

-- 1. OBSERVACIÓN POSITIVA
INSERT INTO observaciones (
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
) VALUES (
    'Excelente participación en clase',
    'Angelo demostró un gran interés en la clase de matemáticas hoy. Participó activamente respondiendo preguntas y ayudando a sus compañeros. Su actitud positiva es un ejemplo para todos.',
    'Académica',
    'Positiva',
    'Angelo Curiel',
    9,  -- ID del profesor (ajustar según tu base de datos)
    8,  -- ID del acudiente (ajustar según tu base de datos)
    6,  -- ID del estudiante Angelo (ajustar según tu base de datos)
    NOW(),
    0,  -- No leído inicialmente
    NULL,
    NULL
);

-- 2. OBSERVACIÓN NEUTRAL
INSERT INTO observaciones (
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
) VALUES (
    'Información sobre cambio de horario',
    'Se informa que Angelo estuvo presente durante el simulacro de evacuación realizado hoy. Siguió las instrucciones correctamente y se mantuvo en orden durante todo el procedimiento.',
    'Comportamiento',
    'Neutral',
    'Angelo Curiel',
    9,  -- ID del profesor
    8,  -- ID del acudiente
    6,  -- ID del estudiante Angelo
    NOW(),
    0,  -- No leído inicialmente
    NULL,
    NULL
);

-- 3. OBSERVACIÓN DE MEJORA
INSERT INTO observaciones (
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
) VALUES (
    'Necesita mejorar la puntualidad',
    'Angelo ha llegado tarde a clase en tres ocasiones esta semana. Es importante que trabaje en ser más puntual para no perderse el inicio de las lecciones y para desarrollar buenos hábitos de responsabilidad.',
    'Comportamiento',
    'Mejora',
    'Angelo Curiel',
    9,  -- ID del profesor
    8,  -- ID del acudiente
    6,  -- ID del estudiante Angelo
    NOW(),
    0,  -- No leído inicialmente
    NULL,
    NULL
);

-- =====================================================
-- VERIFICAR LAS OBSERVACIONES CREADAS
-- =====================================================

-- Ver todas las observaciones de Angelo con sus tipos
SELECT 
    o.id,
    o.titulo,
    o.descripcion,
    o.tipo,
    o.tipo_observacion,
    o.fecha,
    o.leido,
    o.fecha_lectura,
    CASE 
        WHEN o.leido = 1 THEN 'Leída'
        ELSE 'No leída'
    END as estado_lectura
FROM observaciones o
WHERE o.hijo = 'Angelo Curiel'
ORDER BY o.fecha DESC;

-- Contar observaciones por tipo para Angelo
SELECT 
    tipo_observacion,
    COUNT(*) as cantidad
FROM observaciones 
WHERE hijo = 'Angelo Curiel'
GROUP BY tipo_observacion;

-- =====================================================
-- INSTRUCCIONES DE USO
-- =====================================================

/*
PASOS PARA EJECUTAR:

1. Abre phpMyAdmin
2. Selecciona tu base de datos 'login'
3. Ve a la pestaña 'SQL'
4. Ejecuta primero las consultas SELECT para verificar los IDs correctos
5. Ajusta los IDs en los INSERT si es necesario
6. Ejecuta los INSERT para crear las observaciones
7. Ejecuta las consultas de verificación al final

RESULTADO ESPERADO:
- 3 observaciones nuevas para Angelo Curiel
- 1 Positiva (verde) - Excelente participación
- 1 Neutral (gris) - Información sobre simulacro  
- 1 Mejora (naranja) - Necesita mejorar puntualidad

PROBAR EN LA APLICACIÓN:
1. Como Profesor: Ve a /profesor/observaciones
2. Como Acudiente: Ve a /acudiente/observaciones
3. Verifica que se muestren los badges de colores correctos
4. Prueba el sistema de lectura (marcar como leído/no leído)
*/
