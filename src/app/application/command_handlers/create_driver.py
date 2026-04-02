"""Módulo que contiene la lógica de creación de Drivers en el dominio."""

# Librerías Internas.
from app.domain.entities.driver import Driver

from app.application.ports.persistence.uow import UnitOfWorkPort
from app.application.commands.create_driver import CreateDriverCommand


class CreateDriverHandler:
    """Módulo que contiene la lógica y orquestación de creación de una
    entidad Driver."""

    def __init__(self, unit_of_work: UnitOfWorkPort) -> None:
        """Método de instanciación de objetos de clase.
        
        Args:
        ----------
        unit_of_work: UnitOfWorkPort.
            Puerto de atomicidad de transacciones."""
        
        self._unit_of_work = unit_of_work

    def handle(self, command: CreateDriverCommand) -> str:
        """Método que orquesta la creación de Drivers.
        
        Args:
        ----------
        command: CreateDriverCommand.
            Comando que contiene la información necesaria de creación.
        
        Returns:
        ----------
        str.
            ID del nuevo conductor."""
        
        with self._unit_of_work as uow:
            new_driver = Driver(id = command.driver_id, last_delivery = command.last_delivery)
            uow.driver_repository.save(driver = new_driver)

            uow.commit()

            return new_driver.id.value
