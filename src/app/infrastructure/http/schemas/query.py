"""Módulo que contiene la definición de esquemas para queries."""

# Librerías Externas.
from typing import Any, Dict, Optional

from marshmallow import Schema, fields, post_load, INCLUDE

# Librerías Internas.
from app.application.ports.persistence.criteria import Criteria

from app.infrastructure.http.query_processor import QueryParamsProcessor


class QuerySchema(Schema):
    """Clase que define el esquema esperado para los query parameters."""

    limit = fields.Integer(required = False, load_default = 10)
    offset = fields.Integer(required = False, load_default = 0)
    order_by = fields.String(required = False, load_default = "created_at")
    order_dir = fields.String(required = False, load_default = "desc")

    def load(self, data: Dict[str, Any], *, many: Optional[bool] = None,
             partial: Optional[bool] = None, unknown: Optional[str] = None, **kwargs) -> Dict[str, Any]:
        """Método que se encarga de cargar 
        
        Args:
        ----------
        data: Dict[str, Any].
            Query params cargados como Dict.
        
        many: Optional[bool].
            Elemento que indica si debe validar múltiples instancias de query.
        
        partial: Optional[bool].
            Indica si la validación de esquema es parcial.
        
        unknown: Optional[str].
            Indice si aceptamos campos más allá de los declarados. En caso de query params, siempre True.
        
        Returns:
        ----------
        Dict[str, Any].
            Diccionario con los query params."""
        
        return super().load(data, many = many, partial = partial, unknown = INCLUDE, **kwargs)

    @post_load
    def prepare_criteria(self, query_data: Dict[str, Any], **kwargs) -> Criteria:
        """Método que permite, una vez cargador los query params
        del request, mapearlos a algo que entienda el dominio.
        
        Args:
        ----------
        query_data: Dict[str, Any].
            Query params del request.
        
        Returns:
        ----------
        Criteria.
            Objeto del patrón de diseño Specs para filtrar entidades de dominio."""
        
        return QueryParamsProcessor.process_params(query_data)
    