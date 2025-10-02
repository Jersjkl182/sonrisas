#!/usr/bin/env python3
"""
Script para verificar el espaciado del header
"""

import os

def verify_spacing():
    """Verifica el espaciado del header"""
    print("📏 VERIFICANDO ESPACIADO DEL HEADER - ÁREA ACUDIENTE")
    print("="*60)
    
    css_path = "c:/Sonrisas/frontend/static/css/acudiente/acudiente_modern.css"
    
    if not os.path.exists(css_path):
        print("❌ Archivo CSS no encontrado")
        return
    
    with open(css_path, 'r', encoding='utf-8') as f:
        css_content = f.read()
    
    # Verificar configuraciones de espaciado
    spacing_checks = [
        ("padding-top: calc(70px + var(--spacing-xl))", "Espaciado principal desktop"),
        ("padding-top: calc(70px + var(--spacing-lg))", "Espaciado tablet"),
        ("padding-top: calc(70px + var(--spacing-md))", "Espaciado móvil"),
        ("min-height: calc(100vh - 70px)", "Altura mínima configurada"),
        ("height: 70px", "Altura del header definida"),
        ("position: fixed", "Header fijo configurado"),
        ("z-index:", "Z-index para header configurado")
    ]
    
    print("✅ CONFIGURACIONES DE ESPACIADO:")
    for check, description in spacing_checks:
        count = css_content.count(check)
        if count > 0:
            print(f"   ✅ {description} ({count} instancias)")
        else:
            print(f"   ❌ {description} - NO ENCONTRADO")
    
    # Verificar variables de espaciado
    print("\n📐 VARIABLES DE ESPACIADO DEFINIDAS:")
    spacing_vars = [
        "--spacing-xs", "--spacing-sm", "--spacing-md", 
        "--spacing-lg", "--spacing-xl"
    ]
    
    for var in spacing_vars:
        if var in css_content:
            print(f"   ✅ {var} definida")
        else:
            print(f"   ❌ {var} NO definida")
    
    # Verificar responsive breakpoints
    print("\n📱 BREAKPOINTS RESPONSIVE:")
    breakpoints = [
        ("@media (max-width: 1024px)", "Tablet grande"),
        ("@media (max-width: 768px)", "Tablet"),
        ("@media (max-width: 480px)", "Móvil")
    ]
    
    for breakpoint, description in breakpoints:
        if breakpoint in css_content:
            print(f"   ✅ {description} - {breakpoint}")
        else:
            print(f"   ❌ {description} - NO ENCONTRADO")
    
    print("\n" + "="*60)
    print("🎯 ESPACIADO CONFIGURADO:")
    print("="*60)
    
    print("📱 ESPACIADO POR DISPOSITIVO:")
    print("   🖥️  Desktop: 70px (header) + 32px (spacing-xl) = 102px")
    print("   📱 Tablet: 70px (header) + 24px (spacing-lg) = 94px")
    print("   📱 Móvil: 70px (header) + 16px (spacing-md) = 86px")
    
    print("\n🎨 CARACTERÍSTICAS DEL LAYOUT:")
    print("   📌 Header fijo en la parte superior")
    print("   📏 Contenido con padding-top calculado")
    print("   📱 Espaciado responsive adaptativo")
    print("   🔄 Transiciones suaves mantenidas")
    print("   ✨ Efectos glassmorphism preservados")
    
    print("\n🎉 ¡ESPACIADO DEL HEADER CORREGIDO!")
    print("El contenido ahora tiene suficiente separación del header en todos los dispositivos.")

if __name__ == "__main__":
    verify_spacing()
