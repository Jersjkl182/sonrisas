# 🚀 Deploy del Jardín Infantil Sonrisas en Railway

## 📋 Pasos para Deploy

### 1. Preparar Repositorio GitHub
```bash
git add .
git commit -m "Preparar para deploy en Railway"
git push origin main
```

### 2. Exportar Base de Datos desde phpMyAdmin
1. Abrir phpMyAdmin
2. Seleccionar base de datos `login`
3. Ir a pestaña "Exportar"
4. Método: Rápido, Formato: SQL
5. Descargar archivo `login.sql`

### 3. Configurar Railway
1. Ir a [railway.app](https://railway.app)
2. Registrarse con GitHub
3. **New Project** → **Deploy from GitHub repo**
4. Seleccionar repositorio `Sonrisas`

### 4. Agregar Base de Datos MySQL
1. En el proyecto Railway: **+ Add Service**
2. Seleccionar **MySQL**
3. Railway creará automáticamente la BD

### 5. Importar Datos
1. En Railway, click en el servicio **MySQL**
2. Pestaña **Data**
3. **Import** → Subir archivo `login.sql`
4. Confirmar importación

### 6. Variables de Entorno (Automáticas)
Railway configurará automáticamente:
- `DATABASE_URL`
- `MYSQL_HOST`
- `MYSQL_USER` 
- `MYSQL_PASSWORD`
- `MYSQL_DB`

### 7. Configurar Variables Adicionales
En Railway → **Variables**:
```
FLASK_SECRET_KEY=una_clave_secreta_super_segura_y_aleatoria_para_TeachingNotes_2025!
FLASK_ENV=production
FLASK_DEBUG=False
```

### 8. Deploy Automático
Railway detectará automáticamente:
- `requirements.txt`
- `Procfile`
- `railway.toml`

¡Tu aplicación estará disponible en una URL como: `https://tu-proyecto.railway.app`!

## 🔧 Solución de Problemas

### Error de Conexión BD
- Verificar que las variables de entorno estén configuradas
- Comprobar que la importación SQL fue exitosa

### Error de Archivos Estáticos
- Los archivos subidos se perderán en cada deploy
- Considerar usar servicios de almacenamiento externos

### Límites Gratuitos Railway
- 500 horas de ejecución por mes
- 1GB de RAM
- 1GB de almacenamiento

## 📞 Soporte
Si tienes problemas, Railway tiene documentación excelente y soporte por Discord.
