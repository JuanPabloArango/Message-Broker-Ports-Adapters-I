"""Módulo que contiene una pequeña prueba unitaria para validar el
correcto comportamiento de la dataclass."""

# Librerías Exteras.
import pytest

# Librerías Internas.
from app.application.queries.get_package_by_id import GetPackageQuery


class TestGetPackageQuery:
    """Clase que encapsula las pruebas unitarias de la query."""

    def test_init(self) -> None:
        """Método que contiene la prueba unitaria que valida que todo se instancia
        correctamente."""

        query = GetPackageQuery(package_id = "42")

        assert query.package_id == "42", "Valide que se mapeen correctamente los valores."

    def test_raise_init_error(self) -> None:
        """Método que contiene la prueba unitaria que valida que si no se instancia
        bien la Query, se arroja un error."""

        with pytest.raises(ValueError):
            GetPackageQuery(package_id = 42)
