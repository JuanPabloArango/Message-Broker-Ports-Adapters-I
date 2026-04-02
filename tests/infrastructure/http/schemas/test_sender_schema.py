"""Módulo que contiene pruebas unitarias para la validación
de DTOs externos que ingresan a nuestra app."""

# Librerías Externas.
import pytest

import datetime as dt

from marshmallow.exceptions import ValidationError

# Librerías Internas.
from app.infrastructure.http.schemas.sender import CreateSenderRequestSchema, SenderResponseSchema


class TestCreateSenderRequestSchema:
    """Clase que encapsula las pruebas unitarias para la
    validación de DTOs externos."""

    def test_empty_data(self) -> None:
        """Método que contiene la prueba unitaria encargada
        de validar que si un request llega vacío, la app lo entiende."""

        data = {}
        result = CreateSenderRequestSchema().load(data)

        assert result == {"sender_id": None}, "Valide que si el request body está vacío, no falle."
        
    def test_not_empty_data(self) -> None:
        """Método que contiene la prueba unitaria para validar un
        request no vacio."""

        data = {"sender_id": "321",
                "some_random_field": 123}

        result = CreateSenderRequestSchema().load(data)

        assert result == {"sender_id": "321"}, "Valide que se pasen las validaciones."
        
    def test_not_empty_data_fail(self) -> None:
        """Método contiene la prueba unitaria que valida que si
        no se cumplen requisitos de esquema, se levanta un fallo."""

        data = {"sender_id": 321}

        with pytest.raises(ValidationError):
            CreateSenderRequestSchema().load(data)


class TestSenderResponseSchema:
    """Clase que encapsula las pruebas unitarias para validar
    respuestas de nuestra app."""

    def test_succesful_single_response(self) -> None:
        """Método que contiene la prueba unitaria para validar
        que podamos enviar una entidad como respuesta a nuestro cliente."""

        data = {"id": "123",
                "status": "VERIFIED",
                "created_at": dt.datetime(1996, 3, 4, 13, 0, 0),
                "updated_at": dt.datetime(2025, 10, 1, 12, 0, 0)}

        result = SenderResponseSchema(many = False).load(data)

        assert result == {"id": "123",
                          "status": "VERIFIED",
                          "created_at": dt.datetime(1996, 3, 4, 13, 0, 0),
                          "updated_at": dt.datetime(2025, 10, 1, 12, 0, 0)}, "Valide que se haya transformado la data en una entidad JSON."

    def test_succesful_many_responses(self) -> None:
        """Método que contiene la prueba unitaria para validar
        que podamos enviar múltiples entidades como respuesta a nuestro cliente."""

        data = [{"id": "123",
                 "status": "VERIFIED",
                 "created_at": dt.datetime(1996, 3, 4, 13, 0, 0),
                 "updated_at": dt.datetime(2025, 10, 1, 12, 0, 0)},
                {"id": "124",
                 "status": "UNVERIFIED",
                 "created_at": dt.datetime(1996, 3, 4, 13, 0, 0),
                 "updated_at": dt.datetime(2025, 10, 1, 12, 0, 0)},]

        result = SenderResponseSchema(many = True).load(data)

        assert result == [{"id": "123",
                           "status": "VERIFIED",
                           "created_at": dt.datetime(1996, 3, 4, 13, 0, 0),
                           "updated_at": dt.datetime(2025, 10, 1, 12, 0, 0)},
                          {"id": "124",
                           "status": "UNVERIFIED",
                           "created_at": dt.datetime(1996, 3, 4, 13, 0, 0),
                           "updated_at": dt.datetime(2025, 10, 1, 12, 0, 0)},], "Valide que se haya transformado la data en una entidad JSON."

    def test_failed_validation(self) -> None:
        """Método que contiene la prueba unitaria para validar
        que si no se cumple el esquema, se levanta un fallo."""

        data = {"id": "123",
                "status": "VERIFIED"}

        with pytest.raises(ValidationError):
            SenderResponseSchema(many = False).load(data)
