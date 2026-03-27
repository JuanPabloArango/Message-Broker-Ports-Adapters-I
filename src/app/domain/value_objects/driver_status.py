"""Módulo que define los posibles estados en los que se encuentra una entidad
Driver."""

# Librerías Externas.
from enum import Enum


class DriverStatus(Enum):
    """Clase que define los posibles estados de un Driver."""

    OCCUPIED: str = "OCCUPIED"
    AVAILABLE: str = "AVAILABLE"

    def __repr__(self) -> str:
        """Método que nos permite renderizar el estado del Driver de una
        manera legible.
        
        Returns:
        ----------
        str.
            Estado del Driver."""

        return f"{self.value}"
