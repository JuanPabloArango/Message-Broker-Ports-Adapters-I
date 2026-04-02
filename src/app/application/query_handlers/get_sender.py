"""Módulo que define un handler sobre el cual aplicar queries enfocadas en
obtener una entidad de dominio según identificación."""

# Librerías Externas.
from typing import Union

# Librerías Internas.
from app.domain.entities.sender import Sender

from app.application.ports.persistence.uow import UnitOfWorkPort
from app.application.queries.get_sender_by_id import GetSenderQuery

from app.application.dtos.sender import SenderDTO
from app.application.exceptions import SenderNotFound


class GetSenderHandler:
    """Clase que encapsula las lógicas del Query Handler."""

    def __init__(self, unit_of_work: UnitOfWorkPort) -> None:
        """Método de instanciación de objetos de la clase.
        
        Args:
        ----------
        unit_of_work: UnitOfWorkPort.
            Puerto de UoW enfocado en hacer transacciones atómicas."""
        
        self._unit_of_work = unit_of_work

    def handle(self, query: GetSenderQuery) -> Union[Sender, None]:
        """Método que se encarga de gestionar la búsqueda en su caso de uso.
        
        Args:
        ----------
        query: GetSenderQuery.
            Query que contiene la información necesaria para la búsqueda.
            
        Returns:
        ----------
        Union[Sender, None].
            Entidad de dominio hallada."""
        
        with self._unit_of_work as uow:
            sender = uow.sender_repository.get(sender_id = query.sender_id)
            if not sender:
                raise SenderNotFound(f"El Sender con ID {query.sender_id} no existe.")
            return SenderDTO.from_entity(sender)
