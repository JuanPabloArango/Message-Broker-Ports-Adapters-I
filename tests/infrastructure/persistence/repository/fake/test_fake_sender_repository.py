"""Módulo que contiene las pruebas unitarias para el repositorio Sender enfocado
en su Adapter de Fake."""

# Librerías Externas.
from typing import List

# Librerías Internas.
from app.domain.entities.sender import Sender
from app.domain.value_objects.sender_status import SenderStatus

from app.application.ports.persistence.criteria import Criteria, Pagination, Filter, Operator

from app.infrastructure.persistence.repository.fake.sender_repository import FakeSenderRepositoryAdapter


class TestFakeFakeSenderRepositoryAdapter:
    """Clase que encapsula las pruebas unitarias para el adapter Fake
    del repositorio."""

    def test_repository_save(self, base_senders: List[Sender]) -> None:
        """Método que contiene la prueba unitaria para validar que se
        puede almacenar una entidad de dominio en el repositorio.
        
        Args:
        ----------
        base_senders: List[Sender].
            Fixture que simula una base que contiene estas entidades persistidas."""

        repository = FakeSenderRepositoryAdapter(base = base_senders)

        sender = Sender(id = "39")

        repository.save(sender = sender)
        retrived_sender = next((sender for sender in repository._base if sender.id.value == "39"), None)

        assert sender == retrived_sender, "Valida que se haya almacenado la entidad de dominio."
        assert isinstance(retrived_sender, Sender), "Valida que la entidad de dominio almacenada sea igual a la persistida."

    def test_repository_get(self, base_senders: List[Sender]) -> None:
        """Método que contiene la prueba unitaria para validar que se puede
        obtener una entidad de dominio del repositorio.
        
        Args:
        ----------
        base_senders: List[Sender].
            Fixture que simula una base que contiene estas entidades persistidas."""

        repository = FakeSenderRepositoryAdapter(base = base_senders)

        sender = repository.get(sender_id = "2")

        assert isinstance(sender, Sender), "Valida que la entidad obtenida sea adecuada."
        assert sender.status == SenderStatus.UNVERIFIED, "Valida que el estado sea el adecuado."

        sender = repository.get(sender_id = "1")

        assert isinstance(sender, Sender), "Valida que la entidad obtenida sea adecuada."
        assert sender.status == SenderStatus.VERIFIED, "Valida que el estado sea el adecuado."

    def test_list_all(self, base_senders: List[Sender]) -> None:
        """Método que contiene la prueba unitaria para validar que se pueden
        filtrar y obtener varias entidades de dominio a la vez de un repositorio
        según un criterio de búsqueda.
        
        Args:
        ----------
        base_senders: List[Sender].
            Fixture que simula una base que contiene estas entidades persistidas."""

        repository = FakeSenderRepositoryAdapter(base = base_senders)

        criteria = Criteria(
            filters = [
                Filter(field = "status", value = SenderStatus.VERIFIED, operator = Operator.EQ),
            ],
            pagination = Pagination(limit = 2)
        )

        filtered_senders = repository.list_all(criteria = criteria)

        assert len(filtered_senders) == 2, "Valide que el filtro se aplique correctamente."
