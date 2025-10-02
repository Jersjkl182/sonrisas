/* =======================================
JAVASCRIPT MODERNO PARA TARJETAS DESPLEGABLES
Página de Inicio - Teaching Notes
======================================= */

document.addEventListener('DOMContentLoaded', function() {
    const cards = document.querySelectorAll('.info-toggle-card');

    cards.forEach((card, index) => {
        const content = card.querySelector('.card-content');
        const title = card.querySelector('h2');
        initializeCard(card, content, index);
        card.addEventListener('click', () => toggleCard(card, content));
        card.addEventListener('keydown', (e) => {
            if (e.key === 'Enter' || e.key === ' ') {
                e.preventDefault();
                toggleCard(card, content);
            }
        });
        card.addEventListener('mouseenter', () => addHoverEffect(card));
        card.addEventListener('mouseleave', () => removeHoverEffect(card));
    });

    function initializeCard(card, content, index) {
        card.setAttribute('data-expanded', 'false');
        card.setAttribute('tabindex', '0');
        card.setAttribute('role', 'button');
        card.setAttribute('aria-expanded', 'false');
        card.setAttribute('aria-label', `Expandir información: ${card.querySelector('h2').textContent}`);
        content.style.maxHeight = '0';
        content.style.opacity = '0';
        content.style.padding = '0';
        content.style.marginTop = '0';
        content.style.overflow = 'hidden';
        card.style.animationDelay = `${0.6 + (index * 0.1)}s`;
        addClickIndicator(card);
    }

    function toggleCard(card, content) {
        const isExpanded = card.getAttribute('data-expanded') === 'true';
        const hasContent = content && content.textContent.trim().length > 0;
        if (!hasContent) return; // No expandir si está vacía
        if (!isExpanded) {
            expandCard(card, content);
        } else {
            collapseCard(card, content);
        }
    }

    function expandCard(card, content) {
        card.setAttribute('data-expanded', 'true');
        card.setAttribute('aria-expanded', 'true');
        card.classList.add('expanded');
        card.style.background = 'rgba(255, 255, 255, 0.35)';
        card.style.boxShadow = '0 16px 40px rgba(110, 142, 251, 0.3)';
        card.style.borderColor = 'rgba(110, 142, 251, 0.6)';
        card.style.transform = 'translateY(-4px) scale(1.03)';
        card.style.minHeight = '250px';
        content.style.display = 'block';
        setTimeout(() => {
            content.style.maxHeight = '400px';
            content.style.opacity = '1';
            content.style.padding = '16px 0 8px 0';
            content.style.marginTop = '16px';
        }, 10);
        createRippleEffect(card);
        updateClickIndicator(card, true);
    }

    function collapseCard(card, content) {
        card.setAttribute('data-expanded', 'false');
        card.setAttribute('aria-expanded', 'false');
        card.classList.remove('expanded');
        card.style.background = '';
        card.style.boxShadow = '';
        card.style.borderColor = '';
        card.style.transform = '';
        card.style.minHeight = '';
        content.style.maxHeight = '0';
        content.style.opacity = '0';
        content.style.padding = '0';
        content.style.marginTop = '0';
        setTimeout(() => {
            content.style.display = 'none';
        }, 500);
        updateClickIndicator(card, false);
    }

    function addHoverEffect(card) {
        if (card.getAttribute('data-expanded') !== 'true') {
            card.style.transform = 'translateY(-2px) scale(1.01)';
            card.style.boxShadow = '0 8px 25px rgba(110, 142, 251, 0.25)';
        }
    }
    function removeHoverEffect(card) {
        if (card.getAttribute('data-expanded') !== 'true') {
            card.style.transform = '';
            card.style.boxShadow = '';
        }
    }
    function createRippleEffect(card) {
        const ripple = document.createElement('span');
        const rect = card.getBoundingClientRect();
        const size = Math.max(rect.width, rect.height);
        ripple.style.cssText = `
            position: absolute;
            width: ${size}px;
            height: ${size}px;
            left: 50%;
            top: 50%;
            transform: translate(-50%, -50%) scale(0);
            background: rgba(255, 255, 255, 0.3);
            border-radius: 50%;
            animation: ripple 0.6s linear;
            pointer-events: none;
            z-index: 1;
        `;
        card.appendChild(ripple);
        setTimeout(() => {
            ripple.remove();
        }, 600);
    }
    function addClickIndicator(card) {
        const indicator = document.createElement('div');
        indicator.className = 'click-indicator';
        indicator.innerHTML = '<i class="fas fa-chevron-down"></i>';
        indicator.style.cssText = `
            position: absolute;
            top: 20px;
            right: 20px;
            color: rgba(255, 255, 255, 0.7);
            font-size: 0.9rem;
            transition: all 0.3s ease;
            pointer-events: none;
        `;
        card.appendChild(indicator);
    }
    function updateClickIndicator(card, isExpanded) {
        const indicator = card.querySelector('.click-indicator');
        if (indicator) {
            if (isExpanded) {
                indicator.innerHTML = '<i class="fas fa-chevron-up"></i>';
                indicator.style.color = 'rgba(255, 255, 255, 0.9)';
                indicator.style.transform = 'rotate(180deg)';
            } else {
                indicator.innerHTML = '<i class="fas fa-chevron-down"></i>';
                indicator.style.color = 'rgba(255, 255, 255, 0.7)';
                indicator.style.transform = 'rotate(0deg)';
            }
        }
    }
    // Animaciones CSS dinámicas y accesibilidad igual que antes...
    const style = document.createElement('style');
    style.textContent = `
        @keyframes ripple {
            to {
                transform: translate(-50%, -50%) scale(4);
                opacity: 0;
            }
        }
        .glass-card { position: relative; overflow: hidden; }
        .glass-card::before {
            content: '';
            position: absolute;
            top: 0;
            left: -100%;
            width: 100%;
            height: 100%;
            background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.1), transparent);
            transition: left 0.5s;
            pointer-events: none;
        }
        .glass-card:hover::before { left: 100%; }
        .glass-card:focus-visible {
            outline: 2px solid rgba(255, 255, 255, 0.8);
            outline-offset: 2px;
        }
    `;
    document.head.appendChild(style);
    document.addEventListener('keydown', function(e) {
        if (e.key === 'Tab') {
            cards.forEach(card => {
                card.setAttribute('tabindex', '0');
            });
        }
    });
    // Animación de entrada escalonada para las tarjetas
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.style.opacity = '1';
                entry.target.style.transform = 'translateY(0)';
            }
        });
    }, observerOptions);
    cards.forEach(card => {
        observer.observe(card);
    });
    console.log('✅ JavaScript moderno para tarjetas de inicio cargado correctamente');
}); 