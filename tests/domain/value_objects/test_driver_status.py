"""Módulo que contiene pruebas unitarias sobre los posibles estados de un Driver."""

# Librerías Externas.
import pytest

# Librerías Internas.
from app.domain.value_objects.driver_status import DriverStatus


class TestDriverStatus:
    """Clase que encpasula las pruebas unitarias del VO DriverStatus."""

    def test_valid_status(self) -> None:
        """Método que contiene la prueba unitaria para validar los estados
        válidos."""

        occupied = DriverStatus.OCCUPIED
        available = DriverStatus.AVAILABLE

        assert isinstance(occupied.value, str), "Los estados siempre se renderizan como str."
        assert isinstance(available.value, str), "Los estados siempre se renderizan como str."

        assert repr(occupied) == "OCCUPIED", "Valida que la representación sea correcta."
        assert repr(available) == "AVAILABLE", "Valida que la representación sea correcta."

    def test_invalid_status(self) -> None:
        """Método que contiene la prueba unitaria para validar que los estados
        son finitios y delimitados."""

        with pytest.raises(ValueError):
            DriverStatus(value = "UNAVAILABLE")
        
        with pytest.raises(ValueError):
            DriverStatus(value = "BUSY")
