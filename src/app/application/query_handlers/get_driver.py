"""Módulo que define un handler sobre el cual aplicar queries enfocadas en
obtener una entidad de dominio según identificación."""

# Librerías Externas.
from typing import Union

# Librerías Internas.
from app.domain.entities.driver import Driver

from app.application.dtos.driver import DriverDTO

from app.application.ports.persistence.uow import UnitOfWorkPort
from app.application.queries.get_driver_by_id import GetDriverQuery

from app.application.exceptions import DriverNotFound


class GetDriverHandler:
    """Clase que encapsula las lógicas del Query Handler."""

    def __init__(self, unit_of_work: UnitOfWorkPort) -> None:
        """Método de instanciación de objetos de la clase.
        
        Args:
        ----------
        unit_of_work: UnitOfWorkPort.
            Puerto de UoW enfocado en hacer transacciones atómicas."""
        
        self._unit_of_work = unit_of_work

    def handle(self, query: GetDriverQuery) -> Union[Driver, None]:
        """Método que se encarga de gestionar la búsqueda en su caso de uso.
        
        Args:
        ----------
        query: GetDriverQuery.
            Query que contiene la información necesaria para la búsqueda.
            
        Returns:
        ----------
        Union[Driver, None].
            Entidad de dominio hallada."""
        
        with self._unit_of_work as uow:

            driver = uow.driver_repository.get(driver_id = query.driver_id)
            if not driver:
                raise DriverNotFound(f"El conductor con ID {query.driver_id} no existe.")
            return DriverDTO.from_entity(driver)
