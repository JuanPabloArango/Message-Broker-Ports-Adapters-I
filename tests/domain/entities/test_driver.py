"""Módulo que contiene las pruebas unitarias para la entidad de dominio Driver."""

# Librerías Externas.
import pytest

# Librerías Internas.
from app.domain.entities.driver import Driver

from app.domain.value_objects.id import ID
from app.domain.value_objects.delivery_date import DeliveryDate
from app.domain.value_objects.driver_status import DriverStatus

from app.domain.exceptions import DriverAlreadyAvailableError, DriverCurrenlyOccupiedError


class TestDriver:
    """Clase que encapsula las pruebas unitarias para Driver."""

    def test_init_driver(self) -> None:
        """Método que contiene la prueba unitaria para validar la instanciación
        de la entidad Driver."""

        instance = Driver(id = "321", last_delivery = "2025-10-01 14:30:45")

        assert instance.id == ID(value = "321"), "Valide que el ID de la entidad tenga el tipo y valor correcto."
        assert instance.status == DriverStatus.AVAILABLE, "Valide que todo conductor se instancia como 'AVAILABLE'."
        assert instance.last_delivery == DeliveryDate(last_delivery = "2025-10-01 14:30:45"), "Valide que el último envío tenga la fecha correcta."

    def test_create_driver(self) -> None:
        """Método que contiene la prueba unitaria para hacer la creación
        de una entidad."""

        driver = Driver.create()

        assert isinstance(driver, Driver), "Valide que la instancia sea del tipo esperado."
        assert len(driver.id.value) == 32, "Valide que el ID sea un UUID."
        assert driver.last_delivery.last_delivery == None, "Valide que un conductor nuevo no tenga fecha de última entrega."

    def test_mark_as_occupied(self) -> None:
        """Método que contiene la prueba unitaria para hacer transición de
        estado a 'OCCUPIED'."""

        driver = Driver.create()
        driver.mark_as_occupied()

        assert driver.status == DriverStatus.OCCUPIED, "Valida que la transición sea la correcta."

    def test_mark_as_occupied_error(self) -> None:
        """Método que contiene la prueba unitaria que valida problemas al 
        hacer transición de estado a 'OCCUPIED'."""

        driver = Driver.create()
        driver.mark_as_occupied()

        with pytest.raises(DriverCurrenlyOccupiedError):
            driver.mark_as_occupied()

    def test_mark_as_available(self) -> None:
        """Método que contiene la prueba unitaria para hacer transición de
        estado a 'AVAILABLE'."""

        driver = Driver.create()

        driver.mark_as_occupied()
        assert driver.status == DriverStatus.OCCUPIED, "Valida la correcta transición."

        driver.mark_as_available()
        assert driver.status == DriverStatus.AVAILABLE, "Valida la correcta transición."

    def test_mark_as_available_error(self) -> None:
        """Método que contiene la prueba unitaria que valida problemas al 
        hacer transición de estado a 'AVAILABLE'."""

        driver = Driver.create()

        with pytest.raises(DriverAlreadyAvailableError):
            driver.mark_as_available()
