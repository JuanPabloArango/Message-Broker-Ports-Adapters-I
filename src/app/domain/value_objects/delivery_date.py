"""Módulo que contiene la definición del VO que se encarga de definir el
funcionamiento de fechas."""

# Librerías Externas.
from __future__ import annotations
from typing import Union

import datetime as dt
from dataclasses import dataclass

# Librerías Internas.
from app.domain.exceptions import DeliveryDateError


@dataclass
class DeliveryDate:
    """Clase que contiene la definición del VO enfocado en asegurar
    ordenamiento de Drivers."""

    last_delivery: Union[str, None] = None

    def __post_init__(self) -> None:
        """Método dunder encargado de validar la instanciación del VO."""

        if not isinstance(self.last_delivery, (str, type(None))):
            raise ValueError(f"La fecha de última entrega hecha por un Driver no puede ser {type(self.last_delivery)}.")
        
        if self.last_delivery:
            try:
                self.last_delivery = dt.datetime.fromisoformat(self.last_delivery)
            except ValueError:
                raise DeliveryDateError(f"La fecha {self.last_delivery} no tiene un formato válido. Use el formato 'YYYY-MM-DD HH:MM:SS'")
        
    def __lt__(self, other: DeliveryDate) -> bool:
        """Método dunde encargado de aplicar las comparaciones entre objetos.
        
        Args:
        ----------
        other: DeliveryDate.
            Instancia ajena con la cual se comparará.
            
        Returns:
        ----------
        bool.
            Si el objeto actual es inferior al objeto comparado."""

        if not isinstance(other, DeliveryDate):
            raise TypeError("No se pueden comparar dos objetos cuando uno de ellos no es de tipo 'DeliveryDate'.")

        if not other.last_delivery and not self.last_delivery:
            return False
        elif not other.last_delivery:
            return False
        elif not self.last_delivery:
            return True
        else:
            return self.last_delivery < other.last_delivery
        
    def __repr__(self) -> str:
        """Método que permite tener una representación legible del VO.
        
        Returns:
        ----------
        str.
            Representación del VO."""
        
        return f"{self.last_delivery}"
