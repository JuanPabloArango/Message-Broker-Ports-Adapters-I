"""Módulo que contiene la definición de la entidad de dominio Driver."""

# Librerías Externas.
from __future__ import annotations
from typing import Optional, Union, Optional

import datetime as dt

# Librerías Internas.
from app.domain.value_objects.id import ID
from app.domain.value_objects.driver_status import DriverStatus
from app.domain.value_objects.delivery_date import DeliveryDate

from app.domain.exceptions import DriverCurrenlyOccupiedError, DriverAlreadyAvailableError


class Driver:
    """Clase que contiene la definición de la entidad Aggregate Root Driver."""

    def __init__(self, id: Optional[str] = None, last_delivery: Optional[str] = None) -> None:
        """Método de instanciación de objetos de la clase.
        
        Args:
        ----------
        id: Optional[str].
            ID que desea asignarle a la entidad. Si es None, se generará en
            automático.
        
        last_delivery: Optional[str].
            Fecha de último trabajo realizado por el Driver."""
        
        self._id: ID = ID(value = id)

        self._status: DriverStatus = DriverStatus.AVAILABLE
        self._last_delivery: DeliveryDate = DeliveryDate(last_delivery = last_delivery)

        self._created_at: Optional[dt.datetime] = None
        self._updated_at: Optional[dt.datetime] = None

    def mark_as_available(self) -> None:
        """Método que se encarga de marcar a un conductor como libre cuando
        ha entregado un paquete."""
        
        if self._status != DriverStatus.OCCUPIED:
            raise DriverAlreadyAvailableError("No se puede marcar como 'AVAILABLE' a un conductor que ya está libre.")
        
        self._status = DriverStatus.AVAILABLE

    def mark_as_occupied(self) -> None:
        """Método que se encarga de marcar a un conductor como ocupado cuando
        se le ha asignado un paquete."""
        
        if self._status != DriverStatus.AVAILABLE:
            raise DriverCurrenlyOccupiedError("No se puede asignar un paquete a un conductor que ya tiene trabajo.")
        
        self._status = DriverStatus.OCCUPIED

    @property
    def id(self) -> ID:
        """Propiedad que encapsula el ID de la entidad.
        
        Returns:
        ----------
        ID.
            ID de la entidad."""
        
        return self._id
    
    @property
    def status(self) -> DriverStatus:
        """Propieda que encapsula el atributo status.
        
        Returns:
        ----------
        DriverStatus.
            Estado actual del Driver."""

        return self._status
    
    @property
    def last_delivery(self) -> Union[None, dt.datetime]:
        """Propieda que encapsula el atributo last_delivery.
        
        Returns:
        ----------
        Union[None, dt.datetime].
            Momento del último despacho hecho por la entidad."""

        return self._last_delivery
    
    @classmethod
    def create(cls, id: Optional[str] = None, last_delivery: Optional[str] = None) -> Driver:
        """Método de clase que define, en nomenclatura de DDD, la creación
        de una entidad.
        
        Args:
        ----------
        id: Optional[str].
            ID con el que desea crear la entidad. Si no pasa un valor, se creará
            un UUID4 en automático.
        
        last_delivery: Optional[str].
            Fecha de último trabajo realizado por el Driver.
        
        Returns:
        ----------
        Package.
            Entidad de dominio."""

        instance = cls(id = id, last_delivery = last_delivery)
        return instance
    
    def __repr__(self) -> str:
        """Método dunder que permite representar a la entidad en un formato
        legible.
        
        Returns:
        ----------
        str.
            Representación del objeto."""
        
        return f"Driver(id={self._id}, last_delivery={self._last_delivery}, status={self._status})"
