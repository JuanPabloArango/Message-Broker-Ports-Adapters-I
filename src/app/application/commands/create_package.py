"""Módulo que define el comando que usaremos para la creación de Packages."""

# Librerías Externas.
from typing import Optional
from dataclasses import dataclass

# Librerías Internas.
from app.application.commands.base import Command


@dataclass(frozen = True)
class CreatePackageCommand(Command):
    """Clase que contiene la información necesaria que construye el
    comando de creación de una entidad de dominio Package."""

    sender_id: str
    package_id: Optional[str] = None

    def __post_init__(self) -> None:
        """Método dunder ara aplicar un poco de seguridad y validación."""

        if not isinstance(self.sender_id, str):
            raise ValueError("El ID de un sender debe ser un string.")
        
        if self.package_id and not isinstance(self.package_id, str):
            raise ValueError("El ID de un paquete debe ser un string.")

