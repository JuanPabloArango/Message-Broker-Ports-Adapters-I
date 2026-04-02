"""Módulo que define el comando que usaremos para la marcación de Packages."""

# Librerías Externas.
from dataclasses import dataclass

# Librerías Internas.
from app.application.commands.base import Command


@dataclass(frozen = True)
class DeliverPackageCommand(Command):
    """Clase que contiene la información necesaria que construye el
    comando de marcación de un Package."""

    package_id: str

    def __post_init__(self) -> None:
        """Método dunder ara aplicar un poco de seguridad y validación."""

        if not isinstance(self.package_id, str):
            raise ValueError("El ID de un paquete debe ser un string.")
        
