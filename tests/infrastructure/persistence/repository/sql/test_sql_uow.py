"""Módulo que contiene las pruebas unitarias para el adaptador de atomicidad
de trabajo de SQLAlchemy (objeto colaborador)."""

# Librerías Externas.
from typing import Type, Generator

import pytest

from sqlalchemy import text
from sqlalchemy.orm import Session

# Librerías Internas.
from app.domain.entities.driver import Driver
from app.domain.entities.sender import Sender
from app.domain.entities.package import Package

from app.domain.value_objects.sender_status import SenderStatus

from app.infrastructure.persistence.repository.sql.uow import SQLUnitOfWorkAdapter


class TestSQLUnitOfWorkAdapter:
    """Clase que encapsula las pruebas unitarias del adaptador
    SQLUnitOfWorkAdapter."""

    def test_commit(self, create_session_factory: Generator[Type[Session], None, None]) -> None:
        """Método que contiene la prueba unitaria enfocada en validar
        la confirmación de cambios en bases de datos.
        
        Args:
        ----------
        create_session_factory: Generator[Type[Session], None, None].
            Factory como generador para luego descargar mappers."""
        
        session = create_session_factory()
        unit_of_work = SQLUnitOfWorkAdapter(session_factory = create_session_factory)

        assert not hasattr(unit_of_work, "driver_repository"), "Valide que no tenga accesos a atributos fuera del context manager."

        with unit_of_work as uow:

            driver = Driver(id = "43")
            sender = Sender(id = "56")
            package = Package(id = "78", sender_id = sender.id)

            uow.driver_repository.save(driver)
            uow.sender_repository.save(sender)
            uow.package_repository.save(package)

            uow.commit()

            assert hasattr(unit_of_work, "driver_repository"), "Valide que tenga accesos a atributos fuera del context manager."

        driver = session.get(Driver, "43")
        sender = session.get(Sender, "56")
        package = session.get(Package, "78")

        assert isinstance(driver, Driver), "Valide que haya obtenido la entidad almacenada."
        assert isinstance(sender, Sender), "Valide que haya obtenido la entidad almacenada."
        assert isinstance(package, Package), "Valide que haya obtenido la entidad almacenada."

        stmt = """
        SELECT a.id AS package_id, a.status AS package_status,
               b.id AS sender_id, b.status AS sender_status
        FROM packages AS a
        INNER JOIN senders AS b
                   ON a.sender_id = b.id
        """

        row = session.execute(text(stmt)).all()

        assert row == [("78", "PENDING", "56", "UNVERIFIED")], "Valide que haya un registro completo del sistema en commit."

    def test_rollback_missing_commit(self, create_session_factory: Generator[Type[Session], None, None]) -> None:
        """Método que contiene la prueba unitaria enfocada en validar que si no se
        da la confirmación de cambios en bases de datos, no se persisten los cambios.
        
        Args:
        ----------
        create_session_factory: Generator[Type[Session], None, None].
            Factory como generador para luego descargar mappers."""
        
        session = create_session_factory()
        unit_of_work = SQLUnitOfWorkAdapter(session_factory = create_session_factory)

        with unit_of_work as uow:

            driver = Driver(id = "43")
            sender = Sender(id = "56")
            package = Package(id = "78", sender_id = sender.id)

            uow.driver_repository.save(driver)
            uow.sender_repository.save(sender)
            uow.package_repository.save(package)

            uow.commit()

        retrived_sender = session.get(Sender, "56")
        assert retrived_sender.status == SenderStatus.UNVERIFIED, "Valide que la transacción culmine con el estado esperado."

        with unit_of_work as uow:
            
            sender = uow.sender_repository.get(sender_id = "56")
            sender.verify()

        retrived_sender = session.get(Sender, "56")
        assert retrived_sender.status == SenderStatus.UNVERIFIED, "Valide que la transacción no cambie su estado si no hace commit."

    def test_rollback_on_exception(self, create_session_factory: Generator[Type[Session], None, None]) -> None:
        """Método que contiene la prueba unitaria enfocada en validar
        que si ocurre un error en transacción, la persistencia queda justo
        como estaba antes de la transacción.
        
        Args:
        ----------
        create_session_factory: Generator[Type[Session], None, None].
            Factory como generador para luego descargar mappers."""
        
        session = create_session_factory()
        unit_of_work = SQLUnitOfWorkAdapter(session_factory = create_session_factory)

        with pytest.raises(ValueError):
            with unit_of_work as uow:

                driver = Driver(id = "43")
                sender = Sender(id = "56")
                package = Package(id = "78", sender_id = sender.id)

                uow.driver_repository.save(driver)
                uow.sender_repository.save(sender)
                uow.package_repository.save(package)

                raise ValueError("Error simulador")

        retrived_sender = session.get(Sender, "56")
        assert retrived_sender is None, "Valide que la transacción culmine con el estado esperado."
