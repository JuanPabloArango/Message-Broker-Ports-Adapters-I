"""Módulo que contiene una pequeña prueba unitaria para validar el
correcto comportamiento de la dataclass."""

# Librerías Exteras.
import pytest

# Librerías Internas.
from app.application.queries.list_drivers import ListDriversQuery
from app.application.ports.persistence.criteria import Criteria, Filter, Pagination, Operator


class TestListSendersQuery:
    """Clase que encapsula las pruebas unitarias de la query."""

    def test_init(self) -> None:
        """Método que contiene la prueba unitaria que valida que todo se instancia
        correctamente."""

        criteria = Criteria(
            filters = [
                Filter(field = "field_1", value = 34, operator = Operator.GTE),
                Filter(field = "field_2", value = ["A", "B", "C"], operator = Operator.IN)
            ],
            pagination = Pagination(limit = 15)
        )

        query = ListDriversQuery(criteria = criteria)

        assert len(query.criteria.filters) == 2, "Valide que sus filtros se conserven bien."
        assert criteria.pagination, "Valide que pueda tener paginación en sus queries."

        assert criteria.pagination.limit == 15, "Valide que se conserve la parametría en búsquedas."
        assert criteria.filters[0].field == "field_1", "Valide que se conserve la parametría en búsquedas."
        assert criteria.filters[1].operator == Operator.IN, "Valide que se conserve la parametría en búsquedas."

    def test_raise_init_error(self) -> None:
        """Método que contiene la prueba unitaria que valida que si no se instancia
        bien la Query, se arroja un error."""

        with pytest.raises(ValueError):
            ListDriversQuery(criteria = [
                ("field_1", 34, Operator.GTE),
                ("field_2", ["A", "B", "C"], Operator.IN)
            ])
