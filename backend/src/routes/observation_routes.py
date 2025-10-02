"""Rutas para gestionar notas de observación.
Admin: CRUD completo.
Acudiente: solo lectura.
"""

from flask import Blueprint, render_template, request, redirect, url_for, flash, session, jsonify, send_file
from ..services.observation_service import ObservationService
from ..services.multimedia_service import MultimediaService
from ..models.observation_view_model import ObservationViewModel
from ..utils.decorators import login_required, role_required  # Usamos role_required para roles específicos
import os

# IDs de rol (ajusta según tu tabla roles)
ADMIN_ROLE_ID = 1
PROF_ROLE_ID = 2
ACUD_ROLE_ID = 4

obs_bp = Blueprint('obs_bp', __name__)

# ----------------- PROFESOR -----------------
import datetime

from werkzeug.security import generate_password_hash, check_password_hash
from ..models.user_model import UserModel
from ..services.user_service import UserService

@obs_bp.route('/profesor/perfil', methods=['GET', 'POST'])
@login_required
@role_required([PROF_ROLE_ID])
def perfil_profesor():
    user = UserModel.find_by_id(session['id'])
    if request.method == 'POST':
        nombre = request.form.get('nombre')
        apellido = request.form.get('apellido')
        correo = request.form.get('correo')
        if not nombre or not apellido or not correo:
            flash('Todos los campos son obligatorios.', 'warning')
        else:
            UserService.update_user(session['id'], correo=correo, nombre=nombre, apellido=apellido)
            session['nombre'] = nombre
            flash('Perfil actualizado.', 'success')
            return redirect(url_for('obs_bp.perfil_profesor'))
    return render_template('profesor/perfil.html', user=user)

@obs_bp.route('/profesor/cambiar-contrasena', methods=['POST'])
@login_required
@role_required([PROF_ROLE_ID])
def cambiar_contrasena_profesor():
    actual = request.form.get('contrasena_actual')
    nueva = request.form.get('nueva_contrasena')
    confirmar = request.form.get('confirmar_contrasena')
    user = UserModel.find_by_id(session['id'])
    if not check_password_hash(user['contrasena'], actual):
        flash('Contraseña actual incorrecta.', 'danger')
    elif nueva != confirmar:
        flash('La nueva contraseña y su confirmación no coinciden.', 'warning')
    else:
        hashed = generate_password_hash(nueva)
        UserModel.update_user(session['id'], hashed_password=hashed)
        flash('Contraseña actualizada.', 'success')
    return redirect(url_for('obs_bp.perfil_profesor'))

@obs_bp.route('/profesor/progreso')
@login_required
@role_required([PROF_ROLE_ID])
def progreso_profesor():
    notas = ObservationService.listar_por_profesor(session['id'])
    estudiantes = ObservationService.listar_estudiantes_profesor(session['id'])
    total_observaciones = len(notas)
    semana_atras = datetime.datetime.utcnow() - datetime.timedelta(days=7)
    obs_recientes = [n for n in notas if n['fecha'] >= semana_atras]
    return render_template('profesor/progreso_dashboard.html', total_observaciones=total_observaciones, recientes=len(obs_recientes), total_estudiantes=len(estudiantes))


@obs_bp.route('/profesor/estudiantes')
@login_required
@role_required([PROF_ROLE_ID])
def listar_estudiantes_profesor():
    from ..models.student_model import StudentModel
    # Para la lista de estudiantes del profesor, mostrar solo los suyos
    estudiantes = StudentModel.get_students_by_professor_only(session['id'])
    return render_template('profesor/estudiantes_lista.html', estudiantes=estudiantes)

# FUNCIONALIDAD MOVIDA AL ADMINISTRADOR
# Los profesores ya no pueden crear estudiantes
# @obs_bp.route('/profesor/estudiantes/nuevo', methods=['GET', 'POST'])
# @login_required
# @role_required([PROF_ROLE_ID])
# def crear_estudiante():
#     flash('Esta funcionalidad ha sido trasladada al administrador del sistema.', 'info')
#     return redirect(url_for('obs_bp.listar_estudiantes_profesor'))

# FUNCIONALIDAD MOVIDA AL ADMINISTRADOR
# Los profesores ya no pueden editar estudiantes
# @obs_bp.route('/profesor/estudiantes/<int:student_id>/editar', methods=['GET', 'POST'])
# @login_required
# @role_required([PROF_ROLE_ID])
# def editar_estudiante(student_id):
#     flash('Esta funcionalidad ha sido trasladada al administrador del sistema.', 'info')
#     return redirect(url_for('obs_bp.listar_estudiantes_profesor'))

# FUNCIONALIDAD MOVIDA AL ADMINISTRADOR
# Los profesores ya no pueden eliminar estudiantes
# @obs_bp.route('/profesor/estudiantes/<int:student_id>/eliminar', methods=['POST'])
# @login_required
# @role_required([PROF_ROLE_ID])
# def eliminar_estudiante(student_id):
#     flash('Esta funcionalidad ha sido trasladada al administrador del sistema.', 'info')
#     return redirect(url_for('obs_bp.listar_estudiantes_profesor'))

