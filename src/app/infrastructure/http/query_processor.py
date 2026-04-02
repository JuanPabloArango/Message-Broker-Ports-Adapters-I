"""Módulo encargado de realizar el procesamiento de los query parameters."""

# Librerías Externas.
from typing import Dict, List

import re

# Librerías Internas.
from app.application.ports.persistence.criteria import Criteria, Filter, Pagination, Operator


class QueryParamsProcessor:
    """Clase cuya responsabilidad es mapear de query params
    al patrón Criteria."""

    _PATTERN = re.compile(pattern = r"^filter\[(\w+)\]\[(\w+)\]$")

    @classmethod
    def process_params(cls, query_params: Dict[str, str]) -> Criteria:
        """Método de clase que creará specs de búsqueda según
        los parámetros compartidos por el usuario.

        Args:
        ----------
        query_params: Dict[str, str].
            Query parameters sobre el endpoint.
        
        Returns:
        ----------
        Criteria.
            Specs de búsqueda."""
                
        filters: List[Filter] = []
        for query_key, query_value in query_params.items():

            match = re.match(cls._PATTERN, query_key)
            if not match:
                continue

            field, operator = match.group(1), match.group(2)
            try:
                operator = Operator(operator)
            except ValueError:
                continue

            if operator == Operator.IN:
                query_value = query_value.split(",")

            filters.append(Filter(field = field, value = query_value, operator = operator))
        
        pagination = Pagination(limit = query_params.get("limit"),
                                offset = query_params.get("offset"),
                                order_by = query_params.get("order_by"),
                                order_dir = query_params.get("order_dir"))
        
        criteria = Criteria(filters = filters, pagination = pagination)
        return criteria
