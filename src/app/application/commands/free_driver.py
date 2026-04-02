"""Módulo que define el comando que usaremos para la liberación de Driver."""

# Librerías Externas.
from dataclasses import dataclass

# Librerías Internas.
from app.application.commands.base import Command


@dataclass(frozen = True)
class FreeDriverCommand(Command):
    """Clase que contiene la información necesaria que construye el
    comando de liberación de un Driver."""

    driver_id: str

    def __post_init__(self) -> None:
        """Método dunder ara aplicar un poco de seguridad y validación."""

        if not isinstance(self.driver_id, str):
            raise ValueError("El ID de un Driver debe ser un string.")
        
