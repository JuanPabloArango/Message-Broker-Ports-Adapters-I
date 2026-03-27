"""Módulo que contiene la definición de la entidad de dominio Package."""

# Librerías Externas.
from __future__ import annotations
from typing import Optional, Union

import datetime as dt

# Librerías Internas.
from app.domain.value_objects.id import ID
from app.domain.value_objects.package_status import PackageStatus

from app.domain.exceptions import PackageTransitionError


class Package:
    """Clase que contiene la definición de la entidad Aggregate Root Package."""

    def __init__(self, sender_id: ID, id: Optional[str] = None) -> None:
        """Método de instanciación de objetos de la clase.
        
        Args:
        ----------
        sender_id: ID.
            ID del usuario quien hace el envío del Package.

        id: Optional[str].
            ID que desea asignarle a la entidad. Si es None, se generará en
            automático."""
        
        self._sender_id: ID = sender_id
        self._driver_id: Optional[ID] = None
        
        self._id: ID = ID(value = id)
        self._status: PackageStatus = PackageStatus.PENDING

        self._created_at: Optional[dt.datetime] = None
        self._updated_at: Optional[dt.datetime] = None

    def assign_driver(self, driver_id: ID) -> None:
        """Método que permite asignar un transportador al paquete.
        
        Args:
        ----------
        driver_id: ID.
            ID del conductor encargado."""
        
        if self._status != PackageStatus.PENDING:
            raise PackageTransitionError("Un paquete solo puede ser asignado si su estado actual es 'PENDING'.")
        
        self._driver_id = driver_id
        self._status = PackageStatus.ASSIGNED

    def deliver(self) -> None:
        """Método cuya única responsabilidad es marcar un paquete como
        entregado."""

        if self._status != PackageStatus.ASSIGNED:
            raise PackageTransitionError("Un paquete solo puede ser marcado como entregado, si antes fue reportado como 'ASSIGNED'.")
        
        self._status = PackageStatus.DELIVERED

    @property
    def id(self) -> ID:
        """Propiedad que encapsula el ID de la entidad.
        
        Returns:
        ----------
        ID.
            ID de la entidad."""
        
        return self._id
    
    @property
    def sender_id(self) -> ID:
        """Propiedad que encapsula el ID del Sender dueño del paquete.
        
        Returns:
        ----------
        ID.
            ID del Sender."""
        
        return self._sender_id
    
    @property
    def driver_id(self) -> Union[None, ID]:
        """Propiedad que encapsula el ID del conductor asignado.
        
        Returns:
        ----------
        Union[None, ID].
            ID del conductor asignado."""
        
        return self._driver_id
    
    @property
    def status(self) -> PackageStatus:
        """Propieda que encapsula el atributo status.
        
        Returns:
        ----------
        PackageStatus.
            Estado actual del Driver."""

        return self._status
    
    @classmethod
    def create(cls, sender_id: ID, id: Optional[str] = None) -> Package:
        """Método de clase que define, en nomenclatura de DDD, la creación
        de una entidad.
        
        Args:
        ----------
        sender_id: ID.
            ID del usuario quien hace el envío del Package.

        id: Optional[str].
            ID con el que desea crear la entidad. Si no pasa un valor, se creará
            un UUID4 en automático.
        
        Returns:
        ----------
        Package.
            Entidad de dominio."""

        instance = cls(id = id, sender_id = sender_id)
        return instance
    
    def __repr__(self) -> str:
        """Método dunder que permite representar a la entidad en un formato
        legible.
        
        Returns:
        ----------
        str.
            Representación del objeto."""
        
        return f"Package(id={self._id}, sender_id={self._sender_id}, driver_id={self._driver_id}, status={self._status})"
