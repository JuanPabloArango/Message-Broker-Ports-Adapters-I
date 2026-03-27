"""Módulo que contiene las pruebas unitarias para el Object Relational Mapping
entre la entidad de dominio Driver y su tabla de persistencia."""

# Librerías Externas.
import datetime as dt

from sqlalchemy import text
from sqlalchemy.orm import Session

# Librerías Internas.
from app.domain.entities.driver import Driver

from app.domain.value_objects.id import ID
from app.domain.value_objects.driver_status import DriverStatus
from app.domain.value_objects.delivery_date import DeliveryDate


class TestDriverORM:
    """Clase que encapsula las pruebas unitarias del ORM de Sender."""

    def test_driver_insertion(self, test_session: Session) -> None:
        """Método que contiene la prueba unitaria para validar la correcta
        inserción de entidades de dominio.
        
        Args:
        ----------
        test_session: Session.
            Sesión de conexión a BD."""

        stmt = """
        INSERT INTO drivers (id, status, last_delivery, created_at, updated_at)
        VALUES (:id, :status, :last_delivery, :created_at, :updated_at)
        """

        test_session.execute(text(stmt), {"id": "1312",
                                          "status": "OCCUPIED",
                                          "last_delivery": dt.datetime(2026, 3, 24, 9, 48, 30),
                                          "created_at": dt.datetime(2024, 4, 8, 10, 10, 10),
                                          "updated_at": dt.datetime(2026, 3, 24, 9, 48, 30)})
        
        driver = test_session.get(Driver, "1312")

        assert isinstance(driver, Driver), "Valide que el registro de la tabla se haya cargado como entidad de dominio."

        assert driver.id == ID(value = "1312"), "Valide que en su entidad se carguen los VO adecuados con su valor correcto."
        assert driver.status == DriverStatus.OCCUPIED, "Valide que en su entidad se carguen los VO adecuados con su valor correcto."
        assert driver.last_delivery == DeliveryDate(last_delivery = "2026-03-24 09:48:30"), "Valide que en su entidad se carguen los VO adecuados con su valor correcto."

        assert hasattr(driver, "_created_at") and hasattr(driver, "_updated_at"), "Valide que columnas de su tabla se mapeen como atributos de su instancia."

    def test_driver_bulk_insertion(self, test_session: Session) -> None:
        """Método que contiene la prueba unitaria para validar la correcta
        inserción masiva de entidades de dominio.
        
        Args:
        ----------
        test_session: Session.
            Sesión de conexión a BD."""

        stmt = """
        INSERT INTO drivers (id, status, last_delivery, created_at, updated_at)
        VALUES ("1", "OCCUPIED", "2023-10-01 12:00:00", "2022-10-01 12:00:00", "2023-10-01 12:00:00"),
               ("2", "AVAILABLE", "2024-10-01 12:00:00", "2023-10-01 12:00:00", "2024-10-01 12:00:00"),
               ("3", "OCCUPIED", "2025-10-01 12:00:00", "2024-10-01 12:00:00", "2025-10-01 12:00:00");
        """

        test_session.execute(text(stmt))
        
        occupied_drivers = test_session.query(Driver).where(Driver._status == "OCCUPIED").all()
        available_drivers = test_session.query(Driver).where(Driver._status == "AVAILABLE").all()

        assert len(occupied_drivers) == 2, "Valide que se puedan aplicar filtros de obtención mediante atributos de instancia."
        assert len(available_drivers) == 1, "Valide que se puedan aplicar filtros de obtención mediante atributos de instancia."
        assert all((isinstance(driver, Driver) for driver in occupied_drivers)), "Valide que las filas cargadas de la tabla se cargan como entidades."

    def test_driver_retrieval(self, test_session: Session) -> None:
        """Método que contiene la prueba unitaria para validar la correcta
        extracción de una entidad de dominio.
        
        Args:
        ----------
        test_session: Session.
            Sesión de conexión a BD."""

        driver = Driver(id = "123", last_delivery = "2026-04-03 12:12:12")

        test_session.add(driver)
        test_session.commit()

        stmt = """
        SELECT id, status, last_delivery
        FROM drivers
        WHERE id = "123"
        """

        row = test_session.execute(text(stmt)).one()

        assert row == ("123", "AVAILABLE", "2026-04-03 12:12:12.000000"), "Valide que la entidad insertada si haya almacenado los valores correctos en tabla."
        
    def test_driver_bulk_retrieval(self, test_session: Session) -> None:
        """Método que contiene la prueba unitaria para validar la correcta
        extracción de varias entidades de dominio.
        
        Args:
        ----------
        test_session: Session.
            Sesión de conexión a BD."""

        driver1 = Driver(id = "123", last_delivery = "2026-04-03 12:12:12")
        driver2 = Driver()
        driver3 = Driver(id = "321")

        test_session.add_all((driver1, driver2, driver3))
        test_session.commit()

        stmt = """
        SELECT id, status, last_delivery
        FROM drivers;
        """

        drivers = test_session.execute(text(stmt)).all()

        assert len(drivers) == 3, "Valide que en su tabla haya tantas filas como entidades de dominio."
        assert drivers[0] == ("123", "AVAILABLE", "2026-04-03 12:12:12.000000"), "Valide que sus filas tengan los valores."
        assert len(drivers[1][0]) == 32, "Valide que cuando se crea una entidad sin ID, se genera automáticamente un UUID4."

    def test_driver_update(self, test_session: Session) -> None:
        """Método que contiene la prueba unitaria para validar que la actualización
        de una entidad se puede ver reflejada en su persistencia.
        
        Args:
        ----------
        test_session: Session.
            Sesión de conexión a BD."""

        created_driver = Driver(id = "123")

        test_session.add(created_driver)
        test_session.commit()

        retrieved_driver = test_session.get(Driver, "123")

        assert retrieved_driver.status == DriverStatus.AVAILABLE, "Valide un estado inicial."
        assert created_driver == retrieved_driver, "Valide que los objetos de dominicio persistidos y obtenidos sean iguales."
        
        retrieved_driver.mark_as_occupied()
        test_session.commit()

        stmt = """
        SELECT id, status
        FROM drivers
        WHERE id = "123";
        """

        row = test_session.execute(text(stmt)).one()

        assert row == ("123", "OCCUPIED"), "Valide que haya habido una actualización de estado."

    def test_driver_deletion(self, test_session: Session) -> None:
        """Método que contiene la prueba unitaria para validar la correcta
        eliminación de una entidad de dominio.
        
        Args:
        ----------
        test_session: Session.
            Sesión de conexión a BD."""

        created_driver = Driver(id = "420")

        test_session.add(created_driver)
        test_session.commit()

        retrieved_driver = test_session.get(Driver, ID(value = "420"))

        assert isinstance(retrieved_driver, Driver), "Valida que se haya obtenido la entidad de dominio."

        test_session.delete(retrieved_driver)
        test_session.commit()

        stmt = """
        SELECT id, status
        FROM senders
        WHERE id = "420";
        """

        row = test_session.execute(text(stmt)).one_or_none()

        assert not row, "Valide que haya habido una eliminación de la entidad.."

