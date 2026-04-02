"""Módulo que contiene las lógicas de transformación de entidades de dominio
a objetos que se puedan transferir a fuentes externas."""

# Librerías Externas.
from __future__ import annotations
from typing import Optional

import datetime as dt
from dataclasses import dataclass

# Librerías Internas.
from app.domain.entities.package import Package


@dataclass(frozen = True)
class PackageDTO:
    """Clase que se encarga de tranformar una entidad de dominio
    a un objeto que se pueda comunicar con el exterior."""

    id: str
    sender_id: str
    driver_id: Optional[str]

    status: str
    created_at: dt.datetime
    updated_at: dt.datetime

    @classmethod
    def from_entity(cls, package: Package) -> PackageDTO:
        """Método de clase que tiene la responsabilidad de traducir
        entidades de dominio a objetos serializables.
        
        Args:
        ----------
        package: Package.
            Entidad a ser transformada.
            
        Returns:
        ----------
        PackageDTO.
            Objeto que contiene la información de dominio."""

        return cls(
            id = package.id.value,
            sender_id = package.sender_id.value,
            driver_id = package.driver_id.value if package.driver_id else None,
            status = package.status.value,
            created_at = package.created_at,
            updated_at = package.updated_at,
        )