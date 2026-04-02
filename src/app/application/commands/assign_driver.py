"""Módulo que define el comando que usaremos para la asignación de Driver
para entregar un Package."""

# Librerías Externas.
from typing import Optional
from dataclasses import dataclass

# Librerías Internas.
from app.application.commands.base import Command


@dataclass(frozen = True)
class AssignDriverCommand(Command):
    """Clase que contiene la información necesaria que construye el
    comando de asignación de un Driver a una entidad de dominio Package."""

    package_id: str

    def __post_init__(self) -> None:
        """Método dunder ara aplicar un poco de seguridad y validación."""

        if not isinstance(self.package_id, str):
            raise ValueError("El ID de un paquete debe ser un string.")

