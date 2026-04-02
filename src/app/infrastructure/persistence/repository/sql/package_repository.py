"""Módulo que contiene la realización del puerto de persistencia enfocado
en definir el contrato del repositorio para la entidad Package."""

# Librerías Externas.
from typing import Any, List, Dict, Callable

from sqlalchemy import Column, select
from sqlalchemy.orm import Session

# Librerías Internas.
from app.domain.entities.package import Package

from app.application.ports.persistence.criteria import Operator, Criteria
from app.application.ports.persistence.repositories.package_repository import PackageRepositoryPort

from app.application.exceptions import NotAValidAttribute

from app.infrastructure.persistence.orm.tables.package import packages_table


class SQLPackageRepositoryAdapter(PackageRepositoryPort):
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
        "id": packages_table.c.id,
        "sender_id": packages_table.c.sender_id,
        "driver_id": packages_table.c.driver_id,
        "status": packages_table.c.status,
        "created_at": packages_table.c.created_at,
        "updated_at": packages_table.c.updated_at
    }

    def __init__(self, session: Session) -> None:
        """Método de instanciación de objetos de clase.
        
        Args:
        ----------
        session: Session.
            Sesión que establece la conexión con la BD."""
        
        self._session = session

    def get(self, package_id: str) -> Package:
        """Método que permite obtener la entidad de dominio mediante
        la Primary Key asociada en la definición de la tabla.
        
        Args:
        ----------
        package_id: str.
            ID del paquete que desea consultar.
        
        Returns:
        ----------
        Package.
            Entidad de dominio."""
        
        package = self._session.get(Package, package_id)
        return package
    
    def save(self, package: Package) -> None:
        """Métoo que permite almacenar la entidad de dominio en la tabla
        de persistencia.
        
        Args:
        ----------
        package: Package.
            Entidad a almacenar."""
        
        self._session.add(package)

    def list_all(self, criteria: Criteria) -> List[Package]:
        """Método que permite listar todas las entidades persistidas.

        Args:
        ----------
        criteria: Criteria.
            Criterios de búsqueda sobre todas las entidades.
        
        Returns:
        ----------
        List[Package].
            Entidades de dominio."""
        
        q = self._session.query(Package)
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

        filterd_packages = q.all()
        return filterd_packages
    
    def list_pending(self) -> List[Package]:
        """Método que permite listar todas los paquetes que no han sido asignados.
        
        Returns:
        ----------
        List[Package].
            Entidades de dominio."""
        
        filter_column = self.COLUMN_MAP["status"]
        stmt = select(Package).where(filter_column == "PENDING")

        packages = self._session.scalars(stmt).all()
        return packages
