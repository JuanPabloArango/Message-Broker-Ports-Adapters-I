"""Módulo que define el comando que usaremos para la creación de Senders."""

# Librerías Externas.
from typing import Optional
from dataclasses import dataclass

# Librerías Internas.
from app.application.commands.base import Command


@dataclass(frozen = True)
class CreateSenderCommand(Command):
    """Clase que contiene la información necesaria que construye el
    comando de creación de una entidad de dominio Sender."""

    sender_id: Optional[str] = None

    def __post_init__(self) -> None:
        """Método dunder ara aplicar un poco de seguridad y validación."""

        if self.sender_id and not isinstance(self.sender_id, str):
            raise ValueError("El ID de un sender debe ser un string.")
        
