# 🌟 Sistema Jardín Infantil Sonrisas - Documentación Completa

## 📋 Resumen del Sistema

El **Jardín Infantil Sonrisas** es una aplicación web completa desarrollada con Flask (Python) para la gestión educativa de un jardín infantil. El sistema permite a profesores crear observaciones con multimedia (fotos y videos), a administradores gestionar usuarios y enlaces, y a acudientes visualizar y descargar el progreso de sus hijos.

## 🏗️ Arquitectura del Sistema

### Backend (Flask)
```
backend/
├── app.py                          # Punto de entrada principal
├── src/
│   ├── app.py                      # Configuración de la aplicación Flask
│   ├── models/                     # Modelos de datos
│   │   ├── user_model.py          # Gestión de usuarios
│   │   ├── student_model.py       # Gestión de estudiantes
│   │   ├── observation_model.py   # Gestión de observaciones
│   │   └── multimedia_model.py    # Gestión de archivos multimedia
│   ├── routes/                     # Rutas y controladores
│   │   ├── admin_routes.py        # Rutas del administrador
│   │   ├── observation_routes.py  # Rutas de observaciones y multimedia
│   │   └── auth_routes.py         # Autenticación
│   ├── services/                   # Lógica de negocio
│   │   ├── multimedia_service.py  # Servicio de archivos multimedia
│   │   └── user_service.py        # Servicio de usuarios
│   └── utils/                      # Utilidades
│       └── decorators.py          # Decoradores de seguridad
```

### Frontend (Templates HTML)
```
frontend/
├── template/
│   ├── administrador/             # Templates del administrador
│   │   ├── admin_enlaces.html     # Gestión de enlaces
│   │   ├── admin_reportes.html    # Reportes del sistema
│   │   └── admin_auditoria_completa.html # Auditorías
│   ├── profesor/                  # Templates del profesor
│   │   ├── multimedia_lista.html  # Gestión de multimedia
│   │   └── observaciones_lista.html # Lista de observaciones
│   └── acudiente/                 # Templates del acudiente
│       └── multimedia_lista.html  # Visualización de multimedia
└── static/                        # Archivos estáticos (CSS, JS)
```

## 👥 Roles y Funcionalidades

### 🔧 Administrador
**Funcionalidades principales:**
- ✅ **Gestión de usuarios**: Crear, editar, eliminar usuarios (profesores, acudientes)
- ✅ **Gestión de estudiantes**: CRUD completo de estudiantes
- ✅ **Gestión de enlaces**: Vincular estudiantes con profesores y acudientes
- ✅ **Auditorías**: Seguimiento completo de actividades del sistema
- ✅ **Reportes**: Estadísticas y análisis del sistema
- ✅ **Seguridad**: Control de acceso y permisos

**Rutas principales:**
- `/admin/` - Dashboard principal
- `/admin/usuarios` - Gestión de usuarios
- `/admin/estudiantes` - Gestión de estudiantes
- `/admin/enlaces` - Gestión de vinculaciones
- `/admin/reportes` - Reportes del sistema
- `/admin/auditoria` - Auditorías completas

### 👨‍🏫 Profesor
**Funcionalidades principales:**
- ✅ **Observaciones**: Crear, editar, eliminar observaciones de estudiantes
- ✅ **Multimedia**: Subir fotos y videos a las observaciones
- ✅ **Gestión de archivos**: Organizar y eliminar archivos multimedia
- ✅ **Visualización**: Ver solo sus estudiantes asignados

**Rutas principales:**
- `/profesor/observaciones` - Lista de observaciones
- `/profesor/observaciones/nueva` - Crear observación
- `/profesor/observaciones/<id>/multimedia` - Gestionar multimedia
- `/profesor/estudiantes` - Ver estudiantes asignados

### 👨‍👩‍👧‍👦 Acudiente
**Funcionalidades principales:**
- ✅ **Visualización**: Ver observaciones de sus hijos
- ✅ **Multimedia**: Visualizar fotos y videos
- ✅ **Descarga**: Descargar archivos multimedia
- ✅ **Seguimiento**: Monitorear el progreso educativo