# FUNCIONALIDAD MOVIDA AL ADMINISTRADOR
# Los profesores ya no pueden asignar acudientes a estudiantes
# @obs_bp.route('/profesor/estudiantes/<int:student_id>/asignar-acudiente', methods=['GET', 'POST'])
# @login_required
# @role_required([PROF_ROLE_ID])
# def asignar_acudiente_existente(student_id):
#     flash('Esta funcionalidad ha sido trasladada al administrador del sistema.', 'info')
#     return redirect(url_for('obs_bp.listar_estudiantes_profesor'))

@obs_bp.route('/debug/acudientes')
def debug_acudientes():
    """Endpoint temporal para debug de acudientes - SIN LOGIN REQUERIDO PARA DEBUG"""
    from ..services.user_service import UserService
    from ..models.user_model import UserModel
    
    # Probar el servicio directamente
    try:
        html = "<h1>🔍 Debug Acudientes - Diagnóstico Completo</h1>"
        html += "<style>body{font-family:Arial;margin:20px;} h1,h2,h3{color:#333;} .error{color:red;} .success{color:green;} .info{color:blue;}</style>"
        
        # 1. Probar UserService.get_all_acudientes()
        html += "<h2>1. Resultado del servicio UserService.get_all_acudientes():</h2>"
        acudientes = UserService.get_all_acudientes()
        html += f"<p class='info'>Cantidad encontrada: <strong>{len(acudientes) if acudientes else 0}</strong> acudientes</p>"
        
        if acudientes:
            html += "<h3>✅ Acudientes encontrados:</h3><ul>"
            for acudiente in acudientes:
                html += f"<li><strong>ID:</strong> {acudiente.get('id')}, <strong>Nombre:</strong> {acudiente.get('nombre')} {acudiente.get('apellido')}, <strong>Email:</strong> {acudiente.get('correo')}, <strong>Activo:</strong> {acudiente.get('activo')}</li>"
            html += "</ul>"
        else:
            html += "<p class='error'>❌ No se encontraron acudientes</p>"
        
        # 2. Probar UserModel.get_users_by_role(4) directamente
        html += "<h2>2. Resultado directo de UserModel.get_users_by_role(4):</h2>"
        acudientes_directo = UserModel.get_users_by_role(4)
        html += f"<p class='info'>Cantidad encontrada: <strong>{len(acudientes_directo) if acudientes_directo else 0}</strong> acudientes</p>"
        
        if acudientes_directo:
            html += "<h3>✅ Acudientes encontrados (directo):</h3><ul>"
            for acudiente in acudientes_directo:
                html += f"<li><strong>ID:</strong> {acudiente.get('id')}, <strong>Nombre:</strong> {acudiente.get('nombre')} {acudiente.get('apellido')}, <strong>Email:</strong> {acudiente.get('correo')}</li>"
            html += "</ul>"
        else:
            html += "<p class='error'>❌ No se encontraron acudientes (directo)</p>"
        
        # 3. Consulta SQL directa para verificar
        html += "<h2>3. Consulta SQL directa - Todos los usuarios:</h2>"
        try:
            from ..database.db_connection import mysql
            cur = mysql.connection.cursor()
            cur.execute("SELECT id, correo, nombre, apellido, id_rol FROM usuarios ORDER BY id_rol, nombre")
            todos_usuarios = cur.fetchall()
            cur.close()
            
            html += f"<p class='info'>Total usuarios en la base de datos: <strong>{len(todos_usuarios)}</strong></p>"
            
            # Debug: mostrar estructura de la consulta
            html += f"<p class='info'>🔍 Debug: Cada usuario tiene {len(todos_usuarios[0]) if todos_usuarios else 0} columnas</p>"
            if todos_usuarios:
                html += f"<p class='info'>📋 Ejemplo de usuario: {todos_usuarios[0]}</p>"
            
            # Contar por roles (accediendo como diccionario)
            roles_count = {}
            for usuario in todos_usuarios:
                # Los datos vienen como diccionario, no como tupla
                if isinstance(usuario, dict) and 'id_rol' in usuario:
                    rol_id = usuario['id_rol']
                    roles_count[rol_id] = roles_count.get(rol_id, 0) + 1
                elif hasattr(usuario, '__getitem__') and len(usuario) > 4:
                    # Fallback para tuplas
                    rol_id = usuario[4]
                    roles_count[rol_id] = roles_count.get(rol_id, 0) + 1
                else:
                    html += f"<p class='error'>⚠️ Usuario con estructura incorrecta: {usuario}</p>"
            
            html += "<h3>📊 Conteo por roles:</h3><ul>"
            for rol_id, count in roles_count.items():
                rol_nombre = {1: "Administrador", 2: "Profesor", 3: "Acudiente (Rol 3)", 4: "Acudiente (Rol 4)"}.get(rol_id, f"Rol {rol_id}")
                html += f"<li><strong>Rol {rol_id}</strong> ({rol_nombre}): <strong>{count}</strong> usuarios</li>"
            html += "</ul>"
            
            html += "<h3>👥 Detalle de todos los usuarios:</h3>"
            html += "<table border='1' style='border-collapse:collapse; margin:10px 0;'>"
            html += "<tr style='background:#f0f0f0;'><th>ID</th><th>Email</th><th>Nombre</th><th>Apellido</th><th>Rol ID</th><th>Tipo</th></tr>"
            
            for usuario in todos_usuarios:
                if isinstance(usuario, dict):
                    # Acceder como diccionario
                    rol_id = usuario.get('id_rol', 'N/A')
                    rol_nombre = {1: "Administrador", 2: "Profesor", 3: "Acudiente (Rol 3)", 4: "Acudiente (Rol 4)"}.get(rol_id, f"Rol {rol_id}")
                    color = "background:#e8f5e8;" if rol_id == 4 else "background:#fff3cd;" if rol_id == 3 else ""
                    html += f"<tr style='{color}'><td>{usuario.get('id', 'N/A')}</td><td>{usuario.get('correo', 'N/A')}</td><td>{usuario.get('nombre', 'N/A')}</td><td>{usuario.get('apellido', 'N/A')}</td><td>{rol_id}</td><td>{rol_nombre}</td></tr>"
                elif hasattr(usuario, '__getitem__') and len(usuario) > 4:
                    # Fallback para tuplas
                    rol_id = usuario[4]
                    rol_nombre = {1: "Administrador", 2: "Profesor", 3: "Acudiente (Rol 3)", 4: "Acudiente (Rol 4)"}.get(rol_id, f"Rol {rol_id}")
                    color = "background:#e8f5e8;" if rol_id == 4 else "background:#fff3cd;" if rol_id == 3 else ""
                    html += f"<tr style='{color}'><td>{usuario[0]}</td><td>{usuario[1]}</td><td>{usuario[2]}</td><td>{usuario[3]}</td><td>{usuario[4]}</td><td>{rol_nombre}</td></tr>"
                else:
                    html += f"<tr style='background:#ffebee;'><td colspan='6'>Error: Usuario con estructura incorrecta: {usuario}</td></tr>"
            
            html += "</table>"
            
            # 4. Consulta específica para acudientes
            html += "<h2>4. 🎯 Consulta específica para acudientes (id_rol = 4):</h2>"
            cur = mysql.connection.cursor()
            cur.execute("SELECT id, correo, nombre, apellido, id_rol FROM usuarios WHERE id_rol = 4")
            acudientes_sql = cur.fetchall()
            cur.close()
            
            html += f"<p class='info'>Acudientes con id_rol = 4: <strong>{len(acudientes_sql)}</strong></p>"
            
            if acudientes_sql:
                html += "<table border='1' style='border-collapse:collapse; margin:10px 0;'>"
                html += "<tr style='background:#e8f5e8;'><th>ID</th><th>Email</th><th>Nombre</th><th>Apellido</th><th>Rol ID</th></tr>"
                for acudiente in acudientes_sql:
                    if isinstance(acudiente, dict):
                        html += f"<tr><td>{acudiente.get('id', 'N/A')}</td><td>{acudiente.get('correo', 'N/A')}</td><td>{acudiente.get('nombre', 'N/A')}</td><td>{acudiente.get('apellido', 'N/A')}</td><td>{acudiente.get('id_rol', 'N/A')}</td></tr>"
                    elif hasattr(acudiente, '__getitem__') and len(acudiente) > 4:
                        html += f"<tr><td>{acudiente[0]}</td><td>{acudiente[1]}</td><td>{acudiente[2]}</td><td>{acudiente[3]}</td><td>{acudiente[4]}</td></tr>"
                    else:
                        html += f"<tr><td colspan='5'>Error en estructura: {acudiente}</td></tr>"
                html += "</table>"
                
                # Mostrar información adicional del acudiente encontrado
                html += "<h3>✅ ¡Acudiente encontrado!</h3>"
                html += "<p class='success'>El sistema debería mostrar este acudiente en la lista de asignación.</p>"
                
            else:
                html += "<p class='error'>❌ No hay usuarios con id_rol = 4</p>"
                html += "<p class='info'>💡 <strong>Solución:</strong> Si tienes acudientes con id_rol = 3, puedes cambiarlos a 4 con:</p>"
                html += "<code style='background:#f0f0f0; padding:10px; display:block; margin:10px 0;'>UPDATE usuarios SET id_rol = 4 WHERE id_rol = 3;</code>"
            
        except Exception as e:
            html += f"<p class='error'>Error en consulta directa: {str(e)}</p>"
            import traceback
            html += f"<pre>{traceback.format_exc()}</pre>"
        
        return html
        
    except Exception as e:
        import traceback
        return f"<h1>Error en debug:</h1><pre>{str(e)}\n\n{traceback.format_exc()}</pre>"

