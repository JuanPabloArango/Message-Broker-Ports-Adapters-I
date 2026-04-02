"""Módulo que contiene pruebas unitarias para nuestra utilidad de
procesamiento de query params."""

# Librerías Internas.
from app.application.ports.persistence.criteria import Criteria, Pagination, Operator, Filter

from app.infrastructure.http.query_processor import QueryParamsProcessor


class TestQueryParamsProcessor:
    """Clase que encapsula pruebas unitarias de la feature 'QueryParamsProcessor'."""

    def test_normal_operations(self) -> None:
        """Método que contiene pruebas unitarias para
        validar el comportamiento esperado."""

        data = {"filter[id][eq]": "123",
                "filter[updated_at][lte]": "2025-10-01"}

        created_criteria = QueryParamsProcessor.process_params(query_params = data)

        assert created_criteria == Criteria(
            filters = [
                Filter(field = "id", value = "123", operator = Operator.EQ),
                Filter(field = "updated_at", value = "2025-10-01", operator = Operator.LTE)
            ],
            pagination = Pagination(
                limit = None,
                offset = None,
                order_by = None,
                order_dir = None
            ))

    def test_operator_not_found(self) -> None:
        """Método que contiene pruebas unitarias para validar
        que un typo del usuario no lleve un error de dominio."""

        data = {"filter[id][random_operator]": "123",
                "filter[updated_at][lte]": "2025-10-01",
                "limit": 10, "offset": 5, "order_by": "id", "order_dir": "asc"}

        created_criteria = QueryParamsProcessor.process_params(query_params = data)

        assert created_criteria == Criteria(
            filters = [
                Filter(field = "updated_at", value = "2025-10-01", operator = Operator.LTE)
            ],
            pagination = Pagination(
                limit = 10,
                offset = 5,
                order_by = "id",
                order_dir = "asc"
            ))

    def test_not_matched_criteria(self) -> None:
        """Método que contiene pruebas unitarias para validar
        que un query param que no haga match con nuestros requisitos
        no mate el proceso."""

        data = {"id__equals": "123",
                "updated_at": "2025-10-01"}

        created_criteria = QueryParamsProcessor.process_params(query_params = data)

        assert created_criteria == Criteria(
            filters = [],
            pagination = Pagination(
                limit = None,
                offset = None,
                order_by = None,
                order_dir = None
            ))