**Rutas principales:**
- `/acudiente/observaciones` - Ver observaciones
- `/acudiente/estudiante/<id>/multimedia` - Ver multimedia
- `/acudiente/multimedia/<id>/descargar` - Descargar archivos

## 🗄️ Base de Datos

### Tablas Principales

#### usuarios
```sql
- id (INT, PK, AUTO_INCREMENT)
- correo (VARCHAR, UNIQUE)
- contrasena (VARCHAR)
- nombre (VARCHAR)
- apellido (VARCHAR)
- id_rol (INT) -- 1: Admin, 2: Profesor, 4: Acudiente
- is_active (BOOLEAN)
```

#### estudiantes
```sql
- id (INT, PK, AUTO_INCREMENT)
- nombre (VARCHAR)
- apellido (VARCHAR)
- fecha_nacimiento (DATE)
- grado (VARCHAR) -- Párvulos, Pre-jardín, Jardín, Transición
- profesor_id (INT, FK -> usuarios.id)
- acudiente_id (INT, FK -> usuarios.id)
- fecha_registro (DATETIME)
- activo (BOOLEAN)
```

#### observaciones
```sql
- id (INT, PK, AUTO_INCREMENT)
- id_estudiante (INT, FK -> estudiantes.id)
- id_profesor (INT, FK -> usuarios.id)
- descripcion (TEXT)
- tipo (ENUM: 'Positiva', 'Mejora', 'Neutral')
- fecha (DATETIME)
```

#### multimedia (NUEVA)
```sql
- id (INT, PK, AUTO_INCREMENT)
- observation_id (INT, FK -> observaciones.id)
- filename (VARCHAR)
- file_type (ENUM: 'image', 'video')
- file_path (VARCHAR)
- file_size (BIGINT)
- uploaded_by (INT, FK -> usuarios.id)
- upload_date (DATETIME)
- is_active (BOOLEAN)
```

## 🔧 Instalación y Configuración

### 1. Requisitos del Sistema
```bash
Python 3.8+
MySQL 5.7+
Flask 2.0+
```

### 2. Instalación de Dependencias
```bash
cd backend
pip install -r requirements.txt
```

### 3. Configuración de Base de Datos
```bash
# Ejecutar script SQL
mysql -u usuario -p jardin_sonrisas < database/create_multimedia_table.sql
```

### 4. Configuración de Variables de Entorno
```python
# backend/src/utils/config.py
SECRET_KEY = 'tu_clave_secreta'
MYSQL_HOST = 'localhost'
MYSQL_USER = 'tu_usuario'
MYSQL_PASSWORD = 'tu_contraseña'
MYSQL_DB = 'jardin_sonrisas'
```

### 5. Ejecutar la Aplicación
```bash
cd backend
python app.py
```

## 📁 Sistema de Archivos Multimedia

### Estructura de Almacenamiento
```
uploads/
└── multimedia/
    ├── 2024/
    │   ├── 01/
    │   ├── 02/
    │   └── ...
    └── 2025/
        └── ...
```

### Tipos de Archivos Soportados
- **Imágenes**: JPG, JPEG, PNG, GIF, BMP, WEBP
- **Videos**: MP4, AVI, MOV, WMV, FLV, WEBM
- **Tamaño máximo**: 50MB por archivo
- **Límite por subida**: 10 archivos simultáneos

### Seguridad de Archivos
- ✅ Validación de tipos de archivo
- ✅ Nombres únicos generados automáticamente
- ✅ Control de permisos por rol
- ✅ Soft delete (marcado como inactivo)

## 🔐 Seguridad Implementada

### Autenticación y Autorización
- ✅ **Sesiones seguras** con Flask-Session
- ✅ **Protección CSRF** en todos los formularios
- ✅ **Decoradores de rol** para control de acceso
- ✅ **Validación de permisos** en cada ruta

### Auditoría y Logging
- ✅ **Registro de actividades** de usuarios
- ✅ **Logs de sesiones** con timestamps
- ✅ **Seguimiento de cambios** en datos críticos
- ✅ **Exportación de auditorías** para análisis

## 🚀 Funcionalidades Nuevas Implementadas

