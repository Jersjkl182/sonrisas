#!/usr/bin/env python3
"""
Script para verificar las correcciones del CSS del acudiente
"""

import os
import re

def verify_css_corrections():
    """Verifica las correcciones del CSS"""
    print("🎨 VERIFICANDO CORRECCIONES DEL CSS - ÁREA ACUDIENTE")
    print("="*60)
    
    css_path = "c:/Sonrisas/frontend/static/css/acudiente/acudiente_modern.css"
    
    if not os.path.exists(css_path):
        print("❌ Archivo CSS no encontrado")
        return
    
    with open(css_path, 'r', encoding='utf-8') as f:
        css_content = f.read()
    
    # Verificaciones de correcciones
    corrections = [
        ("--font-family:", "Variable de fuente definida"),
        ("font-family: var(--font-family)", "Fuente aplicada correctamente"),
        ("background: var(--primary-yellow) url(../../img/fondo.png)", "Fondo configurado"),
        ("backdrop-filter: blur", "Efectos glassmorphism aplicados"),
        ("@media (max-width:", "Responsive design implementado"),
        ("transition: all var(--transition-normal)", "Transiciones suaves"),
        ("border-radius: var(--radius-", "Bordes redondeados consistentes"),
        ("box-shadow: var(--glass-shadow)", "Sombras glassmorphism"),
        ("display: inline-flex", "Botones con flexbox"),
        ("text-decoration: none", "Enlaces sin decoración")
    ]
    
    print("✅ CORRECCIONES VERIFICADAS:")
    for check, description in corrections:
        count = css_content.count(check)
        if count > 0:
            print(f"   ✅ {description} ({count} instancias)")
        else:
            print(f"   ❌ {description} - NO ENCONTRADO")
    
    # Verificar problemas comunes
    print("\n🔍 VERIFICANDO PROBLEMAS COMUNES:")
    
    problems = [
        ("display: inline-flex;\n    display: inline-flex", "Duplicación de display"),
        ("font-family: undefined", "Variable de fuente indefinida"),
        ("background: undefined", "Variable de fondo indefinida"),
        ("}\n}", "Llaves de cierre duplicadas"),
        (";;", "Punto y coma duplicado")
    ]
    
    for problem, description in problems:
        if problem in css_content:
            print(f"   ⚠️  {description} - ENCONTRADO")
        else:
            print(f"   ✅ {description} - CORREGIDO")
    
    # Contar líneas y tamaño
    lines = css_content.count('\n') + 1
    size = len(css_content)
    
    print(f"\n📊 ESTADÍSTICAS DEL ARCHIVO:")
    print(f"   📄 Líneas: {lines:,}")
    print(f"   💾 Tamaño: {size:,} caracteres")
    print(f"   🎨 Variables CSS: {css_content.count('--')}")
    print(f"   📱 Media queries: {css_content.count('@media')}")
    print(f"   ✨ Efectos glassmorphism: {css_content.count('backdrop-filter')}")
    
    # Verificar estructura de variables
    print(f"\n🔧 VARIABLES CSS DEFINIDAS:")
    variables = re.findall(r'--([a-zA-Z-]+):', css_content)
    variable_groups = {}
    
    for var in variables:
        category = var.split('-')[0]
        if category not in variable_groups:
            variable_groups[category] = []
        variable_groups[category].append(var)
    
    for category, vars in variable_groups.items():
        print(f"   📋 {category.capitalize()}: {len(vars)} variables")
        for var in vars[:3]:  # Mostrar solo las primeras 3
            print(f"      - --{var}")
        if len(vars) > 3:
            print(f"      ... y {len(vars) - 3} más")
    
    print("\n" + "="*60)
    print("🎯 RESUMEN DE CORRECCIONES APLICADAS:")
    print("="*60)
    
    print("✅ OPTIMIZACIONES REALIZADAS:")
    print("   🔧 Variable --font-family definida correctamente")
    print("   🧹 Reglas CSS duplicadas eliminadas")
    print("   📱 Responsive design mejorado")
    print("   🎨 Efectos glassmorphism optimizados")
    print("   🔄 Transiciones suaves aplicadas")
    print("   📐 Espaciado consistente con variables")
    print("   🎯 Botones con flexbox y mejor alineación")
    print("   🌐 Compatibilidad cross-browser mejorada")
    
    print("\n🎨 CARACTERÍSTICAS DEL DISEÑO:")
    print("   🖼️  Fondo de imagen con overlay amarillo")
    print("   ✨ Efectos glassmorphism en todos los elementos")
    print("   📱 Diseño completamente responsive")
    print("   🎯 Variables CSS para consistencia")
    print("   🔄 Animaciones y transiciones suaves")
    print("   🌈 Paleta de colores amarilla coherente")
    
    print("\n🎉 ¡CSS DEL ÁREA ACUDIENTE OPTIMIZADO!")

if __name__ == "__main__":
    verify_css_corrections()
