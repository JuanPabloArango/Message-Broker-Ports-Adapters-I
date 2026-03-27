"""Módulo que contiene las pruebas del servicio de dominio que carga N
entidades Driver y selecciona aquel que menos ha trabajado recientemente."""

# Librerías Internas.
from app.domain.entities.driver import Driver

from app.domain.services.assign_driver import DriverAssignment


class TestDriverAssignment:
    """Clase que encapsula las pruebas unitarias para el servicio de dominio."""

    def test_execute_with_many_available_drivers(self) -> None:
        """Método que contiene la prueba unitaria que se encarga de,
        dado que hay N Drivers disponibles, se seleccione aquel que lleva
        mayor descanso."""

        driver1 = Driver(last_delivery = "2025-10-01 23:12:54")
        driver2 = Driver(last_delivery = "2023-10-01 10:54:00")
        driver3 = Driver(last_delivery = "2026-10-01 07:34:23")

        available_drivers = [driver1, driver2, driver3]

        driver = DriverAssignment.execute(available_drivers)

        assert driver == driver2

    def test_execute_with_one_available_driver(self) -> None:
        """Método que contiene la prueba unitaria que se encarga de,
        dado que hay 1 Driver disponible, se seleccione este."""

        driver1 = Driver(last_delivery = "2025-10-01 23:12:54")

        available_drivers = [driver1]

        driver = DriverAssignment.execute(available_drivers)

        assert driver == driver1

    def test_execute_with_no_available_drivers(self) -> None:
        """Método que contiene la prueba unitaria que se encarga de,
        dado que hay 0 Drivers disponibles, se retorne None y luego,
        alguna entidad, levante un evento frente a este hecho."""

        available_drivers = []

        driver = DriverAssignment.execute(available_drivers)

        assert driver == None
