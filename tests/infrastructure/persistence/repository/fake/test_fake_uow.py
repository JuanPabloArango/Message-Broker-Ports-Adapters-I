"""Módulo que contiene las pruebas unitarias para el adaptador de atomicidad
de trabajo Fake (objeto colaborador)."""

# Librerías Externas.
from typing import List

# Librerías Internas.
from app.domain.entities.driver import Driver
from app.domain.entities.sender import Sender
from app.domain.entities.package import Package

from app.domain.value_objects.driver_status import DriverStatus

from app.infrastructure.persistence.repository.fake.uow import FakeUnitOfWorkAdapter


class TestFakeUnitOfWorkAdapter:
    """Clase que encapsula las pruebas unitarias del FakeUnitOfWorkAdapter."""

    def test_commit(self, base_drivers: List[Driver], base_senders: List[Sender],
                    base_packages: List[Package]) -> None:
        """Método que contiene la prueba unitaria para validar que el fake
        funcione correctamente.
        
        Args:
        ----------
        base_drivers: List[Driver].
            Fixture que simula una base que contiene estas entidades persistidas.

        base_senders: List[Sender].
            Fixture que simula una base que contiene estas entidades persistidas.

        base_packages: List[Package].
            Fixture que simula una base que contiene estas entidades persistidas."""
        
        unit_of_work = FakeUnitOfWorkAdapter(senders = base_senders,
                                             drivers = base_drivers,
                                             packages = base_packages)
        
        assert not hasattr(unit_of_work, "sender_repository"), "Valide que haya atributos que se gestionen solo dentro del context manager."
        
        with unit_of_work as uow:
            driver = uow.driver_repository.get(driver_id = "1")

            driver.mark_as_occupied()

            uow.commit()

            assert hasattr(unit_of_work, "sender_repository"), "Valide que haya atributos que se gestionen solo dentro del context manager."

        retrived_driver = next((driver for driver in uow.driver_repository._base if driver.id.value == "1"), None)
        
        assert uow._commited, "Valida que se haya marcado la transacción como concluída."
        assert retrived_driver.status == DriverStatus.OCCUPIED, "Valide que el UoW sirva como medio de interacción con los repos."
