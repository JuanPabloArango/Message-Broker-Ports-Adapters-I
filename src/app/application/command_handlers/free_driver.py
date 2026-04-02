"""Módulo que contiene la lógica de liberación de un Driver."""

# Librerías Internas.
from app.application.ports.persistence.uow import UnitOfWorkPort
from app.application.commands.free_driver import FreeDriverCommand

from app.application.exceptions import DriverNotFound


class FreeDriverHandler:
    """Módulo que contiene la lógica y orquestación de liberación de un
    Driver."""

    def __init__(self, unit_of_work: UnitOfWorkPort) -> None:
        """Método de instanciación de objetos de clase.
        
        Args:
        ----------
        unit_of_work: UnitOfWorkPort.
            Puerto de atomicidad de transacciones."""
        
        self._unit_of_work = unit_of_work

    def handle(self, command: FreeDriverCommand) -> str:
        """Método que orquesta la liberación de Drivers.
        
        Args:
        ----------
        command: FreeDriverCommand.
            Comando que contiene la información necesaria de creación.
        
        Returns:
        ----------
        str.
            ID conductor liberado."""
                
        with self._unit_of_work as uow:
            driver = uow.driver_repository.get(driver_id = command.driver_id)
            if not driver:
                raise DriverNotFound("No se puede liberar un conductor que no existe.")

            driver.mark_as_available()
            uow.commit()
