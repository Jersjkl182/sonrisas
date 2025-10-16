// =====================================================
// JAVASCRIPT PARA SISTEMA DE LECTURA DE OBSERVACIONES
// =====================================================

class ObservacionesLectura {
    constructor() {
        this.init();
    }

    init() {
        this.bindEvents();
        this.loadEstadisticas();
    }

    bindEvents() {
        // Event listeners para botones de lectura
        document.addEventListener('click', (e) => {
            if (e.target.classList.contains('btn-toggle-lectura')) {
                e.preventDefault();
                const observacionId = e.target.dataset.observacionId;
                this.toggleLectura(observacionId, e.target);
            }
            
            if (e.target.classList.contains('btn-marcar-leido')) {
                e.preventDefault();
                const observacionId = e.target.dataset.observacionId;
                this.marcarComoLeido(observacionId, e.target);
            }
            
            if (e.target.classList.contains('btn-marcar-no-leido')) {
                e.preventDefault();
                const observacionId = e.target.dataset.observacionId;
                this.marcarComoNoLeido(observacionId, e.target);
            }
        });
    }

    async toggleLectura(observacionId, button) {
        try {
            this.showLoading(button);
            
            const response = await fetch(`/lectura/toggle_lectura/${observacionId}`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-Requested-With': 'XMLHttpRequest'
                }
            });

            const data = await response.json();

