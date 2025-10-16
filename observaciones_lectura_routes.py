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
        conn = get_db_connection()
        cursor = conn.cursor()
        
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
        
        conn.commit()
        cursor.close()
        conn.close()
        
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
        conn = get_db_connection()
        cursor = conn.cursor()
        
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
        
        conn.commit()
        cursor.close()
        conn.close()
        
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
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Obtener el estado actual
        cursor.execute("SELECT leido FROM observaciones WHERE id = %s", (observacion_id,))
        result = cursor.fetchone()
        
        if not result:
            return jsonify({'error': 'Observación no encontrada'}), 404
        
        estado_actual = result[0]
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
        
        conn.commit()
        cursor.close()
        conn.close()
        
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
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        
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
        conn.close()
        
        return jsonify({
            'success': True,
            'estadisticas': {
                'total': estadisticas['total'] or 0,
                'leidas': estadisticas['leidas'] or 0,
                'no_leidas': estadisticas['no_leidas'] or 0,
                'porcentaje_leidas': round((estadisticas['leidas'] or 0) / max(estadisticas['total'] or 1, 1) * 100, 1)
            }
        })
        
    except Exception as e:
        return jsonify({'error': f'Error al obtener estadísticas: {str(e)}'}), 500

# =====================================================
# FUNCIONES AUXILIARES
# =====================================================

def obtener_observaciones_con_lectura(user_id, user_role, limit=None):
    """Obtener observaciones con información de lectura"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        
        # Consulta base
        base_query = """
            SELECT o.*, 
                   u_leido.nombre as leido_por_nombre,
                   u_profesor.nombre as profesor_nombre,
                   u_acudiente.nombre as acudiente_nombre,
                   e.nombre as estudiante_nombre
            FROM observaciones o
            LEFT JOIN usuarios u_leido ON o.leido_por = u_leido.id
            LEFT JOIN usuarios u_profesor ON o.id_profesor = u_profesor.id
            LEFT JOIN usuarios u_acudiente ON o.id_acudiente = u_acudiente.id
            LEFT JOIN estudiantes e ON o.id_estudiante = e.id
        """
        
        # Filtrar según el rol
        if user_role == 'Acudiente':
            query = base_query + " WHERE o.id_acudiente = %s"
            params = (user_id,)
        elif user_role == 'Profesor':
            query = base_query + " WHERE o.id_profesor = %s"
            params = (user_id,)
        else:
            query = base_query
            params = ()
        
        # Agregar orden y límite
        query += " ORDER BY o.fecha DESC"
        if limit:
            query += f" LIMIT {limit}"
        
        cursor.execute(query, params)
        observaciones = cursor.fetchall()
        
        cursor.close()
        conn.close()
        
        return observaciones
        
    except Exception as e:
        print(f"Error al obtener observaciones: {e}")
        return []
