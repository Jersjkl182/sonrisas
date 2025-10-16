# =====================================================
# RUTAS PARA SISTEMA DE LECTURA DE OBSERVACIONES
# =====================================================

from flask import Blueprint, request, jsonify, session
from datetime import datetime
from ..database.db_connection import mysql

# Crear blueprint para las rutas de lectura
lectura_bp = Blueprint('lectura', __name__)

@lectura_bp.route('/marcar_leido/<int:observacion_id>', methods=['POST'])
def marcar_como_leido(observacion_id):
    """Marcar una observación como leída"""
    try:
        # Verificar que el usuario esté logueado
        if 'user_id' not in session:
            return jsonify({'error': 'Usuario no autenticado'}), 401
        
        user_id = session['user_id']
        
        # Conectar a la base de datos
        from MySQLdb.cursors import DictCursor
        cursor = mysql.connection.cursor(DictCursor)
        
        # Verificar que la observación existe
        cursor.execute("SELECT id FROM observaciones WHERE id = %s", (observacion_id,))
        if not cursor.fetchone():
            return jsonify({'error': 'Observación no encontrada'}), 404
        
        # Marcar como leída
        cursor.execute("""
            UPDATE observaciones 
            SET leido = 1, fecha_lectura = NOW(), leido_por = %s 
            WHERE id = %s
        """, (user_id, observacion_id))
        
        mysql.connection.commit()
        cursor.close()
        
        return jsonify({
            'success': True, 
            'message': 'Observación marcada como leída',
            'observacion_id': observacion_id,
            'fecha_lectura': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        })
        
    except Exception as e:
        return jsonify({'error': f'Error al marcar como leída: {str(e)}'}), 500

@lectura_bp.route('/marcar_no_leido/<int:observacion_id>', methods=['POST'])
def marcar_como_no_leido(observacion_id):
    """Marcar una observación como no leída"""
    try:
        # Verificar que el usuario esté logueado
        if 'user_id' not in session:
            return jsonify({'error': 'Usuario no autenticado'}), 401
        
        # Conectar a la base de datos
        from MySQLdb.cursors import DictCursor
        cursor = mysql.connection.cursor(DictCursor)
        
        # Verificar que la observación existe
        cursor.execute("SELECT id FROM observaciones WHERE id = %s", (observacion_id,))
        if not cursor.fetchone():
            return jsonify({'error': 'Observación no encontrada'}), 404
        
        # Marcar como no leída
        cursor.execute("""
            UPDATE observaciones 
            SET leido = 0, fecha_lectura = NULL, leido_por = NULL 
            WHERE id = %s
        """, (observacion_id,))
        
        mysql.connection.commit()
        cursor.close()
        
        return jsonify({
            'success': True, 
            'message': 'Observación marcada como no leída',
            'observacion_id': observacion_id
        })
        
    except Exception as e:
        return jsonify({'error': f'Error al marcar como no leída: {str(e)}'}), 500

@lectura_bp.route('/toggle_lectura/<int:observacion_id>', methods=['POST'])
def toggle_estado_lectura(observacion_id):
    """Alternar el estado de lectura de una observación"""
    try:
        # Verificar que el usuario esté logueado
        if 'user_id' not in session:
            return jsonify({'error': 'Usuario no autenticado'}), 401
        
        user_id = session['user_id']
        
        # Conectar a la base de datos
        from MySQLdb.cursors import DictCursor
        cursor = mysql.connection.cursor(DictCursor)
        
        # Obtener el estado actual
        cursor.execute("SELECT leido FROM observaciones WHERE id = %s", (observacion_id,))
        result = cursor.fetchone()
        
        if not result:
            return jsonify({'error': 'Observación no encontrada'}), 404
        
        estado_actual = result['leido']
        nuevo_estado = 1 if estado_actual == 0 else 0
        
        # Actualizar el estado
        if nuevo_estado == 1:  # Marcar como leída
            cursor.execute("""
                UPDATE observaciones 
                SET leido = 1, fecha_lectura = NOW(), leido_por = %s 
                WHERE id = %s
            """, (user_id, observacion_id))
            mensaje = 'Observación marcada como leída'
        else:  # Marcar como no leída
            cursor.execute("""
                UPDATE observaciones 
                SET leido = 0, fecha_lectura = NULL, leido_por = NULL 
                WHERE id = %s
            """, (observacion_id,))
            mensaje = 'Observación marcada como no leída'
        
        mysql.connection.commit()
        cursor.close()
        
        return jsonify({
            'success': True, 
            'message': mensaje,
            'observacion_id': observacion_id,
            'nuevo_estado': nuevo_estado,
            'leido': nuevo_estado == 1
        })
        
    except Exception as e:
        return jsonify({'error': f'Error al cambiar estado: {str(e)}'}), 500

@lectura_bp.route('/estadisticas_lectura')
def estadisticas_lectura():
    """Obtener estadísticas de lectura de observaciones"""
    try:
        # Verificar que el usuario esté logueado
        if 'user_id' not in session:
            return jsonify({'error': 'Usuario no autenticado'}), 401
        
        user_id = session['user_id']
        user_role = session.get('role', '')
        
        # Conectar a la base de datos
        from MySQLdb.cursors import DictCursor
        cursor = mysql.connection.cursor(DictCursor)
        
        # Construir consulta según el rol
        if user_role == 'Acudiente':
            # Para acudientes, solo sus observaciones
            query = """
                SELECT 
                    COUNT(*) as total,
                    SUM(CASE WHEN leido = 1 THEN 1 ELSE 0 END) as leidas,
                    SUM(CASE WHEN leido = 0 THEN 1 ELSE 0 END) as no_leidas
                FROM observaciones 
                WHERE id_acudiente = %s
            """
            cursor.execute(query, (user_id,))
        elif user_role == 'Profesor':
            # Para profesores, sus observaciones creadas
            query = """
                SELECT 
                    COUNT(*) as total,
                    SUM(CASE WHEN leido = 1 THEN 1 ELSE 0 END) as leidas,
                    SUM(CASE WHEN leido = 0 THEN 1 ELSE 0 END) as no_leidas
                FROM observaciones 
                WHERE id_profesor = %s
            """
            cursor.execute(query, (user_id,))
        else:
            # Para administradores, todas las observaciones
            query = """
                SELECT 
                    COUNT(*) as total,
                    SUM(CASE WHEN leido = 1 THEN 1 ELSE 0 END) as leidas,
                    SUM(CASE WHEN leido = 0 THEN 1 ELSE 0 END) as no_leidas
                FROM observaciones
            """
            cursor.execute(query)
        
        estadisticas = cursor.fetchone()
        cursor.close()
        
        total = estadisticas['total'] or 0
        leidas = estadisticas['leidas'] or 0
        no_leidas = estadisticas['no_leidas'] or 0
        
        return jsonify({
            'success': True,
            'estadisticas': {
                'total': total,
                'leidas': leidas,
                'no_leidas': no_leidas,
                'porcentaje_leidas': round((leidas / max(total, 1)) * 100, 1)
            }
        })
        
    except Exception as e:
        return jsonify({'error': f'Error al obtener estadísticas: {str(e)}'}), 500
