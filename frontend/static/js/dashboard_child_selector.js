/* =======================================
SELECTOR DE HIJOS EN EL DASHBOARD
JavaScript para el selector movido al header
======================================= */

// Variables globales para el selector
let selectedChildId = null;
let childrenData = [];
let childrenToggle = null;
let childrenDropdown = null;

// Función para inicializar el selector cuando se carga el dashboard
function initializeDashboardChildSelector() {
    childrenToggle = document.getElementById('childrenToggle');
    childrenDropdown = document.getElementById('childrenDropdown');
    
    if (childrenToggle && childrenDropdown) {
        setupChildSelectorEvents();
        loadChildren();
        console.log('✅ Selector de hijos del dashboard inicializado');
    }
}

// Configurar eventos del selector - Versión mejorada sin conflictos
function setupChildSelectorEvents() {
    let isOpen = false;
    let clickInProgress = false;
    
    // Función para abrir dropdown
    function openDropdown() {
        console.log('📂 ABRIENDO dropdown');
        isOpen = true;
        
        // Mostrar dropdown
        childrenDropdown.style.display = 'block';
        childrenToggle.classList.add('active');
        
        // Animación
        setTimeout(() => {
            childrenDropdown.style.transform = 'translateY(0) scale(1)';
            childrenDropdown.style.opacity = '1';
        }, 10);
        
        // Rotar ícono
        const toggleIcon = childrenToggle.querySelector('.toggle-icon');
        if (toggleIcon) {
            toggleIcon.style.transform = 'rotate(180deg)';
        }
    }
    
    function closeDropdown() {
        console.log('📁 CERRANDO dropdown');
        isOpen = false;
        
        childrenToggle.classList.remove('active');
        
        // Animación de salida
        childrenDropdown.style.transform = 'translateY(-10px) scale(0.95)';
        childrenDropdown.style.opacity = '0';
        
        setTimeout(() => {
            childrenDropdown.style.display = 'none';
        }, 300);
        
        // Resetear ícono
        const toggleIcon = childrenToggle.querySelector('.toggle-icon');
        if (toggleIcon) {
            toggleIcon.style.transform = 'rotate(0deg)';
        }
    }
    
    // Click en el botón selector
    childrenToggle.addEventListener('click', function(e) {
        e.preventDefault();
        e.stopPropagation();
        
        clickInProgress = true;
        
        console.log('🔄 Click en botón, estado:', isOpen);
        
        // Cargar hijos si no se han cargado
        if (childrenData.length === 0) {
            console.log('📥 Cargando hijos...');
            const dropdownContent = childrenDropdown.querySelector('.dropdown-content');
            if (dropdownContent) {
                dropdownContent.innerHTML = `
                    <div class="dropdown-loading" style="padding: 30px 20px; text-align: center;">
                        <div class="loading-spinner">
                            <div class="spinner"></div>
                        </div>
                        <span style="color: #7f8c8d; font-size: 13px; margin-top: 10px; display: block;">Cargando estudiantes...</span>
                    </div>
                `;
            }
            loadChildren();
        }
        
        if (isOpen) {
            closeDropdown();
        } else {
            openDropdown();
        }
        
        // Reset flag después de delay
        setTimeout(() => {
            clickInProgress = false;
        }, 50);
    });
    
    // Prevenir que clicks dentro del dropdown lo cierren
    childrenDropdown.addEventListener('click', function(e) {
        e.stopPropagation();
        console.log('🔒 Click dentro del dropdown');
    });
    
    // Cerrar dropdown al hacer click fuera
    document.addEventListener('click', function(e) {
        if (!clickInProgress && isOpen) {
            if (!childrenToggle.contains(e.target) && !childrenDropdown.contains(e.target)) {
                console.log('🌍 Click fuera - cerrando');
                closeDropdown();
            }
        }
    });
    
    // Cerrar dropdown al presionar Escape
    document.addEventListener('keydown', function(e) {
        if (e.key === 'Escape' && isOpen) {
            closeDropdown();
        }
    });
    
    // Exponer funciones globalmente
    window.showDashboardChildSelector = openDropdown;
    window.hideDashboardChildSelector = closeDropdown;
}