@obs_bp.route('/debug/estudiantes')
@login_required
def debug_estudiantes():
    """Endpoint temporal para debug de estudiantes"""
    from ..models.student_model import StudentModel
    
    try:
        # Obtener ID del profesor desde la sesión
        profesor_id = session.get('id')
        
        html = f"<h2>Debug Estudiantes</h2>"
        html += f"<h3>Profesor ID desde sesión: {profesor_id}</h3>"
        
        # Probar el método get_students_by_professor
        estudiantes = StudentModel.get_students_by_professor(profesor_id)
        
        html += f"<h3>Resultado del método get_students_by_professor({profesor_id}):</h3>"
        html += f"<p>Cantidad encontrada: {len(estudiantes) if estudiantes else 0} estudiantes</p>"
        
        if estudiantes:
            html += "<ul>"
            for estudiante in estudiantes:
                html += f"<li>ID: {estudiante.get('id')}, Nombre: {estudiante.get('nombre')} {estudiante.get('apellido')}, Grado: {estudiante.get('grado')}, Profesor ID: {estudiante.get('profesor_id')}</li>"
            html += "</ul>"
        else:
            html += "<p>No se encontraron estudiantes para este profesor</p>"
            
        # También verificar todos los estudiantes en la tabla
        from ..database.db_connection import mysql, get_cursor
        
        cur = get_cursor('dict')
        cur.execute("SELECT * FROM estudiantes")
        todos_estudiantes = cur.fetchall()
        cur.close()
        
        html += f"<h3>Todos los estudiantes en la tabla:</h3>"
        html += f"<p>Total en la tabla: {len(todos_estudiantes) if todos_estudiantes else 0}</p>"
        
        if todos_estudiantes:
            html += "<ul>"
            for est in todos_estudiantes:
                html += f"<li>ID: {est.get('id')}, Nombre: {est.get('nombre')} {est.get('apellido')}, Profesor ID: {est.get('profesor_id')}, Activo: {est.get('activo')}</li>"
            html += "</ul>"
        
        return html
        
    except Exception as e:
        return f"Error: {str(e)}"

