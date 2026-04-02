"""Módulo que contiene pruebas unitarias para la definición de las vistas
donde se trabaja con entidades Sender."""

# Librerías Externas.
from flask import Flask


class TestSenderView:
    """Clase que contiene pruebas unitarias sobre los endpoints
    correspondientes a la ruta "/sender"."""

    def test_create_sender_201(self, test_client: Flask) -> None:
        """Método que contiene la prueba unitaria donde el cliente
        envía al servidor una petición de creación de entidad de dominio.
        
        Args:
        ----------
        test_client: Flask.
            Servidor de pruebas."""

        response = test_client.post("/sender", json = {})

        assert response.status_code == 201, "Valide que el código de estado sea el adecuado."
        assert response.json["results"].startswith("Se ha creado un nuevo Sender"), "Valide que se haya aplicado la creación."

    def test_get_senders_200(self, test_client: Flask) -> None:
        """Método que contiene la prueba unitaria donde el cliente
        envía al servidor una petición de listar entidades de dominio.
        
        Args:
        ----------
        test_client: Flask.
            Servidor de pruebas."""

        response = test_client.get("/sender")

        assert response.status_code == 200, "Valide que el código de estado sea el adecuado."
        assert len(response.json) == 5, "Valide que haya obtenido la cantidad de entidades esperadas."

    def test_get_senders_400(self, test_client: Flask) -> None:
        """Método que contiene la prueba unitaria donde el cliente
        envía al servidor una petición de listar entidades de dominio
        con un error debido a un posible typo en atributos de entidad.
        
        Args:
        ----------
        test_client: Flask.
            Servidor de pruebas."""

        response = test_client.get("/sender", query_string = {"filter[random_field][eq]": "23"})

        assert response.status_code == 400, "Valide que haya obtenido el código esperado."
        assert response.json["error"] == "El atributo random_field no es un campo de filtrado válido.", "Valide que el mensaje de error al cliente sea el esperado."


class TestSenderDetailView:
    """Clase que contiene pruebas unitarias sobre los endpoints
    correspondientes a la ruta "/sender/<string:sender_id>"."""

    def test_get_sender_200(self, test_client: Flask) -> None:
        """Método que contiene la prueba unitaria donde el cliente
        envía al servidor una petición de obtener una entidad de dominio
        específica.
        
        Args:
        ----------
        test_client: Flask.
            Servidor de pruebas."""

        response = test_client.get("/sender/2")

        assert response.status_code == 200, "Valide que el código de estado sea el adecuado."

        assert response.json["id"] == "2", "Valide que haya obtenido la información esperada."
        assert response.json["status"] == "VERIFIED", "Valide que haya obtenido la información esperada."

        assert isinstance(response.json["created_at"], str), "Valide que campos de dominio hayan tenido la transformación adecuada."

    def test_get_senders_404(self, test_client: Flask) -> None:
        """Método que contiene la prueba unitaria donde el cliente
        envía al servidor una petición de obtener una entidad de dominio
        específica no existente.
        
        Args:
        ----------
        test_client: Flask.
            Servidor de pruebas."""

        response = test_client.get("/sender/45")

        assert response.status_code == 404, "Valide que haya obtenido el código esperado."
        assert response.json["error"] == "El Sender con ID 45 no existe.", "Valide que el mensaje de error al cliente sea el esperado."


class TestSenderVerificationView:
    """Clase que contiene pruebas unitarias sobre los endpoints
    correspondientes a la ruta "/sender/<sender_id>/verify"."""

    def test_verify_sender_204(self, test_client: Flask) -> None:
        """Método que contiene la prueba unitaria donde el cliente
        envía al servidor una petición de verificación de una
        entidad de dominio.
        
        Args:
        ----------
        test_client: Flask.
            Servidor de pruebas."""

        response = test_client.post("/sender/3/verify")

        assert response.status_code == 204, "Valide que el código de estado sea el adecuado."

    def test_verify_sender_409(self, test_client: Flask) -> None:
        """Método que contiene la prueba unitaria donde el cliente
        envía al servidor una petición de verificación de una
        entidad de dominio que falla debido a invariantes internas.
        
        Args:
        ----------
        test_client: Flask.
            Servidor de pruebas."""

        response = test_client.post("/sender/2/verify")

        assert response.status_code == 409, "Valide que el código de estado sea el adecuado."
