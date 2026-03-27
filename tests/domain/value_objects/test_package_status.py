"""Módulo que contiene pruebas unitarias sobre los posibles estados de un Package."""

# Librerías Externas.
import pytest

# Librerías Internas.
from app.domain.value_objects.package_status import PackageStatus


class TestPackageStatus:
    """Clase que encpasula las pruebas unitarias del VO PackageStatus."""

    def test_valid_status(self) -> None:
        """Método que contiene la prueba unitaria para validar los estados
        válidos."""

        pending = PackageStatus.PENDING
        assigned = PackageStatus.ASSIGNED
        delivered = PackageStatus.DELIVERED

        assert isinstance(pending.value, str), "Los estados siempre se renderizan como str."
        assert isinstance(assigned.value, str), "Los estados siempre se renderizan como str."
        assert isinstance(delivered.value, str), "Los estados siempre se renderizan como str."

        assert repr(pending) == "PENDING", "Valida que la representación sea correcta."
        assert repr(assigned) == "ASSIGNED", "Valida que la representación sea correcta."
        assert repr(delivered) == "DELIVERED","Valida que la representación sea correcta."

    def test_invalid_status(self) -> None:
        """Método que contiene la prueba unitaria para validar que los estados
        son finitios y delimitados."""

        with pytest.raises(ValueError):
            PackageStatus(value = "DUMPED")
        
        with pytest.raises(ValueError):
            PackageStatus(value = "DAMAGED")
