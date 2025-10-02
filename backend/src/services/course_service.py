# backend/src/services/course_service.py
"""Capa de servicio que encapsula la lógica de negocio para los cursos.
Se apoya en CourseModel para acceso a datos y provee validaciones simples.
"""
from typing import Optional
from ..models.course_model import CourseModel

class CourseService:
    @staticmethod
    def create_course(nombre: str, descripcion: Optional[str] = None,
                      fecha_inicio: Optional[str] = None, fecha_fin: Optional[str] = None,
                      is_active: bool = True):
        if not nombre:
            return False
        return CourseModel.create_course(nombre, descripcion, fecha_inicio, fecha_fin, is_active)

    @staticmethod
    def get_all_courses():
        return CourseModel.get_all_courses()

    @staticmethod
    def get_course(course_id: int):
        return CourseModel.find_by_id(course_id)

    @staticmethod
    def update_course(course_id: int, **kwargs):
        return CourseModel.update_course(course_id, **kwargs)

    @staticmethod
    def delete_course(course_id: int):
        return CourseModel.delete_course(course_id)
