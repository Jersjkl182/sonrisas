#!/usr/bin/env python3
"""
Script para probar la asignación corregida
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

# Configurar Flask app context
from backend.src.app import create_app
app = create_app()

def test_fixed_assignment():
    """Prueba la asignación corregida"""
    with app.app_context():
        from backend.src.models.student_acudiente_model import StudentAcudienteModel
        
        print("🧪 Probando asignación corregida...")
        
        # Usar estudiante 6 (Angelo) y acudiente 13 (Carlos)
        student_id = 6
        acudiente_id = 13  # Carlos Gonzalez
        
        print(f"📚 Estudiante ID: {student_id}")
        print(f"👨‍👩‍👧‍👦 Acudiente ID: {acudiente_id}")
        
        # Verificar acudientes actuales
        current_acudientes = StudentAcudienteModel.get_acudientes_by_student(student_id)
        print(f"📊 Acudientes actuales: {len(current_acudientes)}")
        for acud in current_acudientes:
            print(f"   - {acud['nombre']} {acud['apellido']} ({acud['tipo_relacion']})")
        
        # Intentar asignación como secundario
        print(f"\n🔄 Intentando asignar acudiente {acudiente_id} como secundario...")
        success, message = StudentAcudienteModel.assign_acudiente(student_id, acudiente_id, 'secundario')
        
        print(f"📊 Resultado:")
        print(f"   Success: {success}")
        print(f"   Message: '{message}'")
        
        if success:
            print("✅ Asignación exitosa!")
            # Verificar resultado
            updated_acudientes = StudentAcudienteModel.get_acudientes_by_student(student_id)
            print(f"📊 Acudientes después de asignación: {len(updated_acudientes)}")
            for acud in updated_acudientes:
                print(f"   - {acud['nombre']} {acud['apellido']} ({acud['tipo_relacion']})")
        else:
            print(f"❌ Error en asignación: {message}")

if __name__ == "__main__":
    test_fixed_assignment()
