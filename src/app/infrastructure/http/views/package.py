"""Módulo que contiene las vistas enfocadas en la entidad Package."""

# Librerías Externas.
from typing import Any, Dict, List, Tuple

from flask.views import MethodView
from flask_smorest import Blueprint

# Librerías Internas.
from app.application.dtos.package import PackageDTO
from app.application.ports.persistence.criteria import Criteria

from app.application.queries.list_packages import ListPackagesQuery
from app.application.queries.get_package_by_id import GetPackageQuery
from app.application.commands.assign_driver import AssignDriverCommand
from app.application.commands.create_package import CreatePackageCommand
from app.application.commands.deliver_package import DeliverPackageCommand

from app.application.query_handlers.get_package import GetPackageHandler
from app.application.query_handlers.list_packages import ListPackagesHandler
from app.application.command_handlers.assign_driver import AssignDriverHandler
from app.application.command_handlers.create_package import CreatePackageHandler
from app.application.command_handlers.deliver_package import DeliverPackageHandler

from app.infrastructure.http.schemas.query import QuerySchema
from app.infrastructure.http.schemas.package import PackageCreationRequestSchema, PackageResponseSchema


blp = Blueprint(name = "package", import_name = __name__,
                url_prefix = "/package", description = "Blueprint que contiene las vistas relacionadas a la entidad Package.")


class PackagerView(MethodView):
    """Clase que encapsula los métodos REST sujetos a la ruta
    '/package'."""

    def __init__(self, list_handler: ListPackagesHandler, create_handler: CreatePackageHandler) -> None:
        """Método de instanciación de objetos de la clase.
        
        Args:
        ----------
        list_handler: ListPackagesHandler.
            Handler para consultar/filtrar entidades.
        
        create_handler: CreatePackageHandler.
            Handler para crear una entidad de dominio."""

        self._list_handler = list_handler
        self._create_handler = create_handler

    @blp.arguments(QuerySchema, location = "query")
    @blp.response(200, PackageResponseSchema(many = True), description = "Resultados que contienen los DTOs con la información de las entidades.")
    def get(self, query_data: Criteria) -> Tuple[List[PackageDTO], int]:
        """Método RESTful GET para listar entidades de dominio
        de acuerdo a criterios de búsqueda.

        Args:
        ----------
        query_data: Criteria.
            Filtros de búsqueda del request parseados a lenguaje de dominio.
        
        Returns:
        ----------
        List[PackageDTO].
            Lista de entidades de dominio que cumplen criterios.
        
        int.
            Código de estado de la petición."""
        
        query = ListPackagesQuery(criteria = query_data)

        results = self._list_handler.handle(query = query)
        return results, 200

    @blp.arguments(PackageCreationRequestSchema, location = "json")
    def post(self, data: Dict[str, Any]) -> Tuple[Dict[str, str], int]:
        """Método RESTful POST para crear entidades de dominio
        Package.

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
        
        command = CreatePackageCommand(sender_id = data["sender_id"],
                                       package_id = data.get("package_id"))
        
        new_package_id = self._create_handler.handle(command = command)
        return {"results": f"Se ha creado un nuevo Package con ID {new_package_id}"}, 201


class PackageDetailView(MethodView):
    """Clase que encapsula los métodos REST sujetos a la ruta
    '/package/<string:package_id>'."""

    def __init__(self, get_handler: GetPackageHandler) -> None:
        """Método de instanciación de objetos de la clase.
        
        Args:
        ----------
        get_handler: GetPackageHandler.
            Handler para obtener una entidad puntual."""

        self._get_handler = get_handler

    @blp.response(200, PackageResponseSchema, description = "Resultados que contienen el DTO con la información de la entidad.")
    def get(self, package_id: str) -> Tuple[PackageDTO, int]:
        """Método RESTful GET para consultar una entidad de dominio
        particular.
        
        Args:
        ----------
        package_id: str.
            Identidad de la entidad.
        
        Returns:
        ----------
        PackageDTO.
            Entidad hallada.
        
        int.
            Código de estado de la petición."""
        
        query = GetPackageQuery(package_id = package_id)

        package = self._get_handler.handle(query = query)
        return package, 200


class DeliverPackageView(MethodView):
    """Clase que encapsula los métodos REST sujetos a la ruta
    '/package/<string:package_id>'/deliver."""

    def __init__(self, deliver_handler: DeliverPackageHandler) -> None:
        """Método de instanciación de objetos de la clase.
        
        Args:
        ----------
        deliver_handler: FreeDriverHandler.
            Handler encargado de cambiar el estado de un Package."""

        self._deliver_handler = deliver_handler

    def post(self, package_id: str) -> Tuple[str, int]:
        """Método RESTful POST para marcar un paquete como entregado.
        
        Args:
        ----------
        package_id: str.
            ID del package a marcar.
        
        Returns:
        ----------
        str.
            String vació.
        
        int.
            Código de estado del response."""

        command = DeliverPackageCommand(package_id = package_id)

        self._deliver_handler.handle(command = command)
        return "", 204


class AssignDriverView(MethodView):
    """Clase que encapsula los métodos REST sujetos a la ruta
    '/package/<string:package_id>'/assign."""

    def __init__(self, assign_handler: AssignDriverHandler) -> None:
        """Método de instanciación de objetos de la clase.
        
        Args:
        ----------
        assign_handler: AssignDriverHandler.
            Handler encargado de responsabilizar a un Driver de un Package."""

        self._assign_handler = assign_handler

    def post(self, package_id: str) -> Tuple[Dict[str, str], int]:
        """Método RESTful POST para marcar un paquete como asignado.
        
        Args:
        ----------
        package_id: str.
            ID del package a marcar.
        
        Returns:
        ----------
        Dict[str, str].
            Response de la petición.
        
        int.
            Código de estado del response."""

        command = AssignDriverCommand(package_id = package_id)

        assigned_driver_id = self._assign_handler.handle(command = command)
        return {"results": f"El Package {package_id} ha sido asignado al Driver {assigned_driver_id}"}, 201
