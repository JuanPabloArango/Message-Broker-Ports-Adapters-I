"""Módulo que define un handler sobre el cual aplicar queries enfocadas a
obtener varias entidades de dominio según parámetros de búsqueda del usuario."""

# Librerías Externas.
from typing import List

# Librerías Internas.
from app.domain.entities.package import Package

from app.application.dtos.package import PackageDTO

from app.application.ports.persistence.uow import UnitOfWorkPort
from app.application.queries.list_packages import ListPackagesQuery


class ListPackagesHandler:
    """Clase que encapsula las lógicas del Query Handler."""

    def __init__(self, unit_of_work: UnitOfWorkPort) -> None:
        """Método de instanciación de objetos de la clase.
        
        Args:
        ----------
        unit_of_work: UnitOfWorkPort.
            Puerto de UoW enfocado en hacer transacciones atómicas."""
        
        self._unit_of_work = unit_of_work

    def handle(self, query: ListPackagesQuery) -> List[Package]:
        """Método que se encarga de gestionar la búsqueda en su caso de uso.
        
        Args:
        ----------
        query: ListPackagesQuery.
            Query que contiene la información necesaria para la búsqueda.
            
        Returns:
        ----------
        List[Package].
            Resultados que concuerdan con la búsqueda."""
        
        with self._unit_of_work as uow:
            packages = uow.package_repository.list_all(criteria = query.criteria)
            return [PackageDTO.from_entity(package) for package in packages]
