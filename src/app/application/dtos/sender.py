"""Módulo que contiene las lógicas de transformación de entidades de dominio
a objetos que se puedan transferir a fuentes externas."""

# Librerías Externas.
from __future__ import annotations

import datetime as dt
from dataclasses import dataclass

# Librerías Internas.
from app.domain.entities.sender import Sender


@dataclass(frozen = True)
class SenderDTO:
    """Clase que se encarga de tranformar una entidad de dominio
    a un objeto que se pueda comunicar con el exterior."""

    id: str
    status: str
    created_at: dt.datetime
    updated_at: dt.datetime

    @classmethod
    def from_entity(cls, sender: Sender) -> SenderDTO:
        """Método de clase que tiene la responsabilidad de traducir
        entidades de dominio a objetos serializables.
        
        Args:
        ----------
        sender: Sender.
            Entidad a ser transformada.
            
        Returns:
        ----------
        SenderDTO.
            Objeto que contiene la información de dominio."""
        
        return cls(
            id = sender.id.value,
            status = sender.status.value,
            created_at = sender.created_at,
            updated_at = sender.updated_at,
        )
