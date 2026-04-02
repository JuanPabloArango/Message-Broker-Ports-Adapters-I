"""Módulo que define un handler sobre el cual aplicar queries enfocadas a
obtener varias entidades de dominio según parámetros de búsqueda del usuario."""

# Librerías Externas.
from typing import List

# Librerías Internas.
from app.domain.entities.sender import Sender

from app.application.dtos.sender import SenderDTO
from app.application.ports.persistence.uow import UnitOfWorkPort
from app.application.queries.list_senders import ListSendersQuery


class ListSendersHandler:
    """Clase que encapsula las lógicas del Query Handler."""

    def __init__(self, unit_of_work: UnitOfWorkPort) -> None:
        """Método de instanciación de objetos de la clase.
        
        Args:
        ----------
        unit_of_work: UnitOfWorkPort.
            Puerto de UoW enfocado en hacer transacciones atómicas."""
        
        self._unit_of_work = unit_of_work

    def handle(self, query: ListSendersQuery) -> List[Sender]:
        """Método que se encarga de gestionar la búsqueda en su caso de uso.
        
        Args:
        ----------
        query: ListSendersQuery.
            Query que contiene la información necesaria para la búsqueda.
            
        Returns:
        ----------
        List[Sender].
            Resultados que concuerdan con la búsqueda."""
        
        with self._unit_of_work as uow:
            senders = uow.sender_repository.list_all(criteria = query.criteria)
            return [SenderDTO.from_entity(sender) for sender in senders]
