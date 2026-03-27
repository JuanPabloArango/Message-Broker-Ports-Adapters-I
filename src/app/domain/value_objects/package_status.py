"""Módulo que define los posibles estados en los que se encuentra una entidad
Package."""

# Librerías Externas.
from enum import Enum


class PackageStatus(Enum):
    """Clase que define los posibles estados de un Sender."""
    
    PENDING: str = "PENDING"
    ASSIGNED: str = "ASSIGNED"
    DELIVERED: str = "DELIVERED"

    def __repr__(self) -> str:
        """Método que nos permite renderizar el estado del Package de una
        manera legible.
        
        Returns:
        ----------
        str.
            Estado del Package."""

        return f"{self.value}"

