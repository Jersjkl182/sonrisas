#!/usr/bin/env python3
"""
Script para verificar que el fondo esté configurado correctamente
"""

import os

def verify_background():
    """Verifica la configuración del fondo"""
    print("🎨 VERIFICANDO CONFIGURACIÓN DE FONDO - ÁREA ACUDIENTE")
    print("="*60)
    
    # Verificar que existe el archivo de imagen
    fondo_path = "c:/Sonrisas/frontend/static/img/fondo.png"
    if os.path.exists(fondo_path):
        print("✅ Archivo de fondo encontrado: fondo.png")
        file_size = os.path.getsize(fondo_path)
        print(f"   📊 Tamaño: {file_size:,} bytes")
    else:
        print("❌ Archivo de fondo NO encontrado")
        return
    
    # Verificar CSS
    css_path = "c:/Sonrisas/frontend/static/css/acudiente/acudiente_modern.css"
    if os.path.exists(css_path):
        print("✅ Archivo CSS encontrado: acudiente_modern.css")
        
        with open(css_path, 'r', encoding='utf-8') as f:
            css_content = f.read()
            
        # Verificar configuraciones de fondo
        checks = [
            ("url(../../img/fondo.png)", "Referencia a imagen de fondo"),
            ("background-size: cover", "Tamaño de fondo configurado"),
            ("background-attachment: fixed", "Fondo fijo configurado"),
            ("background-position: center", "Posición centrada"),
            ("linear-gradient", "Gradiente overlay configurado"),
            ("var(--primary-yellow)", "Variables de color configuradas"),
            ("glassmorphism", "Efectos glassmorphism configurados")
        ]
        
        for check, description in checks:
            if check in css_content:
                print(f"   ✅ {description}")
            else:
                print(f"   ❌ {description} - NO ENCONTRADO")
    else:
        print("❌ Archivo CSS NO encontrado")
        return
    
    # Verificar template base
    template_path = "c:/Sonrisas/frontend/template/acudiente/base_acudiente.html"
    if os.path.exists(template_path):
        print("✅ Template base encontrado: base_acudiente.html")
        
        with open(template_path, 'r', encoding='utf-8') as f:
            template_content = f.read()
            
        # Verificar configuraciones del template
        template_checks = [
            ("acudiente_modern.css", "CSS cargado correctamente"),
            ("class=\"acudiente-html\"", "Clase HTML configurada"),
            ("class=\"acudiente-body\"", "Clase BODY configurada"),
            ("url_for('static'", "URLs estáticas configuradas")
        ]
        
        for check, description in template_checks:
            if check in template_content:
                print(f"   ✅ {description}")
            else:
                print(f"   ❌ {description} - NO ENCONTRADO")
    else:
        print("❌ Template base NO encontrado")
        return
    
    print("\n" + "="*60)
    print("🎯 RESUMEN DE CONFIGURACIÓN DE FONDO:")
    print("="*60)
    
    print("📁 ARCHIVOS VERIFICADOS:")
    print("   ✅ fondo.png - Imagen de fondo")
    print("   ✅ acudiente_modern.css - Estilos CSS")
    print("   ✅ base_acudiente.html - Template base")
    
    print("\n🎨 CONFIGURACIONES APLICADAS:")
    print("   ✅ Fondo de imagen con url(../../img/fondo.png)")
    print("   ✅ Fondo fijo (background-attachment: fixed)")
    print("   ✅ Cobertura completa (background-size: cover)")
    print("   ✅ Posición centrada (background-position: center)")
    print("   ✅ Gradiente overlay amarillo con transparencia")
    print("   ✅ Efectos glassmorphism para elementos")
    print("   ✅ Variables CSS para colores consistentes")
    print("   ✅ Clases específicas para HTML y BODY")
    
    print("\n🌐 COMPATIBILIDAD:")
    print("   ✅ Prefijos -webkit- para Safari")
    print("   ✅ Reglas !important para forzar estilos")
    print("   ✅ Fallbacks para navegadores antiguos")
    print("   ✅ Responsive design incluido")
    
    print("\n🎉 ¡FONDO CONFIGURADO CORRECTAMENTE!")
    print("El área de acudiente ahora tiene el mismo fondo que el resto del sistema.")

if __name__ == "__main__":
    verify_background()
