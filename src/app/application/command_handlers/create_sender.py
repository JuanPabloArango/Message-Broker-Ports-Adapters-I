"""Módulo que contiene la lógica de creación de Senders en el dominio."""

# Librerías Internas.
from app.domain.entities.sender import Sender

from app.application.ports.persistence.uow import UnitOfWorkPort
from app.application.commands.create_sender import CreateSenderCommand


class CreateSenderHandler:
    """Módulo que contiene la lógica y orquestación de creación de una
    entidad Sender."""

    def __init__(self, unit_of_work: UnitOfWorkPort) -> None:
        """Método de instanciación de objetos de clase.
        
        Args:
        ----------
        unit_of_work: UnitOfWorkPort.
            Puerto de atomicidad de transacciones."""
        
        self._unit_of_work = unit_of_work

    def handle(self, command: CreateSenderCommand) -> str:
        """Método que orquesta la creación de Senders.
        
        Args:
        ----------
        command: CreateSenderCommand.
            Comando que contiene la información necesaria de creación.
        
        Returns:
        ----------
        str.
            ID del nuevo sender."""
        
        with self._unit_of_work as uow:
            
            new_sender = Sender(id = command.sender_id)
            uow.sender_repository.save(sender = new_sender)

            uow.commit()

            return new_sender.id.value