@obs_bp.route('/profesor/acudientes/crear/<int:student_id>', methods=['GET', 'POST'])
@login_required
@role_required([PROF_ROLE_ID])
def crear_acudiente_para_estudiante(student_id):
    from ..models.student_model import StudentModel
    from ..services.user_audit_log_service import UserAuditLogService
    
    # Verificar que el estudiante pertenece al profesor
    student = StudentModel.get_student_by_id(student_id)
    if not student or student['profesor_id'] != session['id']:
        flash('Estudiante no encontrado o no autorizado.', 'danger')
        return redirect(url_for('obs_bp.listar_estudiantes_profesor'))
    
    if request.method == 'POST':
        nombre = request.form.get('nombre')
        apellido = request.form.get('apellido')
        correo = request.form.get('correo')
        telefono = request.form.get('telefono', '')
        direccion = request.form.get('direccion', '')
        contrasena = request.form.get('contrasena')
        
        if not all([nombre, apellido, correo, contrasena]):
            flash('Los campos nombre, apellido, correo y contraseña son obligatorios.', 'danger')
            return render_template('profesor/crear_acudiente.html', student=student)
        
        # Verificar si el correo ya existe
        existing_user = UserModel.find_by_email(correo)
        if existing_user:
            flash('Ya existe un usuario con ese correo electrónico.', 'danger')
            return render_template('profesor/crear_acudiente.html', student=student)
        
        # Crear el acudiente
        hashed_password = generate_password_hash(contrasena)
        success = UserModel.create_user(
            correo=correo,
            hashed_password=hashed_password,
            id_rol=ACUD_ROLE_ID,
            nombre=nombre,
            apellido=apellido
        )
        
        if success:
            # Obtener el ID del nuevo usuario
            new_user = UserModel.find_by_email(correo)
            if new_user:
                # Asignar el acudiente al estudiante
                StudentModel.assign_acudiente(student_id, new_user['id'])
                
                # Registrar en auditoría
                UserAuditLogService.log(
                    admin_id=session['id'],
                    user_id=new_user['id'],
                    accion='crear',
                    detalles=f'Acudiente creado por profesor para estudiante {student["nombre"]} {student["apellido"]}'
                )
                
                flash(f'Acudiente {nombre} {apellido} creado y asignado exitosamente.', 'success')
                return redirect(url_for('obs_bp.listar_estudiantes_profesor'))
        
        flash('Error al crear el acudiente.', 'danger')
    
    return render_template('profesor/crear_acudiente.html', student=student)


