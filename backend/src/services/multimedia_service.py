# backend/src/services/multimedia_service.py

import os
import uuid
from datetime import datetime
from werkzeug.utils import secure_filename
from flask import current_app
from ..models.multimedia_model import MultimediaModel

class MultimediaService:
    """Servicio para gestionar archivos multimedia."""
    
    # Configuración de archivos permitidos
    ALLOWED_EXTENSIONS = {
        'image': ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.webp'],
        'video': ['.mp4', '.avi', '.mov', '.wmv', '.flv', '.webm']
    }
    
    MAX_FILE_SIZE = 500 * 1024 * 1024  # 500MB
    
    @staticmethod
    def get_upload_folder():
        """Obtiene la carpeta de uploads."""
        # Obtener la ruta del proyecto
        project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
        upload_folder = os.path.join(project_root, 'uploads', 'multimedia')
        
        # Crear la carpeta si no existe
        os.makedirs(upload_folder, exist_ok=True)
        
        return upload_folder
    
    @staticmethod
    def allowed_file(filename):
        """Verifica si el archivo es permitido."""
        if not filename:
            return False, None
            
        file_ext = os.path.splitext(filename)[1].lower()
        
        for file_type, extensions in MultimediaService.ALLOWED_EXTENSIONS.items():
            if file_ext in extensions:
                return True, file_type
        
        return False, None
    
    @staticmethod
    def generate_unique_filename(original_filename):
        """Genera un nombre único para el archivo."""
        file_ext = os.path.splitext(original_filename)[1].lower()
        unique_name = f"{uuid.uuid4().hex}{file_ext}"
        return unique_name
    
    @staticmethod
    def save_file(file, observation_id, uploaded_by):
        """Guarda un archivo y crea el registro en la base de datos."""
        try:
            # Validar archivo
            is_allowed, file_type = MultimediaService.allowed_file(file.filename)
            if not is_allowed:
                return False, "Tipo de archivo no permitido"
            
            # Validar tamaño
            file.seek(0, os.SEEK_END)
            file_size = file.tell()
            file.seek(0)
            
            if file_size > MultimediaService.MAX_FILE_SIZE:
                return False, f"El archivo es demasiado grande. Máximo permitido: {MultimediaService.MAX_FILE_SIZE // (1024*1024)}MB"
            
            # Generar nombre único
            original_filename = secure_filename(file.filename)
            unique_filename = MultimediaService.generate_unique_filename(original_filename)
            
            # Crear estructura de carpetas por fecha
            upload_folder = MultimediaService.get_upload_folder()
            date_folder = datetime.now().strftime('%Y/%m')
            full_upload_path = os.path.join(upload_folder, date_folder)
            os.makedirs(full_upload_path, exist_ok=True)
            
            # Ruta completa del archivo
            file_path = os.path.join(full_upload_path, unique_filename)
            relative_path = os.path.join('uploads', 'multimedia', date_folder, unique_filename).replace('\\', '/')
            
            # Guardar archivo físico
            file.save(file_path)
            
            # Crear registro en la base de datos
            multimedia_id = MultimediaModel.create_multimedia(
                observation_id=observation_id,
                filename=original_filename,
                file_type=file_type,
                file_path=relative_path,
                file_size=file_size,
                uploaded_by=uploaded_by
            )
            
            if multimedia_id:
                return True, {
                    'id': multimedia_id,
                    'filename': original_filename,
                    'file_type': file_type,
                    'file_path': relative_path,
                    'file_size': file_size
                }
            else:
                # Si falla la BD, eliminar archivo físico
                try:
                    os.remove(file_path)
                except:
                    pass
                return False, "Error al guardar en la base de datos"
                
        except Exception as e:
            print(f"Error al guardar archivo: {e}")
            return False, f"Error interno: {str(e)}"
    
    @staticmethod
    def delete_file(multimedia_id, user_id):
        """Elimina un archivo multimedia."""
        try:
            # Obtener información del archivo
            file_data = MultimediaModel.get_multimedia_by_id(multimedia_id)
            if not file_data:
                return False, "Archivo no encontrado"
            
            # Por ahora, permitir eliminar cualquier archivo (sin verificación de permisos)
            # TODO: Implementar verificación de permisos cuando se agregue la columna uploaded_by
            
            # Eliminar de la BD
            if MultimediaModel.delete_multimedia(multimedia_id):
                # Eliminar archivo físico
                try:
                    project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
                    full_path = os.path.join(project_root, file_data['file_path'])
                    if os.path.exists(full_path):
                        os.remove(full_path)
                        print(f"Archivo físico eliminado: {full_path}")
                    else:
                        print(f"Archivo físico no encontrado: {full_path}")
                except Exception as e:
                    print(f"Error al eliminar archivo físico: {e}")
                    # No fallar si no se puede eliminar el archivo físico
                
                return True, "Archivo eliminado exitosamente"
            else:
                return False, "Error al eliminar archivo de la base de datos"
                
        except Exception as e:
            print(f"Error al eliminar archivo: {e}")
            return False, f"Error interno: {str(e)}"
    
    @staticmethod
    def get_file_url(file_path):
        """Genera la URL para acceder a un archivo."""
        # El file_path ya incluye 'uploads/multimedia/...' así que solo agregamos la barra inicial
        if file_path.startswith('uploads/'):
            return f"/{file_path}"
        else:
            return f"/uploads/{file_path}"
    
    @staticmethod
    def format_file_size(size_bytes):
        """Formatea el tamaño del archivo en formato legible."""
        if size_bytes == 0:
            return "0 B"
        
        size_names = ["B", "KB", "MB", "GB"]
        i = 0
        while size_bytes >= 1024 and i < len(size_names) - 1:
            size_bytes /= 1024.0
            i += 1
        
        return f"{size_bytes:.1f} {size_names[i]}"
    
    @staticmethod
    def get_multimedia_by_observation(observation_id):
        """Obtiene archivos multimedia de una observación con URLs formateadas."""
        files = MultimediaModel.get_multimedia_by_observation(observation_id)
        
        for file_data in files:
            file_data['url'] = MultimediaService.get_file_url(file_data['file_path'])
            file_data['formatted_size'] = MultimediaService.format_file_size(file_data['file_size'])
            
            # Determinar tipo de archivo basándose en la extensión como fallback
            filename = file_data.get('filename', '')
            file_ext = os.path.splitext(filename)[1].lower()
            
            # Primero intentar usar el campo file_type, luego la extensión
            if file_data.get('file_type') == 'image' or file_ext in ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.webp']:
                file_data['is_image'] = True
                file_data['is_video'] = False
            elif file_data.get('file_type') == 'video' or file_ext in ['.mp4', '.avi', '.mov', '.wmv', '.flv', '.webm']:
                file_data['is_image'] = False
                file_data['is_video'] = True
            else:
                file_data['is_image'] = False
                file_data['is_video'] = False
        
        return files
    
    @staticmethod
    def get_multimedia_by_student(student_id):
        """Obtiene archivos multimedia de un estudiante con URLs formateadas."""
        files = MultimediaModel.get_multimedia_by_student(student_id)
        
        for file_data in files:
            file_data['url'] = MultimediaService.get_file_url(file_data['file_path'])
            file_data['formatted_size'] = MultimediaService.format_file_size(file_data['file_size'])
            
            # Determinar tipo de archivo basándose en la extensión como fallback
            filename = file_data.get('filename', '')
            file_ext = os.path.splitext(filename)[1].lower()
            
            # Primero intentar usar el campo file_type, luego la extensión
            if file_data.get('file_type') == 'image' or file_ext in ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.webp']:
                file_data['is_image'] = True
                file_data['is_video'] = False
            elif file_data.get('file_type') == 'video' or file_ext in ['.mp4', '.avi', '.mov', '.wmv', '.flv', '.webm']:
                file_data['is_image'] = False
                file_data['is_video'] = True
            else:
                file_data['is_image'] = False
                file_data['is_video'] = False
        
        return files
    
    @staticmethod
    def validate_upload_request(files, observation_id):
        """Valida una solicitud de subida de archivos."""
        if not files:
            return False, "No se enviaron archivos"
        
        if not observation_id:
            return False, "ID de observación requerido"
        
        # Validar que no se suban demasiados archivos a la vez
        if len(files) > 10:
            return False, "Máximo 10 archivos por vez"
        
        return True, "Validación exitosa"
