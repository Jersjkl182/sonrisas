from flask import Blueprint, render_template, session, jsonify, redirect, url_for
from ..models.user_model import UserModel
from ..services.multimedia_service import MultimediaService
import jinja2

main_bp = Blueprint('main_bp', __name__)

@main_bp.route('/')
def home():
    return render_template('index.html')

@main_bp.route('/inicio-de-sesion')
def inicio_sesion():
    if 'logueado' in session:
        # Redirect based on role if already logged in
        role_redirect_map = {
            1: 'admin_bp.admin',
            4: 'main_bp.acudiente'
        }
        return redirect(url_for(role_redirect_map.get(session['id_rol'], 'main_bp.home')))
    return render_template('inicio_sesion.html')

@main_bp.route('/inicio de sesion')
def inicio_sesion_old():
    return redirect(url_for('main_bp.inicio_sesion'))


@main_bp.route('/Registrarse')
def registro():
    return render_template('Registro.html')

# Routes for different roles (formerly in app.py, now in main_routes for clarity for non-admin)
@main_bp.route('/acudiente')
def acudiente():
    # Redirigir al dashboard unificado
    return redirect(url_for('main_bp.dashboard_unificado'))

@main_bp.route('/acudiente/dashboard')
def dashboard_unificado():
    """Dashboard unificado del acudiente con selector de hijos"""
    try:
        user_id = session.get('id')
        if not user_id:
            return redirect(url_for('main_bp.inicio_sesion'))
        
        return render_template('acudiente/dashboard_unificado.html')
        
    except Exception as e:
        print(f"Error al cargar dashboard: {e}")
        return redirect(url_for('obs_bp.listar_observaciones_acudiente'))

@main_bp.route('/acudiente/api/hijos')
def obtener_hijos_acudiente():
    """API para obtener la lista de hijos del acudiente logueado"""
    try:
        user_id = session.get('id')
        if not user_id:
            return jsonify({'error': 'No autorizado'}), 401
        
        from ..models.student_model import StudentModel
        
        # Obtener estudiantes reales de la base de datos
        estudiantes = StudentModel.get_students_by_acudiente(user_id)
        
        hijos = []
        for estudiante in estudiantes:
            hijos.append({
                'id': estudiante['id'],
                'nombre': f"{estudiante['nombre']} {estudiante['apellido']}",
                'grado': estudiante['grado'],
                'profesor': f"Prof. {estudiante['profesor_nombre']} {estudiante['profesor_apellido']}" if estudiante['profesor_nombre'] else 'Sin profesor asignado'
            })
        
        return jsonify({'hijos': hijos})
        
    except Exception as e:
        print(f"Error al obtener hijos: {e}")
        return jsonify({'error': 'Error interno del servidor'}), 500

@main_bp.route('/acudiente/api/observaciones/<int:hijo_id>')
def obtener_observaciones_hijo(hijo_id):
    """API para obtener las observaciones de un hijo específico"""
    try:
        user_id = session.get('id')
        if not user_id:
            return jsonify({'error': 'No autorizado'}), 401
        
        from ..models.student_model import StudentModel
        from ..models.observation_model import ObservationModel
        
        # Verificar que el estudiante pertenece al acudiente
        student = StudentModel.get_student_by_id(hijo_id)
        if not student or student['acudiente_id'] != user_id:
            return jsonify({'error': 'Estudiante no encontrado o no autorizado'}), 403
        
        # Obtener observaciones reales de la base de datos
        observaciones = ObservationModel.get_observations_by_student(hijo_id)
        
        # Procesar datos para el formato esperado por el frontend
        observaciones_formateadas = []
        total = len(observaciones)
        positivas = 0
        multimedia = 0
        
        for obs in observaciones:
            # Formatear fecha
            fecha_str = obs['fecha'].strftime('%Y-%m-%d') if obs['fecha'] else 'Sin fecha'
            
            # Contar positivas
            if obs['tipo'] == 'Positiva':
                positivas += 1
            
            # Verificar multimedia real
            archivos_multimedia = MultimediaService.get_multimedia_by_observation(obs['id'])
            tiene_fotos = any(archivo.get('is_image', False) for archivo in archivos_multimedia)
            tiene_videos = any(archivo.get('is_video', False) for archivo in archivos_multimedia)
            
            if tiene_fotos or tiene_videos:
                multimedia += 1
            
            observaciones_formateadas.append({
                'id': obs['id'],
                'fecha': fecha_str,
                'tipo': obs['tipo'],
                'descripcion': obs['descripcion'],
                'fotos': tiene_fotos,
                'videos': tiene_videos
            })
        
        datos = {
            'total': total,
            'positivas': positivas,
            'multimedia': multimedia,
            'observaciones': observaciones_formateadas
        }
        
        return jsonify(datos)
        
    except Exception as e:
        print(f"Error al obtener observaciones: {e}")
        return jsonify({'error': 'Error interno del servidor'}), 500

