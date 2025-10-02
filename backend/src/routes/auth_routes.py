# backend/src/routes/auth_routes.py

from flask import Blueprint, request, redirect, url_for, session, flash, current_app, render_template
from flask_mail import Message
from werkzeug.security import generate_password_hash, check_password_hash
from ..services.auth_service import AuthService
from ..services.user_service import UserService # Necesario para create_registration_request si lo usas
import re
import jinja2

auth_bp = Blueprint('auth_bp', __name__)

@auth_bp.route('/acceso-login', methods=["POST"])
@auth_bp.route('/login', methods=["POST"])  # Agregar ruta alternativa
def login():
    if request.method == 'POST':
        print("=== DEBUG LOGIN ===")
        login_method = request.form.get('login_method', 'correo')
        usuario = request.form.get('usuario')
        password = request.form.get('contrasena')
        
        print(f"Método de login: {login_method}")
        print(f"Usuario: {usuario}")
        print(f"Password presente: {'Sí' if password else 'No'}")

        if not usuario or not password or not login_method:
            print("ERROR: Campos faltantes")
            flash('Por favor, completa todos los campos.', 'danger')
            return redirect(url_for('main_bp.inicio_sesion'))

        # Validar formato según el método de login
        format_valid = _validate_login_format(login_method, usuario)
        print(f"Formato válido: {format_valid}")
        
        if not format_valid:
            flash('El formato del documento ingresado no es válido.', 'danger')
            return redirect(url_for('main_bp.inicio_sesion'))

        print("Intentando autenticar usuario...")
        user = AuthService.authenticate_user_multi(login_method, usuario, password)
        print(f"Usuario encontrado: {'Sí' if user else 'No'}")
        
        if user:
            print(f"Usuario autenticado: {user.get('correo', 'N/A')}")
            print(f"Rol del usuario: {user.get('id_rol', 'N/A')}")
            
            # --- INICIO DE LA LÓGICA DE VERIFICACIÓN DE ESTADO ACTIVO ---
            # El objeto 'user' devuelto por AuthService.authenticate_user (que viene de UserModel.find_by_email)
            # ya contiene el campo 'is_active'.
            
            is_active_status = bool(user.get('is_active', False)) # Convertir a booleano, con fallback seguro
            print(f"Usuario activo: {is_active_status}")

            if is_active_status: # La cuenta está activa
                print("Configurando sesión...")
                session.permanent = True
                session['logueado'] = True
                session['id'] = user['id']
                session['id_rol'] = user['id_rol']
                session['nombre'] = user.get('nombre', 'Usuario')
                session['correo'] = user.get('correo', '')

                role_redirect_map = {
                    1: 'admin_bp.admin',
                    2: 'obs_bp.listar_observaciones_profesor',  # Profesor
                    4: 'main_bp.acudiente'
                }
                
                redirect_route = role_redirect_map.get(user['id_rol'], 'main_bp.home')
                print(f"Redirigiendo a: {redirect_route}")
                
                # Asumo que 'nombre_usuario' es la clave correcta en el diccionario 'user' si quieres mostrar el nombre
                flash(f"¡Bienvenido, {user.get('nombre', 'Usuario')}!", 'success') # Usar 'nombre' en lugar de 'nombre_usuario'
                return redirect(url_for(redirect_route))
            else:
                # La cuenta no está activa
                print("ERROR: Cuenta desactivada")
                flash('Tu cuenta ha sido desactivada. Por favor, contacta al administrador.', 'danger')
                return redirect(url_for('main_bp.inicio_sesion'))
            # --- FIN DE LA LÓGICA DE VERIFICACIÓN DE ESTADO ACTIVO ---
        else:
            # Correo o contraseña incorrectos (AuthService no encontró/autenticó al usuario)
            print("ERROR: Usuario no encontrado o contraseña incorrecta")
            flash('Correo o contraseña incorrectos.', 'danger')
            return redirect(url_for('main_bp.inicio_sesion'))
    
    # Esto se ejecuta si la solicitud no es POST (ej. alguien intenta acceder a /acceso-login directamente por GET)
    flash('Acceso no permitido.', 'danger')
    return redirect(url_for('main_bp.inicio_sesion'))

