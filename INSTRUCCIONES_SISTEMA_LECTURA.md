# 📚 SISTEMA DE LECTURA DE OBSERVACIONES - INSTRUCCIONES DE IMPLEMENTACIÓN

## 🗄️ 1. ACTUALIZAR BASE DE DATOS

### Paso 1: Ejecutar el SQL de actualización
```sql
-- Ejecutar en phpMyAdmin o tu cliente MySQL
-- Archivo: update_observaciones_lectura.sql

ALTER TABLE `observaciones` 
ADD COLUMN `leido` TINYINT(1) NOT NULL DEFAULT 0 COMMENT 'Estado de lectura: 0=No leído, 1=Leído';

ALTER TABLE `observaciones` 
ADD COLUMN `fecha_lectura` TIMESTAMP NULL DEFAULT NULL COMMENT 'Fecha y hora cuando se marcó como leído';

ALTER TABLE `observaciones` 
ADD COLUMN `leido_por` INT(11) NULL DEFAULT NULL COMMENT 'ID del usuario que marcó como leído';

ALTER TABLE `observaciones` 
ADD INDEX `idx_leido` (`leido`);

ALTER TABLE `observaciones` 
ADD INDEX `idx_fecha_lectura` (`fecha_lectura`);

ALTER TABLE `observaciones` 
ADD CONSTRAINT `fk_observaciones_leido_por` 
FOREIGN KEY (`leido_por`) REFERENCES `usuarios` (`id`) ON DELETE SET NULL;
```

### Paso 2: Verificar la estructura
```sql
-- Verificar que los campos se agregaron correctamente
DESCRIBE observaciones;

-- Debería mostrar los nuevos campos:
-- leido: tinyint(1) NOT NULL DEFAULT 0
-- fecha_lectura: timestamp NULL DEFAULT NULL
-- leido_por: int(11) NULL DEFAULT NULL
```

## 🐍 2. INTEGRAR RUTAS EN FLASK

### Paso 1: Agregar el blueprint en app.py
```python
# En tu archivo app.py, agregar:
from observaciones_lectura_routes import lectura_bp

# Registrar el blueprint
app.register_blueprint(lectura_bp, url_prefix='/lectura')
```

### Paso 2: Actualizar las consultas existentes
```python
# En tus rutas de observaciones existentes, actualizar las consultas para incluir los nuevos campos:

def obtener_observaciones():
    cursor.execute("""
        SELECT o.*, 
               u_leido.nombre as leido_por_nombre,
               u_profesor.nombre as profesor_nombre,
               u_acudiente.nombre as acudiente_nombre
        FROM observaciones o
        LEFT JOIN usuarios u_leido ON o.leido_por = u_leido.id
        LEFT JOIN usuarios u_profesor ON o.id_profesor = u_profesor.id
        LEFT JOIN usuarios u_acudiente ON o.id_acudiente = u_acudiente.id
        ORDER BY o.fecha DESC
    """)
```

## 🎨 3. ACTUALIZAR TEMPLATES

### Paso 1: Incluir el JavaScript
```html
<!-- En el <head> o antes del </body> de tus templates -->
<script src="{{ url_for('static', filename='js/observaciones_lectura.js') }}"></script>
```

### Paso 2: Actualizar la tabla de observaciones
```html
<!-- Reemplazar la columna de estado actual con: -->
<th>ESTADO LECTURA</th>

<!-- En el tbody: -->
<td>
    {% if obs.leido %}
        <span class="estado-lectura badge badge-success">
            <i class="fas fa-eye"></i> Leído
        </span>
        {% if obs.fecha_lectura %}
            <small class="d-block text-muted">
                {{ obs.fecha_lectura.strftime('%d/%m/%Y %H:%M') }}
            </small>
        {% endif %}
    {% else %}
        <span class="estado-lectura badge badge-warning">
            <i class="fas fa-eye-slash"></i> No leído
        </span>
    {% endif %}
</td>
```

### Paso 3: Actualizar la columna de acciones
```html
<!-- Agregar el botón de toggle lectura antes de los botones existentes -->
<td>
    <div class="btn-lectura-group">
        <!-- Botón Toggle Lectura -->
        {% if obs.leido %}
            <button class="btn btn-sm btn-warning btn-toggle-lectura" 
                    data-observacion-id="{{ obs.id }}"
                    title="Marcar como no leído">
                <i class="fas fa-eye-slash"></i>
            </button>
        {% else %}
            <button class="btn btn-sm btn-success btn-toggle-lectura" 
                    data-observacion-id="{{ obs.id }}"
                    title="Marcar como leído">
                <i class="fas fa-eye"></i>
            </button>
        {% endif %}
        
        <!-- Botones existentes (editar, ver, eliminar) -->
        <a href="{{ url_for('observaciones.editar', id=obs.id) }}" 
           class="btn btn-sm btn-primary" title="Editar">
            <i class="fas fa-edit"></i>
        </a>
        
        <a href="{{ url_for('observaciones.ver', id=obs.id) }}" 
           class="btn btn-sm btn-info" title="Ver">
            <i class="fas fa-eye"></i>
        </a>
        
        <button class="btn btn-sm btn-danger" 
                onclick="confirmarEliminar({{ obs.id }})" title="Eliminar">
            <i class="fas fa-trash"></i>
        </button>
    </div>
</td>
```

## 🎯 4. AGREGAR ESTADÍSTICAS (OPCIONAL)

