// Animación de despliegue/guardado para tarjetas glass en inicio (independiente y sin expandir vacías)

document.addEventListener('DOMContentLoaded', function() {
  const cards = document.querySelectorAll('.info-toggle-card');
  cards.forEach(card => {
    const content = card.querySelector('.card-content');
    const inner = content.firstElementChild;
    card.style.transition = 'box-shadow 0.3s, transform 0.3s, background 0.3s, min-height 0.5s cubic-bezier(.4,0,.2,1)';
    content.style.transition = 'opacity 0.4s, max-height 0.5s cubic-bezier(.4,0,.2,1), padding 0.3s';
    content.style.overflow = 'hidden';
    content.style.maxHeight = '0';
    content.style.opacity = '0';
    content.style.padding = '0';
    content.style.display = 'none';
    card.style.minHeight = '70px';
    if(inner) inner.style.margin = '0';
    card.setAttribute('data-expanded', 'false');
    card.addEventListener('click', function() {
      const isExpanded = card.getAttribute('data-expanded') === 'true';
      const hasContent = content && content.textContent.trim().length > 0;
      if (!isExpanded && hasContent) {
        card.style.background = 'rgba(255,255,255,0.32)';
        card.style.boxShadow = '0 16px 40px 0 rgba(110,142,251,0.28)';
        content.style.display = 'block';
        setTimeout(() => {
          content.style.maxHeight = '400px';
          content.style.opacity = '1';
          content.style.padding = '16px 8px 18px 8px';
        }, 10);
        if(inner) inner.style.margin = '0';
        card.style.transform = 'scale(1.03)';
        card.style.minHeight = '220px';
        card.setAttribute('data-expanded', 'true');
      } else {
        card.style.background = '';
        card.style.boxShadow = '';
        content.style.maxHeight = '0';
        content.style.opacity = '0';
        content.style.padding = '0';
        if(inner) inner.style.margin = '0';
        card.style.transform = 'scale(1)';
        card.style.minHeight = '70px';
        card.setAttribute('data-expanded', 'false');
        setTimeout(() => {
          content.style.display = 'none';
        }, 400); // Espera a que termine la transición
      }
    });
  });
}); 