@obs_bp.route('/profesor/observaciones')
@login_required
@role_required([PROF_ROLE_ID])
def listar_observaciones_profesor():
    """Lista las observaciones creadas por el profesor logueado con estado de lectura y filtros"""
    from ..models.observation_reading_model import ObservationReadingModel
    from ..models.student_model import StudentModel
    from datetime import datetime
    
    profesor_id = session['id']
    
    # Obtener parámetros de filtro
    estudiante_id = request.args.get('estudiante')
    tipo_obs = request.args.get('tipo')
    estado_lectura = request.args.get('lectura')
    fecha_desde = request.args.get('fecha_desde')
    fecha_hasta = request.args.get('fecha_hasta')
    buscar = request.args.get('buscar')
    
    # Obtener todas las observaciones del profesor
    notas = ObservationService.listar_por_profesor(profesor_id)
    
    # Aplicar filtros
    if notas:
        # Agregar estado de lectura a cada observación
        for nota in notas:
            reading_status = ObservationReadingModel.get_reading_status_for_observation(nota.get('id'))
            nota['reading_status'] = reading_status
            nota['is_read'] = reading_status.get('estado_lectura') == 'leida' if reading_status else False
            nota['read_at'] = reading_status.get('read_at') if reading_status else None
            nota['acudiente_info'] = {
                'nombre': reading_status.get('acudiente_nombre') if reading_status else None,
                'apellido': reading_status.get('acudiente_apellido') if reading_status else None,
                'correo': reading_status.get('acudiente_correo') if reading_status else None
            } if reading_status else None
        
        # Filtro por estudiante
        if estudiante_id:
            try:
                estudiante_id = int(estudiante_id)
                notas = [n for n in notas if n.get('id_estudiante') == estudiante_id]
            except (ValueError, TypeError):
                pass
        
        # Filtro por tipo de observación
        if tipo_obs:
            notas = [n for n in notas if n.get('tipo_observacion') == tipo_obs]
        
        # Filtro por estado de lectura
        if estado_lectura:
            if estado_lectura == 'leida':
                notas = [n for n in notas if n.get('is_read')]
            elif estado_lectura == 'no_leida':
                notas = [n for n in notas if not n.get('is_read') and n.get('reading_status', {}).get('id_acudiente')]
            elif estado_lectura == 'sin_acudiente':
                notas = [n for n in notas if not n.get('reading_status', {}).get('id_acudiente')]
        
        # Filtro por fecha desde
        if fecha_desde:
            try:
                fecha_desde_dt = datetime.strptime(fecha_desde, '%Y-%m-%d').date()
                notas = [n for n in notas if n.get('fecha') and n.get('fecha').date() >= fecha_desde_dt]
            except (ValueError, TypeError):
                pass
        
        # Filtro por fecha hasta
        if fecha_hasta:
            try:
                fecha_hasta_dt = datetime.strptime(fecha_hasta, '%Y-%m-%d').date()
                notas = [n for n in notas if n.get('fecha') and n.get('fecha').date() <= fecha_hasta_dt]
            except (ValueError, TypeError):
                pass
        
        # Filtro por búsqueda en título
        if buscar:
            buscar_lower = buscar.lower()
            notas = [n for n in notas if buscar_lower in str(n.get('titulo', '')).lower()]
    
    # Obtener estadísticas generales
    stats = ObservationReadingModel.get_reading_statistics_for_profesor(profesor_id)
    
    # Obtener lista de estudiantes del profesor para el filtro
    estudiantes_list = StudentModel.get_students_by_professor(profesor_id)
    
    return render_template('profesor/observaciones_lista.html', 
                         notas=notas, 
                         reading_stats=stats,
                         estudiantes_list=estudiantes_list)


@obs_bp.route('/profesor/observaciones/nueva', methods=['GET', 'POST'])
@login_required
@role_required([PROF_ROLE_ID])
def crear_observacion():
    from ..models.student_model import StudentModel
    from ..models.observation_model import ObservationModel
    
    if request.method == 'POST':
        titulo = request.form['titulo']
        descripcion = request.form['descripcion']
        id_estudiante = request.form['id_estudiante']
        tipo = request.form.get('tipo', 'Positiva')

        obs_id = ObservationModel.create(titulo, descripcion, session['id'], id_estudiante, tipo)
        if obs_id:
            # Procesar archivos multimedia si se enviaron
            if 'multimedia_files' in request.files:
                files = request.files.getlist('multimedia_files')
                if files and files[0].filename:  # Verificar que hay archivos
                    uploaded_count = 0
                    errors = []
                    
                    for file in files:
                        if file and file.filename:
                            try:
                                success, message = MultimediaService.save_file(file, obs_id, session['id'])
                                if success:
                                    uploaded_count += 1
                                else:
                                    errors.append(f"Error con {file.filename}: {message}")
                            except Exception as e:
                                errors.append(f"Error con {file.filename}: {str(e)}")
                    
                    if uploaded_count > 0:
                        flash(f'Observación creada correctamente con {uploaded_count} archivo(s) multimedia.', 'success')
                    else:
                        flash('Observación creada correctamente.', 'success')
                    
                    # Mostrar errores si los hay
                    for error in errors:
                        flash(error, 'warning')
                else:
                    flash('Observación creada correctamente.', 'success')
            else:
                flash('Observación creada correctamente.', 'success')
        else:
            flash('Error al crear la observación.', 'danger')
        return redirect(url_for('obs_bp.listar_observaciones_profesor'))

    # Para GET obtenemos lista de estudiantes del profesor
    profesor_id = session['id']
    print(f"DEBUG: Obteniendo estudiantes para profesor ID: {profesor_id}")
    
    estudiantes = StudentModel.get_students_by_professor(profesor_id)
    print(f"DEBUG: Estudiantes encontrados: {len(estudiantes) if estudiantes else 0}")
    
    if estudiantes:
        for est in estudiantes:
            print(f"DEBUG: Estudiante - ID: {est.get('id')}, Nombre: {est.get('nombre')} {est.get('apellido')}")
    else:
        print("DEBUG: No se encontraron estudiantes para este profesor")
    
    return render_template('profesor/observaciones_form.html', modo='crear', nota=None, estudiantes=estudiantes)


@obs_bp.route('/profesor/observaciones/<int:obs_id>/editar', methods=['GET', 'POST'])
@login_required
@role_required([PROF_ROLE_ID])
def editar_observacion(obs_id):
    from ..models.observation_model import ObservationModel
    from ..models.student_model import StudentModel
    
    nota = ObservationModel.get_by_id(obs_id)
    if not nota:
        flash('Observación no encontrada.', 'danger')
        return redirect(url_for('obs_bp.listar_observaciones_profesor'))

    if request.method == 'POST':
        titulo = request.form['titulo']
        descripcion = request.form['descripcion']
        tipo = request.form.get('tipo', 'Positiva')

        ObservationModel.update(obs_id, titulo, descripcion, tipo)
        flash('Observación actualizada con éxito.', 'success')
        return redirect(url_for('obs_bp.listar_observaciones_profesor'))

    # Para el formulario de edición, obtenemos los estudiantes del profesor
    estudiantes = StudentModel.get_students_by_professor(session['id'])
    
    # Obtener archivos multimedia existentes
    archivos_multimedia = MultimediaService.get_multimedia_by_observation(obs_id)
    
    return render_template('profesor/observaciones_form.html', 
                         modo='editar', 
                         nota=nota, 
                         estudiantes=estudiantes,
                         archivos_multimedia=archivos_multimedia)


