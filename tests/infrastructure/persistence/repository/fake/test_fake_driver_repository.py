"""Módulo que contiene las pruebas unitarias para el repositorio Driver enfocado
en su Adapter de Fake."""

# Librerías Externas.
from typing import List

import datetime as dt

# Librerías Internas.
from app.domain.entities.driver import Driver

from app.domain.value_objects.driver_status import DriverStatus
from app.domain.value_objects.delivery_date import DeliveryDate

from app.application.ports.persistence.criteria import Criteria, Filter, Pagination, Operator

from app.infrastructure.persistence.repository.fake.driver_repository import FakeDriverRepositoryAdapter


class TestFakeDriverRepositoryAdapter:
    """Clase que encapsula las pruebas unitarias para el adapter Fake
    del repositorio."""

    def test_repository_save(self, base_drivers: List[Driver]) -> None:
        """Método que contiene la prueba unitaria para validar que se
        puede almacenar una entidad de dominio en el repositorio.
        
        Args:
        ----------
        base_drivers: List[Driver].
            Fixture que simula una base que contiene estas entidades persistidas."""

        repository = FakeDriverRepositoryAdapter(base = base_drivers)

        driver = Driver(id = "7", last_delivery = "2000-10-10 10:10:10")

        repository.save(driver = driver)
        retrived_driver = next((driver for driver in repository._base if driver.id.value == "7"), None)

        assert driver == retrived_driver, "Valida que se haya almacenado la entidad de dominio."

        assert isinstance(retrived_driver, Driver), "Valida que la entidad de dominio almacenada sea igual a la persistida."
        assert driver.last_delivery == DeliveryDate("2000-10-10 10:10:10"), "Valida que los valores almacenados correspondan a la realidad."

    def test_repository_get(self, base_drivers: List[Driver]) -> None:
        """Método que contiene la prueba unitaria para validar que se puede
        obtener una entidad de dominio del repositorio.
        
        Args:
        ----------
        base_drivers: List[Driver].
            Fixture que simula una base que contiene estas entidades persistidas."""

        repository = FakeDriverRepositoryAdapter(base = base_drivers)

        driver = repository.get(driver_id = "2")

        assert isinstance(driver, Driver), "Valida que la entidad obtenida sea adecuada."

        assert not driver.last_delivery.last_delivery, "Valida que el estado sea el adecuado."
        assert driver.status == DriverStatus.OCCUPIED, "Valida que el estado sea el adecuado."

        driver = repository.get(driver_id = "1")

        assert isinstance(driver, Driver), "Valida que la entidad obtenida sea adecuada."
        
        assert driver.status == DriverStatus.AVAILABLE, "Valida que el estado sea el adecuado."
        assert driver.last_delivery.last_delivery == dt.datetime.fromisoformat("2024-05-12 23:10:11"), "Valida que el estado sea el adecuado."

    def test_list_all(self, base_drivers: List[Driver]) -> None:
        """Método que contiene la prueba unitaria para validar que se pueden
        filtrar y obtener varias entidades de dominio a la vez de un repositorio
        según un criterio de búsqueda.
        
        Args:
        ----------
        base_drivers: List[Driver].
            Fixture que simula una base que contiene estas entidades persistidas."""

        repository = FakeDriverRepositoryAdapter(base = base_drivers)

        criteria = Criteria(
            filters = [
                Filter(field = "status", value = DriverStatus.OCCUPIED, operator = Operator.EQ),
                Filter(field = "last_delivery", value = DeliveryDate("2025-01-01 00:00:00"), operator = Operator.GT)
            ],
            pagination = Pagination(limit = 2)
        )

        filtered_drivers = repository.list_all(criteria = criteria)

        assert len(filtered_drivers) == 1, "Valide que el filtro se aplique correctamente."