# Ruta para mostrar el formulario de registro
@auth_bp.route('/registro', methods=['GET'])
def mostrar_registro_form():
    return render_template('Registro.html')

# Ruta POST para procesar la solicitud de registro (¡La función ahora se llama 'registrar'!)
@auth_bp.route('/registrar-usuario', methods=["POST"])
def registrar():
    if request.method == 'POST':
        # 1. Recopilar y limpiar los datos del formulario
        nombre = request.form.get('nombre', '').strip()
        correo = request.form.get('correo', '').strip()
        celular = request.form.get('celular', '').strip()
        Nomb_Col = ''  # Campo nombre de colegio eliminado
        estudiantes_str = request.form.get('estudiantes', '').strip()

        # 2. Validación de datos
        errores = []
        if not nombre:
            errores.append('El nombre es un campo obligatorio.')
        if not correo:
            errores.append('El correo electrónico es un campo obligatorio.')
        elif not re.fullmatch(r'[^@]+@[^@]+\.[^@]+', correo):
            errores.append('El formato del correo electrónico es inválido.')
        if not celular:
            errores.append('El número celular es un campo obligatorio.')
        elif not re.fullmatch(r'^\d{10,}$', celular.replace(" ", "")):
            errores.append('El número celular debe contener al menos 10 dígitos numéricos (sin espacios).')
        # Campo nombre de colegio eliminado; no se valida
            # eliminado
        if not estudiantes_str:
            errores.append('La cantidad de estudiantes es un campo obligatorio.')
        else:
            try:
                estudiantes = int(estudiantes_str)
                if estudiantes <= 0:
                    errores.append('La cantidad de estudiantes debe ser un número positivo.')
            except ValueError:
                errores.append('La cantidad de estudiantes debe ser un número válido.')
        
        if errores:
            for error in errores:
                flash(error, 'danger')
            return redirect(url_for('auth_bp.mostrar_registro_form'))
        
        estudiantes = int(estudiantes_str) # Convertir a entero después de la validación

        # 3. Guardar la solicitud en la base de datos (Usando UserService)
        try:
            # Asegúrate de que UserService.create_registration_request exista y sea funcional
            solicitud_guardada = UserService.create_registration_request(
                nombre=nombre, 
                correo=correo, 
                celular=celular,
                nombre_colegio=Nomb_Col,
                cantidad_estudiantes=estudiantes
            )
            
            if not solicitud_guardada:
                flash('Ya existe una solicitud pendiente con este correo. Por favor, espera nuestra respuesta o contáctanos si crees que hay un error.', 'warning')
                return redirect(url_for('auth_bp.mostrar_registro_form'))
        except Exception as e:
            flash(f'Ocurrió un error al guardar tu solicitud en la base de datos. Por favor, inténtalo de nuevo.', 'danger')
            current_app.logger.error(f"Error DB al guardar solicitud: {e}")
            return redirect(url_for('auth_bp.mostrar_registro_form'))

        # 4. Preparar y enviar el correo de notificación al ADMINISTRADOR
        asunto_admin_email = f"Nueva Solicitud de Acceso: {nombre}"
        cuerpo_html_admin_email = f"""
        <html>
        <head>
            <style>
                body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
                .container {{ max-width: 600px; margin: 20px auto; padding: 20px; border: 1px solid #ddd; border-radius: 8px; background-color: #f9f9f9; }}
                h3 {{ color: #0056b3; }}
                p {{ margin-bottom: 10px; }}
                strong {{ color: #555; }}
            </style>
        </head>
        <body>
            <div class="container">
                <h3>Detalles de una nueva solicitud de acceso a Teaching Notes:</h3>
                <p><strong>Nombre del Contacto:</strong> {nombre}</p>
                <p><strong>Correo Electrónico:</strong> {correo}</p>
                <p><strong>Número Celular:</strong> {celular}</p>
                
                <p><strong>Cantidad Estimada de Estudiantes:</strong> {estudiantes}</p>
                <br>
                <p>Esta solicitud ha sido guardada en la base de datos para su revisión.</p>
                <p>Este correo fue generado automáticamente.</p>
            </div>
        </body>
        </html>
        """
        
        msg_admin = Message(
            subject=asunto_admin_email,
            recipients=['teachingnotes14@gmail.com'], # <--- ¡¡¡REEMPLAZA ESTO CON TU CORREO ADMINISTRADOR REAL!!!
            html=cuerpo_html_admin_email,
            sender=current_app.config['MAIL_DEFAULT_SENDER'],
            charset='utf-8'
        )

        # 5. Preparar y enviar el correo de CONFIRMACIÓN al USUARIO
        asunto_user_email = "¡Tu solicitud de acceso a Teaching Notes ha sido recibida!"
        cuerpo_html_user_email = f"""
        <html>
        <head>
            <style>
                body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
                .container {{ max-width: 600px; margin: 20px auto; padding: 20px; border: 1px solid #ddd; border-radius: 8px; background-color: #f9f9f9; }}
                h3 {{ color: #28a745; }}
                p {{ margin-bottom: 10px; }}
            </style>
        </head>
        <body>
            <div class="container">
                <h3>¡Hola {nombre}!</h3>
                <p>Gracias por tu interés en Teaching Notes.</p>
                <p>Hemos recibido correctamente tu solicitud de acceso.</p>
                <p>Nuestro equipo revisará tu solicitud y se pondrá en contacto contigo muy pronto (normalmente en 1-2 días hábiles) para informarte sobre los siguientes pasos.</p>
                <p>Mientras tanto, puedes explorar nuestro sitio web para conocer más sobre Teaching Notes.</p>
                <p>¡Gracias por elegir Teaching Notes!</p>
                <p>Atentamente,<br>El equipo de Teaching Notes</p>
            </div>
        </body>
        </html>
        """
        
        msg_user = Message(
            subject=asunto_user_email,
            recipients=[correo],
            html=cuerpo_html_user_email,
            sender=current_app.config['MAIL_DEFAULT_SENDER'],
            charset='utf-8'
        )

        # 6. Enviar ambos correos y manejar posibles errores de envío
        email_sent_ok = True
        try:
            current_app.mail.send(msg_admin)
            current_app.logger.info(f"Correo de notificación enviado al admin para {correo}")
        except Exception as e:
            current_app.logger.error(f"Error al enviar correo al admin para {correo}: {e}")
            email_sent_ok = False
        
        try:
            current_app.mail.send(msg_user)
            current_app.logger.info(f"Correo de confirmación enviado al usuario {correo}")
        except Exception as e:
            current_app.logger.error(f"Error al enviar correo de confirmación al usuario {correo}: {e}")
            email_sent_ok = False

        if email_sent_ok:
            flash('¡Tu solicitud ha sido enviada con éxito! Revisa tu correo para el mensaje de confirmación.', 'success')
        else:
            flash('Tu solicitud se guardó, pero hubo un error al enviar las notificaciones por correo. Por favor, contáctanos directamente si no recibes una respuesta pronto.', 'warning')
            
        return render_template('agradecimiento.html', nombre=nombre)

    flash('Acceso no permitido.', 'danger')
    return redirect(url_for('auth_bp.mostrar_registro_form'))


def _validate_login_format(login_method, usuario):
    """Valida el formato del documento según el método de login"""
    if login_method == 'correo':
        # Validar formato de email
        email_pattern = r'^[^\s@]+@[^\s@]+\.[^\s@]+$'
        return re.match(email_pattern, usuario) is not None
    
    elif login_method == 'cedula':
        # Validar cédula (6-10 dígitos)
        cedula_pattern = r'^[0-9]{6,10}$'
        return re.match(cedula_pattern, usuario) is not None
    
    elif login_method == 'ppt':
        # Validar PPT (PPT seguido de 9-12 dígitos)
        ppt_pattern = r'^PPT[0-9]{9,12}$'
        return re.match(ppt_pattern, usuario.upper()) is not None
    
    return False

@auth_bp.route('/cerrar-sesion')
def cerrar_sesion():
    session.clear()
    flash('Has cerrado sesión correctamente.', 'info')
    return redirect(url_for('main_bp.home'))