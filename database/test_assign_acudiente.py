#!/usr/bin/env python3
"""
Script para probar la asignación de acudientes
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

# Configurar Flask app context
from backend.src.app import create_app
app = create_app()

def test_assign_acudiente():
    """Prueba la asignación de acudientes"""
    with app.app_context():
        from backend.src.models.student_acudiente_model import StudentAcudienteModel
        from backend.src.models.student_model import StudentModel
        
        print("🧪 Probando asignación de acudientes...")
        
        # Obtener estudiantes disponibles
        students = StudentModel.get_all_students()
        if not students:
            print("❌ No hay estudiantes en el sistema")
            return
        
        student = students[0]
        student_id = student['id']
        print(f"📚 Usando estudiante: {student['nombre']} {student['apellido']} (ID: {student_id})")
        
        # Obtener acudientes disponibles
        available_acudientes = StudentAcudienteModel.get_available_acudientes(student_id)
        if not available_acudientes:
            print("❌ No hay acudientes disponibles")
            return
        
        acudiente = available_acudientes[0]
        acudiente_id = acudiente['id']
        print(f"👨‍👩‍👧‍👦 Usando acudiente: {acudiente['nombre']} {acudiente['apellido']} (ID: {acudiente_id})")
        
        # Probar asignación
        print(f"\n🔄 Asignando acudiente {acudiente_id} a estudiante {student_id}...")
        success, message = StudentAcudienteModel.assign_acudiente(student_id, acudiente_id, 'principal')
        
        if success:
            print(f"✅ {message}")
        else:
            print(f"❌ {message}")
        
        # Verificar resultado
        acudientes_asignados = StudentAcudienteModel.get_acudientes_by_student(student_id)
        print(f"\n📊 Acudientes asignados al estudiante:")
        for acud in acudientes_asignados:
            print(f"   - {acud['nombre']} {acud['apellido']} ({acud['tipo_relacion']})")

if __name__ == "__main__":
    test_assign_acudiente()
