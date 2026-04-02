"""Módulo que contiene pruebas unitarias para la validación
de DTOs externos que ingresan a nuestra app."""

# Librerías Internas.
from app.application.ports.persistence.criteria import Criteria, Pagination, Filter, Operator

from app.infrastructure.http.schemas.query import QuerySchema


class TestQuerySchema:
    """Clase que encapsula las pruebas unitarias para la
    validación de DTOs externos."""

    def test_basic_result(self) -> None:
        """Método que contiene la prueba unitaria que valida
        la obtención cruda de query params."""

        data = {}

        result = QuerySchema().load(data)

        assert result == Criteria(filters = [],
                                  pagination = Pagination(limit = 10, offset = 0,
                                                          order_by = "created_at",
                                                          order_dir = "desc")), "Valide que haya obtenido el criterio apropiado."
        
    def test_result_with_filters(self) -> None:
        """Método que contiene la prueba unitaria
        para casos más puntuales."""

        data = {"filter[status][in]": "A,B,C",
                "filter[created_at][gte]": "2025-10-01",
                "limit": "5", "offset": "2", "order_dir": "asc"}
        
        result = QuerySchema().load(data)

        assert sorted(result.filters, key = lambda x: x.field) == [Filter(field = "created_at", value = "2025-10-01", operator = Operator.GTE),
                                                                   Filter(field = "status", value = ["A", "B", "C"], operator = Operator.IN)], "Valide que haya obtenido los filtros apropiados."
        
        assert result.pagination == Pagination(limit = 5, offset = 2,
                                               order_by = "created_at",
                                               order_dir = "asc"), "Valide que la paginación sea la correcta."
