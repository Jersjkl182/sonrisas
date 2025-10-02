/* =======================================
DASHBOARD UNIFICADO DE ACUDIENTE
JavaScript para funcionalidad completa
======================================= */

document.addEventListener('DOMContentLoaded', function() {
    
    // Variables globales
    let currentObservations = [];
    let selectedChildId = null;
    
    // Elementos del DOM
    const dashboardContent = document.getElementById('dashboardContent');
    const observationsContainer = document.getElementById('observationsContainer');
    const emptyObservations = document.getElementById('emptyObservations');
    
    // Escuchar evento de selección de hijo
    document.addEventListener('childSelected', function(event) {
        const { childId, child } = event.detail;
        selectedChildId = childId;
        
        // Cargar observaciones del hijo seleccionado
        loadObservationsForChild(childId);
    });
    
    // Función para cargar observaciones de un hijo
    async function loadObservationsForChild(childId) {
        try {
            showLoading();
            
            const response = await fetch(`/acudiente/api/observaciones/${childId}`);
            const data = await response.json();
            
            if (data.error) {
                showError('Error al cargar observaciones: ' + data.error);
                return;
            }
            
            currentObservations = data.observaciones || [];
            
            // Actualizar estadísticas
            updateStats(data.total || 0, data.positivas || 0, data.multimedia || 0);
            
            // Renderizar observaciones
            renderObservations(currentObservations);
            
        } catch (error) {
            console.error('Error loading observations:', error);
            showError('Error de conexión al cargar observaciones');
        }
    }
    
    // Función para actualizar estadísticas
    function updateStats(total, positivas, multimedia) {
        document.getElementById('totalObservations').textContent = total;
        document.getElementById('positiveObservations').textContent = positivas;
        document.getElementById('multimediaCount').textContent = multimedia;
    }
    
    // Función para renderizar observaciones
    function renderObservations(observations) {
        if (observations.length === 0) {
            observationsContainer.style.display = 'none';
            emptyObservations.style.display = 'block';
            return;
        }
        
        observationsContainer.style.display = 'block';
        emptyObservations.style.display = 'none';
        
        let html = '';
        observations.forEach(obs => {
            html += createObservationCard(obs);
        });
        
        observationsContainer.innerHTML = html;
    }
    
    // Función para crear tarjeta de observación
    function createObservationCard(obs) {
        const tipoClass = obs.tipo.toLowerCase();
        const multimediaButtons = createMultimediaButtons(obs);
        const fechaCompleta = formatearFechaCompleta(obs.fecha);
        
        return `
            <div class="observation-card" data-obs-id="${obs.id}">
                <div class="observation-header" onclick="toggleObservation(${obs.id})">
                    <div class="observation-summary">
                        <div class="observation-date">
                            <i class="fas fa-calendar-alt"></i>
                            <span>${fechaCompleta}</span>
                        </div>
                        <div class="observation-type ${tipoClass}">
                            <i class="fas ${getTypeIcon(obs.tipo)}"></i>
                            <span>${obs.tipo}</span>
                        </div>
                    </div>
                    <div class="observation-preview">
                        <p>${obs.descripcion.length > 100 ? obs.descripcion.substring(0, 100) + '...' : obs.descripcion}</p>
                    </div>
                    <div class="expand-indicator">
                        <i class="fas fa-chevron-down"></i>
                    </div>
                </div>
                
                <div class="observation-details" id="details-${obs.id}" style="display: none;">
                    <div class="observation-content">
                        <div class="content-section">
                            <h4><i class="fas fa-file-text"></i> Descripción Completa</h4>
                            <p>${obs.descripcion}</p>
                        </div>
                        
                        <div class="metadata-section">
                            <div class="metadata-item">
                                <i class="fas fa-user"></i>
                                <span><strong>Registrado por:</strong> ${obs.profesor || 'Profesor'}</span>
                            </div>
                            <div class="metadata-item">
                                <i class="fas fa-clock"></i>
                                <span><strong>Fecha y hora:</strong> ${fechaCompleta}</span>
                            </div>
                            <div class="metadata-item">
                                <i class="fas fa-tag"></i>
                                <span><strong>Tipo:</strong> ${obs.tipo}</span>
                            </div>
                        </div>
                        
                        <div class="multimedia-section">
                            <h4><i class="fas fa-photo-video"></i> Archivos Multimedia</h4>
                            <div class="observation-multimedia">
                                ${multimediaButtons}
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        `;
    }
    
    // Función para crear botones de multimedia
    function createMultimediaButtons(obs) {
        let buttons = '';
        
        if (obs.fotos) {
            buttons += `
                <button class="media-btn photos" onclick="viewPhotos(${obs.id})">
                    <i class="fas fa-images"></i>
                    <span>Ver Fotos</span>
                </button>
            `;
        }
        
        if (obs.videos) {
            buttons += `
                <button class="media-btn videos" onclick="viewVideos(${obs.id})">
                    <i class="fas fa-video"></i>
                    <span>Ver Videos</span>
                </button>
            `;
        }
        
        if (!obs.fotos && !obs.videos) {
            buttons = `
                <div class="no-multimedia">
                    <i class="fas fa-info-circle"></i>
                    <span>Sin multimedia</span>
                </div>
            `;
        }
        
        return buttons;
    }
    
    // Función para toggle de observaciones
    window.toggleObservation = function(obsId) {
        const detailsDiv = document.getElementById(`details-${obsId}`);
        const card = document.querySelector(`[data-obs-id="${obsId}"]`);
        const chevron = card.querySelector('.expand-indicator i');
        
        if (detailsDiv.style.display === 'none') {
            // Expandir
            detailsDiv.style.display = 'block';
            chevron.classList.remove('fa-chevron-down');
            chevron.classList.add('fa-chevron-up');
            card.classList.add('expanded');
            
            // Animación suave
            detailsDiv.style.opacity = '0';
            detailsDiv.style.transform = 'translateY(-10px)';
            setTimeout(() => {
                detailsDiv.style.transition = 'all 0.3s ease';
                detailsDiv.style.opacity = '1';
                detailsDiv.style.transform = 'translateY(0)';
            }, 10);
        } else {
            // Colapsar
            detailsDiv.style.transition = 'all 0.3s ease';
            detailsDiv.style.opacity = '0';
            detailsDiv.style.transform = 'translateY(-10px)';
            
            setTimeout(() => {
                detailsDiv.style.display = 'none';
                chevron.classList.remove('fa-chevron-up');
                chevron.classList.add('fa-chevron-down');
                card.classList.remove('expanded');
            }, 300);
        }
    };
    
    // Función para formatear fecha completa
    function formatearFechaCompleta(fecha) {
        try {
            const fechaObj = new Date(fecha);
            const opciones = { 
                year: 'numeric', 
                month: 'long', 
                day: 'numeric',
                hour: '2-digit',
                minute: '2-digit'
            };
            return fechaObj.toLocaleDateString('es-ES', opciones);
        } catch (error) {
            return fecha; // Fallback a la fecha original
        }
    }
    
    // Función para obtener icono según tipo
    function getTypeIcon(tipo) {
        switch(tipo) {
            case 'Positiva': return 'fa-smile';
            case 'Mejora': return 'fa-exclamation-triangle';
            case 'Neutral': return 'fa-info-circle';
            default: return 'fa-clipboard';
        }
    }
    
    // Función para mostrar estado de carga
    function showLoading() {
        observationsContainer.innerHTML = `
            <div class="loading-state">
                <i class="fas fa-spinner fa-spin"></i>
                <span>Cargando observaciones...</span>
            </div>
        `;
        observationsContainer.style.display = 'block';
        emptyObservations.style.display = 'none';
    }
    
    // Función para mostrar error
    function showError(message) {
        observationsContainer.innerHTML = `
            <div class="error-state">
                <i class="fas fa-exclamation-triangle"></i>
                <span>${message}</span>
            </div>
        `;
        observationsContainer.style.display = 'block';
        emptyObservations.style.display = 'none';
    }
    
    // Función para refrescar dashboard
    window.refreshDashboard = function() {
        if (selectedChildId) {
            loadObservationsForChild(selectedChildId);
        }
    };
    
    // Función para exportar a PDF
    window.exportToPDF = function() {
        if (!selectedChildId) {
            alert('Selecciona un hijo primero');
            return;
        }
        
        // Simulación de exportación
        const exportBtn = document.querySelector('.export-btn');
        const originalText = exportBtn.innerHTML;
        
        exportBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Generando...';
        exportBtn.disabled = true;
        
        setTimeout(() => {
            // Simular descarga
            const childData = window.acudienteMenu.getChildrenData().find(c => c.id === selectedChildId);
            const fileName = `observaciones_${childData ? childData.nombre.replace(/\s+/g, '_') : 'hijo'}_${new Date().toISOString().split('T')[0]}.pdf`;
            
            // Crear blob simulado
            const content = `Reporte de Observaciones\n\nHijo: ${childData ? childData.nombre : 'N/A'}\nFecha: ${new Date().toLocaleDateString()}\n\nObservaciones: ${currentObservations.length}`;
            const blob = new Blob([content], { type: 'text/plain' });
            const url = URL.createObjectURL(blob);
            
            const a = document.createElement('a');
            a.href = url;
            a.download = fileName;
            a.click();
            
            URL.revokeObjectURL(url);
            
            exportBtn.innerHTML = originalText;
            exportBtn.disabled = false;
        }, 2000);
    };
    
    // Funciones para multimedia (simuladas)
    window.viewPhotos = function(obsId) {
        loadAndShowMultimedia(obsId, 'photos', 'Fotos de la Observación');
    };
    
    window.viewVideos = function(obsId) {
        loadAndShowMultimedia(obsId, 'videos', 'Videos de la Observación');
    };
    
    // Función para cargar y mostrar multimedia real
    async function loadAndShowMultimedia(obsId, type, title) {
        const modal = document.getElementById('multimediaModal');
        const modalTitle = document.getElementById('modalTitle');
        const modalBody = document.getElementById('modalBody');
        
        modalTitle.textContent = title;
        
        // Mostrar loading
        modalBody.innerHTML = `
            <div class="loading-multimedia">
                <i class="fas fa-spinner fa-spin" style="font-size: 2rem; color: #42a5f5; margin-bottom: 1rem;"></i>
                <p>Cargando archivos multimedia...</p>
            </div>
        `;
        
        modal.style.display = 'flex';
        
        try {
            // Cargar multimedia desde la API
            const response = await fetch(`/api/observaciones/${obsId}/multimedia`);
            const data = await response.json();
            
            if (!data.success) {
                throw new Error(data.error || 'Error al cargar multimedia');
            }
            
            const archivos = data.data || [];
            
            if (archivos.length === 0) {
                modalBody.innerHTML = `
                    <div class="no-multimedia-modal">
                        <i class="fas fa-folder-open" style="font-size: 3rem; color: #ccc; margin-bottom: 1rem;"></i>
                        <h4>No hay archivos</h4>
                        <p>Esta observación no tiene archivos multimedia.</p>
                    </div>
                `;
                return;
            }
            
            // Filtrar archivos por tipo
            const filteredFiles = archivos.filter(archivo => {
                if (type === 'photos') {
                    return archivo.is_image;
                } else if (type === 'videos') {
                    return archivo.is_video;
                }
                return false;
            });
            
            if (filteredFiles.length === 0) {
                modalBody.innerHTML = `
                    <div class="no-multimedia-modal">
                        <i class="fas fa-${type === 'photos' ? 'images' : 'video'}" style="font-size: 3rem; color: #ccc; margin-bottom: 1rem;"></i>
                        <h4>No hay ${type === 'photos' ? 'fotos' : 'videos'}</h4>
                        <p>Esta observación no tiene ${type === 'photos' ? 'imágenes' : 'videos'}.</p>
                    </div>
                `;
                return;
            }
            
            // Renderizar archivos
            if (type === 'photos') {
                renderPhotosGallery(filteredFiles, modalBody);
            } else {
                renderVideosGallery(filteredFiles, modalBody);
            }
            
        } catch (error) {
            console.error('Error loading multimedia:', error);
            modalBody.innerHTML = `
                <div class="error-multimedia">
                    <i class="fas fa-exclamation-triangle" style="font-size: 3rem; color: #f44336; margin-bottom: 1rem;"></i>
                    <h4>Error al cargar archivos</h4>
                    <p>${error.message}</p>
                    <button onclick="loadAndShowMultimedia(${obsId}, '${type}', '${title}')" 
                            style="margin-top: 1rem; padding: 8px 16px; background: #42a5f5; color: white; border: none; border-radius: 4px; cursor: pointer;">
                        <i class="fas fa-redo"></i> Reintentar
                    </button>
                </div>
            `;
        }
    }
    
    // Función para renderizar galería de fotos
    function renderPhotosGallery(photos, container) {
        let html = '<div class="photo-gallery">';
        
        photos.forEach(photo => {
            html += `
                <div class="photo-item">
                    <img src="${photo.url}" 
                         alt="${photo.filename}" 
                         class="gallery-image"
                         onclick="openImageFullscreen('${photo.url}', '${photo.filename}')"
                         loading="lazy">
                    <div class="photo-info">
                        <span class="photo-name">${photo.filename}</span>
                        <span class="photo-size">${photo.formatted_size}</span>
                    </div>
                </div>
            `;
        });
        
        html += '</div>';
        container.innerHTML = html;
    }
    
    // Función para renderizar galería de videos
    function renderVideosGallery(videos, container) {
        let html = '<div class="video-gallery">';
        
        videos.forEach(video => {
            html += `
                <div class="video-item">
                    <video controls preload="metadata" class="gallery-video">
                        <source src="${video.url}" type="video/mp4">
                        <source src="${video.url}" type="video/webm">
                        <source src="${video.url}" type="video/avi">
                        Tu navegador no soporta el elemento video.
                    </video>
                    <div class="video-info">
                        <span class="video-name">${video.filename}</span>
                        <span class="video-size">${video.formatted_size}</span>
                    </div>
                </div>
            `;
        });
        
        html += '</div>';
        container.innerHTML = html;
    }
    
    // Función para abrir imagen en pantalla completa
    window.openImageFullscreen = function(url, filename) {
        const fullscreenModal = document.createElement('div');
        fullscreenModal.className = 'fullscreen-modal';
        fullscreenModal.innerHTML = `
            <div class="fullscreen-content">
                <button class="fullscreen-close" onclick="this.parentElement.parentElement.remove()">
                    <i class="fas fa-times"></i>
                </button>
                <img src="${url}" alt="${filename}" class="fullscreen-image">
                <div class="fullscreen-info">
                    <span>${filename}</span>
                </div>
            </div>
        `;
        
        fullscreenModal.addEventListener('click', function(e) {
            if (e.target === this) {
                this.remove();
            }
        });
        
        document.body.appendChild(fullscreenModal);
    };
    
    window.closeMultimediaModal = function() {
        document.getElementById('multimediaModal').style.display = 'none';
    };
    
    // Cerrar modal al hacer clic fuera
    document.getElementById('multimediaModal').addEventListener('click', function(e) {
        if (e.target === this) {
            closeMultimediaModal();
        }
    });
    
    console.log('✅ Dashboard unificado de acudiente cargado correctamente');
});
