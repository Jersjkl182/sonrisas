-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Servidor: 127.0.0.1
-- Tiempo de generación: 02-10-2025 a las 14:20:37
-- Versión del servidor: 10.4.32-MariaDB
-- Versión de PHP: 8.2.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Base de datos: `login`
--

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `estudiantes`
--

CREATE TABLE `estudiantes` (
  `id` int(11) NOT NULL,
  `nombre` varchar(100) NOT NULL,
  `apellido` varchar(100) NOT NULL,
  `fecha_nacimiento` date DEFAULT NULL,
  `grado` varchar(50) DEFAULT NULL,
  `profesor_id` int(11) NOT NULL,
  `acudiente_id` int(11) DEFAULT NULL,
  `fecha_registro` timestamp NOT NULL DEFAULT current_timestamp(),
  `activo` tinyint(1) DEFAULT 1,
  `fecha_matricula` date DEFAULT NULL,
  `eps` varchar(100) DEFAULT NULL,
  `condicion_especiales` text DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `estudiantes`
--

INSERT INTO `estudiantes` (`id`, `nombre`, `apellido`, `fecha_nacimiento`, `grado`, `profesor_id`, `acudiente_id`, `fecha_registro`, `activo`, `fecha_matricula`, `eps`, `condicion_especiales`) VALUES
(6, 'Angelo', 'Curiel', '2015-10-16', 'Preescolar', 9, 8, '2025-09-26 12:28:47', 1, NULL, NULL, NULL),
(7, 'jherson', 'florez', '2023-04-16', 'Jardín', 9, 14, '2025-10-01 02:03:50', 1, '2024-06-15', 'Salud Total', 'Diabetes');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `estudiante_acudientes`
--

CREATE TABLE `estudiante_acudientes` (
  `id` int(11) NOT NULL,
  `estudiante_id` int(11) NOT NULL,
  `acudiente_id` int(11) NOT NULL,
  `tipo_relacion` enum('principal','secundario') NOT NULL DEFAULT 'principal',
  `fecha_asignacion` timestamp NOT NULL DEFAULT current_timestamp(),
  `activo` tinyint(1) DEFAULT 1
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci COMMENT='Tabla de relación entre estudiantes y acudientes. Máximo 2 acudientes por estudiante.';

--
-- Volcado de datos para la tabla `estudiante_acudientes`
--

INSERT INTO `estudiante_acudientes` (`id`, `estudiante_id`, `acudiente_id`, `tipo_relacion`, `fecha_asignacion`, `activo`) VALUES
(1, 6, 8, 'principal', '2025-10-01 12:35:14', 1),
(2, 7, 8, 'principal', '2025-10-01 12:35:14', 0),
(8, 6, 12, 'secundario', '2025-10-01 13:02:38', 0),
(9, 7, 12, 'secundario', '2025-10-01 13:08:59', 0),
(10, 6, 13, 'secundario', '2025-10-01 13:19:58', 1),
(11, 7, 15, 'secundario', '2025-10-01 13:22:16', 0),
(12, 7, 8, 'principal', '2025-10-01 13:22:33', 1),
(13, 7, 15, 'secundario', '2025-10-01 13:22:41', 1);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `multimedia`
--

CREATE TABLE `multimedia` (
  `id` int(11) NOT NULL,
  `observacion_id` int(11) NOT NULL,
  `nombre_archivo` varchar(255) NOT NULL,
  `ruta_archivo` varchar(500) NOT NULL,
  `tipo_archivo` enum('imagen','video','audio','documento') NOT NULL,
  `tamaño_archivo` int(11) DEFAULT NULL,
  `fecha_subida` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Volcado de datos para la tabla `multimedia`
--

INSERT INTO `multimedia` (`id`, `observacion_id`, `nombre_archivo`, `ruta_archivo`, `tipo_archivo`, `tamaño_archivo`, `fecha_subida`) VALUES
(1, 2, 'WIN_20250926_22_29_34_Pro.jpg', 'uploads/multimedia/2025/09/3436933d8e47481aaae204cb87a47c5a.jpg', '', 243148, '2025-10-01 01:06:17'),
(2, 2, 'Grabacion_de_pantalla_2025-09-30_124919.mp4', 'uploads/multimedia/2025/09/d78f8a042ef94e88a13a6206c20b0e3a.mp4', 'video', 2947150, '2025-10-01 01:06:17'),
(4, 3, 'Grabacion_de_pantalla_2025-09-30_124919.mp4', 'uploads/multimedia/2025/09/52e2cdf3cad94dd1b45eecde1e5bb7b4.mp4', 'video', 2947150, '2025-10-01 01:28:31'),
(5, 3, 'WIN_20250926_19_50_23_Pro.jpg', 'uploads/multimedia/2025/09/370383e5b7174862a09723847f3403db.jpg', '', 221802, '2025-10-01 01:28:31');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `notificaciones`
--

CREATE TABLE `notificaciones` (
  `id` int(11) NOT NULL,
  `usuario_id` int(11) NOT NULL,
  `tipo` enum('info','success','warning','error') NOT NULL DEFAULT 'info',
  `titulo` varchar(255) NOT NULL,
  `mensaje` text NOT NULL,
  `leida` tinyint(1) NOT NULL DEFAULT 0,
  `fecha_creacion` timestamp NOT NULL DEFAULT current_timestamp(),
  `fecha_lectura` timestamp NULL DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Volcado de datos para la tabla `notificaciones`
--

INSERT INTO `notificaciones` (`id`, `usuario_id`, `tipo`, `titulo`, `mensaje`, `leida`, `fecha_creacion`, `fecha_lectura`) VALUES
(1, 1, 'info', 'Nuevo usuario registrado', 'Se ha registrado un nuevo profesor en el sistema', 0, '2024-01-25 15:00:00', NULL),
(2, 1, 'warning', 'Sesiones activas altas', 'Hay más de 10 sesiones activas simultáneamente', 0, '2024-01-25 16:30:00', NULL),
(3, 1, 'success', 'Sistema actualizado', 'El sistema se ha actualizado correctamente', 1, '2024-01-25 17:15:00', NULL),
(4, 1, 'info', 'Nueva observación creada', 'El profesor Juan Pérez ha creado una nueva observación', 0, '2024-01-25 19:20:00', NULL),
(5, 1, 'error', 'Error en el sistema', 'Se detectó un error en el módulo de reportes', 0, '2024-01-25 20:45:00', NULL);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `observaciones`
--

CREATE TABLE `observaciones` (
  `id` int(11) NOT NULL,
  `titulo` varchar(120) NOT NULL,
  `descripcion` text NOT NULL,
  `tipo` enum('Positiva','Negativa','Neutra','Académica','Comportamiento','Salud') DEFAULT 'Positiva',
  `tipo_observacion` enum('Positiva','Mejora','Neutral') DEFAULT 'Positiva',
  `hijo` varchar(80) NOT NULL,
  `id_profesor` int(11) NOT NULL,
  `id_acudiente` int(11) NOT NULL,
  `id_estudiante` int(11) DEFAULT NULL,
  `fecha` datetime NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `observaciones`
--

INSERT INTO `observaciones` (`id`, `titulo`, `descripcion`, `tipo`, `tipo_observacion`, `hijo`, `id_profesor`, `id_acudiente`, `id_estudiante`, `fecha`) VALUES
(1, 'muy buen estdiante', 'buen rendimiento', 'Positiva', 'Positiva', 'Angelo Curiel', 9, 8, 6, '2025-09-30 17:36:10'),
(2, 'julian vapero y santiago mamador de vrga', 'en esta imagen podemos ver claramente como julian parece un vapero y santiago un maamdor de vrga premium', 'Positiva', 'Mejora', 'Angelo Curiel', 9, 8, 6, '2025-09-30 19:08:11'),
(3, 'jsjsjsjasjss', 'adsasdasdasdas', 'Positiva', 'Positiva', 'Angelo Curiel', 9, 8, 6, '2025-09-30 20:28:31');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `observation_readings`
--

CREATE TABLE `observation_readings` (
  `id` int(11) NOT NULL,
  `observation_id` int(11) NOT NULL,
  `acudiente_id` int(11) NOT NULL,
  `read_at` datetime NOT NULL DEFAULT current_timestamp(),
  `ip_address` varchar(45) DEFAULT NULL,
  `user_agent` text DEFAULT NULL,
  `created_at` datetime NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `permisos`
--

CREATE TABLE `permisos` (
  `id` int(11) NOT NULL,
  `nombre` varchar(100) NOT NULL,
  `codigo` varchar(50) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `permisos`
--

INSERT INTO `permisos` (`id`, `nombre`, `codigo`) VALUES
(1, 'Gestionar cuentas', 'CUENTAS_FULL'),
(2, 'Ver observaciones', 'OBSERV_VER'),
(3, 'Crear/editar obs.', 'OBSERV_EDIT'),
(4, 'Ver roles', 'ver_roles'),
(5, 'Crear rol', 'crear_rol'),
(6, 'Editar rol', 'editar_rol'),
(7, 'Eliminar rol', 'eliminar_rol'),
(8, 'Ver permisos', 'ver_permisos'),
(9, 'Crear permiso', 'crear_permiso'),
(10, 'Editar permiso', 'editar_permiso'),
(11, 'Eliminar permiso', 'eliminar_permiso');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `roles`
--

CREATE TABLE `roles` (
  `id_rol` int(11) NOT NULL,
  `nombre` varchar(50) NOT NULL,
  `codigo` varchar(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `roles`
--

INSERT INTO `roles` (`id_rol`, `nombre`, `codigo`) VALUES
(1, 'Administrador', 'ADMIN'),
(2, 'Profesor', 'PROF'),
(4, 'Acudiente', 'ACUD');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `rol_permisos`
--

CREATE TABLE `rol_permisos` (
  `id_rol` int(11) NOT NULL,
  `permiso_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `rol_permisos`
--

INSERT INTO `rol_permisos` (`id_rol`, `permiso_id`) VALUES
(1, 1),
(1, 4),
(1, 5),
(1, 6),
(1, 7),
(1, 8),
(1, 9),
(1, 10),
(1, 11),
(2, 2),
(2, 3),
(4, 2);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `session_logs`
--

CREATE TABLE `session_logs` (
  `id` int(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  `login_time` timestamp NOT NULL DEFAULT current_timestamp(),
  `logout_time` timestamp NULL DEFAULT NULL,
  `ip_address` varchar(45) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `system_notifications`
--

CREATE TABLE `system_notifications` (
  `id` int(11) NOT NULL,
  `title` varchar(255) NOT NULL,
  `message` text NOT NULL,
  `type` enum('info','warning','error','success') DEFAULT 'info',
  `priority` enum('low','normal','high','critical') DEFAULT 'normal',
  `created_at` timestamp NOT NULL DEFAULT current_timestamp(),
  `is_read` tinyint(1) DEFAULT 0,
  `read_at` timestamp NULL DEFAULT NULL,
  `expires_at` timestamp NULL DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `system_notifications`
--

INSERT INTO `system_notifications` (`id`, `title`, `message`, `type`, `priority`, `created_at`, `is_read`, `read_at`, `expires_at`) VALUES
(1, 'Sistema iniciado', 'El sistema Jardín Infantil Sonrisas se ha iniciado correctamente', 'success', 'normal', '2025-09-30 17:04:28', 1, '2025-09-30 17:21:44', NULL),
(2, 'Bienvenida', 'Bienvenido al sistema de gestión del Jardín Infantil Sonrisas', 'info', 'normal', '2025-09-30 17:04:28', 1, '2025-09-30 17:21:44', NULL);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `user_audit_logs`
--

CREATE TABLE `user_audit_logs` (
  `id` int(11) NOT NULL,
  `admin_id` int(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  `accion` varchar(50) NOT NULL,
  `detalles` text DEFAULT NULL,
  `fecha` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `user_audit_logs`
--

INSERT INTO `user_audit_logs` (`id`, `admin_id`, `user_id`, `accion`, `detalles`, `fecha`) VALUES
(10, 1, 8, 'crear', 'Usuario creado', '2025-09-17 13:17:25'),
(11, 1, 9, 'crear', 'Usuario creado', '2025-09-17 15:33:46'),
(12, 1, 8, 'editar', 'Usuario desactivado', '2025-09-17 15:38:38'),
(13, 1, 8, 'editar', 'Usuario activado', '2025-09-17 15:38:42'),
(19, 1, 11, 'crear', 'Usuario creado', '2025-09-30 22:37:29'),
(20, 1, 9, 'editar', 'Usuario desactivado', '2025-09-30 22:46:47'),
(21, 1, 9, 'editar', 'Usuario activado', '2025-09-30 22:46:51');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `usuarios`
--

CREATE TABLE `usuarios` (
  `id` int(11) NOT NULL,
  `correo` varchar(120) NOT NULL,
  `cedula` varchar(15) DEFAULT NULL,
  `ppt` varchar(20) DEFAULT NULL,
  `contrasena` varchar(255) NOT NULL,
  `id_rol` int(11) NOT NULL,
  `nombre` varchar(60) DEFAULT NULL,
  `apellido` varchar(60) DEFAULT NULL,
  `is_active` tinyint(1) DEFAULT 1
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `usuarios`
--

INSERT INTO `usuarios` (`id`, `correo`, `cedula`, `ppt`, `contrasena`, `id_rol`, `nombre`, `apellido`, `is_active`) VALUES
(1, 'jerjkl182@gmail.com', '1082867670', NULL, 'scrypt:32768:8:1$VfljApPpz5KkJLMw$00f7ada06a214ac92a443fc2937a18ff18e6d931e8057b35f6cf163c47323a7e9e378f52b31349a38286e9cf954349437c41e266b99b856a5b6c444ddd8a8066', 1, 'Jerson', 'Martinez', 1),
(8, 'julian@gmail.com', NULL, NULL, 'scrypt:32768:8:1$6obW1ivx8Dj5kfOt$4645725680d8fb836d0ca0dfe21b7b5457cff614bfb7ad56fb6f25319d80c35b2b133fcee26b849f3524562f6eab340acb66c43304654c8169a6efd64a6ef860', 4, 'julian', 'florez', 1),
(9, 'santiago@gmail.com', NULL, NULL, 'scrypt:32768:8:1$rIySheDueQL3U0q0$bcd9ecec1fe279887bfd41b4210b1bc6434b61c40168c70c583af2735707225cf6e6b1d24c506e1151b0def054069797a1fbd1e94321f1349f88501668b105cc', 2, 'santiago', 'molina', 1),
(11, 'jherson@gmail.com', NULL, NULL, 'scrypt:32768:8:1$E1nmXZYGH9wl4OJ5$5c267cba7e9c6df25a03653f9eda4ca317b2301bfd2cbe09d5c52edb34302d1138e8aaf61b67d6eafaab62ee196aea43e6826749a41d51e2db07bd6e21d208f2', 1, 'jherson', 'florez', 1),
(12, 'maria.rodriguez@email.com', '12345678', NULL, 'scrypt:32768:8:1$aGjP884Wp1PmVOzx$d58ea35cb7cd44dc192fcf301e77ec1bee1cf40dc2a96bce2a400793e7d9c1f3110ea49a2f0b93cbafd78f9b308b232f82e6b6f33644f40957bb8ec89773621d', 4, 'Maria', 'Rodriguez', 1),
(13, 'carlos.gonzalez@email.com', '87654321', NULL, 'scrypt:32768:8:1$mTIoUaj8JxgURXJE$854bf8227b4426c52ababf0e78117fbdf708d33b9249c0644cbdd24c82d5cdd8898011ae8f4ebff3d03081b9c9f7e920ef1faaad75243d70dda0b9a9d8a79828', 4, 'Carlos', 'Gonzalez', 1),
(14, 'ana.martinez@email.com', NULL, 'PPT123456789', 'scrypt:32768:8:1$My3SMR9XaDn2Ync8$e450e4213561dd41618889e849b014f134d1d73a7a489fb869bca46e29808c6806b83cc3ea057ea95612b7f3ee00235759c80bfd0eb08b838a6722ffe524783b', 4, 'Ana', 'Martinez', 1),
(15, 'luis.perez@email.com', '11223344', NULL, 'scrypt:32768:8:1$PTFfbU1KDxjQzq2n$3c862e3bb0610c11cc9e9395d658832363092927deab62ecb33711a7d91ebb04e2609ce3fdcce483696f81e5dbb09fb5dcd02cea57bab1b6500598054d4c266e', 4, 'Luis', 'Perez', 1);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `usuario_roles`
--

CREATE TABLE `usuario_roles` (
  `id` int(11) NOT NULL,
  `usuario_id` int(11) NOT NULL,
  `id_rol` int(11) NOT NULL,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `usuario_roles`
--

INSERT INTO `usuario_roles` (`id`, `usuario_id`, `id_rol`, `created_at`) VALUES
(1, 1, 1, '2025-09-04 14:54:31');

--
-- Índices para tablas volcadas
--

--
-- Indices de la tabla `estudiantes`
--
ALTER TABLE `estudiantes`
  ADD PRIMARY KEY (`id`),
  ADD KEY `idx_profesor_id` (`profesor_id`),
  ADD KEY `idx_acudiente_id` (`acudiente_id`);

--
-- Indices de la tabla `estudiante_acudientes`
--
ALTER TABLE `estudiante_acudientes`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `unique_active_student_acudiente` (`estudiante_id`,`acudiente_id`,`activo`),
  ADD KEY `idx_estudiante` (`estudiante_id`),
  ADD KEY `idx_acudiente` (`acudiente_id`),
  ADD KEY `idx_tipo_relacion` (`tipo_relacion`);

--
-- Indices de la tabla `multimedia`
--
ALTER TABLE `multimedia`
  ADD PRIMARY KEY (`id`),
  ADD KEY `idx_observacion_id` (`observacion_id`),
  ADD KEY `idx_tipo_archivo` (`tipo_archivo`);

--
-- Indices de la tabla `notificaciones`
--
ALTER TABLE `notificaciones`
  ADD PRIMARY KEY (`id`),
  ADD KEY `idx_usuario_id` (`usuario_id`),
  ADD KEY `idx_leida` (`leida`),
  ADD KEY `idx_tipo` (`tipo`),
  ADD KEY `idx_fecha_creacion` (`fecha_creacion`);

--
-- Indices de la tabla `observaciones`
--
ALTER TABLE `observaciones`
  ADD PRIMARY KEY (`id`),
  ADD KEY `fk_obs_profesor` (`id_profesor`),
  ADD KEY `fk_obs_acudiente` (`id_acudiente`),
  ADD KEY `idx_id_estudiante` (`id_estudiante`);

--
-- Indices de la tabla `observation_readings`
--
ALTER TABLE `observation_readings`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `unique_reading` (`observation_id`,`acudiente_id`),
  ADD KEY `idx_observation_id` (`observation_id`),
  ADD KEY `idx_acudiente_id` (`acudiente_id`),
  ADD KEY `idx_read_at` (`read_at`);

--
-- Indices de la tabla `permisos`
--
ALTER TABLE `permisos`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `codigo` (`codigo`);

--
-- Indices de la tabla `roles`
--
ALTER TABLE `roles`
  ADD PRIMARY KEY (`id_rol`),
  ADD UNIQUE KEY `codigo` (`codigo`);

--
-- Indices de la tabla `rol_permisos`
--
ALTER TABLE `rol_permisos`
  ADD PRIMARY KEY (`id_rol`,`permiso_id`),
  ADD KEY `permiso_id` (`permiso_id`);

--
-- Indices de la tabla `session_logs`
--
ALTER TABLE `session_logs`
  ADD PRIMARY KEY (`id`),
  ADD KEY `idx_session_logs_user_id` (`user_id`),
  ADD KEY `idx_session_logs_login_time` (`login_time`);

--
-- Indices de la tabla `system_notifications`
--
ALTER TABLE `system_notifications`
  ADD PRIMARY KEY (`id`),
  ADD KEY `idx_created_at` (`created_at`),
  ADD KEY `idx_is_read` (`is_read`),
  ADD KEY `idx_type` (`type`),
  ADD KEY `idx_priority` (`priority`);

--
-- Indices de la tabla `user_audit_logs`
--
ALTER TABLE `user_audit_logs`
  ADD PRIMARY KEY (`id`),
  ADD KEY `idx_admin_id` (`admin_id`),
  ADD KEY `idx_user_id` (`user_id`),
  ADD KEY `idx_fecha` (`fecha`),
  ADD KEY `idx_accion` (`accion`);

--
-- Indices de la tabla `usuarios`
--
ALTER TABLE `usuarios`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `correo` (`correo`),
  ADD UNIQUE KEY `cedula` (`cedula`),
  ADD UNIQUE KEY `ppt` (`ppt`),
  ADD KEY `id_rol` (`id_rol`);

--
-- Indices de la tabla `usuario_roles`
--
ALTER TABLE `usuario_roles`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `unique_user_role` (`usuario_id`,`id_rol`),
  ADD KEY `idx_usuario_roles_usuario_id` (`usuario_id`),
  ADD KEY `idx_usuario_roles_id_rol` (`id_rol`);

--
-- AUTO_INCREMENT de las tablas volcadas
--

--
-- AUTO_INCREMENT de la tabla `estudiantes`
--
ALTER TABLE `estudiantes`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=8;

--
-- AUTO_INCREMENT de la tabla `estudiante_acudientes`
--
ALTER TABLE `estudiante_acudientes`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=14;

--
-- AUTO_INCREMENT de la tabla `multimedia`
--
ALTER TABLE `multimedia`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- AUTO_INCREMENT de la tabla `notificaciones`
--
ALTER TABLE `notificaciones`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- AUTO_INCREMENT de la tabla `observaciones`
--
ALTER TABLE `observaciones`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT de la tabla `observation_readings`
--
ALTER TABLE `observation_readings`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `permisos`
--
ALTER TABLE `permisos`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=13;

--
-- AUTO_INCREMENT de la tabla `roles`
--
ALTER TABLE `roles`
  MODIFY `id_rol` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

--
-- AUTO_INCREMENT de la tabla `session_logs`
--
ALTER TABLE `session_logs`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `system_notifications`
--
ALTER TABLE `system_notifications`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT de la tabla `user_audit_logs`
--
ALTER TABLE `user_audit_logs`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=22;

--
-- AUTO_INCREMENT de la tabla `usuarios`
--
ALTER TABLE `usuarios`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=16;

--
-- AUTO_INCREMENT de la tabla `usuario_roles`
--
ALTER TABLE `usuario_roles`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- Restricciones para tablas volcadas
--

--
-- Filtros para la tabla `estudiantes`
--
ALTER TABLE `estudiantes`
  ADD CONSTRAINT `fk_estudiantes_acudiente` FOREIGN KEY (`acudiente_id`) REFERENCES `usuarios` (`id`) ON DELETE SET NULL,
  ADD CONSTRAINT `fk_estudiantes_profesor` FOREIGN KEY (`profesor_id`) REFERENCES `usuarios` (`id`) ON DELETE CASCADE;

--
-- Filtros para la tabla `estudiante_acudientes`
--
ALTER TABLE `estudiante_acudientes`
  ADD CONSTRAINT `estudiante_acudientes_ibfk_1` FOREIGN KEY (`estudiante_id`) REFERENCES `estudiantes` (`id`) ON DELETE CASCADE,
  ADD CONSTRAINT `estudiante_acudientes_ibfk_2` FOREIGN KEY (`acudiente_id`) REFERENCES `usuarios` (`id`) ON DELETE CASCADE;

--
-- Filtros para la tabla `multimedia`
--
ALTER TABLE `multimedia`
  ADD CONSTRAINT `fk_multimedia_observacion` FOREIGN KEY (`observacion_id`) REFERENCES `observaciones` (`id`) ON DELETE CASCADE;

--
-- Filtros para la tabla `notificaciones`
--
ALTER TABLE `notificaciones`
  ADD CONSTRAINT `fk_notificaciones_usuario` FOREIGN KEY (`usuario_id`) REFERENCES `usuarios` (`id`) ON DELETE CASCADE;

--
-- Filtros para la tabla `observaciones`
--
ALTER TABLE `observaciones`
  ADD CONSTRAINT `fk_obs_acudiente` FOREIGN KEY (`id_acudiente`) REFERENCES `usuarios` (`id`),
  ADD CONSTRAINT `fk_obs_profesor` FOREIGN KEY (`id_profesor`) REFERENCES `usuarios` (`id`),
  ADD CONSTRAINT `fk_observaciones_estudiante` FOREIGN KEY (`id_estudiante`) REFERENCES `estudiantes` (`id`) ON DELETE CASCADE;

--
-- Filtros para la tabla `rol_permisos`
--
ALTER TABLE `rol_permisos`
  ADD CONSTRAINT `rol_permisos_ibfk_1` FOREIGN KEY (`id_rol`) REFERENCES `roles` (`id_rol`) ON DELETE CASCADE,
  ADD CONSTRAINT `rol_permisos_ibfk_2` FOREIGN KEY (`permiso_id`) REFERENCES `permisos` (`id`) ON DELETE CASCADE;

--
-- Filtros para la tabla `session_logs`
--
ALTER TABLE `session_logs`
  ADD CONSTRAINT `session_logs_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `usuarios` (`id`) ON DELETE CASCADE;

--
-- Filtros para la tabla `user_audit_logs`
--
ALTER TABLE `user_audit_logs`
  ADD CONSTRAINT `user_audit_logs_ibfk_1` FOREIGN KEY (`admin_id`) REFERENCES `usuarios` (`id`) ON DELETE CASCADE,
  ADD CONSTRAINT `user_audit_logs_ibfk_2` FOREIGN KEY (`user_id`) REFERENCES `usuarios` (`id`) ON DELETE CASCADE;

--
-- Filtros para la tabla `usuarios`
--
ALTER TABLE `usuarios`
  ADD CONSTRAINT `usuarios_ibfk_1` FOREIGN KEY (`id_rol`) REFERENCES `roles` (`id_rol`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