            if (data.success) {
                this.updateEstadoVisual(observacionId, data.leido);
                this.showNotification(data.message, 'success');
                this.loadEstadisticas(); // Actualizar estadísticas
            } else {
                this.showNotification(data.error || 'Error al cambiar estado', 'error');
            }
        } catch (error) {
            console.error('Error:', error);
            this.showNotification('Error de conexión', 'error');
        } finally {
            this.hideLoading(button);
        }
    }

    async marcarComoLeido(observacionId, button) {
        try {
            this.showLoading(button);
            
            const response = await fetch(`/lectura/marcar_leido/${observacionId}`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-Requested-With': 'XMLHttpRequest'
                }
            });

            const data = await response.json();

            if (data.success) {
                this.updateEstadoVisual(observacionId, true);
                this.showNotification(data.message, 'success');
                this.loadEstadisticas();
            } else {
                this.showNotification(data.error || 'Error al marcar como leído', 'error');
            }
        } catch (error) {
            console.error('Error:', error);
            this.showNotification('Error de conexión', 'error');
        } finally {
            this.hideLoading(button);
        }
    }

    async marcarComoNoLeido(observacionId, button) {
        try {
            this.showLoading(button);
            
            const response = await fetch(`/lectura/marcar_no_leido/${observacionId}`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-Requested-With': 'XMLHttpRequest'
                }
            });

            const data = await response.json();

            if (data.success) {
                this.updateEstadoVisual(observacionId, false);
                this.showNotification(data.message, 'success');
                this.loadEstadisticas();
            } else {
                this.showNotification(data.error || 'Error al marcar como no leído', 'error');
            }
        } catch (error) {
            console.error('Error:', error);
            this.showNotification('Error de conexión', 'error');
        } finally {
            this.hideLoading(button);
        }
    }

    updateEstadoVisual(observacionId, leido) {
        // Actualizar el indicador de estado
        const estadoElement = document.querySelector(`[data-observacion-id="${observacionId}"] .estado-lectura`);
        if (estadoElement) {
            if (leido) {
                estadoElement.innerHTML = '<i class="fas fa-eye text-success"></i> Leído';
                estadoElement.className = 'estado-lectura badge badge-success';
            } else {
                estadoElement.innerHTML = '<i class="fas fa-eye-slash text-warning"></i> No leído';
                estadoElement.className = 'estado-lectura badge badge-warning';
            }
        }

        // Actualizar botones de acción
        const toggleButton = document.querySelector(`[data-observacion-id="${observacionId}"].btn-toggle-lectura`);
        if (toggleButton) {
            if (leido) {
                toggleButton.innerHTML = '<i class="fas fa-eye-slash"></i> Marcar no leído';
                toggleButton.className = 'btn btn-sm btn-warning btn-toggle-lectura';
            } else {
                toggleButton.innerHTML = '<i class="fas fa-eye"></i> Marcar leído';
                toggleButton.className = 'btn btn-sm btn-success btn-toggle-lectura';
            }
        }

        // Actualizar fila de la tabla si existe
        const row = document.querySelector(`tr[data-observacion-id="${observacionId}"]`);
        if (row) {
            if (leido) {
                row.classList.add('observacion-leida');
                row.classList.remove('observacion-no-leida');
            } else {
                row.classList.add('observacion-no-leida');
                row.classList.remove('observacion-leida');
            }
        }
    }

    async loadEstadisticas() {
        try {
            const response = await fetch('/lectura/estadisticas_lectura');
            const data = await response.json();

            if (data.success) {
                this.updateEstadisticasVisual(data.estadisticas);
            }
        } catch (error) {
            console.error('Error al cargar estadísticas:', error);
        }
    }

    updateEstadisticasVisual(stats) {
        // Actualizar contadores
        const totalElement = document.getElementById('total-observaciones');
        const leidasElement = document.getElementById('observaciones-leidas');
        const noLeidasElement = document.getElementById('observaciones-no-leidas');
        const porcentajeElement = document.getElementById('porcentaje-leidas');

        if (totalElement) totalElement.textContent = stats.total;
        if (leidasElement) leidasElement.textContent = stats.leidas;
        if (noLeidasElement) noLeidasElement.textContent = stats.no_leidas;
        if (porcentajeElement) porcentajeElement.textContent = `${stats.porcentaje_leidas}%`;

        // Actualizar barra de progreso si existe
        const progressBar = document.getElementById('progress-lectura');
        if (progressBar) {
            progressBar.style.width = `${stats.porcentaje_leidas}%`;
            progressBar.setAttribute('aria-valuenow', stats.porcentaje_leidas);
        }
    }

    showLoading(button) {
        if (button) {
            button.disabled = true;
            button.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Procesando...';
        }
    }

    hideLoading(button) {
        if (button) {
            button.disabled = false;
            // El contenido se actualizará en updateEstadoVisual
        }
    }

    showNotification(message, type = 'info') {
        // Crear notificación toast
        const toast = document.createElement('div');
        toast.className = `alert alert-${type === 'error' ? 'danger' : type} alert-dismissible fade show position-fixed`;
        toast.style.cssText = 'top: 20px; right: 20px; z-index: 9999; min-width: 300px;';
        
        toast.innerHTML = `
            ${message}
            <button type="button" class="close" data-dismiss="alert">
                <span>&times;</span>
            </button>
        `;

        document.body.appendChild(toast);

        // Auto-remove después de 5 segundos
        setTimeout(() => {
            if (toast.parentNode) {
                toast.parentNode.removeChild(toast);
            }
        }, 5000);
    }

    // Método para marcar múltiples observaciones
    async marcarMultiplesComoLeidas(observacionIds) {
        const promises = observacionIds.map(id => 
            fetch(`/lectura/marcar_leido/${id}`, { method: 'POST' })
        );

        try {
            await Promise.all(promises);
            this.showNotification('Observaciones marcadas como leídas', 'success');
            this.loadEstadisticas();
            // Recargar la página o actualizar la lista
            location.reload();
        } catch (error) {
            this.showNotification('Error al marcar observaciones', 'error');
        }
    }

    // Método para filtrar observaciones por estado
    filtrarPorEstado(estado) {
        const rows = document.querySelectorAll('tr[data-observacion-id]');
        
        rows.forEach(row => {
            const esLeida = row.classList.contains('observacion-leida');
            
            if (estado === 'todas') {
                row.style.display = '';
            } else if (estado === 'leidas' && esLeida) {
                row.style.display = '';
            } else if (estado === 'no-leidas' && !esLeida) {
                row.style.display = '';
            } else {
                row.style.display = 'none';
            }
        });
    }
}

// Inicializar cuando el DOM esté listo
document.addEventListener('DOMContentLoaded', () => {
    window.observacionesLectura = new ObservacionesLectura();
});

// Funciones globales para usar en templates
function toggleLectura(observacionId) {
    if (window.observacionesLectura) {
        const button = document.querySelector(`[data-observacion-id="${observacionId}"].btn-toggle-lectura`);
        window.observacionesLectura.toggleLectura(observacionId, button);
    }
}

function marcarComoLeido(observacionId) {
    if (window.observacionesLectura) {
        const button = document.querySelector(`[data-observacion-id="${observacionId}"].btn-marcar-leido`);
        window.observacionesLectura.marcarComoLeido(observacionId, button);
    }
}

function marcarComoNoLeido(observacionId) {
    if (window.observacionesLectura) {
        const button = document.querySelector(`[data-observacion-id="${observacionId}"].btn-marcar-no-leido`);
        window.observacionesLectura.marcarComoNoLeido(observacionId, button);
    }
}
