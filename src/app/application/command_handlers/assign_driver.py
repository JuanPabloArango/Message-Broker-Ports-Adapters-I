"""Módulo que contiene la lógica de asignación de un Driver a un
Package en estado PENDING."""

# Librerías Internas.
from app.domain.services.assign_driver import DriverAssignment

from app.application.ports.persistence.uow import UnitOfWorkPort
from app.application.commands.assign_driver import AssignDriverCommand

from app.application.exceptions import PackageNotFound, NotCurrenltyAvailableDrivers


class AssignDriverHandler:
    """Módulo que contiene la lógica y orquestación de asignación de un
    Driver a un Package."""

    def __init__(self, unit_of_work: UnitOfWorkPort) -> None:
        """Método de instanciación de objetos de clase.
        
        Args:
        ----------
        unit_of_work: UnitOfWorkPort.
            Puerto de atomicidad de transacciones."""
        
        self._unit_of_work = unit_of_work

    def handle(self, command: AssignDriverCommand) -> str:
        """Método que orquesta la asignación de Drivers.
        
        Args:
        ----------
        command: AssignDriverCommand.
            Comando que contiene la información necesaria de creación.
        
        Returns:
        ----------
        str.
            ID conductor asignado."""
                
        with self._unit_of_work as uow:
            package = uow.package_repository.get(package_id = command.package_id)
            if not package:
                raise PackageNotFound("No se puede asignar un paquete que no existe.")

            drivers = uow.driver_repository.list_available()
            assigned_driver = DriverAssignment.execute(available_drivers = drivers)

            if not assigned_driver:
                raise NotCurrenltyAvailableDrivers("Actualmente no hay conductores libres. Tan pronto se libere alguno, su paquete será asignado.")
            
            assigned_driver.mark_as_occupied()
            package.assign_driver(driver_id = assigned_driver.id)

            uow.commit()

            return assigned_driver.id.value
