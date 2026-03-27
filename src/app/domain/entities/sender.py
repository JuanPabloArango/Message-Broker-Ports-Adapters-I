"""Módulo que contiene la definición de la entidad de dominio Sender."""

# Librerías Externas.
from __future__ import annotations
from typing import Optional

import datetime as dt

# Librerías Internas.
from app.domain.value_objects.id import ID
from app.domain.value_objects.sender_status import SenderStatus

from app.domain.exceptions import SenderAlreadyVerified


class Sender:
    """Clase que contiene la definición de la entidad Aggregate Root Sender."""

    def __init__(self, id: Optional[str] = None) -> None:
        """Método de instanciación de objetos de la clase.
        
        Args:
        ----------
        id: Optional[str].
            ID que desea asignarle a la entidad. Si es None, se generará en
            automático."""
        
        self._id: ID = ID(value = id)
        self._status: SenderStatus = SenderStatus.UNVERIFIED

        self._created_at: Optional[dt.datetime] = None
        self._updated_at: Optional[dt.datetime] = None

    def verify(self) -> None:
        """Método que permite validar el Sender y, por ende, habilitarlo
        para hacer envíos."""

        if self._status != SenderStatus.UNVERIFIED:
            raise SenderAlreadyVerified("No puedes validar a un Sender ya validado.")
        
        self._status = SenderStatus.VERIFIED

    def can_send_packages(self) -> bool:
        """Método que permite validar si un Sender puede o no enviar
        paquetes.
        
        Returns:
        ----------
        bool.
            True si puede enviar paquetes."""
        
        if self._status == SenderStatus.VERIFIED:
            return True
        return False

    @property
    def id(self) -> ID:
        """Propiedad que encapsula el ID de la entidad.
        
        Returns:
        ----------
        ID.
            ID de la entidad."""
        
        return self._id
    
    @property
    def status(self) -> SenderStatus:
        """Propieda que encapsula el atributo status.
        
        Returns:
        ----------
        SenderStatus.
            Estado actual del Sender."""

        return self._status
    
    @classmethod
    def create(cls, id: Optional[str] = None) -> Sender:
        """Método de clase que define, en nomenclatura de DDD, la creación
        de una entidad.
        
        Args:
        ----------
        id: Optional[str].
            ID con el que desea crear la entidad. Si no pasa un valor, se creará
            un UUID4 en automático.
        
        Returns:
        ----------
        Sender.
            Entidad de dominio."""

        instance = cls(id = id)
        return instance
    
    def __repr__(self) -> str:
        """Método dunder que permite representar a la entidad en un formato
        legible.
        
        Returns:
        ----------
        str.
            Representación del objeto."""
        
        return f"Sender(id={self._id}, status={self._status})"
