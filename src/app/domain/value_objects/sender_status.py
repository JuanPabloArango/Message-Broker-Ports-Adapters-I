"""Módulo que define los posibles estados en los que se encuentra una entidad
Sender."""

# Librerías Externas.
from enum import Enum


class SenderStatus(Enum):
    """Clase que define los posibles estados de un Sender."""
    
    VERIFIED: str = "VERIFIED"
    UNVERIFIED: str = "UNVERIFIED"

    def __repr__(self) -> str:
        """Método que nos permite renderizar el estado del Sender de una
        manera legible.
        
        Returns:
        ----------
        str.
            Estado del Sender."""

        return f"{self.value}"