@main_bp.route('/debug/observaciones/<int:hijo_id>')
def debug_observaciones_hijo(hijo_id):
    """Debug endpoint para verificar observaciones"""
    try:
        from ..models.observation_model import ObservationModel
        from ..database.db_connection import mysql
        
        html = f"<h2>Debug Observaciones para Estudiante ID: {hijo_id}</h2>"
        
        # Verificar si el estudiante existe
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM estudiantes WHERE id = %s", (hijo_id,))
        estudiante = cur.fetchone()
        cur.close()
        
        if not estudiante:
            return f"<p>Estudiante con ID {hijo_id} no encontrado</p>"
        
        html += f"<p>Estudiante encontrado: {estudiante}</p>"
        
        # Verificar observaciones directamente en la BD
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM observaciones WHERE id_estudiante = %s", (hijo_id,))
        obs_directas = cur.fetchall()
        cur.close()
        
        html += f"<h3>Observaciones directas de BD:</h3>"
        html += f"<p>Cantidad: {len(obs_directas)}</p>"
        
        if obs_directas:
            html += "<ul>"
            for obs in obs_directas:
                html += f"<li>{obs}</li>"
            html += "</ul>"
        
        # Obtener observaciones usando el modelo
        observaciones = ObservationModel.get_observations_by_student(hijo_id)
        
        html += f"<h3>Observaciones usando modelo:</h3>"
        html += f"<p>Cantidad encontrada: {len(observaciones) if observaciones else 0} observaciones</p>"
        
        if observaciones:
            html += "<ul>"
            for obs in observaciones:
                html += f"<li>ID: {obs.get('id')}, Fecha: {obs.get('fecha')}, Descripción: {obs.get('descripcion', 'N/A')[:50]}...</li>"
            html += "</ul>"
        else:
            html += "<p>No se encontraron observaciones para este estudiante</p>"
            
        return html
        
    except Exception as e:
        return f"Error: {str(e)}"

@main_bp.route('/debug/estudiantes-acudientes')
def debug_estudiantes_acudientes():
    """Debug endpoint para ver relaciones estudiante-acudiente"""
    try:
        from ..database.db_connection import mysql
        
        html = "<h2>Debug Estudiantes y Acudientes</h2>"
        
        # Verificar estudiantes con acudientes asignados
        cur = mysql.connection.cursor()
        cur.execute("""
            SELECT e.id, e.nombre, e.apellido, e.acudiente_id, 
                   u.nombre as acudiente_nombre, u.apellido as acudiente_apellido
            FROM estudiantes e
            LEFT JOIN usuarios u ON e.acudiente_id = u.id
            WHERE e.acudiente_id IS NOT NULL
        """)
        estudiantes_con_acudiente = cur.fetchall()
        cur.close()
        
        html += f"<h3>Estudiantes con acudiente asignado:</h3>"
        html += f"<p>Cantidad: {len(estudiantes_con_acudiente)}</p>"
        
        if estudiantes_con_acudiente:
            html += "<ul>"
            for est in estudiantes_con_acudiente:
                html += f"<li>Estudiante ID: {est[0]}, Nombre: {est[1]} {est[2]}, Acudiente ID: {est[3]}, Acudiente: {est[4]} {est[5]}</li>"
            html += "</ul>"
        
        # Verificar observaciones totales
        cur = mysql.connection.cursor()
        cur.execute("SELECT COUNT(*) FROM observaciones")
        total_obs = cur.fetchone()[0]
        cur.close()
        
        html += f"<h3>Total de observaciones en la BD: {total_obs}</h3>"
        
        return html
        
    except Exception as e:
        return f"Error: {str(e)}"

