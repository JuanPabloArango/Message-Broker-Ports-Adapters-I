"""Módulo que contiene pruebas unitarias para la definición de las vistas
donde se trabaja con entidades Package."""

# Librerías Externas.
from flask import Flask

from app.domain.value_objects.id import ID


class TestPackageView:
    """Clase que contiene pruebas unitarias sobre los endpoints
    correspondientes a la ruta "/driver"."""

    def test_create_package_201(self, test_client: Flask) -> None:
        """Método que contiene la prueba unitaria donde el cliente
        envía al servidor una petición de creación de entidad de dominio.
        
        Args:
        ----------
        test_client: Flask.
            Servidor de pruebas."""

        response = test_client.post("/package", json = {"sender_id": "4"})

        assert response.status_code == 201, "Valide que el código de estado sea el adecuado."
        assert response.json["results"].startswith("Se ha creado un nuevo Package"), "Valide que se haya aplicado la creación."

    def test_create_package_400(self, test_client: Flask) -> None:
        """Método que contiene la prueba unitaria donde el cliente
        envía al servidor una petición de creación de entidad de dominio.
        
        Args:
        ----------
        test_client: Flask.
            Servidor de pruebas."""

        response = test_client.post("/package", json = {"sender_id": "1"})

        assert response.status_code == 422, "Valide que el código de estado sea el adecuado."
        assert response.json["error"] == "El sender existe pero su estado actual no le permite enviar paquetes.", "Valide que se haya aplicado la creación."

    def test_get_packages_200(self, test_client: Flask) -> None:
        """Método que contiene la prueba unitaria donde el cliente
        envía al servidor una petición de listar entidades de dominio.
        
        Args:
        ----------
        test_client: Flask.
            Servidor de pruebas."""

        response = test_client.get("/package", query_string = {})

        assert response.status_code == 200, "Valide que el código de estado sea el adecuado."
        assert len(response.json) == 5, "Valide que haya obtenido la cantidad de entidades esperadas."

    def test_get_packages_400(self, test_client: Flask) -> None:
        """Método que contiene la prueba unitaria donde el cliente
        envía al servidor una petición de listar entidades de dominio
        con un error debido a un posible typo en atributos de entidad.
        
        Args:
        ----------
        test_client: Flask.
            Servidor de pruebas."""

        response = test_client.get("/package", query_string = {"filter[random_field][eq]": "23"})

        assert response.status_code == 400, "Valide que haya obtenido el código esperado."
        assert response.json["error"] == "El atributo random_field no es un campo de filtrado válido.", "Valide que el mensaje de error al cliente sea el esperado."


class TestPackageDetailView:
    """Clase que contiene pruebas unitarias sobre los endpoints
    correspondientes a la ruta "/driver/<string:driver_id>"."""

    def test_get_package_200(self, test_client: Flask) -> None:
        """Método que contiene la prueba unitaria donde el cliente
        envía al servidor una petición de obtener una entidad de dominio
        específica.
        
        Args:
        ----------
        test_client: Flask.
            Servidor de pruebas."""

        response = test_client.get("/package/2")

        assert response.status_code == 200, "Valide que el código de estado sea el adecuado."

        assert response.json["id"] == "2", "Valide que haya obtenido la información esperada."
        assert response.json["status"] == "PENDING", "Valide que haya obtenido la información esperada."

        assert isinstance(response.json["created_at"], str), "Valide que campos de dominio hayan tenido la transformación adecuada."

    def test_get_package_404(self, test_client: Flask) -> None:
        """Método que contiene la prueba unitaria donde el cliente
        envía al servidor una petición de obtener una entidad de dominio
        específica no existente.
        
        Args:
        ----------
        test_client: Flask.
            Servidor de pruebas."""

        response = test_client.get("/package/45")

        assert response.status_code == 404, "Valide que haya obtenido el código esperado."
        assert response.json["error"] == "El paquete con ID 45 no existe.", "Valide que el mensaje de error al cliente sea el esperado."


class TestDeliverPackageView:
    """Clase que contiene pruebas unitarias sobre los endpoints
    correspondientes a la ruta "/package/<string:package_id>/deliver"."""

    def test_deliver_package_204(self, test_client: Flask) -> None:
        """Método que contiene la prueba unitaria donde el cliente
        envía al servidor una petición de verificación de una
        entidad de dominio.
        
        Args:
        ----------
        test_client: Flask.
            Servidor de pruebas."""

        response = test_client.post("/package/1/deliver")
        
        assert response.status_code == 204, "Valide que el código de estado sea el adecuado."

    def test_deliver_package_409(self, test_client: Flask) -> None:
        """Método que contiene la prueba unitaria donde el cliente
        envía al servidor una petición de verificación de una
        entidad de dominio que falla debido a invariantes internas.
        
        Args:
        ----------
        test_client: Flask.
            Servidor de pruebas."""

        response = test_client.post("/package/3/deliver")

        assert response.status_code == 409, "Valide que el código de estado sea el adecuado."
        assert response.json["error"] == "Un paquete solo puede ser marcado como entregado, si antes fue reportado como 'ASSIGNED'.", "Valide que el mensaje de error al cliente sea el esperado."


class TestAssignDriverView:
    """Clase que contiene pruebas unitarias sobre los endpoints
    correspondientes a la ruta "/package/<string:package_id>/assign"."""

    def test_assign_package_201(self, test_client: Flask) -> None:
        """Método que contiene la prueba unitaria donde el cliente
        envía al servidor una petición de verificación de una
        entidad de dominio.
        
        Args:
        ----------
        test_client: Flask.
            Servidor de pruebas."""

        response = test_client.post("/package/2/assign")
        
        assert response.status_code == 201, "Valide que el código de estado sea el adecuado."

    def test_assign_package_409(self, test_client: Flask) -> None:
        """Método que contiene la prueba unitaria donde el cliente
        envía al servidor una petición de verificación de una
        entidad de dominio que falla debido a invariantes internas.
        
        Args:
        ----------
        test_client: Flask.
            Servidor de pruebas."""

        response = test_client.post("/package/1/assign")

        assert response.status_code == 409, "Valide que el código de estado sea el adecuado."
        assert response.json["error"] == "Un paquete solo puede ser asignado si su estado actual es 'PENDING'.", "Valide que el mensaje de error al cliente sea el esperado."
