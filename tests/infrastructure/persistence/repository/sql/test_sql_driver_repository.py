"""Módulo que contiene las pruebas unitarias para el repositorio Driver enfocado
en su Adapter de SQLAlchemy."""

# Librerías Externas.
from sqlalchemy import text
from sqlalchemy.orm import Session

# Librerías Internas.
from app.domain.entities.driver import Driver

from app.domain.value_objects.id import ID
from app.domain.value_objects.driver_status import DriverStatus

from app.application.ports.persistence.criteria import Criteria, Filter, Operator, Pagination

from app.infrastructure.persistence.repository.sql.driver_repository import SQLDriverRepositoryAdapter


class TestSQLDriverRepositoryAdapter:
    """Clase que encapsula las pruebas unitarias de la clase.
    SQLDriverRepositoryAdapter."""

    def test_repository_save(self, test_session: Session) -> None:
        """Método que contiene la prueba unitaria para validar adición de
        entidades al repositorio.
        
        Args:
        ----------
        test_session: Session.
            Sesión de conexión a BD."""
        
        repository = SQLDriverRepositoryAdapter(session = test_session)

        driver = Driver(id = "42")

        repository.save(driver)
        test_session.commit()

        stmt = """
        SELECT id, status
        FROM drivers
        WHERE id = "42";
        """

        row = test_session.execute(text(stmt)).one_or_none()

        assert row == ("42", "AVAILABLE"), "Valide que su repositorio sirva para almacenar entidades en BD."

    def test_repository_get(self, test_session: Session) -> None:
        """Método que contiene la prueba unitaria para validar adición de
        entidades al repositorio.
        
        Args:
        ----------
        test_session: Session.
            Sesión de conexión a BD."""
        
        repository = SQLDriverRepositoryAdapter(session = test_session)

        stmt = """
        INSERT INTO drivers (id, status, created_at, updated_at)
        VALUES ("1", "AVAILABLE", "2025-10-01 14:15:16", "2025-10-04 14:15:16"),
               ("2", "OCCUPIED", "2025-10-01 14:15:16", "2025-10-04 14:15:16");
        """

        test_session.execute(text(stmt))

        driver = repository.get(driver_id = "2")

        assert isinstance(driver, Driver), "Valide que su repositorio pueda obtener entidades."

        assert driver.id == ID(value = "2"), "Valide que su obtención de entidades contenga los atributos adecuados."
        assert driver.status == DriverStatus.OCCUPIED, "Valide que su obtención de entidades contenga los atributos adecuados."

    def test_repository_list_all(self, test_session: Session) -> None:
        """Método que contiene la prueba unitaria para validar 
        que se puedan listar entidades.

        Args:
        ----------
        test_session: Session.
            Sesión de conexión a BD."""
        
        repository = SQLDriverRepositoryAdapter(session = test_session)

        stmt = """
        INSERT INTO drivers (id, status, last_delivery, created_at, updated_at)
        VALUES ("1", "AVAILABLE", "2020-12-01 00:00:30", "2025-10-01 14:15:16", "2025-10-04 14:15:16"),
               ("2", "OCCUPIED", "2020-12-01 00:01:00", "2025-10-01 14:15:16", "2025-10-04 14:15:16"),
               ("3", "AVAILABLE", "2020-12-01 00:02:00", "2025-10-01 14:15:16", "2025-10-04 14:15:16"),
               ("4", "OCCUPIED", "2020-12-01 00:03:00", "2025-10-01 14:15:16", "2025-10-04 14:15:16"),
               ("5", "AVAILABLE", "2020-12-01 00:04:00", "2025-10-01 14:15:16", "2025-10-04 14:15:16"),
               ("6", "OCCUPIED", "2020-12-01 00:05:00", "2025-10-01 14:15:16", "2025-10-04 14:15:16"),
               ("7", "AVAILABLE", "2020-12-01 00:06:00", "2025-10-01 14:15:16", "2025-10-04 14:15:16"),
               ("8", "OCCUPIED", "2020-12-01 00:07:00", "2025-10-01 14:15:16", "2025-10-04 14:15:16"),
               ("9", "AVAILABLE", "2020-12-01 00:08:00", "2025-10-01 14:15:16", "2025-10-04 14:15:16"),
               ("10", "OCCUPIED", "2020-12-01 00:09:00", "2025-10-01 14:15:16", "2025-10-04 14:15:16"),
               ("11", "AVAILABLE", "2020-12-01 00:10:00", "2025-10-01 14:15:16", "2025-10-04 14:15:16"),
               ("12", "OCCUPIED", "2020-12-01 00:11:00", "2025-10-01 14:15:16", "2025-10-04 14:15:16");
        """

        test_session.execute(text(stmt))

        filter = Filter(field = "status", value = ["AVAILABLE", "OCCUPIED"], operator = Operator.IN)
        pagination = Pagination(limit = 4, offset = 2, order_by = "updated_at", order_dir = "desc")

        criteria = Criteria(filters = [filter], pagination = pagination)

        filtered_drivers = repository.list_all(criteria)

        assert len(filtered_drivers) == 4, "Valide que la paginación es correcta."
        assert filtered_drivers[0].id.value == "3", "Valide que sus registros si comiencen desde donde indica el offset."

        filter = Filter(field = "status", value = "AVAILABLE", operator = Operator.EQ)
        pagination = Pagination(limit = 5, order_by = "last_delivery", order_dir = "asc")

        criteria = Criteria(filters = [filter], pagination = pagination)

        available_drivers = repository.list_all(criteria)

        assert len(available_drivers) == 5, "Valide que la paginación es correcta."
        assert available_drivers[0].id.value == "1", "Valide que sus registros si comiencen desde donde indica el offset."
