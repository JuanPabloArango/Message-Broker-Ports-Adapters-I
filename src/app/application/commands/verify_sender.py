"""Módulo que define el comando que usaremos para la verificación de Senders."""

# Librerías Externas.
from typing import Optional

from dataclasses import dataclass

# Librerías Internas.
from app.application.commands.base import Command


@dataclass(frozen = True)
class VerifySenderCommand(Command):
    """Clase que contiene la información necesaria que construye el
    comando de verificación de una entidad de dominio Sender."""

    sender_id: str

    def __post_init__(self) -> None:
        """Método dunder ara aplicar un poco de seguridad y validación."""

        if not isinstance(self.sender_id, str):
            raise ValueError("El ID de un sender debe ser un string.")
        