@main_bp.route('/debug/acudiente-completo/<int:acudiente_id>')
def debug_acudiente_completo(acudiente_id):
    """Debug completo para acudiente específico"""
    try:
        from ..models.student_model import StudentModel
        from ..models.observation_model import ObservationModel
        
        html = f"<h2>Debug Completo - Acudiente ID: {acudiente_id}</h2>"
        
        # 1. Verificar que el acudiente existe
        from ..database.db_connection import mysql
        cur = mysql.connection.cursor()
        cur.execute("SELECT id, nombre, apellido, correo FROM usuarios WHERE id = %s AND id_rol = 4", (acudiente_id,))
        acudiente = cur.fetchone()
        cur.close()
        
        if not acudiente:
            return f"<p>Acudiente con ID {acudiente_id} no encontrado</p>"
        
        html += f"<h3>1. Acudiente encontrado:</h3>"
        html += f"<p>ID: {acudiente[0]}, Nombre: {acudiente[1]} {acudiente[2]}, Email: {acudiente[3]}</p>"
        
        # 2. Buscar estudiantes asignados
        estudiantes = StudentModel.get_students_by_acudiente(acudiente_id)
        html += f"<h3>2. Estudiantes asignados:</h3>"
        html += f"<p>Cantidad: {len(estudiantes) if estudiantes else 0}</p>"
        
        if estudiantes:
            html += "<ul>"
            for est in estudiantes:
                html += f"<li>ID: {est.get('id')}, Nombre: {est.get('nombre')} {est.get('apellido')}, Grado: {est.get('grado')}</li>"
            html += "</ul>"
            
            # 3. Para cada estudiante, buscar observaciones
            for est in estudiantes:
                est_id = est.get('id')
                observaciones = ObservationModel.get_observations_by_student(est_id)
                html += f"<h4>Observaciones para {est.get('nombre')} {est.get('apellido')} (ID: {est_id}):</h4>"
                html += f"<p>Cantidad: {len(observaciones) if observaciones else 0}</p>"
                
                if observaciones:
                    html += "<ul>"
                    for obs in observaciones:
                        html += f"<li><strong>{obs.get('titulo')}</strong> - {obs.get('tipo')} - {obs.get('fecha')}</li>"
                    html += "</ul>"
        else:
            html += "<p>No hay estudiantes asignados a este acudiente</p>"
        
        return html
        
    except Exception as e:
        return f"Error: {str(e)}"

@main_bp.route('/debug/session')
def debug_session():
    """Debug de la sesión actual (sin autenticación)"""
    try:
        html = "<h2>Debug de Sesión</h2>"
        html += f"<p><strong>Sesión completa:</strong> {dict(session)}</p>"
        html += f"<p><strong>ID de usuario:</strong> {session.get('id', 'NO ENCONTRADO')}</p>"
        html += f"<p><strong>Nombre de usuario:</strong> {session.get('nombre', 'NO ENCONTRADO')}</p>"
        html += f"<p><strong>Email de usuario:</strong> {session.get('correo', 'NO ENCONTRADO')}</p>"
        html += f"<p><strong>Rol de usuario:</strong> {session.get('id_rol', 'NO ENCONTRADO')}</p>"
        
        # Verificar si hay algún usuario con nombre julian
        from ..database.db_connection import mysql
        cur = mysql.connection.cursor()
        cur.execute("SELECT id, nombre, apellido, correo, id_rol FROM usuarios WHERE nombre LIKE '%julian%' OR correo LIKE '%julian%'")
        julian_users = cur.fetchall()
        cur.close()
        
        html += "<h3>Usuarios Julian en BD:</h3>"
        if julian_users:
            html += "<ul>"
            for user in julian_users:
                html += f"<li>ID: {user[0]}, Nombre: {user[1]} {user[2]}, Email: {user[3]}, Rol: {user[4]}</li>"
            html += "</ul>"
        else:
            html += "<p>No se encontraron usuarios Julian</p>"
        
        return html
    except Exception as e:
        return f"Error: {str(e)}"

