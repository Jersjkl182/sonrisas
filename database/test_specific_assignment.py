#!/usr/bin/env python3
"""
Script para probar asignación específica
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

# Configurar Flask app context
from backend.src.app import create_app
app = create_app()

def test_specific_assignment():
    """Prueba asignación específica"""
    with app.app_context():
        from backend.src.models.student_acudiente_model import StudentAcudienteModel
        
        print("🧪 Probando asignación específica...")
        
        # Usar estudiante 7 (jherson) y acudiente 12 (Maria)
        student_id = 7
        acudiente_id = 12
        
        print(f"📚 Estudiante ID: {student_id}")
        print(f"👨‍👩‍👧‍👦 Acudiente ID: {acudiente_id}")
        
        # Verificar acudientes actuales
        current_acudientes = StudentAcudienteModel.get_acudientes_by_student(student_id)
        print(f"📊 Acudientes actuales: {len(current_acudientes)}")
        for acud in current_acudientes:
            print(f"   - {acud['nombre']} {acud['apellido']} ({acud['tipo_relacion']})")
        
        # Verificar acudientes disponibles
        available = StudentAcudienteModel.get_available_acudientes(student_id)
        print(f"👥 Acudientes disponibles: {len(available)}")
        for acud in available[:3]:  # Solo mostrar los primeros 3
            print(f"   - ID: {acud['id']} - {acud['nombre']} {acud['apellido']}")
        
        # Intentar asignación
        print(f"\n🔄 Intentando asignar acudiente {acudiente_id} a estudiante {student_id}...")
        success, message = StudentAcudienteModel.assign_acudiente(student_id, acudiente_id)
        
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
    test_specific_assignment()
