"""Módulo que contiene las pruebas unitarias para el repositorio Package enfocado
en su Adapter de SQLAlchemy."""

# Librerías Externas.
from sqlalchemy import text
from sqlalchemy.orm import Session

# Librerías Internas.
from app.domain.entities.package import Package

from app.domain.value_objects.id import ID
from app.domain.value_objects.package_status import PackageStatus

from app.application.ports.persistence.criteria import Criteria, Pagination, Operator, Filter
from app.infrastructure.persistence.repository.sql.package_repository import SQLPackageRepositoryAdapter


class TestSQLPackageRepositoryAdapter:
    """Clase que encapsula las pruebas unitarias de la clase.
    SQLPackageRepositoryAdapter."""

    def test_repository_save(self, test_session: Session) -> None:
        """Método que contiene la prueba unitaria para validar adición de
        entidades al repositorio.
        
        Args:
        ----------
        test_session: Session.
            Sesión de conexión a BD."""
        
        repository = SQLPackageRepositoryAdapter(session = test_session)

        package = Package(sender_id = ID(value = "2"), id = "42")

        repository.save(package)
        test_session.commit()

        stmt = """
        SELECT id, sender_id, driver_id, status
        FROM packages
        WHERE id = "42";
        """

        row = test_session.execute(text(stmt)).one_or_none()

        assert row == ("42", "2", None, "PENDING"), "Valide que su repositorio sirva para almacenar entidades en BD."

    def test_repository_get(self, test_session: Session) -> None:
        """Método que contiene la prueba unitaria para validar adición de
        entidades al repositorio.
        
        Args:
        ----------
        test_session: Session.
            Sesión de conexión a BD."""
        
        repository = SQLPackageRepositoryAdapter(session = test_session)

        stmt = """
        INSERT INTO packages (id, sender_id, driver_id, status, created_at, updated_at)
        VALUES ("1", "33", "24", "DELIVERED", "2025-10-01 14:15:16", "2025-10-04 14:15:16"),
               ("2", "24", "33", "ASSIGNED", "2025-10-01 14:15:16", "2025-10-04 14:15:16");
        """

        test_session.execute(text(stmt))

        package = repository.get(package_id = "1")

        assert isinstance(package, Package), "Valide que su repositorio pueda obtener entidades."

        assert package.id == ID(value = "1"), "Valide que su obtención de entidades contenga los atributos adecuados."
        assert package.status == PackageStatus.DELIVERED, "Valide que su obtención de entidades contenga los atributos adecuados."

    def test_repository_list_all(self, test_session: Session) -> None:
        """Método que contiene la prueba unitaria para validar 
        que se puedan listar entidades.

        Args:
        ----------
        test_session: Session.
            Sesión de conexión a BD."""
        
        repository = SQLPackageRepositoryAdapter(session = test_session)

        stmt = """
        INSERT INTO packages (id, sender_id, driver_id, status, created_at, updated_at)
        VALUES ("1", "33", null, "PENDING", "2020-01-04 14:15:16", "2020-01-04 14:15:16"),
               ("2", "44", "3", "ASSIGNED", "2011-10-01 14:15:16", "2025-10-04 14:15:16"),
               ("3", "55", "2", "DELIVERED", "2012-10-01 14:15:16", "2025-10-04 14:15:16"),
               ("4", "44", "1", "ASSIGNED", "2013-10-01 14:15:16", "2025-10-04 14:15:16"),
               ("5", "33", null, "PENDING", "2020-02-04 14:15:16", "2020-02-04 14:15:16"),
               ("6", "55", "3", "ASSIGNED", "2015-10-01 14:15:16", "2025-10-04 14:15:16"),
               ("7", "55", "2", "DELIVERED", "2016-10-01 14:15:16", "2025-10-04 14:15:16"),
               ("8", "33", "1", "ASSIGNED", "2017-10-01 14:15:16", "2025-10-04 14:15:16"),
               ("9", "44", null, "PENDING", "2020-03-04 14:15:16", "2020-03-04 14:15:16"),
               ("10", "33", null, "PENDING", "2020-04-04 14:15:16", "2020-04-04 14:15:16"),
               ("11", "44", null, "PENDING", "2020-05-04 14:15:16", "2020-05-04 14:15:16"),
               ("12", "55", null, "PENDING", "2020-06-04 14:15:16", "2020-06-04 14:15:16"),
               ("13", "33", "1", "DELIVERED", "2011-10-01 14:15:16", "2025-10-04 14:15:16"),
               ("14", "44", "2", "ASSIGNED", "2012-10-01 14:15:16", "2025-10-04 14:15:16"),
               ("15", "44", "3", "DELIVERED", "2013-10-01 14:15:16", "2025-10-04 14:15:16"),
               ("16", "55", "3", "ASSIGNED", "2014-10-01 14:15:16", "2025-10-04 14:15:16"),
               ("17", "55", "2", "DELIVERED", "2015-10-01 14:15:16", "2025-10-04 14:15:16"),
               ("18", "33", "1", "ASSIGNED", "2016-10-01 14:15:16", "2025-10-04 14:15:16"),
               ("19", "44", null, "PENDING", "2025-07-04 14:15:16", "2025-07-04 14:15:16"),
               ("20", "55", "1", "ASSIGNED", "2018-10-01 14:15:16", "2025-10-04 14:15:16");
        """

        test_session.execute(text(stmt))
        
        filter = Filter(field = "status", value = "PENDING", operator = Operator.EQ)
        pagination = Pagination(limit = 5, order_by = "created_at", order_dir = "asc")
        criteria = Criteria(filters = [filter], pagination = pagination)

        pending_packages = repository.list_all(criteria = criteria)

        assert len(pending_packages) == 5, "Valide que obtenga la cantidad de entidades adecuadas según sus filtros y paginación."
        assert all(isinstance(package, Package) for package in pending_packages), "Valide que haya obtenido las entidades de dominio."
        assert pending_packages[0].id.value == "1", "Valide que el ordenamiento sea el adecuado."

        filter1 = Filter(field = "status", value = "DELIVERED", operator = Operator.NEQ)
        filter2 = Filter(field = "created_at", value = "2015-01-01", operator = Operator.GTE)

        pagination = Pagination(limit = 100, order_by = "created_at", order_dir = "asc")
        criteria = Criteria(filters = [filter1, filter2], pagination = pagination)

        filtered_packages = repository.list_all(criteria = criteria)

        assert len(filtered_packages) == 11, "Valide que obtenga la cantidad de entidades adecuadas según sus filtros y paginación."

