"""Módulo que contiene el servicio de dominio enfocado en la selección
de un Driver."""

# Librerías Externas.
from typing import List

# Librerías Internas.
from app.domain.entities.driver import Driver


class DriverAssignment:
    """Clase que define el servicio de dominio de selección de Driver."""

    @staticmethod
    def execute(available_drivers: List[Driver]) -> Driver:
        """Método estático que contiene la lógica de selección de Driver para
        el paquete o que se encarga de indicar que no hay Driver disponible
        para que luego se levante un evento encargo de indicar esto."""

        try:
            driver = sorted(available_drivers, key = lambda x: x.last_delivery)[0]
        except IndexError:
            driver = None
        return driver
