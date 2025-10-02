// Inicializar EmailJS
(function() {
    // Reemplaza "TU_USER_ID" con tu ID de usuario de EmailJS
    emailjs.init("service_r94rr6q");
})();

document.addEventListener('DOMContentLoaded', function() {
    const formulario = document.getElementById('registro-form');
    const btnEnviar = document.getElementById('btn-enviar');
    
    // Verificar si existe un spinner en el botón, si no, crearlo
    let spinner = btnEnviar.querySelector('.spinner');
    if (!spinner) {
        spinner = document.createElement('span');
        spinner.className = 'spinner hidden';
        btnEnviar.appendChild(spinner);
    }
    
    const btnText = btnEnviar.querySelector('.btn-text') || btnEnviar;

    formulario.addEventListener('submit', function(event) {
        event.preventDefault();
        
        // Mostrar spinner y deshabilitar botón
        spinner.classList.remove('hidden');
        if (btnText.textContent) {
            btnText.textContent = 'Enviando...';
        } else {
            btnEnviar.textContent = 'Enviando...';
        }
        btnEnviar.disabled = true;
        
        // Obtener los datos del formulario
        const nombre = document.getElementById('nombre').value;
        const correo = document.getElementById('correo').value;
        const celular = document.getElementById('celular').value;
        const colegio = document.getElementById('Nomb_Col').value;
        const estudiantes = document.getElementById('estudiantes').value;
        
        // Crear mensaje de alerta para mostrar después
        function crearAlerta(tipo, mensaje) {
            const alertaDiv = document.createElement('div');
            alertaDiv.className = `alert alert-${tipo}`;
            alertaDiv.innerHTML = `
                ${mensaje}
                <button type="button" class="btn-close">&times;</button>
            `;
            
            // Agregar evento para cerrar la alerta
            alertaDiv.querySelector('.btn-close').addEventListener('click', function() {
                alertaDiv.remove();
            });
            
            // Agregar la alerta antes del formulario
            formulario.parentNode.insertBefore(alertaDiv, formulario);
            
            // Eliminar automáticamente después de 5 segundos
            setTimeout(() => {
                if (alertaDiv.parentNode) {
                    alertaDiv.remove();
                }
            }, 5000);
        }
        
        // Preparar los parámetros para EmailJS
        const templateParams = {
            nombre: nombre,
            correo: correo,
            celular: celular,
            colegio: colegio,
            estudiantes: estudiantes,
            to_email: "teachingnote7@gmail.com" // Reemplaza con tu correo
        };
        
        // Enviar el correo electrónico
        // Reemplaza "TU_SERVICE_ID" y "TU_TEMPLATE_ID" con tus IDs de EmailJS
        emailjs.send("TU_SERVICE_ID", "TU_TEMPLATE_ID", templateParams)
            .then(function(response) {
                console.log('Correo enviado con éxito:', response);
                
                // Ocultar spinner y habilitar botón
                spinner.classList.add('hidden');
                if (btnText.textContent) {
                    btnText.textContent = 'Enviar solicitud';
                } else {
                    btnEnviar.textContent = 'Enviar solicitud';
                }
                btnEnviar.disabled = false;
                
                // Mostrar mensaje de éxito
                crearAlerta('success', '¡Gracias por registrarte! Te contactaremos pronto.');
                
                // Limpiar el formulario
                formulario.reset();
            })
            .catch(function(error) {
                console.error('Error al enviar el correo:', error);
                
                // Ocultar spinner y habilitar botón
                spinner.classList.add('hidden');
                if (btnText.textContent) {
                    btnText.textContent = 'Enviar solicitud';
                } else {
                    btnEnviar.textContent = 'Enviar solicitud';
                }
                btnEnviar.disabled = false;
                
                // Mostrar mensaje de error
                crearAlerta('danger', 'Hubo un error al enviar tu solicitud. Por favor, intenta de nuevo más tarde.');
            });
    });
    
    // Agregar evento para cerrar las alertas existentes
    document.querySelectorAll('.btn-close').forEach(btn => {
        btn.addEventListener('click', function() {
            this.parentElement.remove();
        });
    });
});