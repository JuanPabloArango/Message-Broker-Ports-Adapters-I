"""Módulo que contiene la lógica de creación de Packages en el dominio."""

# Librerías Internas.
from app.domain.entities.package import Package
from app.domain.value_objects.id import ID

from app.application.ports.persistence.uow import UnitOfWorkPort
from app.application.commands.create_package import CreatePackageCommand

from app.domain.exceptions import SenderNotVerified
from app.application.exceptions import SenderNotFound


class CreatePackageHandler:
    """Módulo que contiene la lógica y orquestación de creación de una
    entidad Package."""

    def __init__(self, unit_of_work: UnitOfWorkPort) -> None:
        """Método de instanciación de objetos de clase.
        
        Args:
        ----------
        unit_of_work: UnitOfWorkPort.
            Puerto de atomicidad de transacciones."""
        
        self._unit_of_work = unit_of_work

    def handle(self, command: CreatePackageCommand) -> str:
        """Método que orquesta la creación de Packages.
        
        Args:
        ----------
        command: CreatePackageCommand.
            Comando que contiene la información necesaria de creación.
        
        Returns:
        ----------
        str.
            ID del nuevo paquete."""
        
        with self._unit_of_work as uow:
            sender = uow.sender_repository.get(sender_id = command.sender_id)
            if not sender:
                raise SenderNotFound(f"El paquete no se ha creado debido a que no se encontró al sender con ID {command.sender_id}.")
            
            if not sender.can_send_packages():
                raise SenderNotVerified("El sender existe pero su estado actual no le permite enviar paquetes.")
            
            new_package = Package(id = command.package_id, sender_id = ID(command.sender_id))
            uow.package_repository.save(package = new_package)

            uow.commit()

            return new_package.id.value
