# backend/src/routes/admin_routes.py

from flask import Blueprint, render_template, request, flash, redirect, url_for, session, jsonify
from ..utils.decorators import role_required, login_required
from ..services.user_service import UserService
from ..services.user_audit_log_service import UserAuditLogService
from ..models.user_model import UserModel
from ..services.session_log_service import SessionLogService
from ..services.notification_service import NotificationService 
import jinja2
 

admin_bp = Blueprint('admin_bp', __name__, template_folder='administrador')


@admin_bp.route('/sesiones')
@role_required([1])
def ver_sesiones():
    logs = SessionLogService.get_all_logs()
    return render_template('administrador/admin_session_logs.html', logs=logs)


@admin_bp.route('/')
@role_required([1])
def admin():
    """
    Ruta para el panel de administrador con estadísticas completas.
    Requiere que el usuario tenga el rol de Administrador (ID 1).
    """
    try:
        # Obtener estadísticas de usuarios
        total_users = UserModel.get_total_users_count()
        
        # Obtener estadísticas de sesiones
        session_stats = SessionLogService.get_session_statistics()
        active_sessions = session_stats.get('active_sessions', 0)
        
        # Obtener estadísticas de observaciones (si existe el modelo)
        total_observations = 0
        try:
            from ..models.observation_model import ObservationModel
            total_observations = ObservationModel.get_total_count()
        except ImportError:
            total_observations = 0
        
        # Calcular actividad del sistema (basado en sesiones activas y usuarios)
        if total_users > 0:
            system_activity = min(100, int((active_sessions / max(total_users * 0.1, 1)) * 100))
        else:
            system_activity = 95
        
        # Obtener actividad reciente de auditoría
        recent_activity = UserAuditLogService.get_recent_activity(limit=5)
        
        return render_template('administrador/admin.html',
                             total_users=total_users,
                             active_sessions=active_sessions,
                             total_observations=total_observations,
                             system_activity=system_activity,
                             recent_activity=recent_activity)
    except Exception as e:
        # En caso de error, mostrar valores por defecto
        return render_template('administrador/admin.html',
                             total_users=0,
                             active_sessions=0,
                             total_observations=0,
                             system_activity=95,
                             recent_activity=[])

