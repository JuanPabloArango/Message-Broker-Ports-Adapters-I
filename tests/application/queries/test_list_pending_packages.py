"""Módulo que contiene una pequeña prueba unitaria para validar el
correcto comportamiento de la dataclass."""

# Librerías Exteras.
import pytest

# Librerías Internas.
from app.application.queries.base import Query
from app.application.queries.list_pending_packages import ListPendingPackagesQuery
from app.application.ports.persistence.criteria import Criteria, Filter, Pagination, Operator


class TestListPendingPackagesQuery:
    """Clase que encapsula las pruebas unitarias de la query."""

    def test_init(self) -> None:
        """Método que contiene la prueba unitaria que valida que todo se instancia
        correctamente."""

        query = ListPendingPackagesQuery()

        assert isinstance(query, Query), "Valide que la super clase sea la correcta."

        assert query.criteria.filters[0].value == "PENDING", "Valide que su query de negocio sí esté bien configurada."
        assert query.criteria.filters[0].field == "status", "Valide que su query de negocio sí esté bien configurada."
