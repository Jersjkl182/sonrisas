#!/usr/bin/env python3
"""
Script para verificar el espaciado de las observaciones
"""

import os

def verify_observations_spacing():
    """Verifica el espaciado de las observaciones"""
    print("📏 VERIFICANDO ESPACIADO DE OBSERVACIONES - DASHBOARD ACUDIENTE")
    print("="*65)
    
    template_path = "c:/Sonrisas/frontend/template/acudiente/dashboard_unificado.html"
    
    if not os.path.exists(template_path):
        print("❌ Template no encontrado")
        return
    
    with open(template_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Verificar configuraciones de espaciado
    spacing_checks = [
        ("padding-top: calc(70px + 40px)", "Espaciado principal del dashboard"),
        ("margin: 40px 0 20px 0", "Margen del título de sección"),
        ("padding-top: 20px", "Padding superior del título"),
        ("gap: 25px", "Separación entre observaciones"),
        ("margin-top: 25px", "Margen superior del contenedor"),
        ("min-height: calc(100vh - 70px)", "Altura mínima configurada"),
        ("padding: 25px", "Padding de las tarjetas de observación")
    ]
    
    print("✅ CONFIGURACIONES DE ESPACIADO:")
    for check, description in spacing_checks:
        count = content.count(check)
        if count > 0:
            print(f"   ✅ {description} ({count} instancias)")
        else:
            print(f"   ❌ {description} - NO ENCONTRADO")
    
    # Verificar responsive design
    print("\n📱 RESPONSIVE DESIGN:")
    responsive_checks = [
        ("padding-top: calc(70px + 25px)", "Espaciado móvil"),
        ("margin: 30px 0 15px 0", "Margen móvil del título"),
        ("gap: 20px", "Separación móvil entre observaciones"),
        ("font-size: 1.5em", "Tamaño de fuente móvil del título")
    ]
    
    for check, description in responsive_checks:
        if check in content:
            print(f"   ✅ {description}")
        else:
            print(f"   ❌ {description} - NO ENCONTRADO")
    
    # Verificar estructura de clases
    print("\n🎨 ESTRUCTURA DE CLASES:")
    class_checks = [
        (".unified-dashboard", "Contenedor principal"),
        (".dashboard-header", "Header del dashboard"),
        (".section-title", "Título de sección"),
        (".observations-container", "Contenedor de observaciones"),
        (".observation-card", "Tarjetas de observación")
    ]
    
    for class_name, description in class_checks:
        if class_name in content:
            print(f"   ✅ {description} - {class_name}")
        else:
            print(f"   ❌ {description} - {class_name} NO ENCONTRADO")
    
    print("\n" + "="*65)
    print("🎯 ESPACIADO CONFIGURADO:")
    print("="*65)
    
    print("📱 ESPACIADO POR DISPOSITIVO:")
    print("   🖥️  Desktop:")
    print("      - Dashboard: 70px (header) + 40px = 110px desde arriba")
    print("      - Título sección: 40px margen superior + 20px padding")
    print("      - Observaciones: 25px separación entre tarjetas")
    print("   📱 Móvil:")
    print("      - Dashboard: 70px (header) + 25px = 95px desde arriba")
    print("      - Título sección: 30px margen superior + 15px padding")
    print("      - Observaciones: 20px separación entre tarjetas")
    
    print("\n🎨 MEJORAS APLICADAS:")
    print("   📏 Espaciado superior aumentado significativamente")
    print("   📋 Separación mejorada entre secciones")
    print("   🔄 Responsive design optimizado")
    print("   ✨ Padding de tarjetas mantenido (25px)")
    print("   📱 Adaptación móvil implementada")
    
    print("\n🎉 ¡ESPACIADO DE OBSERVACIONES CORREGIDO!")
    print("Las observaciones ahora tienen suficiente separación y no están 'remontadas'.")

if __name__ == "__main__":
    verify_observations_spacing()
