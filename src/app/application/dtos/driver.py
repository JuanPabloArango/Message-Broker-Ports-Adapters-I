"""Módulo que contiene las lógicas de transformación de entidades de dominio
a objetos que se puedan transferir a fuentes externas."""

# Librerías Externas.
from __future__ import annotations

import datetime as dt
from dataclasses import dataclass

# Librerías Internas.
from app.domain.entities.driver import Driver


@dataclass(frozen = True)
class DriverDTO:
    """Clase que se encarga de tranformar una entidad de dominio
    a un objeto que se pueda comunicar con el exterior."""

    id: str
    status: str
    last_delivery: dt.datetime
    created_at: dt.datetime
    updated_at: dt.datetime

    @classmethod
    def from_entity(cls, driver: Driver) -> DriverDTO:
        """Método de clase que tiene la responsabilidad de traducir
        entidades de dominio a objetos serializables.
        
        Args:
        ----------
        driver: Driver.
            Entidad a ser transformada.
            
        Returns:
        ----------
        SenderDTO.
            Objeto que contiene la información de dominio."""

        return cls(
            id = driver.id.value,
            status = driver.status.value,
            last_delivery = driver.last_delivery.last_delivery,
            created_at = driver.created_at,
            updated_at = driver.updated_at
        )
