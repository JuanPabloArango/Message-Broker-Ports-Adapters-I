"""Módulo que contiene la lógica de maración de un Package como 'DELIVERED."""

# Librerías Internas.
from app.application.ports.persistence.uow import UnitOfWorkPort
from app.application.commands.deliver_package import DeliverPackageCommand

from app.application.exceptions import PackageNotFound


class DeliverPackageHandler:
    """Módulo que contiene la lógica y orquestación marcación de paquete."""

    def __init__(self, unit_of_work: UnitOfWorkPort) -> None:
        """Método de instanciación de objetos de clase.
        
        Args:
        ----------
        unit_of_work: UnitOfWorkPort.
            Puerto de atomicidad de transacciones."""
        
        self._unit_of_work = unit_of_work

    def handle(self, command: DeliverPackageCommand) -> str:
        """Método que orquesta la liberación de Drivers.
        
        Args:
        ----------
        command: DeliverPackageCommand.
            Comando que contiene la información necesaria de creación.
        
        Returns:
        ----------
        str.
            ID conductor liberado."""
                
        with self._unit_of_work as uow:
            package = uow.package_repository.get(package_id = command.package_id)
            if not package:
                raise PackageNotFound("No se puede marcar un paquete que no existe.")

            package.deliver()

            driver = uow.driver_repository.get(driver_id = package.driver_id.value)
            driver.mark_as_available()
            
            uow.commit()

            return package.id.value
