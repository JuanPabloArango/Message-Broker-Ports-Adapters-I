"""Módulo que contiene la realización del puerto de persistencia enfocado
en definir el contrato del repositorio para la entidad Driver."""

# Librerías Externas.
from typing import Any, Dict, List, Callable, Optional

from sqlalchemy import Column
from sqlalchemy.orm import Session

# Librerías Internas.
from app.domain.entities.sender import Sender

from app.application.ports.persistence.criteria import Operator, Criteria
from app.application.ports.persistence.repositories.sender_repository import SenderRepositoryPort

from app.application.exceptions import NotAValidAttribute

from app.infrastructure.persistence.orm.tables.sender import sender_table


class SQLSenderRepositoryAdapter(SenderRepositoryPort):
    """Clase que sirve como realización del puerto especificado."""

    OPERATOR_MAP: Dict[Operator, Callable[[str, Any], bool]] = {
        Operator.EQ: lambda col, val: col == val,
        Operator.NEQ: lambda col, val: col != val,
        Operator.GT: lambda col, val: col > val,
        Operator.GTE: lambda col, val: col >= val,
        Operator.LT: lambda col, val: col < val,
        Operator.LTE: lambda col, val: col <= val,
        Operator.IN: lambda col, val: col.in_(val)
    }

    COLUMN_MAP: Dict[str, Column] = {
        "id": sender_table.c.id,
        "status": sender_table.c.status,
        "created_at": sender_table.c.created_at,
        "updated_at": sender_table.c.updated_at
    }

    def __init__(self, session: Session) -> None:
        """Método de instanciación de objetos de clase.
        
        Args:
        ----------
        session: Session.
            Sesión que establece la conexión con la BD."""
        
        self._session = session

    def get(self, sender_id: str) -> Sender:
        """Método que permite obtener la entidad de dominio mediante
        la Primary Key asociada en la definición de la tabla.
        
        Args:
        ----------
        sender_id: str.
            ID del usuario que desea consultar.
        
        Returns:
        ----------
        Sender.
            Entidad de dominio."""
        
        sender = self._session.get(Sender, sender_id)
        return sender
    
    def save(self, sender: Sender) -> None:
        """Métoo que permite almacenar la entidad de dominio en la tabla
        de persistencia.
        
        Args:
        ----------
        sender: Sender.
            Entidad a almacenar."""
        
        self._session.add(sender)

    def list_all(self, criteria: Optional[Criteria]) -> List[Sender]:
        """Método que permite listar todas las entidades persistidas.

        Args:
        ----------
        criteria: Optional[Criteria].
            Criterios de búsqueda.
        
        Returns:
        ----------
        List[Sender].
            Entidades de dominio."""
        
        q = self._session.query(Sender)
        
        if criteria:
        
            for filter in criteria.filters:
                column = self.COLUMN_MAP.get(filter.field)
                if column is None:
                    raise NotAValidAttribute(f"El atributo {filter.field} no es un campo de filtrado válido.")
                
                condition = self.OPERATOR_MAP[filter.operator](column, filter.value)
                q = q.filter(condition)

            if criteria.pagination:
                pagination = criteria.pagination
                if pagination.order_by and self.COLUMN_MAP.get(pagination.order_by) is not None:
                    ordering_columns = self.COLUMN_MAP.get(pagination.order_by)
                    ordering_direction = ordering_columns.asc() if pagination.order_dir == "asc" else ordering_columns.desc()

                    q = q.order_by(ordering_direction)

                q = q.offset(pagination.offset).limit(pagination.limit)
        
        else:
            q = q.offset(0).limit(100)

        results = q.all()
        return results