// Cargar hijos desde la API
async function loadChildren() {
    try {
        const dropdownContent = childrenDropdown.querySelector('.dropdown-content');
        if (dropdownContent) {
            dropdownContent.innerHTML = `
                <div class="dropdown-loading" style="padding: 30px 20px; text-align: center;">
                    <div class="loading-spinner">
                        <div class="spinner"></div>
                    </div>
                    <span style="color: #7f8c8d; font-size: 13px; margin-top: 10px; display: block;">Cargando estudiantes...</span>
                </div>
            `;
        }
        
        const controller = new AbortController();
        const timeoutId = setTimeout(() => controller.abort(), 10000);
        
        const response = await fetch('/acudiente/api/hijos-temp', {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
                'Accept': 'application/json'
            },
            signal: controller.signal
        });
        
        clearTimeout(timeoutId);
        
        if (!response.ok) {
            throw new Error(`Error del servidor: ${response.status} - ${response.statusText}`);
        }
        
        const data = await response.json();
        
        if (data.error) {
            throw new Error(data.error);
        }
        
        childrenData = data.hijos || [];
        
        // Si no hay datos del servidor, usar datos de prueba
        if (childrenData.length === 0) {
            childrenData = [
                { id: 1, nombre: 'Angelo Curiel', grado: 'Preescolar' },
                { id: 2, nombre: 'María García', grado: 'Primero' },
                { id: 3, nombre: 'Juan Pérez', grado: 'Segundo' }
            ];
        }
        
        renderChildrenDropdown();
        
    } catch (error) {
        console.error('Error loading children:', error);
        
        // Si es un error de conexión, usar datos de prueba como fallback
        if (error.name === 'AbortError' || error.message.includes('fetch')) {
            childrenData = [
                { id: 1, nombre: 'Angelo Curiel', grado: 'Preescolar' },
                { id: 2, nombre: 'María García', grado: 'Primero' },
                { id: 3, nombre: 'Juan Pérez', grado: 'Segundo' }
            ];
            renderChildrenDropdown();
            return;
        }
        
        // Mostrar error en el contenido del dropdown
        const dropdownContent = childrenDropdown.querySelector('.dropdown-content');
        if (dropdownContent) {
            dropdownContent.innerHTML = `
                <div class="dropdown-error" style="padding: 30px 20px; text-align: center; color: #e74c3c;">
                    <i class="fas fa-exclamation-triangle" style="font-size: 24px; margin-bottom: 10px;"></i>
                    <div style="font-size: 14px; margin-bottom: 10px;">Error de conexión</div>
                    <div style="font-size: 12px; color: #7f8c8d; margin-bottom: 15px;">
                        ${error.message || 'No se pudo conectar con el servidor'}
                    </div>
                    <button onclick="loadChildren()" style="
                        padding: 8px 16px;
                        background: var(--primary-yellow);
                        color: white;
                        border: none;
                        border-radius: 8px;
                        cursor: pointer;
                        font-size: 12px;
                        margin-right: 8px;
                    ">
                        <i class="fas fa-redo" style="margin-right: 4px;"></i>
                        Reintentar
                    </button>
                    <button onclick="useFallbackData()" style="
                        padding: 8px 16px;
                        background: #3498db;
                        color: white;
                        border: none;
                        border-radius: 8px;
                        cursor: pointer;
                        font-size: 12px;
                    ">
                        <i class="fas fa-database" style="margin-right: 4px;"></i>
                        Usar datos de prueba
                    </button>
                </div>
            `;
        }
    }
}

