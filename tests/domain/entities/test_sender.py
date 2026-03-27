"""Módulo que contiene las pruebas unitarias para la entidad de dominio Sender."""

# Librerías Externas.
import pytest

# Librerías Internas.
from app.domain.entities.sender import Sender

from app.domain.value_objects.id import ID
from app.domain.value_objects.sender_status import SenderStatus

from app.domain.exceptions import SenderAlreadyVerified


class TestSender:
    """Clase que encapsula las pruebas unitarias de la entidad Sender."""

    def test_init_sender(self) -> None:
        """Método que contiene la prueba unitaria encargada de validar la
        instanciación por defecto de un Sender."""

        instance = Sender(id = "123")

        assert instance.id == ID(value = "123"), "Valide que la identificación del objeto tenga tipo y valor correcto."
        assert instance.status == SenderStatus.UNVERIFIED, "Valide que todo sender creado siempre se instancia sin verificación."

    def test_create_sender(self) -> None:
        """Método que contiene la prueba unitaria encargada de validar la creación
        de un Sender."""

        sender = Sender.create(id = "123")

        assert isinstance(sender, Sender), "Valide que al crear una instancia de la entidad, esta sí sea Sender."
        assert sender.id.value == "123", "Valide que el ID con el cual creo la entidad sí sea el asignado."

        sender = Sender.create()

        assert isinstance(sender, Sender), "Valide que al crear una instancia de la entidad, esta sí sea Sender."
        assert isinstance(sender.id, ID), "Valide que cuando no se asigna un ID, un UUID se construya en automático."
        assert len(sender.id.value) == 32, "Valide que el ID con el cual creo la entidad sí sea un UUI4."

    def test_verify_sender_successfully(self) -> None:
        """Método que contiene la prueba unitaria que valida que la verificación
        de un Sender sea posible."""

        sender = Sender.create()
        sender.verify()

        assert sender.status == SenderStatus.VERIFIED, "Valide que el estado sí haya transicionado."
        assert sender.can_send_packages(), "Valide que si el usuario está verificado, pueda enviar paquetes."

    def test_verify_sender_failed(self) -> None:
        """Método que contiene la prueba unitaria que valida que la verificación
        de un Sender falle cuando no cumple las invariantes."""

        sender = Sender.create()
        sender.verify()

        with pytest.raises(SenderAlreadyVerified):
            sender.verify()

        assert sender.status == SenderStatus.VERIFIED, "Valide que el estado sí haya transicionado."
        assert sender.can_send_packages(), "Valide que si el usuario está verificado, pueda enviar paquetes."

    def test_cannot_send_package_without_verification(self) -> None:
        """Método que contiene la prueba unitaria que valida que sea imposible
        enviar pedidos sin una validación previa."""

        sender = Sender.create()

        assert not sender.can_send_packages(), "Valide que un Sender sin verificar tenga prohibido hacer envíos."
