/* =======================================
JAVASCRIPT MODERNO PARA AUTENTICACIÓN
Mejoras en UX para formularios de registro y login
======================================= */

document.addEventListener('DOMContentLoaded', function() {
    
    // =======================================
    // MEJORAS EN INPUTS
    // =======================================
    
    // Efecto de focus mejorado para inputs
    const inputs = document.querySelectorAll('input[type="text"], input[type="email"], input[type="password"], input[type="tel"], input[type="number"]');
    
    inputs.forEach(input => {
        // Añadir clase cuando el input tiene contenido
        input.addEventListener('input', function() {
            if (this.value.length > 0) {
                this.classList.add('has-content');
            } else {
                this.classList.remove('has-content');
            }
        });
        
        // Efecto de focus con animación
        input.addEventListener('focus', function() {
            this.parentElement.classList.add('input-focused');
        });
        
        input.addEventListener('blur', function() {
            this.parentElement.classList.remove('input-focused');
        });
        
        // Validación en tiempo real para email
        if (input.type === 'email') {
            input.addEventListener('blur', function() {
                validateEmail(this);
            });
        }
        
        // Validación en tiempo real para teléfono
        if (input.type === 'tel') {
            input.addEventListener('input', function() {
                formatPhoneNumber(this);
            });
        }
        
        // Validación en tiempo real para número de estudiantes
        if (input.type === 'number' && input.id === 'estudiantes') {
            input.addEventListener('input', function() {
                validateStudentCount(this);
            });
        }
    });
    
    // =======================================
    // VALIDACIONES EN TIEMPO REAL
    // =======================================
    
    function validateEmail(input) {
        const email = input.value;
        const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        
        if (email && !emailRegex.test(email)) {
            showInputError(input, 'Por favor ingresa un correo electrónico válido');
        } else {
            clearInputError(input);
        }
    }
    
    function formatPhoneNumber(input) {
        let value = input.value.replace(/\D/g, '');
        
        // Limitar a 10 dígitos
        if (value.length > 10) {
            value = value.substring(0, 10);
        }
        
        // Formatear como XXX XXX XXXX
        if (value.length >= 6) {
            value = value.substring(0, 3) + ' ' + value.substring(3, 6) + ' ' + value.substring(6);
        } else if (value.length >= 3) {
            value = value.substring(0, 3) + ' ' + value.substring(3);
        }
        
        input.value = value;
        
        // Validar longitud mínima
        if (value.length < 10 && value.length > 0) {
            showInputError(input, 'El número debe tener al menos 10 dígitos');
        } else {
            clearInputError(input);
        }
    }
    
    function validateStudentCount(input) {
        const count = parseInt(input.value);
        
        if (count < 1) {
            showInputError(input, 'Debe ser al menos 1 estudiante');
        } else if (count > 9999) {
            showInputError(input, 'El número máximo es 9999 estudiantes');
        } else {
            clearInputError(input);
        }
    }
    
    // =======================================
    // MANEJO DE ERRORES
    // =======================================
    
    function showInputError(input, message) {
        // Remover error anterior si existe
        clearInputError(input);
        
        // Crear elemento de error
        const errorElement = document.createElement('div');
        errorElement.className = 'input-error';
        errorElement.textContent = message;
        errorElement.style.cssText = `
            color: #dc2626;
            font-size: 0.8rem;
            margin-top: 4px;
            font-weight: 500;
            animation: slideInDown 0.3s ease-out;
        `;
        
        // Añadir clase de error al input
        input.classList.add('input-error-state');
        input.parentElement.appendChild(errorElement);
    }
    
    function clearInputError(input) {
        const errorElement = input.parentElement.querySelector('.input-error');
        if (errorElement) {
            errorElement.remove();
        }
        input.classList.remove('input-error-state');
    }
    
    // =======================================
    // MEJORAS EN BOTONES
    // =======================================
    
    const buttons = document.querySelectorAll('.btn-registrar, .btn2');
    
    buttons.forEach(button => {
        // Efecto de loading al hacer click
        button.addEventListener('click', function(e) {
            if (this.type === 'submit') {
                // Verificar si el formulario es válido
                const form = this.closest('form');
                if (form && !form.checkValidity()) {
                    e.preventDefault();
                    showFormErrors(form);
                    return;
                }
                
                // Añadir estado de loading
                this.classList.add('loading');
                const originalText = this.querySelector('span').textContent;
                this.querySelector('span').textContent = 'Procesando...';
                
                // Remover loading después de 3 segundos (fallback)
                setTimeout(() => {
                    this.classList.remove('loading');
                    this.querySelector('span').textContent = originalText;
                }, 3000);
            }
        });
        
        // Efecto de ripple
        button.addEventListener('click', function(e) {
            const ripple = document.createElement('span');
            const rect = this.getBoundingClientRect();
            const size = Math.max(rect.width, rect.height);
            const x = e.clientX - rect.left - size / 2;
            const y = e.clientY - rect.top - size / 2;
            
            ripple.style.cssText = `
                position: absolute;
                width: ${size}px;
                height: ${size}px;
                left: ${x}px;
                top: ${y}px;
                background: rgba(255, 255, 255, 0.3);
                border-radius: 50%;
                transform: scale(0);
                animation: ripple 0.6s linear;
                pointer-events: none;
            `;
            
            this.appendChild(ripple);
            
            setTimeout(() => {
                ripple.remove();
            }, 600);
        });
    });
    
    // =======================================
    // VALIDACIÓN DE FORMULARIOS
    // =======================================
    
    function showFormErrors(form) {
        const invalidInputs = form.querySelectorAll(':invalid');
        
        invalidInputs.forEach(input => {
            input.classList.add('input-error-state');
            
            // Mostrar mensaje de error específico
            let message = '';
            if (input.validity.valueMissing) {
                message = 'Este campo es obligatorio';
            } else if (input.validity.typeMismatch && input.type === 'email') {
                message = 'Por favor ingresa un correo electrónico válido';
            } else if (input.validity.rangeUnderflow && input.type === 'number') {
                message = 'El valor debe ser mayor a 0';
            } else if (input.validity.rangeOverflow && input.type === 'number') {
                message = 'El valor máximo es 9999';
            } else if (input.validity.patternMismatch && input.type === 'tel') {
                message = 'Por favor ingresa un número de teléfono válido';
            }
            
            if (message) {
                showInputError(input, message);
            }
        });
        
        // Scroll al primer error
        if (invalidInputs.length > 0) {
            invalidInputs[0].scrollIntoView({ behavior: 'smooth', block: 'center' });
        }
    }
    
    // =======================================
    // MEJORAS EN CHECKBOX
    // =======================================
    
    const checkboxes = document.querySelectorAll('input[type="checkbox"]');
    
    checkboxes.forEach(checkbox => {
        checkbox.addEventListener('change', function() {
            if (this.checked) {
                this.parentElement.classList.add('checked');
            } else {
                this.parentElement.classList.remove('checked');
            }
        });
    });
    
    // =======================================
    // ANIMACIONES CSS
    // =======================================
    
    // Añadir estilos CSS dinámicamente
    const style = document.createElement('style');
    style.textContent = `
        @keyframes ripple {
            to {
                transform: scale(4);
                opacity: 0;
            }
        }
        
        @keyframes slideInDown {
            from {
                opacity: 0;
                transform: translateY(-10px);
            }
            to {
                opacity: 1;
                transform: translateY(0);
            }
        }
        
        .input-error-state {
            border-color: #dc2626 !important;
            box-shadow: 0 0 0 4px rgba(220, 38, 38, 0.15) !important;
        }
        
        .btn-registrar.loading,
        .btn2.loading {
            pointer-events: none;
            opacity: 0.8;
        }
        
        .input-focused {
            transform: translateY(-2px);
        }
        
        .has-content {
            border-color: #6e8efb !important;
        }
    `;
    document.head.appendChild(style);
    
    // =======================================
    // MEJORAS EN MENSAJES FLASH
    // =======================================
    
    const flashMessages = document.querySelectorAll('.flash-messages .success, .flash-messages .error, .flash-messages .info, ul.flashes li');
    
    flashMessages.forEach(message => {
        // Auto-ocultar mensajes después de 5 segundos
        setTimeout(() => {
            message.style.animation = 'slideOutUp 0.5s ease-out forwards';
            setTimeout(() => {
                message.remove();
            }, 500);
        }, 5000);
        
        // Botón para cerrar mensaje
        const closeButton = document.createElement('button');
        closeButton.innerHTML = '&times;';
        closeButton.style.cssText = `
            position: absolute;
            right: 10px;
            top: 50%;
            transform: translateY(-50%);
            background: none;
            border: none;
            font-size: 1.2rem;
            cursor: pointer;
            color: inherit;
            opacity: 0.7;
            transition: opacity 0.3s;
        `;
        
        closeButton.addEventListener('click', () => {
            message.remove();
        });
        
        closeButton.addEventListener('mouseenter', () => {
            closeButton.style.opacity = '1';
        });
        
        closeButton.addEventListener('mouseleave', () => {
            closeButton.style.opacity = '0.7';
        });
        
        message.style.position = 'relative';
        message.appendChild(closeButton);
    });
    
    // =======================================
    // MEJORAS DE ACCESIBILIDAD
    // =======================================
    
    // Navegación por teclado mejorada
    document.addEventListener('keydown', function(e) {
        if (e.key === 'Enter' && e.target.tagName === 'INPUT') {
            const form = e.target.closest('form');
            if (form) {
                const submitButton = form.querySelector('button[type="submit"]');
                if (submitButton) {
                    submitButton.click();
                }
            }
        }
    });
    
    // Focus visible mejorado
    const focusableElements = document.querySelectorAll('input, button, a, select, textarea');
    
    focusableElements.forEach(element => {
        element.addEventListener('focus', function() {
            this.style.outline = '2px solid #6e8efb';
            this.style.outlineOffset = '2px';
        });
        
        element.addEventListener('blur', function() {
            this.style.outline = '';
            this.style.outlineOffset = '';
        });
    });
    
    console.log('✅ JavaScript moderno para autenticación cargado correctamente');
}); 