@main_bp.route('/debug/api-hijos')
def debug_api_hijos():
    """Debug de la API de hijos para el usuario logueado"""
    try:
        user_id = session.get('id')
        user_name = session.get('nombre', 'Usuario')
        
        html = f"<h2>Debug API Hijos - Usuario Logueado</h2>"
        html += f"<p><strong>Usuario ID:</strong> {user_id}</p>"
        html += f"<p><strong>Usuario Nombre:</strong> {user_name}</p>"
        html += f"<p><strong>Sesión completa:</strong> {dict(session)}</p>"
        
        if not user_id:
            return html + "<p><strong>ERROR:</strong> No hay usuario logueado</p>"
        
        from ..models.student_model import StudentModel
        
        # Verificar estudiantes directamente
        estudiantes = StudentModel.get_students_by_acudiente(user_id)
        html += f"<h3>Estudiantes encontrados:</h3>"
        html += f"<p>Cantidad: {len(estudiantes) if estudiantes else 0}</p>"
        
        if estudiantes:
            html += "<ul>"
            for est in estudiantes:
                html += f"<li>ID: {est.get('id')}, Nombre: {est.get('nombre')} {est.get('apellido')}, Grado: {est.get('grado')}</li>"
            html += "</ul>"
        else:
            html += "<p>No se encontraron estudiantes para este acudiente</p>"
            
            # Verificar en la base de datos directamente
            from ..database.db_connection import mysql
            cur = mysql.connection.cursor()
            cur.execute("SELECT * FROM estudiantes WHERE acudiente_id = %s", (user_id,))
            estudiantes_bd = cur.fetchall()
            cur.close()
            
            html += f"<h4>Consulta directa a BD:</h4>"
            html += f"<p>Estudiantes con acudiente_id = {user_id}: {len(estudiantes_bd)}</p>"
            if estudiantes_bd:
                html += "<ul>"
                for est in estudiantes_bd:
                    html += f"<li>{est}</li>"
                html += "</ul>"
        
        return html
        
    except Exception as e:
        return f"Error: {str(e)}"

@main_bp.route('/debug/hijos-julian')
def debug_hijos_julian():
    """Debug específico para Julian (sin autenticación)"""
    try:
        from ..models.student_model import StudentModel
        
        # Usar directamente el ID 13 de Julian
        estudiantes = StudentModel.get_students_by_acudiente(13)
        
        html = "<h2>Debug Hijos de Julian (ID: 13)</h2>"
        html += f"<p>Estudiantes encontrados: {len(estudiantes) if estudiantes else 0}</p>"
        
        if estudiantes:
            html += "<ul>"
            for est in estudiantes:
                html += f"<li>ID: {est.get('id')}, Nombre: {est.get('nombre')} {est.get('apellido')}, Grado: {est.get('grado')}</li>"
            html += "</ul>"
            
            # También mostrar las observaciones
            for est in estudiantes:
                from ..models.observation_model import ObservationModel
                obs = ObservationModel.get_observations_by_student(est.get('id'))
                html += f"<h4>Observaciones para {est.get('nombre')}:</h4>"
                html += f"<p>Total: {len(obs) if obs else 0}</p>"
                if obs:
                    html += "<ul>"
                    for o in obs[:3]:  # Solo mostrar las primeras 3
                        html += f"<li>{o.get('titulo')} - {o.get('tipo')}</li>"
                    html += "</ul>"
        else:
            html += "<p>No se encontraron estudiantes para Julian</p>"
        
        return html
        
    except Exception as e:
        return f"Error: {str(e)}"

