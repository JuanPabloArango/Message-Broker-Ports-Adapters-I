"""Módulo que contiene las excepciones de aplicación."""


class ApplicationException(Exception):
    """Clase base que define la excepción base de aplicación para englobar
    todas las posibles excepciones que surjan en el mismo."""

    ...


class NotAValidAttribute(ApplicationException):
    """Clase que define errores sobre queries en nuestras entidades de
    dominio."""

    ...


class SenderNotFound(ApplicationException):
    """Clase que define un error en el cual un paquete no puede ser creado
    debido a la no existencia del Sender."""

    ...
    

class PackageNotFound(ApplicationException):
    """Clase que define un error en el cual un paquete no ha sido hallado."""

    ...


class DriverNotFound(ApplicationException):
    """Clase que define un error en el cual un conductor no ha sido hallado."""

    ...


class NotCurrenltyAvailableDrivers(ApplicationException):
    """Clase que define un error de la imposibilidad de asignación de un paquete."""

    ...