@obs_bp.route('/profesor/observaciones/<int:obs_id>/eliminar', methods=['POST'])
@login_required
@role_required([PROF_ROLE_ID])
def eliminar_observacion(obs_id):
    ObservationService.eliminar(obs_id)
    flash('Observación eliminada.', 'info')
    return redirect(url_for('obs_bp.listar_observaciones_profesor'))

# ----------------- ACUDIENTE -----------------
@obs_bp.route('/acudiente/observaciones')
@login_required
@role_required([ACUD_ROLE_ID])
def listar_observaciones_acudiente():
    from ..models.observation_reading_model import ObservationReadingModel
    
    acudiente_id = session['id']
    print(f"DEBUG: Acudiente ID desde sesión: {acudiente_id}")
    
    notas = ObservationService.listar_para_acudiente(acudiente_id)
    print(f"DEBUG: Número de observaciones encontradas: {len(notas) if notas else 0}")
    
    # Agregar estado de lectura a cada observación
    if notas:
        for nota in notas:
            reading_status = ObservationReadingModel.is_read_by_acudiente(nota.get('id'), acudiente_id)
            nota['is_read'] = reading_status is not None
            nota['read_at'] = reading_status.get('read_at') if reading_status else None
            print(f"DEBUG: Observación - ID: {nota.get('id')}, Estudiante: {nota.get('estudiante_nombre')} {nota.get('estudiante_apellido')}, Leída: {nota['is_read']}")
    else:
        print("DEBUG: No se encontraron observaciones")
    
    return render_template('acudiente/observaciones_lista.html', notas=notas)

@obs_bp.route('/acudiente/observaciones/<int:obs_id>/marcar-leida', methods=['POST'])
@login_required
@role_required([ACUD_ROLE_ID])
def marcar_observacion_leida(obs_id):
    """Marca una observación como leída por el acudiente"""
    from ..models.observation_reading_model import ObservationReadingModel
    from ..models.observation_model import ObservationModel
    
    acudiente_id = session['id']
    
    # Verificar que la observación pertenece al acudiente
    observacion = ObservationModel.get_by_id(obs_id)
    if not observacion or observacion.get('id_acudiente') != acudiente_id:
        flash('Observación no encontrada o sin permisos.', 'danger')
        return redirect(url_for('obs_bp.listar_observaciones_acudiente'))
    
    # Obtener información del request
    ip_address = request.environ.get('HTTP_X_FORWARDED_FOR', request.environ.get('REMOTE_ADDR'))
    user_agent = request.environ.get('HTTP_USER_AGENT')
    
    # Marcar como leída
    success = ObservationReadingModel.mark_as_read(obs_id, acudiente_id, ip_address, user_agent)
    
    if success:
        flash('Observación marcada como leída.', 'success')
    else:
        flash('Esta observación ya había sido marcada como leída anteriormente.', 'info')
    
    return redirect(url_for('obs_bp.listar_observaciones_acudiente'))

@obs_bp.route('/acudiente/api/observaciones-no-leidas')
@login_required
@role_required([ACUD_ROLE_ID])
def api_observaciones_no_leidas():
    """API para obtener el número de observaciones no leídas"""
    from ..models.observation_reading_model import ObservationReadingModel
    
    acudiente_id = session['id']
    observaciones_no_leidas = ObservationReadingModel.get_unread_observations_for_acudiente(acudiente_id)
    
    return jsonify({
        'count': len(observaciones_no_leidas),
        'observations': observaciones_no_leidas
    })

# ----------------- MULTIMEDIA (FOTOS Y VIDEOS) -----------------

@obs_bp.route('/profesor/observaciones/<int:obs_id>/multimedia', methods=['GET'])
@login_required
@role_required([PROF_ROLE_ID])
def ver_multimedia_observacion(obs_id):
    """Ver archivos multimedia de una observación."""
    from ..models.observation_model import ObservationModel
    
    # Verificar que la observación existe y pertenece al profesor
    observacion = ObservationModel.get_by_id(obs_id)
    if not observacion or observacion['id_profesor'] != session['id']:
        flash('Observación no encontrada o sin permisos.', 'danger')
        return redirect(url_for('obs_bp.listar_observaciones_profesor'))
    
    # Obtener archivos multimedia
    archivos = MultimediaService.get_multimedia_by_observation(obs_id)
    
    return render_template('profesor/multimedia_lista.html', 
                         observacion=observacion, 
                         archivos=archivos)

