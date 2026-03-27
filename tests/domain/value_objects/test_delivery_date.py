"""Módulo que contiene las pruebas unitarias para el VO enfocado en tener la
lógica de fechas de entrega."""

# Librerías Externas.
import pytest

import datetime as dt

# Librerías Internas.
from app.domain.value_objects.delivery_date import DeliveryDate

from app.domain.exceptions import DeliveryDateError


class TestDeliveryDate:
    """Clase que encapsula las pruebas unitarias del VO DeliveryDate."""

    def test_init_none(self) -> None:
        """Método que contiene la prueba unitaria que valida que None también
        es un valor válido y representa a aquellos Drivers que aún no entregan."""

        delivery_date = DeliveryDate()

        assert not delivery_date.last_delivery, "Cuando no se pase un valor al VO, su valor es None."

    def test_init_datetime(self) -> None:
        """Método que contiene la prueba unitaria que valida que se puede
        instanciar el VO con una fecha. Por ejemplo, para cuando un Driver ya
        tenga experiencia."""

        delivery_date = DeliveryDate(last_delivery = "2024-06-12")

        assert isinstance(delivery_date.last_delivery, dt.datetime), "Validar que el tipado es datetime cuando se comparte un valor."
        assert delivery_date.last_delivery == dt.datetime(2024, 6, 12, 0, 0, 0), "Validar que el valor , si se pasa, es un objeto datetime."

    def test_init_error(self) -> None:
        """Método que contiene la prueba unitaria para validar errores de 
        instanciación."""

        with pytest.raises(ValueError):
            DeliveryDate(last_delivery = dt.datetime(2025, 10, 1))

        with pytest.raises(DeliveryDateError):
            DeliveryDate(last_delivery = "01-10-2025 13:10:58")

    def test_date_comparisson(self) -> None:
        """Método que contiene la prueba unitaria encargada de validar
        cómo es la lógica de ordenamiento de fechas para selección de Drivers."""

        date1 = DeliveryDate(last_delivery = "2025-10-01 13:12:11")
        date2 = DeliveryDate(last_delivery = "2026-01-01 00:00:00")

        assert date1 < date2, "Se debe de validar que siempre se organicen Drivers por menor fecha."

        date1 = DeliveryDate(last_delivery = None)
        date2 = DeliveryDate(last_delivery = "2026-01-01 00:00:00")

        assert date1 < date2, "Se debe de validar que siempre se organicen Drivers por menor fecha."

        date1 = DeliveryDate(last_delivery = "2025-10-01 13:12:11")
        date2 = DeliveryDate(last_delivery = None)

        assert date1 > date2, "Se debe de validar que siempre se organicen Drivers por menor fecha."

        date1 = DeliveryDate(last_delivery = None)
        date2 = DeliveryDate(last_delivery = None)

        assert not date1 > date2, "Se debe de validar que siempre se organicen Drivers por menor fecha."

    def test_invalid_comparisson(self) -> None:
        """Método que contiene la prueba unitaria que valida que cuando haya
        comparaciones inválidas, se arrojará error."""

        date1 = DeliveryDate(last_delivery = "2025-01-01")
        date2 = dt.datetime(2026, 10, 1)

        with pytest.raises(TypeError):
            date1 < date2

    def test_sorting(self) -> None:
        """Método que contiene la prueba unitaria base para el ordenamiento
        de Drivers según su atributo."""

        date1 = DeliveryDate(last_delivery = "2025-10-01 13:12:11")
        date2 = DeliveryDate(last_delivery = "2026-01-01 00:00:00")
        date3 = DeliveryDate(last_delivery = "2025-10-01 10:00:30")
        date4 = DeliveryDate(last_delivery = None)

        ordering = sorted([date1, date2, date3, date4])

        assert ordering == [date4, date3, date1, date2], "El ordenamiento siempre debe poner en primer lugar las fechas más antiguas."
