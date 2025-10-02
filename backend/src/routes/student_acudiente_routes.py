# backend/src/routes/student_acudiente_routes.py

from flask import Blueprint, render_template, request, redirect, url_for, flash, session, jsonify
from ..models.student_acudiente_model import StudentAcudienteModel
from ..models.student_model import StudentModel
from ..models.user_model import UserModel
from ..utils.decorators import login_required, role_required

student_acudiente_bp = Blueprint('student_acudiente_bp', __name__, url_prefix='/estudiantes')

@student_acudiente_bp.route('/<int:student_id>/acudientes')
@login_required
@role_required([1, 2])  # Admin y Profesor
def ver_acudientes_estudiante(student_id):
    """Ver acudientes asignados a un estudiante"""
    try:
        # Obtener información del estudiante
        student = StudentModel.get_student_by_id(student_id)
        if not student:
            flash('Estudiante no encontrado.', 'danger')
            return redirect(url_for('admin_bp.listar_estudiantes'))
        
        # Obtener acudientes del estudiante
        acudientes = StudentAcudienteModel.get_acudientes_by_student(student_id)
        
        # Obtener acudientes disponibles para asignar
        available_acudientes = StudentAcudienteModel.get_available_acudientes(student_id)
        
        # Contar acudientes actuales
        current_count = StudentAcudienteModel.get_student_acudiente_count(student_id)
        can_add_more = current_count < 2
        
        return render_template('administrador/student_acudientes.html',
                             student=student,
                             acudientes=acudientes,
                             available_acudientes=available_acudientes,
                             can_add_more=can_add_more,
                             current_count=current_count)
                             
    except Exception as e:
        print(f"Error al ver acudientes del estudiante: {e}")
        flash('Error al cargar la información.', 'danger')
        return redirect(url_for('admin_bp.listar_estudiantes'))

@student_acudiente_bp.route('/<int:student_id>/acudientes/asignar', methods=['POST'])
@login_required
@role_required([1, 2])  # Admin y Profesor
def asignar_acudiente(student_id):
    """Asignar un acudiente a un estudiante"""
    try:
        acudiente_id = request.form.get('acudiente_id')
        tipo_relacion = request.form.get('tipo_relacion', 'principal')
        
        if not acudiente_id:
            flash('Debe seleccionar un acudiente.', 'danger')
            return redirect(url_for('student_acudiente_bp.ver_acudientes_estudiante', student_id=student_id))
        
        # Verificar que el acudiente existe
        acudiente = UserModel.find_by_id(int(acudiente_id))
        if not acudiente:
            flash('Acudiente no encontrado.', 'danger')
            return redirect(url_for('student_acudiente_bp.ver_acudientes_estudiante', student_id=student_id))
        
        # Asignar acudiente
        success, message = StudentAcudienteModel.assign_acudiente(student_id, int(acudiente_id), tipo_relacion)
        
        if success:
            flash(f'Acudiente asignado exitosamente. {message}', 'success')
        else:
            flash(f'Error al asignar acudiente: {message}', 'danger')
            
        return redirect(url_for('student_acudiente_bp.ver_acudientes_estudiante', student_id=student_id))
        
    except Exception as e:
        print(f"Error al asignar acudiente: {e}")
        flash('Error al asignar acudiente.', 'danger')
        return redirect(url_for('student_acudiente_bp.ver_acudientes_estudiante', student_id=student_id))

@student_acudiente_bp.route('/<int:student_id>/acudientes/<int:acudiente_id>/remover', methods=['POST'])
@login_required
@role_required([1, 2])  # Admin y Profesor
def remover_acudiente(student_id, acudiente_id):
    """Remover un acudiente de un estudiante"""
    try:
        success, message = StudentAcudienteModel.remove_acudiente(student_id, acudiente_id)
        
        if success:
            flash(f'Acudiente removido exitosamente.', 'success')
        else:
            flash(f'Error al remover acudiente: {message}', 'danger')
            
        return redirect(url_for('student_acudiente_bp.ver_acudientes_estudiante', student_id=student_id))
        
    except Exception as e:
        print(f"Error al remover acudiente: {e}")
        flash('Error al remover acudiente.', 'danger')
        return redirect(url_for('student_acudiente_bp.ver_acudientes_estudiante', student_id=student_id))

@student_acudiente_bp.route('/<int:student_id>/acudientes/<int:acudiente_id>/cambiar-tipo', methods=['POST'])
@login_required
@role_required([1, 2])  # Admin y Profesor
def cambiar_tipo_acudiente(student_id, acudiente_id):
    """Cambiar el tipo de relación de un acudiente (principal/secundario)"""
    try:
        new_type = request.form.get('new_type')
        
        if new_type not in ['principal', 'secundario']:
            flash('Tipo de relación inválido.', 'danger')
            return redirect(url_for('student_acudiente_bp.ver_acudientes_estudiante', student_id=student_id))
        
        success, message = StudentAcudienteModel.change_acudiente_type(student_id, acudiente_id, new_type)
        
        if success:
            flash(f'Tipo de relación actualizado exitosamente.', 'success')
        else:
            flash(f'Error al cambiar tipo: {message}', 'danger')
            
        return redirect(url_for('student_acudiente_bp.ver_acudientes_estudiante', student_id=student_id))
        
    except Exception as e:
        print(f"Error al cambiar tipo de acudiente: {e}")
        flash('Error al cambiar tipo de relación.', 'danger')
        return redirect(url_for('student_acudiente_bp.ver_acudientes_estudiante', student_id=student_id))

@student_acudiente_bp.route('/api/<int:student_id>/acudientes')
@login_required
@role_required([1, 2, 4])  # Admin, Profesor y Acudiente
def api_get_acudientes(student_id):
    """API para obtener acudientes de un estudiante"""
    try:
        acudientes = StudentAcudienteModel.get_acudientes_by_student(student_id)
        
        # Formatear datos para JSON
        acudientes_data = []
        for acudiente in acudientes:
            acudientes_data.append({
                'id': acudiente['acudiente_id'],
                'nombre': f"{acudiente['nombre']} {acudiente['apellido']}",
                'correo': acudiente['correo'],
                'tipo_relacion': acudiente['tipo_relacion'],
                'fecha_asignacion': acudiente['fecha_asignacion'].isoformat() if acudiente['fecha_asignacion'] else None
            })
        
        return jsonify({
            'success': True,
            'acudientes': acudientes_data,
            'total': len(acudientes_data)
        })
        
    except Exception as e:
        print(f"Error en API de acudientes: {e}")
        return jsonify({
            'success': False,
            'error': 'Error al obtener acudientes'
        }), 500