@main_bp.route('/acudiente/api/hijos-temp')
def obtener_hijos_temp():
    """API temporal para hijos de Julian (sin autenticación)"""
    try:
        from ..models.student_model import StudentModel
        
        print(f"DEBUG: Buscando estudiantes para acudiente ID 8 (Julian)")
        
        # Usar directamente el ID 8 de Julian (según la base de datos)
        estudiantes = StudentModel.get_students_by_acudiente(8)
        
        print(f"DEBUG: Estudiantes encontrados: {len(estudiantes)}")
        
        if len(estudiantes) == 0:
            print("DEBUG: No hay estudiantes asignados a Julian. Verificando si hay estudiantes sin acudiente...")
            # Si no hay estudiantes asignados, buscar estudiantes sin acudiente para asignar
            all_students = StudentModel.get_all_students()
            print(f"DEBUG: Total estudiantes en el sistema: {len(all_students)}")
            
            students_without_acudiente = [s for s in all_students if s.get('acudiente_id') is None]
            print(f"DEBUG: Estudiantes sin acudiente: {len(students_without_acudiente)}")
            
            if students_without_acudiente:
                print("DEBUG: Usando estudiantes sin acudiente como ejemplo")
                estudiantes = students_without_acudiente[:3]  # Tomar máximo 3 como ejemplo
        
        hijos = []
        for estudiante in estudiantes:
            hijo_data = {
                'id': estudiante['id'],
                'nombre': f"{estudiante['nombre']} {estudiante['apellido']}",
                'grado': estudiante['grado'] or 'Sin grado',
                'profesor': f"Prof. {estudiante['profesor_nombre']} {estudiante['profesor_apellido']}" if estudiante.get('profesor_nombre') else 'Sin profesor asignado'
            }
            hijos.append(hijo_data)
            print(f"DEBUG: Hijo agregado: {hijo_data}")
        
        return jsonify({'hijos': hijos})
        
    except Exception as e:
        print(f"Error al obtener hijos: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500

@main_bp.route('/acudiente/api/observaciones-temp/<int:hijo_id>')
def obtener_observaciones_temp(hijo_id):
    """API temporal para observaciones (sin autenticación)"""
    try:
        from ..database.db_connection import mysql
        
        # Consulta directa a la base de datos
        cur = mysql.connection.cursor()
        query = """
            SELECT o.id, o.titulo, o.descripcion, o.tipo, o.fecha, o.hijo,
                   e.nombre as estudiante_nombre, e.apellido as estudiante_apellido,
                   u.nombre as profesor_nombre, u.apellido as profesor_apellido
            FROM observaciones o
            JOIN estudiantes e ON o.id_estudiante = e.id
            JOIN usuarios u ON o.id_profesor = u.id
            WHERE o.id_estudiante = %s
            ORDER BY o.fecha DESC
        """
        cur.execute(query, (hijo_id,))
        rows = cur.fetchall()
        cur.close()
        
        # Convertir a formato JSON
        observaciones = []
        for row in rows:
            observaciones.append({
                'id': row[0],
                'titulo': row[1],
                'descripcion': row[2],
                'tipo': row[3],
                'fecha': row[4].strftime('%Y-%m-%d %H:%M:%S') if row[4] else '',
                'hijo': row[5],
                'estudiante_nombre': row[6],
                'estudiante_apellido': row[7],
                'profesor_nombre': row[8],
                'profesor_apellido': row[9]
            })
        
        return jsonify({'observaciones': observaciones})
        
    except Exception as e:
        print(f"Error al obtener observaciones: {e}")
        return jsonify({'error': str(e)}), 500

@main_bp.route('/acudiente/perfil')
def perfil_acudiente():
    """Ruta para mostrar el perfil del acudiente"""
    try:
        user_id = session.get('id')
        if not user_id:
            return redirect(url_for('auth_bp.inicio_sesion'))
        
        from ..models.user_model import UserModel
        from ..models.student_model import StudentModel
        from ..models.observation_model import ObservationModel
        
        # Obtener datos reales del usuario
        user = UserModel.find_by_id(user_id)
        if not user:
            flash('Usuario no encontrado', 'danger')
            return redirect(url_for('auth_bp.inicio_sesion'))
        
        # Obtener hijos del acudiente
        hijos = StudentModel.get_students_by_acudiente(user_id)
        
        # Obtener observaciones totales
        observaciones = ObservationModel.get_for_acudiente(user_id)
        
        perfil_data = {
            'nombre': user['nombre'],
            'apellido': user['apellido'],
            'email': user['correo'],
            'telefono': '+57 300 123 4567',  # Campo que se puede agregar a la BD
            'direccion': 'Calle 123 #45-67, Bogotá',  # Campo que se puede agregar a la BD
            'fecha_registro': '2023-08-15',  # Se puede obtener de created_at si existe
            'ultimo_acceso': '2024-01-16 09:30:00',  # Se puede obtener de session logs
            'hijos_registrados': len(hijos),
            'observaciones_totales': len(observaciones),
            'notificaciones_activas': True,  # Campo que se puede agregar a la BD
            'estado_cuenta': 'Activa' if user['is_active'] else 'Inactiva'
        }
        
        return render_template('acudiente/perfil_acudiente.html', perfil=perfil_data)
        
    except Exception as e:
        print(f"Error al cargar perfil: {e}")
        flash('Error al cargar el perfil', 'danger')
        return redirect(url_for('main_bp.acudiente'))


