/* =============================
JS EXTRA PARA PÁGINA DE INICIO
Contadores animados y slider de testimonios
============================= */

document.addEventListener('DOMContentLoaded', () => {
    /* ---------- CONTADORES ---------- */
    const counters = document.querySelectorAll('.counter');
    const speed = 50; // menor = más rápido
    const startCounting = (counter) => {
        const target = +counter.getAttribute('data-count');
        const update = () => {
            const current = +counter.innerText;
            const increment = Math.ceil(target / speed);
            if (current < target) {
                counter.innerText = current + increment;
                setTimeout(update, 30);
            } else {
                counter.innerText = target;
            }
        };
        update();
    };
    const counterObserver = new IntersectionObserver((entries, obs) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                startCounting(entry.target);
                obs.unobserve(entry.target);
            }
        });
    }, { threshold: 0.6 });
    counters.forEach(c => counterObserver.observe(c));

    /* ---------- SLIDER TESTIMONIOS ---------- */
    const testimonials = document.querySelectorAll('.testimonials-section .testimonial');
    let current = 0;
    const cycleTestimonials = () => {
        testimonials[current].classList.remove('active');
        current = (current + 1) % testimonials.length;
        testimonials[current].classList.add('active');
    };
    if (testimonials.length > 1) {
        setInterval(cycleTestimonials, 6000);
    }
    console.log('✅ JS extra de inicio cargado');

    /* ---------- ENTRY ANIMATIONS FOR HERO ---------- */
    const fadeElems = document.querySelectorAll('.fade-init');
    const observer = new IntersectionObserver(entries => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.remove('fade-init');
                entry.target.classList.add('fade-in');
                observer.unobserve(entry.target);
            }
        });
    }, { threshold: 0.1 });
    fadeElems.forEach(el => {
        observer.observe(el);
        // fallback: si ya está visible, fuerza animación
        const rect = el.getBoundingClientRect();
        if (rect.top < window.innerHeight) {
            el.classList.remove('fade-init');
            el.classList.add('fade-in');
        }
    });

    /* ---------- FAQ ACCORDION ---------- */
    const faqItems = document.querySelectorAll('.faq-item');
    faqItems.forEach(item => {
        const btn = item.querySelector('.faq-question');
        btn.addEventListener('click', () => {
            item.classList.toggle('open');
        });
    });
});
