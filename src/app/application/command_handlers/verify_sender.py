"""Módulo que contiene la lógica de verificación de un Sender en el dominio."""

# Librerías Internas.
from app.application.ports.persistence.uow import UnitOfWorkPort
from app.application.commands.verify_sender import VerifySenderCommand

from app.application.exceptions import SenderNotFound


class VerifySenderHandler:
    """Módulo que contiene la lógica y orquestación de verificación de una
    entidad Sender."""

    def __init__(self, unit_of_work: UnitOfWorkPort) -> None:
        """Método de instanciación de objetos de clase.
        
        Args:
        ----------
        unit_of_work: UnitOfWorkPort.
            Puerto de atomicidad de transacciones."""
        
        self._unit_of_work = unit_of_work

    def handle(self, command: VerifySenderCommand) -> str:
        """Método que orquesta la verificación de Senders.
        
        Args:
        ----------
        command: VerifySenderCommand.
            Comando que contiene la información necesaria de creación.
        
        Returns:
        ----------
        str.
            ID del nuevo conductor."""
        
        with self._unit_of_work as uow:
            sender = uow.sender_repository.get(sender_id = command.sender_id)
            if not sender:
                raise SenderNotFound(f"No se halló un sender con el ID {command.sender_id}.")
            
            sender.verify()
            uow.commit()
