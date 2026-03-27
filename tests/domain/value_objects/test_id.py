"""Módulo que contiene las pruebas unitarias para el módulo de generación de IDs."""

# Librerías Externas.
import pytest

# Librerías Internas.
from app.domain.value_objects.id import ID


class TestIDValueObject:
    """Clase que encapsula las pruebas unitarias para el objeto de valor ID."""

    def test_id_setup(self) -> None:
        """Método que contiene la prueba unitaria enfocada en validar que si
        se pasa un valor al VO, ese valor se da por exacto."""

        id = ID(value = "123")

        assert isinstance(id.value, str), "Los IDs de dominio solo pueden ser str."
        assert id.value == "123", "Los IDs, cuando son pasados a la dataclass, deben ser exactos."
        assert repr(id) == "123", "La representación de la dataclass es automática y debe cumplir."

    def test_default_id_setup(self) -> None:
        """Método que contiene la prueba unitaria que valida que se genere,
        autómaticamente, UUID4 para que nuestras entidades nazcan con identidad."""

        id = ID()

        assert isinstance(id.value, str), "Los IDs de dominio solo pueden ser str."
        assert len(id.value) == 32, "Cuando el valor no se pasa, se genera un UUID4 de 32 caracteres."
        assert repr(id) == f"{id.value}", "La representación de la dataclass es automática y debe cumplir."

    def test_id_setup_errors(self) -> None:
        """Método que contiene la prueba unitaria que valida que solo se pueden
        crear IDs con string en caso de que no se desee generar un UUID."""

        with pytest.raises(ValueError):
            ID(value = 123)

        with pytest.raises(ValueError):
            ID(value = (1, ))

    def test_comparisson(self) -> None:
        """Método que contiene la prueba unitaria para validar comparación
        de IDs."""

        id1 = ID(value = "123")
        id2 = ID(value = "123")
        id3 = ID(value = None)
        id4 = "123"

        assert id1 == id2, "Debe validar que si el valor de ID es igual, su objeto es igual."
        assert id1 != id3, "Debe validar que si el valor de ID es diferente, su objeto es diferente."
        assert id2 != id4, "Debe validar que si el valor de ID es igua, pero su instancia es diferente, no debe haber validación."