### 1. Sistema de Multimedia
- **Subida de archivos**: Profesores pueden subir fotos y videos
- **Gestión de archivos**: Organización y eliminación de multimedia
- **Visualización**: Acudientes pueden ver contenido multimedia
- **Descarga**: Funcionalidad de descarga para acudientes

### 2. Gestión Avanzada de Enlaces
- **Panel de enlaces**: Administrador puede gestionar todas las vinculaciones
- **Estadísticas**: Métricas de estudiantes sin profesor/acudiente
- **Actualización masiva**: Cambios rápidos de asignaciones

### 3. Reportes y Auditorías
- **Dashboard de reportes**: Estadísticas completas del sistema
- **Auditoría completa**: Seguimiento detallado de actividades
- **Exportación de datos**: Funcionalidad de backup y análisis

### 4. Mejoras en la Interfaz
- **Templates modernos**: Diseño actualizado con glass morphism
- **Responsive design**: Adaptable a dispositivos móviles
- **Interactividad**: JavaScript para mejor experiencia de usuario

## 📊 API Endpoints

### Administrador
```
GET  /admin/api/dashboard-stats     # Estadísticas del dashboard
GET  /admin/api/reportes/datos      # Datos de reportes
PUT  /admin/api/estudiantes/<id>/enlace # Actualizar enlaces
```

### Multimedia
```
GET  /api/observaciones/<id>/multimedia # Obtener archivos
DELETE /api/multimedia/<id>             # Eliminar archivo
```

## 🔄 Flujo de Trabajo

### 1. Creación de Observación con Multimedia
1. **Profesor** crea observación básica
2. **Profesor** accede a gestión de multimedia
3. **Profesor** sube fotos/videos relacionados
4. **Sistema** procesa y almacena archivos
5. **Acudiente** recibe notificación (futuro)

### 2. Visualización por Acudiente
1. **Acudiente** accede a observaciones
2. **Acudiente** ve lista con enlaces multimedia
3. **Acudiente** accede a galería de archivos
4. **Acudiente** puede descargar contenido

### 3. Gestión Administrativa
1. **Administrador** crea usuarios y estudiantes
2. **Administrador** establece enlaces profesor-estudiante-acudiente
3. **Administrador** monitorea actividad del sistema
4. **Administrador** genera reportes periódicos

## 🎯 Estado del Proyecto

### ✅ Completado
- [x] Sistema de usuarios y roles
- [x] Gestión de estudiantes por administrador
- [x] Observaciones con multimedia
- [x] Descarga de archivos para acudientes
- [x] Panel de enlaces y vinculaciones
- [x] Auditorías y reportes
- [x] Seguridad y validaciones
- [x] Templates modernos y responsivos

### 🔮 Funcionalidades Futuras (Sugeridas)
- [ ] Sistema de notificaciones en tiempo real
- [ ] Chat entre profesores y acudientes
- [ ] Calendario de actividades
- [ ] Reportes automáticos por email
- [ ] App móvil nativa
- [ ] Integración con sistemas de pago

## 🛠️ Comandos Útiles

### Desarrollo
```bash
# Iniciar servidor de desarrollo
python backend/app.py

# Ejecutar en modo debug
export FLASK_ENV=development
python backend/app.py
```

### Base de Datos
```bash
# Crear tabla multimedia
mysql -u root -p jardin_sonrisas < database/create_multimedia_table.sql

# Backup de la base de datos
mysqldump -u root -p jardin_sonrisas > backup.sql
```

### Mantenimiento
```bash
# Limpiar archivos multimedia huérfanos
python backend/scripts/cleanup_multimedia.py

# Generar reporte de uso
python backend/scripts/usage_report.py
```

## 📞 Soporte y Contacto

Para soporte técnico o consultas sobre el sistema:
- **Documentación**: Este archivo
- **Logs**: Revisar `backend/logs/`
- **Base de datos**: Verificar conexión y permisos

---

**🌟 ¡El Sistema Jardín Infantil Sonrisas está completo y listo para usar! 🌟**

*Desarrollado con ❤️ para facilitar la comunicación entre educadores y familias.*