@obs_bp.route('/profesor/observaciones/<int:obs_id>/multimedia/subir', methods=['POST'])
@login_required
@role_required([PROF_ROLE_ID])
def subir_multimedia(obs_id):
    """Subir archivos multimedia a una observación."""
    from ..models.observation_model import ObservationModel
    
    # Verificar que la observación existe y pertenece al profesor
    observacion = ObservationModel.get_by_id(obs_id)
    if not observacion or observacion['id_profesor'] != session['id']:
        flash('Observación no encontrada o sin permisos.', 'danger')
        return redirect(url_for('obs_bp.listar_observaciones_profesor'))
    
    # Verificar que se enviaron archivos
    if 'files' not in request.files:
        flash('No se enviaron archivos.', 'warning')
        return redirect(url_for('obs_bp.ver_multimedia_observacion', obs_id=obs_id))
    
    files = request.files.getlist('files')
    
    # Validar la solicitud
    is_valid, message = MultimediaService.validate_upload_request(files, obs_id)
    if not is_valid:
        flash(message, 'danger')
        return redirect(url_for('obs_bp.ver_multimedia_observacion', obs_id=obs_id))
    
    # Procesar cada archivo
    uploaded_count = 0
    errors = []
    
    for file in files:
        if file.filename == '':
            continue
            
        success, result = MultimediaService.save_file(file, obs_id, session['id'])
        if success:
            uploaded_count += 1
        else:
            errors.append(f"{file.filename}: {result}")
    
    # Mostrar resultados
    if uploaded_count > 0:
        flash(f'Se subieron {uploaded_count} archivo(s) exitosamente.', 'success')
    
    if errors:
        for error in errors:
            flash(error, 'warning')
    
    return redirect(url_for('obs_bp.ver_multimedia_observacion', obs_id=obs_id))

@obs_bp.route('/multimedia/<int:multimedia_id>/eliminar', methods=['POST'])
@login_required
@role_required([PROF_ROLE_ID])
def eliminar_multimedia(multimedia_id):
    """Eliminar un archivo multimedia."""
    success, message = MultimediaService.delete_file(multimedia_id, session['id'])
    
    if success:
        flash(message, 'success')
    else:
        flash(message, 'danger')
    
    # Redirigir de vuelta a la observación
    obs_id = request.form.get('obs_id')
    if obs_id:
        return redirect(url_for('obs_bp.ver_multimedia_observacion', obs_id=obs_id))
    else:
        return redirect(url_for('obs_bp.listar_observaciones_profesor'))

@obs_bp.route('/uploads/<path:filename>')
def uploaded_file(filename):
    """Servir archivos multimedia subidos."""
    try:
        # Obtener la ruta del proyecto
        project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
        upload_folder = os.path.join(project_root, 'uploads')
        file_path = os.path.join(upload_folder, filename)
        
        # Verificar que el archivo existe
        if not os.path.exists(file_path):
            flash('Archivo no encontrado.', 'danger')
            return redirect(url_for('obs_bp.listar_observaciones_profesor'))
        
        return send_file(file_path)
    except Exception as e:
        print(f"Error al servir archivo: {e}")
        flash('Error al acceder al archivo.', 'danger')
        return redirect(url_for('obs_bp.listar_observaciones_profesor'))

# ----------------- ACUDIENTE - DESCARGA DE MULTIMEDIA -----------------

@obs_bp.route('/acudiente/estudiante/<int:student_id>/multimedia')
@login_required
@role_required([ACUD_ROLE_ID])
def ver_multimedia_estudiante(student_id):
    """Ver archivos multimedia de un estudiante (para acudientes)."""
    from ..models.student_model import StudentModel
    
    # Verificar que el estudiante pertenece al acudiente
    estudiante = StudentModel.get_student_by_id(student_id)
    if not estudiante or estudiante['acudiente_id'] != session['id']:
        flash('Estudiante no encontrado o sin permisos.', 'danger')
        return redirect(url_for('obs_bp.listar_observaciones_acudiente'))
    
    # Obtener archivos multimedia del estudiante
    archivos = MultimediaService.get_multimedia_by_student(student_id)
    
    return render_template('acudiente/multimedia_lista.html', 
                         estudiante=estudiante, 
                         archivos=archivos)

@obs_bp.route('/acudiente/multimedia/<int:multimedia_id>/descargar')
@login_required
@role_required([ACUD_ROLE_ID])
def descargar_multimedia(multimedia_id):
    """Descargar un archivo multimedia (para acudientes)."""
    from ..models.multimedia_model import MultimediaModel
    from ..models.student_model import StudentModel
    
    # Obtener información del archivo
    archivo = MultimediaModel.get_multimedia_by_id(multimedia_id)
    if not archivo:
        flash('Archivo no encontrado.', 'danger')
        return redirect(url_for('obs_bp.listar_observaciones_acudiente'))
    
    # Verificar permisos: el archivo debe pertenecer a una observación de un estudiante del acudiente
    try:
        from ..models.observation_model import ObservationModel
        observacion = ObservationModel.get_by_id(archivo['observation_id'])
        if not observacion:
            flash('Observación no encontrada.', 'danger')
            return redirect(url_for('obs_bp.listar_observaciones_acudiente'))
        
        estudiante = StudentModel.get_student_by_id(observacion['id_estudiante'])
        if not estudiante or estudiante['acudiente_id'] != session['id']:
            flash('Sin permisos para descargar este archivo.', 'danger')
            return redirect(url_for('obs_bp.listar_observaciones_acudiente'))
        
        # Servir el archivo para descarga
        project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
        file_path = os.path.join(project_root, archivo['file_path'])
        
        if not os.path.exists(file_path):
            flash('Archivo físico no encontrado.', 'danger')
            return redirect(url_for('obs_bp.listar_observaciones_acudiente'))
        
        return send_file(file_path, as_attachment=True, download_name=archivo['filename'])
        
    except Exception as e:
        print(f"Error al descargar archivo: {e}")
        flash('Error al descargar archivo.', 'danger')
        return redirect(url_for('obs_bp.listar_observaciones_acudiente'))