@admin_bp.route('/api/dashboard-stats')
@role_required([1])
def get_dashboard_stats():
    """API endpoint para obtener estadísticas del dashboard en tiempo real."""
    try:
        # Obtener estadísticas actualizadas
        total_users = UserModel.get_total_users_count()
        session_stats = SessionLogService.get_session_statistics()
        active_sessions = session_stats.get('active_sessions', 0)
        
        # Obtener estadísticas de observaciones
        total_observations = 0
        try:
            from ..models.observation_model import ObservationModel
            total_observations = ObservationModel.get_total_count()
        except ImportError:
            total_observations = 0
        
        # Calcular actividad del sistema
        if total_users > 0:
            system_activity = min(100, int((active_sessions / max(total_users * 0.1, 1)) * 100))
        else:
            system_activity = 95
        
        return jsonify({
            'success': True,
            'data': {
                'total_users': total_users,
                'active_sessions': active_sessions,
                'total_observations': total_observations,
                'system_activity': system_activity,
                'today_sessions': session_stats.get('today_sessions', 0),
                'unique_users_today': session_stats.get('unique_users_today', 0)
            }
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@admin_bp.route('/api/recent-activity')
@role_required([1])
def get_recent_activity():
    """API endpoint para obtener actividad reciente."""
    try:
        recent_activity = UserAuditLogService.get_recent_activity(limit=5)
        return jsonify({
            'success': True,
            'data': recent_activity
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@admin_bp.route('/api/notifications')
@role_required([1])
def get_notifications():
    """API endpoint para obtener notificaciones del dashboard."""
    try:
        notifications_data = NotificationService.get_dashboard_notifications()
        return jsonify({
            'success': True,
            'data': notifications_data
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@admin_bp.route('/api/notifications/<int:notification_id>/read', methods=['POST'])
@role_required([1])
def mark_notification_read(notification_id):
    """API endpoint para marcar una notificación como leída."""
    try:
        success = NotificationService.mark_as_read(notification_id)
        return jsonify({
            'success': success,
            'message': 'Notificación marcada como leída' if success else 'Error al marcar notificación'
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@admin_bp.route('/api/notifications/mark-all-read', methods=['POST'])
@role_required([1])
def mark_all_notifications_read():
    """API endpoint para marcar todas las notificaciones como leídas."""
    try:
        success = NotificationService.mark_all_as_read()
        return jsonify({
            'success': success,
            'message': 'Todas las notificaciones marcadas como leídas' if success else 'Error al marcar notificaciones'
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@admin_bp.route('/crear-usuario', methods=['GET', 'POST'])
@role_required([1])
def crear_usuario_admin():
    """
    Ruta para crear un nuevo usuario desde el panel de administrador.
    Permite tanto mostrar el formulario (GET) como procesar la creación (POST).
    Requiere que el usuario tenga el rol de Administrador (ID 1).
    """
    if request.method == 'POST':
        nombre = request.form.get('nombre')
        apellido = request.form.get('apellido')
        correo = request.form.get('correo')
        password = request.form.get('contrasena')
        id_rol = request.form.get('id_rol')
        tipo_documento = request.form.get('tipo_documento', '').strip()
        numero_documento = request.form.get('numero_documento', '').strip()
        # is_active se establecerá a True por defecto en UserService, no es necesario pedirlo aquí en la creación inicial.

        if not nombre or not apellido or not correo or not password or not id_rol:
            flash('Todos los campos obligatorios (nombre, apellido, correo, contraseña, rol).', 'danger')
            return render_template('administrador/admin_crear_usuario.html')

        # Procesar documento según el tipo seleccionado
        cedula = None
        ppt = None
        
        if tipo_documento and numero_documento:
            import re
            
            if tipo_documento == 'cedula':
                if not re.match(r'^[0-9]{6,10}$', numero_documento):
                    flash('La cédula debe tener entre 6 y 10 números.', 'danger')
                    return render_template('administrador/admin_crear_usuario.html')
                
                # Verificar que la cédula no esté en uso
                existing_user = UserModel.find_by_cedula(numero_documento)
                if existing_user:
                    flash('Ya existe un usuario con esta cédula.', 'warning')
                    return render_template('administrador/admin_crear_usuario.html')
                
                cedula = numero_documento
                
            elif tipo_documento == 'ppt':
                if not re.match(r'^PPT[0-9]{9,12}$', numero_documento.upper()):
                    flash('El PPT debe tener el formato PPT seguido de 9-12 números.', 'danger')
                    return render_template('administrador/admin_crear_usuario.html')
                
                # Verificar que el PPT no esté en uso
                existing_user = UserModel.find_by_ppt(numero_documento.upper())
                if existing_user:
                    flash('Ya existe un usuario con este PPT.', 'warning')
                    return render_template('administrador/admin_crear_usuario.html')
                
                ppt = numero_documento.upper()

        try:
            id_rol = int(id_rol)
        except ValueError:
            flash('El rol seleccionado no es válido.', 'danger')
            return render_template('administrador/admin_crear_usuario.html')

        if UserService.create_new_user_with_documents(correo, password, id_rol, nombre=nombre, apellido=apellido, cedula=cedula, ppt=ppt):
            # Auditoría
            admin_id = session.get('id')
            new_user = UserModel.find_by_email(correo)
            if new_user:
                UserAuditLogService.log(admin_id, new_user['id'], 'crear', 'Usuario creado')
            flash('Usuario creado exitosamente.', 'success')
            return redirect(url_for('admin_bp.ver_usuarios_admin')) # Redirige a ver usuarios para que vean el nuevo
        else:
            flash('Ya existe un usuario con este correo electrónico.', 'warning')
            return render_template('administrador/admin_crear_usuario.html')

    return render_template('administrador/admin_crear_usuario.html')


@admin_bp.route('/usuarios/restablecer/<int:user_id>', methods=['POST'])
@role_required([1])
def restablecer_contrasena_admin(user_id):
    """Permite al administrador restablecer la contraseña de un usuario y genera una nueva temporal."""
    success, temp_pass = UserService.reset_password(user_id)
    if success:
        admin_id = session.get('id')
        UserAuditLogService.log(admin_id, user_id, 'restablecer', 'Contraseña restablecida')
        flash(f'Contraseña restablecida. Nueva contraseña temporal: <strong>{temp_pass}</strong>', 'success')
    else:
        flash('No se pudo restablecer la contraseña.', 'danger')
    return redirect(url_for('admin_bp.editar_usuario_admin', user_id=user_id))

@admin_bp.route('/ver-usuarios')
@role_required([1])
def ver_usuarios_admin():
    """
    Ruta para ver todos los usuarios registrados.
    Requiere que el usuario tenga el rol de Administrador (ID 1).
    """
    users = UserService.get_all_users_with_roles()
    return render_template('administrador/admin_ver_usuarios.html', users=users)

@admin_bp.route('/editar-usuario/<int:user_id>', methods=['GET', 'POST'])
@role_required([1])
def editar_usuario_admin(user_id):
    """
    Ruta para editar un usuario existente.
    Permite mostrar el formulario con datos del usuario (GET) y procesar la actualización (POST).
    Requiere que el usuario tenga el rol de Administrador (ID 1).
    """
    user = UserModel.find_by_id(user_id)

    if not user:
        flash('Usuario no encontrado.', 'danger')
        return redirect(url_for('admin_bp.ver_usuarios_admin'))

    if request.method == 'POST':
        nombre = request.form.get('nombre')
        apellido = request.form.get('apellido')
        correo = request.form.get('correo')
        new_password = request.form.get('contrasena')
        id_rol = request.form.get('id_rol')
        is_active_str = request.form.get('is_active')  # Obtener el valor del checkbox/radio
        is_active = True if is_active_str == 'on' else False  # Convertir a booleano
        
        # Manejar documentos
        tipo_documento = request.form.get('tipo_documento', '').strip()
        numero_documento = request.form.get('numero_documento', '').strip()

        if not nombre or not apellido or not correo or not id_rol:
            flash('El correo y el rol son obligatorios.', 'danger')
            # Pasa user_dict para que el formulario se repopule
            user_data_for_template = dict(user) 
            user_data_for_template['is_active'] = is_active # Mantener el estado enviado si hubo error
            return render_template('administrador/admin_editar_usuario.html', user=user_data_for_template)

        # Procesar documento según el tipo seleccionado
        cedula = None
        ppt = None
        
        if tipo_documento and numero_documento:
            import re
            
            if tipo_documento == 'cedula':
                if not re.match(r'^[0-9]{6,10}$', numero_documento):
                    flash('La cédula debe tener entre 6 y 10 números.', 'danger')
                    user_data_for_template = dict(user)
                    user_data_for_template['is_active'] = is_active
                    return render_template('administrador/admin_editar_usuario.html', user=user_data_for_template)
                
                # Verificar que la cédula no esté en uso por otro usuario
                existing_user = UserModel.find_by_cedula(numero_documento)
                if existing_user and existing_user['id'] != user_id:
                    flash('Ya existe otro usuario con esta cédula.', 'warning')
                    user_data_for_template = dict(user)
                    user_data_for_template['is_active'] = is_active
                    return render_template('administrador/admin_editar_usuario.html', user=user_data_for_template)
                
                cedula = numero_documento
                
            elif tipo_documento == 'ppt':
                if not re.match(r'^PPT[0-9]{9,12}$', numero_documento.upper()):
                    flash('El PPT debe tener el formato PPT seguido de 9-12 números.', 'danger')
                    user_data_for_template = dict(user)
                    user_data_for_template['is_active'] = is_active
                    return render_template('administrador/admin_editar_usuario.html', user=user_data_for_template)
                
                # Verificar que el PPT no esté en uso por otro usuario
                existing_user = UserModel.find_by_ppt(numero_documento.upper())
                if existing_user and existing_user['id'] != user_id:
                    flash('Ya existe otro usuario con este PPT.', 'warning')
                    user_data_for_template = dict(user)
                    user_data_for_template['is_active'] = is_active
                    return render_template('administrador/admin_editar_usuario.html', user=user_data_for_template)
                
                ppt = numero_documento.upper()

        try:
            id_rol = int(id_rol)
        except ValueError:
            flash('El rol seleccionado no es válido.', 'danger')
            user_data_for_template = dict(user)
            user_data_for_template['is_active'] = is_active
            return render_template('administrador/admin_editar_usuario.html', user=user_data_for_template)

        # Pasar nombre, apellido, documentos y is_active al servicio de actualización
        if UserService.update_user_with_documents(user_id, correo=correo, new_password=new_password, id_rol=id_rol, nombre=nombre, apellido=apellido, cedula=cedula, ppt=ppt, is_active=is_active):
            # Auditoría
            admin_id = session.get('id')
            UserAuditLogService.log(admin_id, user_id, 'editar', 'Datos del usuario actualizados')
            flash('Usuario actualizado exitosamente.', 'success')
            return redirect(url_for('admin_bp.ver_usuarios_admin'))
        else:
            flash('Error al actualizar usuario o el correo ya existe.', 'warning')
            user_data_for_template = dict(user)
            user_data_for_template['is_active'] = is_active
            return render_template('administrador/admin_editar_usuario.html', user=user_data_for_template)

    # Para la solicitud GET, convertir el objeto user a un diccionario para Jinja y manejar is_active
    user_data_for_template = dict(user)
    # MySQL BOOLEAN se mapea a 0 o 1, Python espera True/False
    user_data_for_template['is_active'] = bool(user_data_for_template['is_active']) 
    return render_template('administrador/admin_editar_usuario.html', user=user_data_for_template)


@admin_bp.route('/auditoria', methods=['GET'])
@role_required([1])
def ver_auditoria():
    """Muestra la bitácora de auditoría con filtros y paginación."""
    import datetime as _dt
    # Parámetros de filtro
    start_date_str = request.args.get('start_date')
    end_date_str = request.args.get('end_date')
    accion = request.args.get('accion') or None
    admin_id = request.args.get('admin_id') or None
    q = request.args.get('q') or None
    page = int(request.args.get('page', 1))
    limit = 25
    offset = (page - 1) * limit

    # Convertir fechas
    start_date = None
    end_date = None
    try:
        if start_date_str:
            start_date = _dt.datetime.strptime(start_date_str, '%Y-%m-%d')
        if end_date_str:
            end_date = _dt.datetime.strptime(end_date_str, '%Y-%m-%d') + _dt.timedelta(days=1)
    except ValueError:
        flash('Formato de fecha inválido.', 'warning')

    # Obtener registros (limit +1 para saber si hay siguiente página)
    logs = UserAuditLogService.get_filtered(start_date, end_date, accion, admin_id, q, offset, limit + 1)
    has_next = len(logs) > limit
    logs = logs[:limit]
    has_prev = page > 1

    # Para selects
    admins = UserAuditLogService.get_admins()
    acciones = ['crear', 'editar', 'eliminar', 'restablecer', 'activar', 'desactivar']
    
    # Obtener logs de hoy
    today = _dt.date.today()
    today_start = _dt.datetime.combine(today, _dt.time.min)
    today_end = _dt.datetime.combine(today, _dt.time.max)
    today_logs = UserAuditLogService.get_filtered(today_start, today_end, None, None, None, 0, 1000)
    today_logs_count = len(today_logs)

    return render_template(
        'administrador/admin_ver_auditoria.html',
        logs=logs,
        admins=admins,
        acciones=acciones,
        today_logs_count=today_logs_count,
        filtros={
            'start_date': start_date_str or '',
            'end_date': end_date_str or '',
            'accion': accion or '',
            'administrador/admin_id': int(admin_id) if admin_id else '',
            'q': q or ''
        },
        paginacion={
            'page': page,
            'has_next': has_next,
            'has_prev': has_prev
        }
    )

@admin_bp.route('/solicitudes-registro')
@role_required([1])
def ver_solicitudes_registro():
    """Placeholder temporal para gestionar solicitudes de registro."""
    # TODO: Implementar lógica real de solicitudes
    return render_template('administrador/admin_solicitudes_registro.html')


@admin_bp.route('/auditoria/export', methods=['GET'])
@role_required([1])
def export_auditoria():
    """Exporta los registros filtrados a CSV."""
    import csv, io, datetime as _dt
    # Reutilizar misma lógica de filtros
    start_date_str = request.args.get('start_date')
    end_date_str = request.args.get('end_date')
    accion = request.args.get('accion') or None
    admin_id = request.args.get('admin_id') or None
    q = request.args.get('q') or None

    start_date = None
    end_date = None
    try:
        if start_date_str:
            start_date = _dt.datetime.strptime(start_date_str, '%Y-%m-%d')
        if end_date_str:
            end_date = _dt.datetime.strptime(end_date_str, '%Y-%m-%d') + _dt.timedelta(days=1)
    except ValueError:
        pass

    logs = UserAuditLogService.get_filtered(start_date, end_date, accion, admin_id, q, 0, 10000)

    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(['Fecha', 'Acción', 'Administrador', 'Usuario', 'Detalles'])
    for log in logs:
        writer.writerow([
            log.get('fecha').strftime('%Y-%m-%d %H:%M:%S') if log.get('fecha') else '',
            log.get('accion'),
            log.get('admin_correo') or '',
            log.get('user_correo') or '',
            log.get('detalles') or ''
        ])
    csv_data = output.getvalue()
    output.close()

    from flask import Response
    resp = Response(csv_data, mimetype='text/csv')
    resp.headers['Content-Disposition'] = 'attachment; filename=audit_logs.csv'
    return resp


@admin_bp.route('/toggle-active/<int:user_id>', methods=['POST'])
@role_required([1])
def toggle_user_active(user_id):
    """
    Ruta para alternar el estado 'activo' de un usuario.
    Requiere que el usuario tenga el rol de Administrador (ID 1).
    """
    user = UserModel.find_by_id(user_id) # Usamos UserModel directamente ya que AuthService no tiene un get_user_by_id
    if not user:
        flash('Usuario no encontrado.', 'danger')
        return redirect(url_for('admin_bp.ver_usuarios_admin'))

    # No permitir que un administrador se desactive a sí mismo (opcional, pero buena práctica)
    # Asumo que 'id' y 'id_rol' están en la sesión y en el diccionario 'user'
    if user['id'] == session.get('id') and user['id_rol'] == 1:
        flash('No puedes desactivar tu propia cuenta de administrador.', 'danger')
        return redirect(url_for('admin_bp.ver_usuarios_admin'))

    # Determinar el nuevo estado
    # MySQL devuelve 0 o 1 para BOOLEAN, convertir a booleano Python
    current_status = bool(user['is_active']) 
    new_status = not current_status

    if UserService.update_user(user_id, is_active=new_status): 
        status_text = "activado" if new_status else "desactivado"
        # Auditoría
        admin_id = session.get('id')
        UserAuditLogService.log(admin_id, user_id, 'editar', f'Usuario {status_text}')
        flash(f'Usuario {user["correo"]} ha sido {status_text} exitosamente.', 'success')
    else:
        flash('Error al actualizar el estado del usuario.', 'danger')

    return redirect(url_for('admin_bp.ver_usuarios_admin'))


@admin_bp.route('/eliminar-usuario/<int:user_id>', methods=['POST'])
@role_required([1])
def eliminar_usuario_admin(user_id):
    """
    Ruta para eliminar un usuario. Solo accesible vía POST para seguridad.
    Requiere que el usuario tenga el rol de Administrador (ID 1).
    """
    # No permitir que un administrador se elimine a sí mismo
    if user_id == session.get('id') and session.get('id_rol') == 1:
        flash('No puedes eliminar tu propia cuenta de administrador.', 'danger')
        return redirect(url_for('admin_bp.ver_usuarios_admin'))

    if UserService.delete_user(user_id):
        # Auditoría
        admin_id = session.get('id')
        UserAuditLogService.log(admin_id, user_id, 'eliminar', 'Usuario eliminado')
        flash('Usuario eliminado exitosamente.', 'success')
    else:
        flash('Error al eliminar usuario.', 'danger')
    return redirect(url_for('admin_bp.ver_usuarios_admin'))

@admin_bp.route('/perfil')
@role_required([1, 2, 3, 4]) # Todos los roles pueden ver su propio perfil
def perfil_usuario():
    """
    Ruta para mostrar el perfil del usuario logeado.
    Obtiene los datos del usuario de la sesión y los pasa a la plantilla.
    """
    user_id = session.get('id')
    user_data = UserModel.find_by_id(user_id)

    if not user_data:
        flash('No se pudieron cargar los datos del perfil.', 'danger')
        return redirect(url_for('main_bp.home'))

    user_data_dict = dict(user_data)
    user_data_dict['rol_nombre'] = UserModel.get_rol_name(user_data_dict['id_rol'])
    # Asegúrate de que is_active se pasa como booleano para la plantilla
    user_data_dict['is_active'] = bool(user_data_dict['is_active'])

    # Obtener estadísticas adicionales para el perfil mejorado
    try:
        from datetime import datetime, timedelta
        
        # Estadísticas de sesiones
        session_stats = SessionLogService.get_user_session_stats(user_id)
        total_logins = session_stats.get('total_sessions', 0) if session_stats else 0
        active_sessions = session_stats.get('active_sessions', 0) if session_stats else 0
        last_login = session_stats.get('last_login', 'No disponible') if session_stats else 'No disponible'
        
        # Calcular horas desde el último login
        hours_since_login = 0
        if last_login and last_login != 'No disponible':
            try:
                if isinstance(last_login, str):
                    last_login_dt = datetime.strptime(last_login, '%Y-%m-%d %H:%M:%S')
                else:
                    last_login_dt = last_login
                hours_since_login = int((datetime.now() - last_login_dt).total_seconds() / 3600)
            except:
                hours_since_login = 0
        
        # Estadísticas de usuarios (solo para administradores)
        total_users = 0
        users_created = 0
        total_modifications = 0
        if user_data_dict['id_rol'] == 1:  # Solo administradores
            total_users = UserModel.get_total_users_count()
            users_created = UserAuditLogService.get_users_created_by_admin(user_id)
            total_modifications = UserAuditLogService.get_total_modifications_by_admin(user_id)
        
        # Calcular días como administrador/usuario
        creation_date = user_data_dict.get('fecha_creacion', datetime.now())
        if isinstance(creation_date, str):
            try:
                creation_date = datetime.strptime(creation_date, '%Y-%m-%d %H:%M:%S')
            except:
                creation_date = datetime.now()
        days_since_creation = (datetime.now() - creation_date).days
        
        # Días activo (aproximado basado en sesiones)
        days_active = min(days_since_creation, total_logins)
        
        # Observaciones revisadas (placeholder)
        observations_reviewed = 0
        
        # Actividad reciente
        last_user_edit = 'No hay modificaciones recientes'
        last_edit_time = 'N/A'
        last_config_update = 'N/A'
        
        # Agregar todas las estadísticas al contexto
        context_data = {
            'user': user_data_dict,
            'total_logins': total_logins,
            'active_sessions': active_sessions,
            'last_login': last_login,
            'hours_since_login': hours_since_login,
            'total_users': total_users,
            'users_created': users_created,
            'total_modifications': total_modifications,
            'days_since_creation': days_since_creation,
            'days_active': days_active,
            'observations_reviewed': observations_reviewed,
            'last_user_edit': last_user_edit,
            'last_edit_time': last_edit_time,
            'last_config_update': last_config_update
        }
        
    except Exception as e:
        # Si hay algún error, usar valores por defecto
        context_data = {
            'user': user_data_dict,
            'total_logins': 0,
            'active_sessions': 0,
            'last_login': 'No disponible',
            'hours_since_login': 0,
            'total_users': 0,
            'users_created': 0,
            'total_modifications': 0,
            'days_since_creation': 0,
            'days_active': 0,
            'observations_reviewed': 0,
            'last_user_edit': 'No hay modificaciones recientes',
            'last_edit_time': 'N/A',
            'last_config_update': 'N/A'
        }

    return render_template('administrador/admin_perfil_usuario.html', **context_data)


# =======================================
# GESTIÓN DE ESTUDIANTES (MOVIDO DESDE PROFESOR)
# =======================================

@admin_bp.route('/test-estudiantes')
def test_estudiantes():
    """Ruta de prueba SIN DECORADORES para verificar que funciona"""
    return "<h1>¡Funciona! Las rutas de estudiantes están activas.</h1><p><a href='/admin/estudiantes'>Ir a lista de estudiantes</a></p><p>Session: " + str(session) + "</p>"

@admin_bp.route('/test-simple')
def test_simple():
    """Ruta de prueba súper simple"""
    return "<h1>RUTA SIMPLE FUNCIONA</h1>"

@admin_bp.route('/estudiantes')
@login_required
@role_required([1])  # Solo administrador
def listar_estudiantes():
    """Lista todos los estudiantes del sistema con filtros"""
    try:
        from ..models.student_model import StudentModel
        from ..services.user_service import UserService
        
        # Obtener parámetros de filtro
        grado = request.args.get('grado')
        profesor_id = request.args.get('profesor_id')
        condicion = request.args.get('condicion')
        acudiente = request.args.get('acudiente')
        buscar = request.args.get('buscar')
        
        # El administrador puede ver TODOS los estudiantes
        estudiantes = StudentModel.get_all_students()
        
        # Aplicar filtros
        if estudiantes:
            # Filtro por grado
            if grado:
                estudiantes = [e for e in estudiantes if e.get('grado') == grado]
            
            # Filtro por profesor
            if profesor_id:
                try:
                    profesor_id = int(profesor_id)
                    estudiantes = [e for e in estudiantes if e.get('profesor_id') == profesor_id]
                except (ValueError, TypeError):
                    pass
            
            # Filtro por condición especial
            if condicion:
                if condicion == 'N/A':
                    estudiantes = [e for e in estudiantes if not e.get('condicion_especiales') or 'N/A' in str(e.get('condicion_especiales', ''))]
                else:
                    estudiantes = [e for e in estudiantes if e.get('condicion_especiales') and condicion in str(e.get('condicion_especiales', ''))]
            
            # Filtro por estado de acudiente
            if acudiente:
                if acudiente == 'con_acudiente':
                    estudiantes = [e for e in estudiantes if e.get('acudiente_id')]
                elif acudiente == 'sin_acudiente':
                    estudiantes = [e for e in estudiantes if not e.get('acudiente_id')]
            
            # Filtro por búsqueda de nombre
            if buscar:
                buscar_lower = buscar.lower()
                estudiantes = [e for e in estudiantes if 
                             buscar_lower in str(e.get('nombre', '')).lower() or 
                             buscar_lower in str(e.get('apellido', '')).lower()]
        
        # Obtener lista de profesores para el filtro
        profesores = UserService.get_users_by_role(2)  # Rol profesor = 2
        
        return render_template('administrador/admin_estudiantes_lista.html', 
                             estudiantes=estudiantes, profesores=profesores)
    except Exception as e:
        flash(f'Error al cargar estudiantes: {str(e)}', 'danger')
        return redirect(url_for('admin_bp.admin'))


@admin_bp.route('/estudiantes/nuevo', methods=['GET', 'POST'])
@login_required
@role_required([1])  # Solo administrador
def crear_estudiante():
    """Crear un nuevo estudiante - Solo administrador"""
    from ..models.student_model import StudentModel
    from ..services.user_service import UserService
    
    if request.method == 'POST':
        nombre = request.form.get('nombre')
        apellido = request.form.get('apellido')
        fecha_nacimiento = request.form.get('fecha_nacimiento')
        grado = request.form.get('grado')
        profesor_id = request.form.get('profesor_id')  # El admin asigna el profesor
        fecha_matricula = request.form.get('fecha_matricula')
        eps = request.form.get('eps')
        
        # Procesar condiciones especiales (checkboxes)
        condiciones_seleccionadas = request.form.getlist('condiciones[]')
        otra_condicion = request.form.get('otra_condicion')
        
        # Combinar condiciones seleccionadas y otra condición
        condiciones_finales = []
        if condiciones_seleccionadas:
            condiciones_finales.extend(condiciones_seleccionadas)
        if otra_condicion and otra_condicion.strip():
            condiciones_finales.append(f"Otra: {otra_condicion.strip()}")
        
        condicion_especiales = "; ".join(condiciones_finales) if condiciones_finales else None
        
        if not all([nombre, apellido, fecha_nacimiento, grado, profesor_id, fecha_matricula]):
            flash('Los campos obligatorios deben ser completados.', 'danger')
            profesores = UserService.get_users_by_role(2)  # Rol profesor = 2
            return render_template('administrador/admin_estudiante_form_clean.html', 
                                 modo='crear', profesores=profesores)
        
        student_id = StudentModel.create_student(
            nombre=nombre,
            apellido=apellido,
            fecha_nacimiento=fecha_nacimiento,
            grado=grado,
            profesor_id=profesor_id,
            fecha_matricula=fecha_matricula,
            eps=eps if eps else None,
            condicion_especiales=condicion_especiales if condicion_especiales else None
        )
        
        if student_id:
            flash(f'Estudiante {nombre} {apellido} creado exitosamente.', 'success')
            return redirect(url_for('admin_bp.listar_estudiantes'))
        else:
            flash('Error al crear el estudiante.', 'danger')
    
    # Obtener lista de profesores para el formulario
    profesores = UserService.get_users_by_role(2)  # Rol profesor = 2
    return render_template('administrador/admin_estudiante_form_clean.html', 
                         modo='crear', profesores=profesores)


@admin_bp.route('/estudiantes/<int:student_id>/editar', methods=['GET', 'POST'])
@login_required
@role_required([1])  # Solo administrador
def editar_estudiante(student_id):
    """Editar estudiante - Solo administrador"""
    from ..models.student_model import StudentModel
    from ..services.user_service import UserService
    
    # El administrador puede editar cualquier estudiante
    student = StudentModel.get_student_by_id(student_id)
    if not student:
        flash('Estudiante no encontrado.', 'danger')
        return redirect(url_for('admin_bp.listar_estudiantes'))
    
    if request.method == 'POST':
        nombre = request.form.get('nombre')
        apellido = request.form.get('apellido')
        fecha_nacimiento = request.form.get('fecha_nacimiento')
        grado = request.form.get('grado')
        profesor_id = request.form.get('profesor_id')
        fecha_matricula = request.form.get('fecha_matricula')
        eps = request.form.get('eps')
        
        # Procesar condiciones especiales (checkboxes)
        condiciones_seleccionadas = request.form.getlist('condiciones[]')
        otra_condicion = request.form.get('otra_condicion')
        
        # Combinar condiciones seleccionadas y otra condición
        condiciones_finales = []
        if condiciones_seleccionadas:
            condiciones_finales.extend(condiciones_seleccionadas)
        if otra_condicion and otra_condicion.strip():
            condiciones_finales.append(f"Otra: {otra_condicion.strip()}")
        
        condicion_especiales = "; ".join(condiciones_finales) if condiciones_finales else None
        
        if not all([nombre, apellido, fecha_nacimiento, grado, profesor_id, fecha_matricula]):
            flash('Los campos obligatorios deben ser completados.', 'danger')
            profesores = UserService.get_users_by_role(2)
            return render_template('administrador/admin_estudiante_form_clean.html', 
                                 modo='editar', estudiante=student, profesores=profesores)
        
        success = StudentModel.update_student(
            student_id=student_id,
            nombre=nombre,
            apellido=apellido,
            fecha_nacimiento=fecha_nacimiento,
            grado=grado,
            profesor_id=profesor_id,
            fecha_matricula=fecha_matricula,
            eps=eps if eps else None,
            condicion_especiales=condicion_especiales if condicion_especiales else None
        )
        
        if success:
            flash(f'Estudiante {nombre} {apellido} actualizado exitosamente.', 'success')
            return redirect(url_for('admin_bp.listar_estudiantes'))
        else:
            flash('Error al actualizar el estudiante.', 'danger')
    
    profesores = UserService.get_users_by_role(2)
    return render_template('administrador/admin_estudiante_form_clean.html', 
                         modo='editar', estudiante=student, profesores=profesores)


@admin_bp.route('/estudiantes/<int:student_id>/eliminar', methods=['POST'])
@login_required
@role_required([1])  # Solo administrador
def eliminar_estudiante(student_id):
    """Eliminar estudiante - Solo administrador"""
    from ..models.student_model import StudentModel
    
    student = StudentModel.get_student_by_id(student_id)
    if not student:
        flash('Estudiante no encontrado.', 'danger')
        return redirect(url_for('admin_bp.listar_estudiantes'))
    
    success = StudentModel.delete_student(student_id)
    
    if success:
        flash(f'Estudiante {student["nombre"]} {student["apellido"]} eliminado exitosamente.', 'success')
    else:
        flash('Error al eliminar el estudiante.', 'danger')
    
    return redirect(url_for('admin_bp.listar_estudiantes'))


@admin_bp.route('/estudiantes/<int:student_id>/asignar-acudiente', methods=['GET', 'POST'])
@login_required
@role_required([1])  # Solo administrador
def asignar_acudiente_estudiante(student_id):
    """Asignar acudiente a estudiante - Solo administrador"""
    from ..models.student_model import StudentModel
    from ..services.user_service import UserService
    
    student = StudentModel.get_student_by_id(student_id)
    if not student:
        flash('Estudiante no encontrado.', 'danger')
        return redirect(url_for('admin_bp.listar_estudiantes'))
    
    if request.method == 'POST':
        acudiente_id = request.form.get('acudiente_id')
        
        if not acudiente_id:
            flash('Debe seleccionar un acudiente.', 'danger')
        else:
            success = StudentModel.assign_acudiente(student_id, acudiente_id)
            
            if success:
                flash(f'Acudiente asignado exitosamente a {student["nombre"]} {student["apellido"]}.', 'success')
                return redirect(url_for('admin_bp.listar_estudiantes'))
            else:
                flash('Error al asignar el acudiente.', 'danger')
    
    # Obtener todos los acudientes disponibles
    acudientes = UserService.get_all_acudientes()
    
    return render_template('administrador/admin_asignar_acudiente.html', 
                         estudiante=student, 
                         acudientes=acudientes)

# ----------------- GESTIÓN DE ENLACES Y VINCULACIONES -----------------

@admin_bp.route('/enlaces')
@login_required
@role_required([1])  # Solo administrador
def gestionar_enlaces():
    """Panel de gestión de enlaces entre usuarios y estudiantes."""
    from ..models.student_model import StudentModel
    from ..services.user_service import UserService
    
    # Obtener todos los estudiantes con información de sus enlaces
    estudiantes = StudentModel.get_all_students()
    
    # Obtener profesores y acudientes para los selectores
    profesores = UserService.get_users_by_role(2)  # Profesores
    acudientes = UserService.get_all_acudientes()  # Acudientes
    
    # Estadísticas de enlaces
    estudiantes_sin_profesor = len([e for e in estudiantes if not e.get('profesor_id')])
    estudiantes_sin_acudiente = len([e for e in estudiantes if not e.get('acudiente_id')])
    
    return render_template('administrador/admin_enlaces.html',
                         estudiantes=estudiantes,
                         profesores=profesores,
                         acudientes=acudientes,
                         estudiantes_sin_profesor=estudiantes_sin_profesor,
                         estudiantes_sin_acudiente=estudiantes_sin_acudiente)

@admin_bp.route('/enlaces/estudiante/<int:student_id>/profesor', methods=['POST'])
@login_required
@role_required([1])  # Solo administrador
def cambiar_profesor_estudiante(student_id):
    """Cambiar el profesor asignado a un estudiante."""
    from ..models.student_model import StudentModel
    
    nuevo_profesor_id = request.form.get('profesor_id')
    
    if not nuevo_profesor_id:
        flash('Debe seleccionar un profesor.', 'danger')
        return redirect(url_for('admin_bp.gestionar_enlaces'))
    
    try:
        nuevo_profesor_id = int(nuevo_profesor_id)
    except ValueError:
        flash('ID de profesor inválido.', 'danger')
        return redirect(url_for('admin_bp.gestionar_enlaces'))
    
    success = StudentModel.update_student(student_id, profesor_id=nuevo_profesor_id)
    
    if success:
        flash('Profesor asignado exitosamente.', 'success')
    else:
        flash('Error al asignar el profesor.', 'danger')
    
    return redirect(url_for('admin_bp.gestionar_enlaces'))

@admin_bp.route('/enlaces/estudiante/<int:student_id>/acudiente', methods=['POST'])
@login_required
@role_required([1])  # Solo administrador
def cambiar_acudiente_estudiante(student_id):
    """Cambiar el acudiente asignado a un estudiante."""
    from ..models.student_model import StudentModel
    
    nuevo_acudiente_id = request.form.get('acudiente_id')
    
    if nuevo_acudiente_id == '':
        # Permitir remover acudiente
        nuevo_acudiente_id = None
    elif nuevo_acudiente_id:
        try:
            nuevo_acudiente_id = int(nuevo_acudiente_id)
        except ValueError:
            flash('ID de acudiente inválido.', 'danger')
            return redirect(url_for('admin_bp.gestionar_enlaces'))
    
    success = StudentModel.update_student(student_id, acudiente_id=nuevo_acudiente_id)
    
    if success:
        if nuevo_acudiente_id:
            flash('Acudiente asignado exitosamente.', 'success')
        else:
            flash('Acudiente removido exitosamente.', 'success')
    else:
        flash('Error al actualizar el acudiente.', 'danger')
    
    return redirect(url_for('admin_bp.gestionar_enlaces'))

# ----------------- AUDITORÍAS Y SEGUIMIENTO -----------------

@admin_bp.route('/auditoria/completa')
@login_required
@role_required([1])  # Solo administrador
def auditoria_completa():
    """Panel completo de auditoría del sistema."""
    from ..services.user_audit_log_service import UserAuditLogService
    from ..services.session_log_service import SessionLogService
    from ..models.multimedia_model import MultimediaModel
    
    # Obtener estadísticas de auditoría
    recent_activity = UserAuditLogService.get_recent_activity(limit=20)
    session_stats = SessionLogService.get_session_statistics()
    multimedia_stats = MultimediaModel.get_multimedia_stats()
    
    # Estadísticas adicionales
    total_multimedia = MultimediaModel.get_total_multimedia_count()
    
    return render_template('administrador/admin_auditoria_completa.html',
                         recent_activity=recent_activity,
                         session_stats=session_stats,
                         multimedia_stats=multimedia_stats,
                         total_multimedia=total_multimedia)

@admin_bp.route('/auditoria/usuario/<int:user_id>')
@login_required
@role_required([1])  # Solo administrador
def auditoria_usuario(user_id):
    """Auditoría específica de un usuario."""
    from ..services.user_audit_log_service import UserAuditLogService
    from ..models.user_model import UserModel
    
    # Obtener información del usuario
    user = UserModel.find_by_id(user_id)
    if not user:
        flash('Usuario no encontrado.', 'danger')
        return redirect(url_for('admin_bp.ver_usuarios_admin'))
    
    # Obtener logs de auditoría del usuario
    user_logs = UserAuditLogService.get_user_activity(user_id)
    
    return render_template('administrador/admin_auditoria_usuario.html',
                         user=user,
                         user_logs=user_logs)

# ----------------- REPORTES Y ESTADÍSTICAS -----------------

@admin_bp.route('/reportes')
@login_required
@role_required([1])  # Solo administrador
def reportes_sistema():
    """Panel de reportes y estadísticas del sistema."""
    from ..models.student_model import StudentModel
    from ..models.observation_model import ObservationModel
    from ..models.multimedia_model import MultimediaModel
    from ..services.user_service import UserService
    
    # Estadísticas generales
    total_estudiantes = StudentModel.get_total_students_count()
    total_observaciones = ObservationModel.get_total_count()
    total_multimedia = MultimediaModel.get_total_multimedia_count()
    
    # Estadísticas por rol
    total_profesores = len(UserService.get_users_by_role(2))
    total_acudientes = len(UserService.get_all_acudientes())
    
    # Estadísticas de enlaces
    estudiantes = StudentModel.get_all_students()
    estudiantes_con_profesor = len([e for e in estudiantes if e.get('profesor_id')])
    estudiantes_con_acudiente = len([e for e in estudiantes if e.get('acudiente_id')])
    
    # Estadísticas de multimedia
    multimedia_stats = MultimediaModel.get_multimedia_stats()
    
    return render_template('administrador/admin_reportes.html',
                         total_estudiantes=total_estudiantes,
                         total_observaciones=total_observaciones,
                         total_multimedia=total_multimedia,
                         total_profesores=total_profesores,
                         total_acudientes=total_acudientes,
                         estudiantes_con_profesor=estudiantes_con_profesor,
                         estudiantes_con_acudiente=estudiantes_con_acudiente,
                         multimedia_stats=multimedia_stats)

# ----------------- API ENDPOINTS PARA ADMINISTRADOR -----------------

@admin_bp.route('/api/estudiantes/<int:student_id>/enlace', methods=['PUT'])
@login_required
@role_required([1])  # Solo administrador
def api_actualizar_enlace_estudiante(student_id):
    """API para actualizar enlaces de un estudiante."""
    from ..models.student_model import StudentModel
    
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({'success': False, 'error': 'No se enviaron datos'}), 400
        
        # Actualizar profesor si se especifica
        if 'profesor_id' in data:
            profesor_id = data['profesor_id'] if data['profesor_id'] != '' else None
            success = StudentModel.update_student(student_id, profesor_id=profesor_id)
            if not success:
                return jsonify({'success': False, 'error': 'Error al actualizar profesor'}), 500
        
        # Actualizar acudiente si se especifica
        if 'acudiente_id' in data:
            acudiente_id = data['acudiente_id'] if data['acudiente_id'] != '' else None
            success = StudentModel.update_student(student_id, acudiente_id=acudiente_id)
            if not success:
                return jsonify({'success': False, 'error': 'Error al actualizar acudiente'}), 500
        
        return jsonify({'success': True, 'message': 'Enlaces actualizados exitosamente'})
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@admin_bp.route('/api/reportes/datos')
@login_required
@role_required([1])  # Solo administrador
def api_datos_reportes():
    """API para obtener datos de reportes en tiempo real."""
    try:
        from ..models.student_model import StudentModel
        from ..models.observation_model import ObservationModel
        from ..models.multimedia_model import MultimediaModel
        from ..services.user_service import UserService
        
        # Recopilar todas las estadísticas
        data = {
            'estudiantes': {
                'total': StudentModel.get_total_students_count(),
                'por_grado': {}  # Se puede implementar después
            },
            'observaciones': {
                'total': ObservationModel.get_total_count()
            },
            'multimedia': {
                'total': MultimediaModel.get_total_multimedia_count(),
                'stats': MultimediaModel.get_multimedia_stats()
            },
            'usuarios': {
                'profesores': len(UserService.get_users_by_role(2)),
                'acudientes': len(UserService.get_all_acudientes())
            }
        }
        
        return jsonify({'success': True, 'data': data})
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500
