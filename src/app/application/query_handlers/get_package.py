"""Módulo que define un handler sobre el cual aplicar queries enfocadas en
obtener una entidad de dominio según identificación."""

# Librerías Externas.
from typing import Union

# Librerías Internas.
from app.domain.entities.package import Package

from app.application.dtos.package import PackageDTO

from app.application.ports.persistence.uow import UnitOfWorkPort
from app.application.queries.get_package_by_id import GetPackageQuery

from app.application.exceptions import PackageNotFound


class GetPackageHandler:
    """Clase que encapsula las lógicas del Query Handler."""

    def __init__(self, unit_of_work: UnitOfWorkPort) -> None:
        """Método de instanciación de objetos de la clase.
        
        Args:
        ----------
        unit_of_work: UnitOfWorkPort.
            Puerto de UoW enfocado en hacer transacciones atómicas."""
        
        self._unit_of_work = unit_of_work

    def handle(self, query: GetPackageQuery) -> Union[Package, None]:
        """Método que se encarga de gestionar la búsqueda en su caso de uso.
        
        Args:
        ----------
        query: GetPackageQuery.
            Query que contiene la información necesaria para la búsqueda.
            
        Returns:
        ----------
        Union[Package, None].
            Entidad de dominio hallada."""
        
        with self._unit_of_work as uow:
            package = uow.package_repository.get(package_id = query.package_id)
            if not package:
                raise PackageNotFound(f"El paquete con ID {query.package_id} no existe.")
            return PackageDTO.from_entity(package)
