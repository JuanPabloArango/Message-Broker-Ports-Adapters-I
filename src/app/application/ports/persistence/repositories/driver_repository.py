"""Módulo que contiene la definición del puerto para el repositorio del Aggregate
Root Driver."""

# Librerías Externas.
from typing import List, Union
from abc import ABC, abstractmethod

# Librerías Internas.
from app.domain.entities.driver import Driver

from app.application.ports.persistence.criteria import Criteria


class DriverRepositoryPort(ABC):
    """Clase que define el contrato nominal para el puerto del repositorio
    de Driver."""

    @abstractmethod
    def get(self, driver_id: str) -> Union[Driver, None]:
        """Método abstracto que define parte del contrato nominal enfocado
        en la obtención de entidades según su primery key.
        
        Args:
        ----------
        driver_id: str.
            ID de la entidad a obtener de la BD.
            
        Returns:
        ----------
        Union[Driver, None].
            Entidad de dominio."""
        
        raise NotImplementedError("Si tu clase es una realización de 'DriverRepositoryPort', debes implementar el método 'get'.")
    
    @abstractmethod
    def save(self, driver: Driver) -> None:
        """Método abstracto que define parte del contrato nominal enfocado en el
        almacenamiento de entidades.
        
        Args:
        ----------
        driver: Driver.
            Entidad de dominio que desea almacenar."""
        
        raise NotImplementedError("Si tu clase es una realización de 'DriverRepositoryPort', debes implementar el método 'save'.")
    
    @abstractmethod
    def list_all(self, criteria: Criteria) -> List[Driver]:
        """Método abstracto que define parte del contrato nominal enfocado en la
        obtención de entidades Driver de acuerdo a criterios de filtro.

        Args:
        ----------
        criteria: Criteria.
            Objeto que contiene los filtros de búsqueda sobre las entidades.
        
        Returns:
        ----------
        List[Driver].
            Entidades de dominio que cumplen con los criterios de búsqueda."""
        
        raise NotImplementedError("Si tu clase es una realización de 'DriverRepositoryPort', debes implementar el método 'list_all'.")

    @abstractmethod
    def list_available(self) -> List[Driver]:
        """Método que permite listar todas las entidades disponibles.
        
        Returns:
        ----------
        List[Driver].
            Entidades de dominio."""
        
        raise NotImplementedError("Si tu clase es una realización de 'DriverRepositoryPort', debes implementar el método 'list_available'.")