### Paso 1: Crear función para obtener estadísticas
```python
def obtener_estadisticas_lectura(user_id, user_role):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    if user_role == 'Acudiente':
        query = """
            SELECT 
                COUNT(*) as total,
                SUM(CASE WHEN leido = 1 THEN 1 ELSE 0 END) as leidas,
                SUM(CASE WHEN leido = 0 THEN 1 ELSE 0 END) as no_leidas
            FROM observaciones 
            WHERE id_acudiente = %s
        """
        cursor.execute(query, (user_id,))
    else:
        # Para profesores y administradores
        query = """
            SELECT 
                COUNT(*) as total,
                SUM(CASE WHEN leido = 1 THEN 1 ELSE 0 END) as leidas,
                SUM(CASE WHEN leido = 0 THEN 1 ELSE 0 END) as no_leidas
            FROM observaciones
        """
        cursor.execute(query)
    
    stats = cursor.fetchone()
    cursor.close()
    conn.close()
    
    return {
        'total': stats['total'] or 0,
        'leidas': stats['leidas'] or 0,
        'no_leidas': stats['no_leidas'] or 0,
        'porcentaje_leidas': round((stats['leidas'] or 0) / max(stats['total'] or 1, 1) * 100, 1)
    }
```

### Paso 2: Pasar estadísticas al template
```python
@app.route('/observaciones')
def lista_observaciones():
    user_id = session['user_id']
    user_role = session['role']
    
    observaciones = obtener_observaciones_con_lectura(user_id, user_role)
    estadisticas = obtener_estadisticas_lectura(user_id, user_role)
    
    return render_template('observaciones_lista.html', 
                         observaciones=observaciones,
                         estadisticas=estadisticas)
```

## 🎨 5. ESTILOS CSS ADICIONALES

```css
/* Agregar a tu CSS principal */
.observacion-leida {
    background-color: rgba(40, 167, 69, 0.1) !important;
}

.observacion-no-leida {
    background-color: rgba(255, 193, 7, 0.1) !important;
}

.estado-lectura {
    font-size: 0.85rem;
    padding: 4px 8px;
    border-radius: 12px;
}

.btn-lectura-group {
    display: flex;
    gap: 5px;
    flex-wrap: wrap;
}

@media (max-width: 768px) {
    .btn-lectura-group {
        flex-direction: column;
    }
    
    .btn-lectura-group .btn {
        width: 100%;
        margin-bottom: 5px;
    }
}

.estadisticas-lectura {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
    border-radius: 15px;
    padding: 20px;
    margin-bottom: 20px;
}
```

## 🧪 6. TESTING

### Paso 1: Verificar funcionalidad básica
1. ✅ Cargar la página de observaciones
2. ✅ Ver el estado "No leído" en observaciones nuevas
3. ✅ Hacer clic en el botón de "Marcar como leído"
4. ✅ Verificar que el estado cambia a "Leído"
5. ✅ Verificar que las estadísticas se actualizan

### Paso 2: Probar en diferentes roles
1. ✅ **Acudiente**: Solo ve sus observaciones
2. ✅ **Profesor**: Ve las observaciones que creó
3. ✅ **Administrador**: Ve todas las observaciones

### Paso 3: Verificar responsive
1. ✅ Probar en móviles (botones se apilan verticalmente)
2. ✅ Probar en tablets (layout se adapta)
3. ✅ Verificar que las notificaciones aparecen correctamente

## 🚀 7. FUNCIONALIDADES ADICIONALES

### Notificaciones automáticas
```python
# Agregar en la creación de observaciones
def crear_observacion():
    # ... código existente ...
    
    # Enviar notificación al acudiente
    enviar_notificacion(acudiente_id, f"Nueva observación: {titulo}")
```

### Filtros avanzados
```javascript
// Agregar filtros por fecha, tipo, etc.
function filtrarObservaciones(filtros) {
    // Implementar lógica de filtrado
}
```

### Reportes
```python
# Generar reportes de lectura
def generar_reporte_lectura():
    # Implementar generación de reportes
    pass
```

## ✅ CHECKLIST DE IMPLEMENTACIÓN

- [ ] 1. Ejecutar SQL de actualización de base de datos
- [ ] 2. Copiar archivos Python y JavaScript
- [ ] 3. Registrar blueprint en app.py
- [ ] 4. Actualizar templates existentes
- [ ] 5. Agregar estilos CSS
- [ ] 6. Probar funcionalidad básica
- [ ] 7. Probar en diferentes roles
- [ ] 8. Verificar responsive
- [ ] 9. Implementar estadísticas (opcional)
- [ ] 10. Testing completo

## 🆘 SOLUCIÓN DE PROBLEMAS

### Error: "Column 'leido' doesn't exist"
- **Causa**: No se ejecutó el SQL de actualización
- **Solución**: Ejecutar `update_observaciones_lectura.sql`

### Error: "Blueprint not found"
- **Causa**: No se registró el blueprint
- **Solución**: Agregar `app.register_blueprint(lectura_bp, url_prefix='/lectura')` en app.py

### Los botones no funcionan
- **Causa**: JavaScript no se carga
- **Solución**: Verificar que `observaciones_lectura.js` esté en la ruta correcta

### Estadísticas no se actualizan
- **Causa**: Error en la consulta o permisos
- **Solución**: Verificar logs del servidor y consultas SQL

---

¡Con estos archivos y instrucciones tendrás un sistema completo de lectura de observaciones! 🎉
