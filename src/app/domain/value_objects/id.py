"""Módulo que define la construcción de IDs para todas las entidades."""

# Librerías Externas.
from __future__ import annotations
from typing import Optional

import uuid
from dataclasses import dataclass


@dataclass(unsafe_hash = True)
class ID:
    """Clase que define la construcción de IDs en etapa de producción,
    pero también soporta la asignación de IDs base para desarrollo."""

    value: Optional[str] = None

    def __post_init__(self) -> None:
        """Método dunder de validación y/o creación del ID para entidades."""

        if not self.value:
            self.value = uuid.uuid4().hex
        
        if not isinstance(self.value, str):
            raise ValueError("Solo soportamos IDs cuyo typing sea 'str'.")
        
    def __eq__(self, other: ID) -> bool:
        """Método dunder para poder comparar dos IDs.
        
        Args:
        ----------
        other: ID.
            Otro VO ID contra el cual comparar.
        
        Returns:
        ----------
        bool.
            Si ambos IDs son iguales."""
        
        if not isinstance(other, ID):
            return False
        return self.value == other.value
    
    def __repr__(self) -> str:
        """Método que permite tener una representación legible del VO.
        
        Returns:
        ----------
        str.
            Representación del VO."""
        
        return self.value or "None"
