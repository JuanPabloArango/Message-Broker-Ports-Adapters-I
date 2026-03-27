"""Módulo que contiene las excepciones de dominio."""


class DomainException(Exception):
    """Clase base que define la excepción base de dominio para englobar
    todas las posibles excepciones que surjan en el mismo."""

    ...


class DeliveryDateError(DomainException):
    """Clase que representa errores de dominio sobre el VO 'DeliveryDate'"""

    ...


class SenderAlreadyVerified(DomainException):
    """Clase que representa errores al internar verificar un Sender ya verificado."""

    ...


class PackageTransitionError(DomainException):
    """Clase que representa un error de transición en el estado de un Package."""

    ...


class DriverCurrenlyOccupiedError(DomainException):
    """Clase que representa un error de sobreasignación de trabajo a un conductor."""

    ...


class DriverAlreadyAvailableError(DomainException):
    """Clase que representa un error de marcación de un conductor."""

    ...
