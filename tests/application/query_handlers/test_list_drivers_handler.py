"""Módulo que contiene pruebas unitarias para un handler de Queries."""

# Librerías Externas.
from typing import List

# Librerías Internas.
from app.domain.entities.driver import Driver
from app.domain.value_objects.delivery_date import DeliveryDate

from app.application.ports.persistence.criteria import Criteria, Filter, Operator

from app.application.queries.list_drivers import ListDriversQuery
from app.application.query_handlers.list_drivers import ListDriversHandler

from app.infrastructure.persistence.repository.fake.uow import FakeUnitOfWorkAdapter


class TestListDriversHandler:
    """Clase que encapsula las pruebas unitarias para el handler ListDriversHandler."""

    def test_list_many_drivers_handler(self, base_drivers: List[Driver]) -> None:
        """Método que contiene la prueba unitaria del método 'handle' en el
        caso donde existe la entidad.
        
        Args:
        ----------
        base_drivers: List[Driver].
            Lista base de los conductores para la prueba."""

        uow = FakeUnitOfWorkAdapter(drivers = base_drivers)

        criteria = Criteria(
            filters = [
                Filter(field = "last_delivery", value = DeliveryDate(None), operator = Operator.NEQ)
            ]
        )

        handler = ListDriversHandler(unit_of_work = uow)
        drivers = handler.handle(query = ListDriversQuery(criteria = criteria))

        assert len(drivers) == 3, "Valide que haya obtenido la cantidad esperada de Drivers."
        assert all([driver.last_delivery.last_delivery is not None for driver in drivers]), "Valide que se cumpla el criterio de filtrado."

    def test_list_no_drivers_handler(self, base_drivers: List[Driver]) -> None:
        """Método que contiene la prueba unitaria del método 'handle' en el
        caso donde existe la entidad.
        
        Args:
        ----------
        base_drivers: List[Driver].
            Lista base de los conductores para la prueba."""

        uow = FakeUnitOfWorkAdapter(drivers = base_drivers)

        criteria = Criteria(
            filters = [
                Filter(field = "last_delivery", value = DeliveryDate(last_delivery = "2026-10-10"), operator = Operator.GT)
            ]
        )

        handler = ListDriversHandler(unit_of_work = uow)
        drivers = handler.handle(query = ListDriversQuery(criteria = criteria))

        assert len(drivers) == 0, "Valide que haya obtenido la cantidad esperada de Drivers."

    