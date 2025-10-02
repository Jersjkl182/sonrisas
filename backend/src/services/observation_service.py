"""ObservationService
Capa de negocio para las notas de observación.
"""

from ..models.observation_model import ObservationModel

class ObservationService:
    """Métodos de alto nivel para gestionar observaciones."""

    @staticmethod
    def crear_nota(titulo: str, descripcion: str, id_admin: int, id_acudiente: int, hijo: str) -> int:
        return ObservationModel.create(titulo, descripcion, id_admin, id_acudiente, hijo)

    @staticmethod
    def listar_por_admin(id_admin: int):
        """Lista observaciones creadas por un usuario con rol Administrador (usa id_profesor en la tabla)."""
        return ObservationModel.get_all_for_profesor(id_admin)

    # Nuevo método para profesores (rol 2)
    @staticmethod
    def listar_por_profesor(id_profesor: int):
        """Lista observaciones creadas por un profesor."""
        return ObservationModel.get_all_for_profesor(id_profesor)

    @staticmethod
    def listar_estudiantes_profesor(id_profesor: int):
        """Devuelve estudiantes vinculados al profesor"""
        return ObservationModel.get_students_for_profesor(id_profesor)

    @staticmethod
    def listar_para_acudiente(id_acudiente: int):
        return ObservationModel.get_for_acudiente(id_acudiente)

    @staticmethod
    def obtener(obs_id: int):
        return ObservationModel.get_by_id(obs_id)

    @staticmethod
    def actualizar(obs_id: int, titulo: str, descripcion: str, hijo: str):
        ObservationModel.update(obs_id, titulo, descripcion, hijo)

    @staticmethod
    def eliminar(obs_id: int):
        ObservationModel.delete(obs_id)
