"""Módulo que define el comando que usaremos para la creación de Drivers."""

# Librerías Externas.
from typing import Optional

from dataclasses import dataclass

# Librerías Internas.
from app.application.commands.base import Command


@dataclass(frozen = True)
class CreateDriverCommand(Command):
    """Clase que contiene la información necesaria que construye el
    comando de creación de una entidad de dominio Driver."""

    driver_id: Optional[str] = None
    last_delivery: Optional[str] = None

    def __post_init__(self) -> None:
        """Método dunder ara aplicar un poco de seguridad y validación."""

        if self.driver_id and not isinstance(self.driver_id, str):
            raise ValueError("El ID de un conductor debe ser un string.")
        
        if self.last_delivery and not isinstance(self.last_delivery, str):
            raise ValueError("Si va a usar el parámetro 'last_delivey' debe enviar un string.")