// Renderizar dropdown de hijos
function renderChildrenDropdown() {
    const dropdownContent = childrenDropdown.querySelector('.dropdown-content');
    
    if (childrenData.length === 0) {
        dropdownContent.innerHTML = `
            <div class="dropdown-empty" style="padding: 30px 20px; text-align: center; color: #7f8c8d;">
                <i class="fas fa-info-circle" style="font-size: 24px; margin-bottom: 10px; color: var(--primary-yellow);"></i>
                <div>Sin estudiantes registrados</div>
            </div>
        `;
        return;
    }
    
    let html = '';
    childrenData.forEach((child, index) => {
        html += `
            <div class="student-item" data-child-id="${child.id}" style="
                display: flex;
                align-items: center;
                gap: 12px;
                padding: 12px 20px;
                cursor: pointer;
                transition: all 0.2s ease;
                border-bottom: 1px solid rgba(0, 0, 0, 0.05);
                animation: fadeInUp 0.3s ease-out ${index * 0.1}s both;
            ">
                <div class="student-avatar" style="
                    width: 32px;
                    height: 32px;
                    background: var(--primary-yellow);
                    border-radius: 50%;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    color: white;
                    font-size: 12px;
                    flex-shrink: 0;
                ">
                    <i class="fas fa-user-graduate"></i>
                </div>
                <div class="student-info" style="flex: 1; min-width: 0;">
                    <div class="student-name" style="
                        font-weight: 600;
                        color: #2c3e50;
                        font-size: 13px;
                        margin-bottom: 2px;
                        white-space: nowrap;
                        overflow: hidden;
                        text-overflow: ellipsis;
                    ">${child.nombre}</div>
                    <div class="student-grade" style="
                        font-size: 11px;
                        color: var(--primary-yellow);
                        font-weight: 500;
                    ">${child.grado}</div>
                </div>
                <div class="select-indicator" style="
                    width: 16px;
                    height: 16px;
                    border: 2px solid #ddd;
                    border-radius: 50%;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    transition: all 0.2s ease;
                ">
                    <i class="fas fa-check" style="font-size: 8px; color: #27ae60; opacity: 0;"></i>
                </div>
            </div>
        `;
    });
    
    dropdownContent.innerHTML = html;
    
    // Agregar event listeners y efectos hover
    const studentItems = dropdownContent.querySelectorAll('.student-item');
    studentItems.forEach(item => {
        // Hover effects
        item.addEventListener('mouseenter', function() {
            this.style.background = 'rgba(246, 218, 99, 0.1)';
            this.style.transform = 'translateX(4px)';
            const indicator = this.querySelector('.select-indicator');
            indicator.style.borderColor = 'var(--primary-yellow)';
            indicator.style.background = 'rgba(246, 218, 99, 0.1)';
        });
        
        item.addEventListener('mouseleave', function() {
            this.style.background = 'transparent';
            this.style.transform = 'translateX(0)';
            const indicator = this.querySelector('.select-indicator');
            indicator.style.borderColor = '#ddd';
            indicator.style.background = 'transparent';
        });
        
        // Click event
        item.addEventListener('click', function() {
            const childId = parseInt(this.dataset.childId);
            
            // Animación de selección
            const checkIcon = this.querySelector('.fas.fa-check');
            const indicator = this.querySelector('.select-indicator');
            
            indicator.style.background = '#27ae60';
            indicator.style.borderColor = '#27ae60';
            checkIcon.style.opacity = '1';
            checkIcon.style.color = 'white';
            
            setTimeout(() => {
                selectChild(childId);
            }, 300);
        });
    });
}

// Seleccionar hijo
function selectChild(childId) {
    const child = childrenData.find(c => c.id === childId);
    if (!child) return;
    
    selectedChildId = childId;
    
    // Actualizar texto del botón selector
    const selectorText = childrenToggle.querySelector('.selector-text');
    if (selectorText) {
        selectorText.style.opacity = '0';
        setTimeout(() => {
            selectorText.textContent = child.nombre;
            selectorText.style.opacity = '1';
        }, 150);
    }
    
    // Cerrar dropdown usando la función global
    if (window.hideDashboardChildSelector) {
        window.hideDashboardChildSelector();
    }
    
    // Disparar evento personalizado para el dashboard
    const event = new CustomEvent('childSelected', {
        detail: { childId: childId, child: child }
    });
    document.dispatchEvent(event);
    
    console.log('✅ Hijo seleccionado:', child.nombre);
}

// Función para usar datos de prueba como fallback
window.useFallbackData = function() {
    childrenData = [
        { id: 1, nombre: 'Angelo Curiel', grado: 'Preescolar' },
        { id: 2, nombre: 'María García', grado: 'Primero' },
        { id: 3, nombre: 'Juan Pérez', grado: 'Segundo' }
    ];
    renderChildrenDropdown();
};

// Exponer función para uso global
window.loadChildren = loadChildren;

// Inicializar cuando el DOM esté listo
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initializeDashboardChildSelector);
} else {
    initializeDashboardChildSelector();
}

console.log('📦 Módulo de selector de hijos del dashboard cargado');