# ----------------- API ENDPOINTS -----------------

@obs_bp.route('/api/observaciones/<int:obs_id>/multimedia', methods=['GET'])
@login_required
def api_get_multimedia(obs_id):
    """API para obtener archivos multimedia de una observación."""
    try:
        archivos = MultimediaService.get_multimedia_by_observation(obs_id)
        return jsonify({
            'success': True,
            'data': archivos
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@obs_bp.route('/api/multimedia/<int:multimedia_id>', methods=['DELETE'])
@login_required
@role_required([PROF_ROLE_ID])
def api_delete_multimedia(multimedia_id):
    """API para eliminar un archivo multimedia."""
    try:
        success, message = MultimediaService.delete_file(multimedia_id, session['id'])
        return jsonify({
            'success': success,
            'message': message
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

# ----------------- VISUALIZACIONES DE OBSERVACIONES -----------------

@obs_bp.route('/api/observacion/<int:observation_id>/marcar-vista', methods=['POST'])
@login_required
@role_required([ACUD_ROLE_ID])
def mark_observation_as_viewed(observation_id):
    """Marca una observación como vista por el acudiente."""
    try:
        acudiente_id = session.get('id')
        ip_address = request.environ.get('HTTP_X_FORWARDED_FOR', request.environ.get('REMOTE_ADDR'))
        user_agent = request.headers.get('User-Agent')
        
        success = ObservationViewModel.mark_as_viewed(
            observation_id=observation_id,
            acudiente_id=acudiente_id,
            ip_address=ip_address,
            user_agent=user_agent
        )
        
        if success:
            return jsonify({
                'success': True,
                'message': 'Observación marcada como vista'
            })
        else:
            return jsonify({
                'success': False,
                'error': 'No se pudo marcar la observación como vista'
            }), 500
            
    except Exception as e:
        print(f"Error al marcar observación como vista: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@obs_bp.route('/api/observaciones/marcar-vistas', methods=['POST'])
@login_required
@role_required([ACUD_ROLE_ID])
def bulk_mark_observations_as_viewed():
    """Marca múltiples observaciones como vistas."""
    try:
        data = request.get_json()
        observation_ids = data.get('observation_ids', [])
        
        if not observation_ids:
            return jsonify({
                'success': False,
                'error': 'No se proporcionaron IDs de observaciones'
            }), 400
        
        acudiente_id = session.get('id')
        ip_address = request.environ.get('HTTP_X_FORWARDED_FOR', request.environ.get('REMOTE_ADDR'))
        user_agent = request.headers.get('User-Agent')
        
        success = ObservationViewModel.bulk_mark_as_viewed(
            observation_ids=observation_ids,
            acudiente_id=acudiente_id,
            ip_address=ip_address,
            user_agent=user_agent
        )
        
        if success:
            return jsonify({
                'success': True,
                'message': f'{len(observation_ids)} observaciones marcadas como vistas'
            })
        else:
            return jsonify({
                'success': False,
                'error': 'No se pudieron marcar las observaciones como vistas'
            }), 500
            
    except Exception as e:
        print(f"Error al marcar observaciones como vistas: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@obs_bp.route('/api/observaciones/estadisticas-vistas')
@login_required
@role_required([ACUD_ROLE_ID])
def get_view_statistics():
    """Obtiene estadísticas de visualización para el acudiente."""
    try:
        acudiente_id = session.get('id')
        stats = ObservationViewModel.get_view_statistics_for_acudiente(acudiente_id)
        
        return jsonify({
            'success': True,
            'data': stats
        })
        
    except Exception as e:
        print(f"Error al obtener estadísticas de visualización: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@obs_bp.route('/api/observaciones/no-vistas')
@login_required
@role_required([ACUD_ROLE_ID])
def get_unviewed_observations():
    """Obtiene las observaciones no vistas por el acudiente."""
    try:
        acudiente_id = session.get('id')
        unviewed = ObservationViewModel.get_unviewed_observations_for_acudiente(acudiente_id)
        
        return jsonify({
            'success': True,
            'data': unviewed
        })
        
    except Exception as e:
        print(f"Error al obtener observaciones no vistas: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@obs_bp.route('/api/observaciones/vistas-recientes')
@login_required
@role_required([ACUD_ROLE_ID])
def get_recent_views():
    """Obtiene las visualizaciones más recientes del acudiente."""
    try:
        acudiente_id = session.get('id')
        limit = request.args.get('limit', 10, type=int)
        
        recent_views = ObservationViewModel.get_recent_views_for_acudiente(acudiente_id, limit)
        
        return jsonify({
            'success': True,
            'data': recent_views
        })
        
    except Exception as e:
        print(f"Error al obtener visualizaciones recientes: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500
