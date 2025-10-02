document.addEventListener('DOMContentLoaded', function() {
    // Seleccionar todos los encabezados de las tarjetas que tienen la clase 'info-header'
    const cardHeaders = document.querySelectorAll('.info-header');

    // Iterar sobre cada encabezado encontrado
    cardHeaders.forEach(header => {
        // Añadir un "escuchador de eventos" para el clic en cada encabezado
        header.addEventListener('click', function() {
            // 'this' se refiere al 'header' que fue clicado.
            // 'closest('.info-card')' busca el ancestro más cercano con la clase 'info-card'.
            // Esto asegura que estamos trabajando solo dentro de la tarjeta que fue clicada.
            const infoCard = this.closest('.info-card');
            
            // Dentro de esa tarjeta específica, encuentra el icono.
            const icon = this.querySelector('.icon');

            // Alternar la clase 'active' en la tarjeta principal.
            // Esto controlará la expansión/contracción de la altura y el padding.
            infoCard.classList.toggle('active');
            
            // Alternar la clase 'rotated' en el icono para animar la flecha.
            icon.classList.toggle('rotated');

            // Importante: NO hay lógica aquí para cerrar otras tarjetas.
            // Cada tarjeta se maneja de forma completamente individual.
        });
    });
});
