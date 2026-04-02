"""Módulo que contiene todas las vistas relacionadas con la entidad Sender."""

# Librerías Externas.
from typing import Dict, List, Tuple

from flask.views import MethodView
from flask_smorest import Blueprint

# Librerías Internas.
from app.application.ports.persistence.criteria import Criteria

from app.application.dtos.sender import SenderDTO

from app.application.queries.list_senders import ListSendersQuery
from app.application.queries.get_sender_by_id import GetSenderQuery
from app.application.commands.create_sender import CreateSenderCommand
from app.application.commands.verify_sender import VerifySenderCommand

from app.application.query_handlers.get_sender import GetSenderHandler
from app.application.query_handlers.list_senders import ListSendersHandler
from app.application.command_handlers.create_sender import CreateSenderHandler
from app.application.command_handlers.verify_sender import VerifySenderHandler

from app.infrastructure.http.schemas.query import QuerySchema
from app.infrastructure.http.schemas.sender import CreateSenderRequestSchema, SenderResponseSchema


blp = Blueprint(name = "sender", import_name = __name__,
                url_prefix = "/sender", description = "Blueprint que contiene las vistas relacionadas a la entidad Sender.")


class SenderView(MethodView):
    """Clase que encapsula los métodos REST sujetos a la ruta
    '/sender'."""

    def __init__(self, list_handler: ListSendersHandler, create_handler: CreateSenderHandler) -> None:
        """Método de instanciación de objetos de la clase.
        
        Args:
        ----------
        list_handler: ListSendersHandler.
            Handler usado para listar N entidades.
       
        create_handler: CreateSenderHandler.
            Handler usado para crear una entidad."""
        
        self._list_handler = list_handler
        self._create_handler = create_handler

    @blp.arguments(QuerySchema, location = "query", description = "Query parameters construidos por el usuario en el request.")
    @blp.response(200, SenderResponseSchema(many = True), description = "Resultados que contienen los DTOs con la información de las entidades.")
    def get(self, query_data: Criteria) -> Tuple[List[SenderDTO], int]:
        """Método RESTful GET para listar las entidades Sender
        de acuerdo a criterios de búsqueda.
        
        Args:
        ----------
        query_data: Criteria.
            Criterios de búsqueda definidos por el usuario y limpiados
            por marshmallow.
        
        Returns:
        ----------
        List[SenderDTO].
            Data-transfer objects que contienen la información
            que disponibilizamos desde dominio.
        
        int.
            Código de estado."""

        query = ListSendersQuery(criteria = query_data)

        senders = self._list_handler.handle(query = query)
        return senders, 200

    @blp.arguments(CreateSenderRequestSchema, location = "json", description = "Body del Request para creación de Senders.")
    def post(self, data: Dict[str, str]) -> Tuple[Dict[str, str], int]:
        """Método RESTful POST para crear una entidad Sender.
        
        Args:
        ----------
        data: Dict[str, str].
            Data proveniente del request ya limpiada por marshmallow.
        
        Returns:
        ----------
        Dict[str, str].
            Body de la respuesta al cliente.
        
        int.
            Código de estado."""

        command = CreateSenderCommand(sender_id = data.get("sender_id"))

        new_sender_id = self._create_handler.handle(command = command)
        return {"results": f"Se ha creado un nuevo Sender con ID {new_sender_id}"}, 201


class SenderDetailView(MethodView):
    """Clase que encapsula los métodos REST sujetos a la ruta 
    '/sender/<string:sender_id>."""

    def __init__(self, get_handler: GetSenderHandler) -> None:
        """Método de instanciación de objetos de la clase.
        
        Args:
        ----------
        list_handler: GetSenderHandler.
            Handler usado para obtener una entidad específica."""
        
        self._get_handler = get_handler

    @blp.response(200, SenderResponseSchema, description = "Resultados que contienen el DTO con la información de la entidad.")
    def get(self, sender_id: str) -> Tuple[SenderDTO, int]:
        """Método RESTful GET para obtener una entidad específica.
        
        Args:
        ----------
        sender_id: str.
            ID de la entidad que desea consultar.
        
        Returns:
        ----------
        SenderDTO.
            Data-transfer object que contiene la información de la entidad.
        
        int.
            Código de estado."""
        
        query = GetSenderQuery(sender_id = sender_id)

        sender = self._get_handler.handle(query = query)
        return sender, 200


class SenderVerificationView(MethodView):
    """Clase que encapsula los métodos REST sujetos a la ruta
    '/sender/<string:sender_id>/verify'."""

    def __init__(self, verification_handler: VerifySenderHandler) -> None:
        """Método de instanciación de objetos de la clase.
        
        Args:
        ----------
        verification_handler: VerifySenderHandler.
            Handler de verificación de senders."""

        self._verification_handler = verification_handler

    def post(self, sender_id: str) -> int:
        """Método RESTful POST encargado de verificar a un Sender.
        
        Args:
        ----------
        sender_id: str.
            ID del Sender a verificar.
        
        Returns:
        ----------
        int.
            Código de estado."""
        
        command = VerifySenderCommand(sender_id = sender_id)
        
        self._verification_handler.handle(command = command)
        return "", 204
