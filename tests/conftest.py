"""Módulo que contiene los fixtures necesarios para la ejecución de pruebas
unitarias y de integración."""

# Librerías Externas.
from typing import List, Type, Callable, Generator

import pytest

from sqlalchemy import Engine, create_engine
from sqlalchemy.orm import Session, sessionmaker, clear_mappers

# Librerías Internas.
from app.domain.entities.driver import Driver
from app.domain.entities.sender import Sender
from app.domain.entities.package import Package

from app.domain.value_objects.id import ID

from app.infrastructure.persistence.orm import start_mappers
from app.infrastructure.persistence.orm.base import metadata


@pytest.fixture
def create_test_engine() -> Engine:
    """Fixture para crear un motor de bases de datos para pruebas."""

    engine: Engine = create_engine("sqlite:///:memory:")
    metadata.create_all(engine)
    return engine

@pytest.fixture
def create_session_factory(create_test_engine: Callable[[], Engine]) -> Generator[Type[Session], None, None]:
    """Fixture que permite generar un Session Factory para creación
    de sesiones de conexión a BD.
    
    Args:
    ----------
    create_test_engine: Callable[[], Engine].
        Fixture que permite crear una BD en memoria para tests.
    
    Returns:
    ----------
    Generator[Type[Session], None, None].
        Generador que permite crear un Factory de sesiones para luego seguir
        contexto de ejecución que permita limpiar ambiente de pruebas."""

    start_mappers()

    session_factory = sessionmaker(bind = create_test_engine)
    yield session_factory

    clear_mappers()

@pytest.fixture
def test_session(create_session_factory: Generator[Type[Session], None, None]) -> Session:
    """Fixture que permite crear una sesión de conexión a BD.
    
    Args:
    ----------
    Generator[Type[Session], None, None].
        Generador que contiene un Factory que permite crear las sesiones.
    
    Returns:
    ----------
    Session.
        Sesión de conexión a BD."""

    session: Session = create_session_factory()
    return session

@pytest.fixture
def base_senders() -> List[Sender]:
    """Fixture que define una base persistida de Senders.
    
    Returns:
    ----------
    List[Sender].
        Lista base que se ha extraído de la BD."""
    
    sender1 = Sender(id = "1")
    sender2 = Sender(id = "2")
    sender3 = Sender(id = "3")

    sender1.verify()
    sender3.verify()

    return [sender1, sender2, sender3]

@pytest.fixture
def base_drivers() -> List[Driver]:
    """Fixture que define una base persistida de Senders.
    
    Returns:
    ----------
    List[Sender].
        Lista base que se ha extraído de la BD."""
    
    driver1 = Driver(id = "1", last_delivery = "2024-05-12 23:10:11")
    driver2 = Driver(id = "2")
    driver3 = Driver(id = "3")
    driver4 = Driver(id = "4", last_delivery = "2025-12-12 05:23:18")
    driver5 = Driver(id = "5")
    driver6 = Driver(id = "6", last_delivery = "2020-01-10 05:23:18")

    driver2.mark_as_occupied()
    driver4.mark_as_occupied()
    driver5.mark_as_occupied()

    return [driver1, driver2, driver3, driver4, driver5, driver6]

@pytest.fixture
def base_packages() -> List[Package]:
    """Fixture que define una base persistida de Senders.
    
    Returns:
    ----------
    List[Sender].
        Lista base que se ha extraído de la BD."""
    
    package1 = Package(id = "1", sender_id = ID("42"))
    package2 = Package(id = "2", sender_id = ID("64"))
    package3 = Package(id = "3", sender_id = ID("13"))

    package2.assign_driver(driver_id = ID("42"))

    return [package1, package2, package3]
