"""Módulo que contiene pruebas unitarias sobre los posibles estados de un Sender."""

# Librerías Externas.
import pytest

# Librerías Internas.
from app.domain.value_objects.sender_status import SenderStatus


class TestSenderStatus:
    """Clase que encpasula las pruebas unitarias del VO SenderStatus."""

    def test_valid_status(self) -> None:
        """Método que contiene la prueba unitaria para validar los estados
        válidos."""

        verified = SenderStatus.VERIFIED
        unverified = SenderStatus.UNVERIFIED

        assert isinstance(verified.value, str), "Los estados siempre se renderizan como str."
        assert isinstance(unverified.value, str), "Los estados siempre se renderizan como str."

        assert repr(verified) == "VERIFIED", "Valida que la representación sea correcta."
        assert repr(unverified) == "UNVERIFIED", "Valida que la representación sea correcta."

    def test_invalid_status(self) -> None:
        """Método que contiene la prueba unitaria para validar que los estados
        son finitios y delimitados."""

        with pytest.raises(ValueError):
            SenderStatus(value = "DELETED")
        
        with pytest.raises(ValueError):
            SenderStatus(value = "OUT-OF-BUSINESS")
