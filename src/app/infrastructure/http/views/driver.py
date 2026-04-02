"""Módulo que contiene las vistas enfocadas en la entidad Driver."""

# Librerías Externas.
from typing import Any, Dict, List, Tuple

from flask.views import MethodView
from flask_smorest import Blueprint

# Librerías Internas.
from app.application.dtos.driver import DriverDTO
from app.application.ports.persistence.criteria import Criteria

from app.application.queries.list_drivers import ListDriversQuery
from app.application.queries.get_driver_by_id import GetDriverQuery
from app.application.commands.free_driver import FreeDriverCommand
from app.application.commands.create_driver import CreateDriverCommand

from app.application.query_handlers.get_driver import GetDriverHandler
from app.application.query_handlers.list_drivers import ListDriversHandler
from app.application.command_handlers.free_driver import FreeDriverHandler
from app.application.command_handlers.create_driver import CreateDriverHandler

from app.infrastructure.http.schemas.query import QuerySchema
from app.infrastructure.http.schemas.driver import CreateDriverRequestSchema, DriverResponseSchema


blp = Blueprint(name = "driver", import_name = __name__,
                url_prefix = "/driver", description = "Blueprint que contiene las vistas relacionadas a la entidad Driver.")


class DriverView(MethodView):
    """Clase que encapsula los métodos REST sujetos a la ruta
    '/driver'."""

    def __init__(self, list_handler: ListDriversHandler, create_handler: CreateDriverHandler) -> None:
        """Método de instanciación de objetos de la clase.
        
        Args:
        ----------
        list_handler: ListDriversHandler.
            Handler para consultar/filtrar entidades.
        
        create_handler: CreateDriverHandler.
            Handler para crear una entidad de dominio."""

        self._list_handler = list_handler
        self._create_handler = create_handler

    @blp.arguments(QuerySchema, location = "query")
    @blp.response(200, DriverResponseSchema(many = True), description = "Resultados que contienen los DTOs con la información de las entidades.")
    def get(self, query_data: Criteria) -> Tuple[List[DriverDTO], int]:
        """Método RESTful GET para listar entidades de dominio
        de acuerdo a criterios de búsqueda.

        Args:
        ----------
        criteria: Criteria.
            Filtros de búsqueda del request parseados a lenguaje de dominio.
        
        Returns:
        ----------
        List[DriverDTO].
            Lista de entidades de dominio que cumplen criterios.
        
        int.
            Código de estado de la petición."""
                
        query = ListDriversQuery(criteria = query_data)

        results = self._list_handler.handle(query = query)
        return results, 200

    @blp.arguments(CreateDriverRequestSchema, location = "json")
    def post(self, data: Dict[str, Any]) -> Tuple[Dict[str, str], int]:
        """Método RESTful POST para crear entidades de dominio
        Driver.

        Args:
        ----------
        data: Dict[str, Any].
            Data proveniente del request ya limpiada por marshmallow.
        
        Returns:
        ----------
        Dict[str, str].
            Resultado de la operación.
        
        int.
            Código de estado de la petición."""
        
        command = CreateDriverCommand(driver_id = data.get("id"),
                                      last_delivery = data.get("last_delivery"))
        
        new_driver_id = self._create_handler.handle(command = command)
        return {"results": f"Se ha creado un nuevo Driver con ID {new_driver_id}"}, 201


class DriverDetailView(MethodView):
    """Clase que encapsula los métodos REST sujetos a la ruta
    '/driver/<string:driver_id>'."""

    def __init__(self, get_handler: GetDriverHandler) -> None:
        """Método de instanciación de objetos de la clase.
        
        Args:
        ----------
        get_handler: GetDriverHandler.
            Handler para obtener una entidad puntual."""

        self._get_handler = get_handler

    @blp.response(200, DriverResponseSchema, description = "Resultados que contienen el DTO con la información de la entidad.")
    def get(self, driver_id: str) -> Tuple[DriverDTO, int]:
        """Método RESTful GET para consultar una entidad de dominio
        particular.
        
        Args:
        ----------
        driver_id: str.
            Identidad de la entidad.
        
        Returns:
        ----------
        DriverDTO.
            Entidad hallada.
        
        int.
            Código de estado de la petición."""
        
        query = GetDriverQuery(driver_id = driver_id)

        driver = self._get_handler.handle(query = query)
        return driver, 200


class FreeDriverView(MethodView):
    """Clase que encapsula los métodos REST sujetos a la ruta
    '/driver/<string:driver_id>'/free."""

    def __init__(self, free_handler: FreeDriverHandler) -> None:
        """Método de instanciación de objetos de la clase.
        
        Args:
        ----------
        free_handler: FreeDriverHandler.
            Handler encargado de cambiar el estado de un Driver."""

        self._free_handler = free_handler

    def post(self, driver_id: str) -> Tuple[str, int]:
        """Método RESTful POST para liberar a un Driver que acaba
        de entregar un paquete.
        
        Args:
        ----------
        data: Dict[str, str].
            Datos del request ya organizados por marshmallow.
        
        Returns:
        ----------
        str.
            String vació.
        
        int.
            Código de estado del response."""

        command = FreeDriverCommand(driver_id = driver_id)

        self._free_handler.handle(command = command)
        return "", 204
